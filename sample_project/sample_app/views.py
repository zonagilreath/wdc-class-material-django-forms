from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import datetime

from .models import Author, Book


def index(request):
    errors = {}
    has_errors = False
    book_data = {}
    if request.method == 'POST':
        book_data = {
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'isbn': request.POST.get('isbn'),
            'popularity': request.POST.get('popularity'),
        }
        title = request.POST.get('title')
        if not title:
            has_errors = True
            errors['title'] = "A title must be provided"

    sort_method = request.GET.get('sort', 'asc')
    books = Book.objects.all()
    if sort_method == 'asc':
        books = books.order_by('popularity')
    elif sort_method == 'desc':
        books = books.order_by('-popularity')

    if 'q' in request.GET:
        q = request.GET['q']
        books = books.filter(title__icontains=q)
    return render(request, 'index.html', {
        'books': books,
        'authors': Author.objects.all(),
        'sort_method': sort_method,
        'book_data': book_data,
        'has_errors': has_errors,
        'errors': errors,
    })


def create_book(request):
    # author = Author.objects.get(id=request.POST['author'])
    author = get_object_or_404(Author, id=request.POST['author'])

    # here
    Book.objects.create(
        title=request.POST['title'],
        author=author,
        isbn=request.POST['isbn'],
        popularity=request.POST['popularity'])

    return redirect('/')


def edit_book(request, book_id=None):
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()
    errors = {}

    if request.method == 'POST':
        author = get_object_or_404(Author, id=request.POST['author'])
        title = request.POST['title']

        if not title:
            errors['title'] = "A title must be provided"

        if len(title) > 30:
            errors['title'] = "Title can't be longer than 30 chars"

        if not errors:
            book.title = title
            book.author = author
            book.isbn = request.POST['isbn']
            book.popularity = request.POST['popularity']
            book.save()
            return redirect('/')

    return render(
        request,
        'edit_book.html',
        context={
            'book': book,
            'authors': authors,
            'errors': errors,
            'book_data': {
                'title': request.POST.get('title'),
                'author': request.POST.get('author'),
                'isbn': request.POST.get('isbn'),
                'popularity': request.POST.get('popularity'),
            }
        }
    )


def delete_book(request):
    book_id = request.POST.get('book_id')

    book = get_object_or_404(Book, id=book_id)

    book.delete()
    return redirect('/')


def authors(request):
    authors = Author.objects.all()
    return render(request, 'authors.html', {
        'authors': authors
    })


def author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return HttpResponseNotFound()

    return render(request, 'author.html', {
        'author': author
    })
