from rest_framework import serializers

from .models import DataTag, Dataset
from .search_parser import FacetParser, ParserException, SearchParser


class AgeField(serializers.DurationField):
    def to_internal_value(self, data):
        return super().to_internal_value(data.replace('days ', ''))


class QueryField(serializers.CharField):
    """A field taking a parseable search query as text."""

    def to_representation(self, value):
        raise Exception('A query can only be used as a "write-only" field.')

    def to_internal_value(self, data):
        parser = SearchParser()
        value = super().to_internal_value(data)

        try:
            return parser.parse(value)
        except ParserException as e:
            raise serializers.ValidationError(str(e))


class FacetField(serializers.CharField):
    def to_representation(self, value):
        raise Exception('A facet can only be used as a "write-only" field.')

    def to_internal_value(self, data):
        parser = FacetParser()
        value = super().to_internal_value(data)

        try:
            return parser.parse(value)
        except ParserException as e:
            raise serializers.ValidationError(str(e))


class DatasetSerializer(serializers.ModelSerializer):
    related_publications = serializers.SlugRelatedField(
        many=True, slug_field='doi', read_only=True)
    keywords = serializers.SlugRelatedField(
        many=True, slug_field='keyword', read_only=True)

    age = AgeField(required=False)

    class Meta:
        model = Dataset
        fields = [
            'created', 'updated', 'related_publications', 'keywords', 'path', 'size',
            'genotype', 'subject_id', 'age', 'number_of_electrodes', 'lab',
            'session_start_time', 'experimenter', 'session_id', 'species',
            'identifier', 'session_description', 'institution', 'number_of_units',
            'nwb_version'
        ]


class DatasetFacetSerializer(serializers.Serializer):
    facet = FacetField(write_only=True, required=True)
    query = QueryField(write_only=True, required=False)


class DataTagSerializer(serializers.ModelSerializer):
    datasets = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='dataset-detail'
    )

    # The query can match a huge number of datasets and possibly kill the
    # server, should we have a limit in place and return a 400 if the
    # result set is too large?
    query = QueryField(write_only=True, required=True)

    class Meta:
        model = DataTag
        fields = ['id', 'created', 'updated', 'datasets', 'name', 'query']

    def create(self, data):
        query = data.pop('query')
        datatag = super().create(data)

        for dataset in Dataset.objects.filter(query).values('pk').all():
            datatag.datasets.add(dataset['pk'])

        return datatag

    def update(self, datatag, data):
        query = data.pop('query', None)
        datatag = super().update(datatag, data)

        if query is None:
            return datatag

        datatag.datasets.clear()
        for dataset in Dataset.objects.filter(query).values('pk').all():
            datatag.datasets.add(dataset['pk'])

        return datatag


class DataTagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataTag
        fields = ['id', 'created', 'updated', 'name']
