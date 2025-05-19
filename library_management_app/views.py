from django.shortcuts import render
from .models import book

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, "base.html")


def get_books(request):
    books = book.objects.all()
    authors = [book.author for book in books]
    authors_distinct = set(authors)
    return HttpResponse(f"{author} \n" for author in authors_distinct)
    # return render(request, "books.html")
