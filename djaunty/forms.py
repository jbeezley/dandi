from django import forms

from .search_parser import ParserException, SearchParser


class SearchField(forms.CharField):
    def clean(self, text):
        search_parser = SearchParser()

        try:
            parsed = search_parser.parse(text)
        except ParserException as e:
            raise forms.ValidationError(str(e))

        return parsed


class SearchForm(forms.Form):
    search_text = SearchField(label='Search', widget=forms.Textarea)


class TextSearchForm(forms.Form):
    search_text = forms.CharField(label='Search')
