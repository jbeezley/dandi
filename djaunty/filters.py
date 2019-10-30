from django_filters import rest_framework as filters

from .models import Dataset, Keyword, Publication


class DatasetFilter(filters.FilterSet):
    related_publications = filters.ModelChoiceFilter(queryset=Publication.objects.all())
    keywords = filters.ModelChoiceFilter(queryset=Keyword.objects.all())

    class Meta:
        model = Dataset
        fields = [
            'genotype',
            'subject_id',
            'age',
            'number_of_electrodes',
            'lab',
            'session_start_time',
            'experimenter',
            'session_id',
            'species',
            'identifier',
            'session_description',
            'institution',
            'number_of_units',
            'nwb_version',
            'related_publications',
        ]
