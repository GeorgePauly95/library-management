from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import book, bookInstance
from datetime import datetime, date


def home(request):
    books = book.objects.all()
    genre = [book.genre[0] for book in books]
    print(genre)
    context = {"languages": set([book.language for book in books])}
    return render(request, "home.html", context)


def get_book(request, isbn):
    selected_book = book.objects.filter(isbn=isbn)
    print(selected_book)
    selected_book_data = f"Author:{selected_book[0].author} Title:{selected_book[0].title} \n Summary: {selected_book[0].summary}"
    return HttpResponse(selected_book_data)


def get_by_language(request, language):
    books = book.objects.all()
    books_lang = books.filter(language=language)
    context = {"books": books_lang}
    return render(request, "books.html", context)


def add_book(request):
    if request.method == "GET":
        return render(request, "add_book.html")
    book_details = request.POST
    b = book(
        isbn=book_details["isbn"],
        title=book_details["title"],
        genre=book_details["genres"],
        author=book_details["author"],
        summary=book_details["summary"],
        publisher=book_details["publisher"],
        language=book_details["language"],
        edition=book_details["edition"],
    )
    b.save()
    for i in range(0, int(book_details["copy-count"])):
        bI = bookInstance(isbn=b, purchase_date=date.today())
        bI.save()
    return HttpResponse(
        f"{book_details["copy-count"]} copies of {book_details["title"]} have been added to the library"
    )
