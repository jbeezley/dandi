from rest_framework import exceptions, filters

from .search_parser import ParserException, SearchParser


class TextSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(search_vector=search)
        return queryset


class ComplexSearchFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        parser = SearchParser()
        query = request.query_params.get('query')
        if query:
            try:
                filter = parser.parse(query)
            except ParserException as e:
                detail = f'Invalid query: {e}'
                raise exceptions.ValidationError(detail=detail)
            queryset = queryset.filter(filter)
        return queryset
