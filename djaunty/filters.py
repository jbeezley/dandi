from django_filters import rest_framework as filters

from .models import Dataset, Keyword, Publication


class DatasetFilter(filters.FilterSet):
    # Limit the results sent back for the filtering form...
    # Ideally this, but it is slow:
    # publication_qs = Publication.objects \
    #     .annotate(Count('datasets')).order_by('-datasets__count', 'doi')[:100]
    publication_qs = Publication.objects.all().order_by('doi')[:100]
    related_publications = filters.ModelChoiceFilter(queryset=publication_qs)

    # keyword_qs = Keyword.objects \
    #     .annotate(Count('datasets')).order_by('-datasets__count', 'keyword')[:100]
    keyword_qs = Keyword.objects.all().order_by('keyword')[:100]
    keywords = filters.ModelChoiceFilter(queryset=keyword_qs)

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
        ]
