from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/books", views.add_book, name="add_book"),
    path("api/books/<int:isbn>", views.get_book, name="getBook"),
    path(
        "api/books/language/<str:language>", views.get_by_language, name="getByLanguage"
    ),
]
