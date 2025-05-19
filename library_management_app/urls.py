from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/books", views.get_books, name="getBooks"),
    path(
        "api/books/language/<str:language>", views.get_by_language, name="getByLanguage"
    ),
]
