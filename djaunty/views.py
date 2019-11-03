from django.shortcuts import render

from .forms import TextSearchForm
from .models import Dataset
from .serializers import DatasetSerializer


def search(request):
    results = None
    if request.method == 'POST':
        form = TextSearchForm(request.POST)
        if form.is_valid():
            query = form.clean()['search_text']
            results = DatasetSerializer(Dataset.objects.filter(
                search_vector=query).all()[:10], many=True).data
    else:
        form = TextSearchForm()

    return render(request, 'search.html', {'form': form, 'results': results})
