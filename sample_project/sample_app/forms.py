from django import forms

from .models import Country, Author, Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'popularity']
