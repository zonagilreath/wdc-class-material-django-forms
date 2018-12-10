from django import forms

from .models import Country, Author, Book


class BookForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    author = forms.ModelChoiceField(label='Author', queryset=Author.objects.all())
    isbn = forms.CharField(label='ISBN', max_length=20)
    popularity = forms.FloatField(label='Popularity', min_value=0)
