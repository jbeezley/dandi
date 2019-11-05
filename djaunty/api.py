from django.db.models import Count

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import ComplexSearchFilter, TextSearchFilter
from .models import DataTag, Dataset, Keyword, Publication
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

    def create(self, request, *args, **kwargs):
        data = request.data
        publications_data = data.pop('related_publications', [])
        keywords_data = data.pop('keywords', [])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        dataset = serializer.save()
        for doi in publications_data:
            dataset.related_publications.add(
                Publication.objects.get_or_create(doi=doi, defaults={'dataset': dataset})[0]
            )

        for keyword in keywords_data:
            dataset.keywords.add(
                Keyword.objects.get_or_create(keyword=keyword, defaults={'dataset': dataset})[0]
            )

        dataset.save()  # necessary?
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data

        publications_data = data.pop('related_publications', None)
        if not partial and publications_data is None:
            publications_data = []

        keywords_data = data.pop('keywords', None)
        if not partial and keywords_data is None:
            keywords_data = []

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if publications_data is not None:
            instance.related_publications.clear()

            for doi in publications_data:
                instance.related_publications.add(
                    Publication.objects.get_or_create(doi=doi, defaults={'dataset': instance})[0]
                )

        if keywords_data is not None:
            instance.keywords.clear()

            for keyword in keywords_data:
                instance.keywords.add(
                    Keyword.objects.get_or_create(keyword=keyword, defaults={'dataset': instance})[0]
                )

        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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
