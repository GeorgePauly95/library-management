from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import book, bookInstance, user, borrow
from datetime import datetime, date, timedelta
from .forms import AddUserForm, AddBookForm


def home(request):
    books = book.objects.all()
    context = {"languages": set([book.language for book in books])}
    return render(request, "home.html", context)


def get_by_language(request, language):
    books = book.objects.all()
    books_lang = books.filter(language=language)
    copies = bookInstance.objects.all()
    context = {"books": books_lang, "languages": set([book.language for book in books])}
    return render(request, "books.html", context)


def get_book(request, isbn):
    books = book.objects.all()
    selected_book = book.objects.filter(isbn=isbn)
    book_details = selected_book[0]
    copies = bookInstance.objects.filter(isbn=book_details.isbn)
    copies_borrowed = borrow.objects.filter(isbn=book_details.isbn)
    copies_due_dates = [copy.due_date for copy in copies_borrowed]
    if copies.count() == 0 and len(copies_due_dates) > 0:
        context = {
            "book_details": book_details,
            "languages": set([book.language for book in books]),
            "copy_count": copies.count(),
            "check_date": min(copies_due_dates) + timedelta(days=1),
        }
        return render(request, "book_details.html", context)
    elif copies.count() > 0:
        context = {
            "book_details": book_details,
            "languages": set([book.language for book in books]),
            "copy_count": copies.count(),
        }
        return render(request, "book_details.html", context)
    else:
        context = {
            "book_details": book_details,
            "languages": set([book.language for book in books]),
            "copy_count": "Out of Stock!",
            "check_date": None,
        }
        return render(request, "book_details.html", context)


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


def borrow_book(request, isbn):
    Books = book.objects.all()
    Book = Books.filter(isbn=isbn)
    print(Book[0].title)
    Users = user.objects.all()
    User_id = Users.filter(user_id=2)
    bw = borrow(
        isbn=Book[0], due_date=date.today() + timedelta(days=14), user_id=User_id[0]
    )
    bw.save()
    copies = bookInstance.objects.all()
    copy = copies.filter(isbn=isbn)
    copy[0].delete()
    fine = 10

    context = {
        "due_date": date.today() + timedelta(days=14),
        "fine": fine,
        "book_name": Book[0],
        "languages": set([book.language for book in Books]),
    }
    return render(request, "borrow.html", context)
