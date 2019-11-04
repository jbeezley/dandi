from rest_framework import serializers

from .models import DataTag, Dataset


class AgeField(serializers.DurationField):
    def to_internal_value(self, data):
        return super().to_internal_value(data.replace('days ', ''))


class DatasetSerializer(serializers.ModelSerializer):
    related_publications = serializers.SlugRelatedField(
        many=True, slug_field='doi', read_only=True)
    keywords = serializers.SlugRelatedField(
        many=True, slug_field='keyword', read_only=True)

    age = AgeField(required=False)

    class Meta:
        model = Dataset
        exclude = ['search_vector']


class DataTagSerializer(serializers.ModelSerializer):
    datasets = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='dataset-detail')

    class Meta:
        model = DataTag
        fields = '__all__'
