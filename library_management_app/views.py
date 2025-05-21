from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import book, bookInstance, user
from datetime import datetime, date
from .forms import AddUserForm, AddBookForm


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
        form = AddBookForm()
        return render(request, "add_book.html", {"form": form})
    form = AddBookForm(request.POST)
    if form.is_valid():
        Isbn = form.cleaned_data["isbn"]
        Title = form.cleaned_data["title"]
        Genre = form.cleaned_data["genre"]
        Author = form.cleaned_data["author"]
        Summary = form.cleaned_data["summary"]
        Publisher = form.cleaned_data["publisher"]
        Language = form.cleaned_data["language"]
        Edition = form.cleaned_data["edition"]
        Copy_count = form.cleaned_data["copy_count"]
        b = book(
            isbn=Isbn,
            title=Title,
            genre=Genre,
            author=Author,
            summary=Summary,
            publisher=Publisher,
            language=Language,
            edition=Edition,
        )
        b.save()
        for i in range(0, Copy_count):
            bI = bookInstance(isbn=b, purchase_date=date.today())
            bI.save()
        return HttpResponse(
            f"{Copy_count} copies of {Title} have been added to the library"
        )
    return render(request, "add_book.html")


def add_user(request):
    if request.method == "GET":
        form = AddUserForm()
        return render(request, "add_user.html", {"form": form})
    form = AddUserForm(request.POST)
    if form.is_valid():
        First_name = form.cleaned_data["first_name"]
        Last_name = form.cleaned_data["last_name"]
        Age = form.cleaned_data["age"]
        Created_at = (datetime.now,)
        u = user(
            first_name=First_name, last_name=Last_name, age=Age, created_at=Created_at
        )
        u.save()
        return HttpResponse("You're cool now!")
    else:
        form = AddUserForm()
        return render(request, "add_user.html", {"form": form})
