from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import book, bookInstance, user, borrow, genres
from datetime import datetime, date, timedelta
from .forms import AddUserForm, AddBookForm

books = book.objects.all()
genre_list = genres.objects.all()
base_context = {
    "languages": set([book.language for book in books]),
    "genres": [Genre.genre for Genre in genre_list],
}


def home(request):
    context = {"languages": base_context["languages"], "genres": base_context["genres"]}
    return render(request, "home.html", context)


def get_by_language(request, language):
    books_lang = books.filter(language=language)
    context = {
        "books": books_lang,
        "languages": base_context["languages"],
        "genres": base_context["genres"],
    }
    return render(request, "books.html", context)


def get_by_genre(request, genre):
    genre_id = genres.objects.filter(genre=genre).values("id")[0]["id"]
    books_genre = book.objects.filter(genre=genre_id)
    context = {
        "books": books_genre,
        "languages": base_context["languages"],
        "genres": base_context["genres"],
    }
    return render(request, "books.html", context)


def get_book(request, isbn):
    selected_book = book.objects.filter(isbn=isbn)
    book_details = selected_book[0]
    book_genres = book_details.genre.all().values("genre")
    book_genre_list = [book_genres[i]["genre"] for i in range(0, len(book_genres))]
    copies = bookInstance.objects.filter(isbn=book_details.isbn)
    copies_borrowed = borrow.objects.filter(isbn=book_details.isbn)
    copies_due_dates = [copy.due_date for copy in copies_borrowed]

    if copies.count() == 0 and len(copies_due_dates) > 0:
        context = {
            "book_details": book_details,
            "languages": base_context["languages"],
            "genres": base_context["genres"],
            "copy_count": copies.count(),
            "check_date": min(copies_due_dates) + timedelta(days=1),
            "book_genres": book_genre_list,
        }
        return render(request, "book_details.html", context)
    elif copies.count() > 0:
        context = {
            "book_details": book_details,
            "languages": base_context["languages"],
            "genres": base_context["genres"],
            "copy_count": copies.count(),
            "book_genres": book_genre_list,
        }
        return render(request, "book_details.html", context)
    else:
        context = {
            "book_details": book_details,
            "languages": base_context["languages"],
            "genres": base_context["genres"],
            "copy_count": "Out of Stock!",
            "check_date": None,
            "book_genres": book_genre_list,
        }
        return render(request, "book_details.html", context)


def add_book(request):
    if request.method == "GET":
        form = AddBookForm()
        return render(
            request,
            "add_book.html",
            {
                "form": form,
                "languages": base_context["languages"],
                "genres": base_context["genres"],
            },
        )
    form = AddBookForm(request.POST)

    if not form.is_valid():
        return render(request, "add_book.html")
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
        author=Author,
        summary=Summary,
        publisher=Publisher,
        language=Language,
        edition=Edition,
    )
    b.save()
    b.genre.set(Genre)
    # b.save()
    for i in range(0, Copy_count):
        bI = bookInstance(isbn=b, purchase_date=date.today())
        bI.save()
    return HttpResponse(
        f"{Copy_count} copies of {Title} have been added to the library"
    )


def add_user(request):
    if request.method == "GET":
        form = AddUserForm()
        return render(
            request,
            "add_user.html",
            {
                "form": form,
                "languages": base_context["languages"],
                "genres": base_context["genres"],
            },
        )
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
        return render(
            request, "add_user.html", {"form": form, "genres": base_context["genres"]}
        )


def borrow_book(request, isbn):
    Book = books.filter(isbn=isbn)
    User_id = user.objects.filter(user_id=2)
    bw = borrow(
        isbn=Book[0], due_date=date.today() + timedelta(days=14), user_id=User_id[0]
    )
    bw.save()
    copy = bookInstance.objects.filter(isbn=isbn)
    copy[0].delete()
    fine = 10
    context = {
        "due_date": date.today() + timedelta(days=14),
        "fine": fine,
        "book_name": Book[0],
        "languages": base_context["languages"],
        "genres": base_context["genres"],
    }
    return render(request, "borrow.html", context)
