from django.shortcuts import render
from .models import book

# Create your views here.
from django.http import HttpResponse


def index(request):
    books = book.objects.all()
    context = {"languages": set([book.language for book in books])}
    print(context)
    return render(request, "base.html", context)


def get_books(request):
    books = book.objects.all()
    books_data = [f"{book.author} {book.title} {book.pk}" for book in books]
    return HttpResponse([f"{book}\n" for book in books_data])
    # return render(request, "books.html")


def get_by_language(request, language):
    books = book.objects.all()
    books_lang = books.filter(language=language)
    return HttpResponse(f"{book.title}\n" for book in books_lang)
