from django.shortcuts import render

from .forms import SearchForm, TextSearchForm
from .models import Dataset
from .serializers import DatasetSerializer


def search(request):
    total = 0
    results = None
    if request.method == 'POST':
        form = TextSearchForm(request.POST)
        if form.is_valid():
            query = form.clean()['search_text']
            qs = Dataset.objects.filter(search_vector=query)
            total = qs.count()
            results = DatasetSerializer(qs[:10], many=True).data
    else:
        form = TextSearchForm()

    context = {
        'form': form.as_table(),
        'results': results,
        'action': 'search',
        'total': total
    }
    return render(request, 'search.html', context)


def filter(request):
    total = 0
    results = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.clean()['search_text']
            qs = Dataset.objects.filter(query)
            total = qs.count()
            results = DatasetSerializer(qs[:10], many=True).data
    else:
        form = SearchForm()

    context = {
        'form': form.as_table(),
        'results': results,
        'action': 'filter',
        'total': total
    }
    return render(request, 'search.html', context)
