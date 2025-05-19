from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("books", views.get_books, name="getBooks"),
]
