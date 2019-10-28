from rest_framework import serializers

from .models import Dataset, Publication


class AgeField(serializers.DurationField):
    def to_internal_value(self, data):
        return super().to_internal_value(data.replace('days ', ''))


class PublicationSerializer(serializers.ModelSerializer):
    model = Publication
    fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    related_publications = serializers.SlugRelatedField(
        many=True, slug_field='doi', read_only=True)

    age = AgeField(required=False)

    class Meta:
        model = Dataset
        fields = '__all__'
