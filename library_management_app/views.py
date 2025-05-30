from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import book, bookInstance, user, borrow, genres
from datetime import datetime, date, timedelta
from .forms import AddUserForm, AddBookForm, ReturnBook, DeleteBook

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
    copies = bookInstance.objects.filter(isbn=book_details.isbn).filter(deleted_at=None)
    copies_borrowed = borrow.objects.filter(isbn=book_details.isbn).filter(
        returned_date=None
    )
    copies_due_dates = [copy.due_date for copy in copies_borrowed]

    if copies.count() - copies_borrowed.count() == 0 and len(copies_due_dates) > 0:
        context = {
            "book_details": book_details,
            "languages": base_context["languages"],
            "genres": base_context["genres"],
            "copy_count": copies.count() - copies_borrowed.count(),
            "check_date": min(copies_due_dates) + timedelta(days=1),
            "book_genres": book_genre_list,
        }
        return render(request, "book_details.html", context)
    elif copies.count() - copies_borrowed.count() > 0:
        context = {
            "book_details": book_details,
            "languages": base_context["languages"],
            "genres": base_context["genres"],
            "copy_count": copies.count() - copies_borrowed.count(),
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
    # multiple requests issue
    Book = books.filter(isbn=isbn)
    copies = bookInstance.objects.filter(isbn=isbn).values("id")
    copies_ids = [copy["id"] for copy in copies]
    borrows = borrow.objects.filter(isbn=isbn).values("copy").filter(returned_date=None)
    borrows_ids = [borrow["copy"] for borrow in borrows]
    copy_available_id = min([copy for copy in copies_ids if copy not in borrows_ids])
    copy_available = bookInstance.objects.filter(id=copy_available_id)[0]
    User_id = user.objects.filter(user_id=2)
    bw = borrow(
        isbn=Book[0],
        due_date=date.today() + timedelta(days=14),
        user_id=User_id[0],
        copy=copy_available,
    )
    bw.save()
    fine = 10
    context = {
        "due_date": date.today() + timedelta(days=14),
        "fine": fine,
        "book_name": Book[0],
        "languages": base_context["languages"],
        "genres": base_context["genres"],
    }
    return render(request, "borrow.html", context)


def borrowed_books(request):
    if request.method == "GET":
        form = ReturnBook()
        context = {
            "form": form,
            "languages": set([book.language for book in books]),
            "genres": [Genre.genre for Genre in genre_list],
        }
        return render(request, "returns.html", context)
    form = ReturnBook(request.POST)
    if form.is_valid():
        User_Id = form.cleaned_data["user_id"]
        if User_Id not in [
            user["user_id"]
            for user in user.objects.filter(deleted_at=None).values("user_id")
        ]:
            return HttpResponse("This is not a valid User!")
        borrowed_books = borrow.objects.filter(user_id=User_Id).filter(
            returned_date=None
        )
        borrowed_books_isbns = borrowed_books.values("isbn_id")
        book_titles = [
            (
                borrowed_books[i].isbn_id,
                borrowed_books[i].due_date,
                borrowed_books[i].copy_id,
                books.filter(isbn=borrowed_books_isbns[i]["isbn_id"]).values("title")[
                    0
                ]["title"],
                borrowed_books[i].returned_date,
            )
            for i in range(0, len(borrowed_books_isbns))
        ]

        return render(
            request,
            "borrowed_books.html",
            {"books": book_titles, "borrowed_books": borrowed_books},
        )


def return_book(request, isbn, copy_id):
    borrowed_book = borrow.objects.filter(isbn=isbn).filter(copy_id=copy_id)[0]
    borrowed_book.returned_date = date.today()
    borrowed_book.save()

    return HttpResponse("Thank you for returning the book!")


def delete_user(request):
    if request.method == "GET":
        form = ReturnBook()
        return render(request, "delete_user.html", {"form": form})
    form = ReturnBook(request.POST)
    if form.is_valid():
        User_Id = form.cleaned_data["user_id"]
        if User_Id not in [
            user["user_id"]
            for user in user.objects.filter(deleted_at=None).values("user_id")
        ]:
            return HttpResponse("This is not a valid User!")
        User = user.objects.filter(user_id=User_Id)[0]
        User.deleted_at = datetime.now()
        User.save()
        return HttpResponse("User Has Been Deleted!")


def delete_book(request):
    if request.method == "GET":
        form = DeleteBook()
        return render(request, "delete_book.html", {"form": form})
    form = DeleteBook(request.POST)
    if form.is_valid():
        Isbn = form.cleaned_data["isbn"]
        Copy_count_to_be_deleted = form.cleaned_data["copy_count"]
        Copy_borrowed = borrow.objects.filter(isbn=Isbn).filter(returned_date=None)
        Copy_count_borrowed = len(Copy_borrowed)
        Copy_current = bookInstance.objects.filter(isbn=Isbn).filter(deleted_at=None)
        Copy_count_current = len(Copy_current)
        if Copy_count_borrowed != 0:
            return HttpResponse(
                "Copies of this book cannot be deleted at the moment since some of them have been borrowed"
            )
        elif Copy_count_current == 0:
            return HttpResponse("We currently do not have any copies of this book!")
        elif Copy_count_to_be_deleted > Copy_count_current:
            return HttpResponse(
                f"There are only {Copy_count_current} copies of this book at the library, not {Copy_count_to_be_deleted}"
            )
        elif Copy_count_to_be_deleted < Copy_count_current:
            for i in range(0, Copy_count_to_be_deleted):
                Copy_current[i].deleted_at = datetime.now()
                Copy_current[i].save()
            return HttpResponse(
                f"There are now {Copy_count_current-Copy_count_to_be_deleted} copies of this book left"
            )
        elif Copy_count_to_be_deleted == Copy_count_current:
            for i in range(0, Copy_count_current):
                Copy_current[i].deleted_at = datetime.now()
                Copy_current[i].save()
            return HttpResponse(f"All copies of this book have been deleted!")
