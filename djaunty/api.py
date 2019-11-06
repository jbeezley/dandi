from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from .filters import ComplexSearchFilter, TextSearchFilter
from .models import DataTag, Dataset
from .serializers import DataTagListSerializer, DataTagSerializer, \
    DatasetFacetSerializer, DatasetSerializer


class DatasetPagination(PageNumberPagination):
    page_size = 25
    max_page_size = 100
    page_size_query_param = 'page_size'


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all().order_by('id')
    serializer_class = DatasetSerializer
    pagination_class = DatasetPagination
    filter_backends = [TextSearchFilter, ComplexSearchFilter, OrderingFilter]

    @action(detail=False, methods=['POST'])
    def facet(self, request, *args, **kwargs):
        serializer = DatasetFacetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        qs = Dataset.objects  # TODO: where does the default queryset come in?

        if 'query' in data:
            qs = qs.filter(data['query'])

        qs = qs.annotate(facet=data['facet'])

        values = qs.values('facet').annotate(count=Count('facet')).filter(count__gt=0).order_by('-count')
        page = self.paginate_queryset(values)
        return self.get_paginated_response(page)


class DataTagViewSet(viewsets.ModelViewSet):
    queryset = DataTag.objects.all().order_by('id')
    serializer_class = DataTagSerializer
    pagination_class = DatasetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return DataTagListSerializer

        return DataTagSerializer
