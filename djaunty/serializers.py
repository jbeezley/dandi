from rest_framework import serializers

from .models import Dataset, Publication


class PublicationSerializer(serializers.ModelSerializer):
    model = Publication
    fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):
    related_publications = serializers.SlugRelatedField(
        many=True, slug_field='doi', read_only=True)

    class Meta:
        model = Dataset
        fields = '__all__'
