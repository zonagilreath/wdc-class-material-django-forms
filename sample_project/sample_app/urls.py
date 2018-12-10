from django.urls import path

from . import views


urlpatterns = [
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author, name='author_by_id'),
    path('create_book/', views.create_book, name='create_book'),
    path('delete_book', views.delete_book, name='delete_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('', views.index, name='index'),
]
