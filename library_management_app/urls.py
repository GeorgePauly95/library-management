from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/books", views.add_book, name="add_book"),
    path("api/books/<int:isbn>", views.get_book, name="get_book"),
    path(
        "api/books/language/<str:language>",
        views.get_by_language,
        name="get_by_language",
    ),
    path("api/users", views.add_user, name="add_user"),
    path("api/borrow/<int:isbn>", views.borrow_book, name="borrow"),
]
