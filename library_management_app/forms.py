from django import forms


class AddBookForm(forms.Form):
    isbn = forms.IntegerField(label="isbn")
    title = forms.CharField(label="Title")
    genre = forms.CharField(label="Genre")
    author = forms.CharField(label="Author")
    summary = forms.CharField(label="Summary")
    publisher = forms.CharField(label="Publisher")
    language = forms.CharField(label="Language")
    edition = forms.CharField(label="Edition")
    copy_count = forms.IntegerField(label="Number of copies")


class AddUserForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    age = forms.IntegerField(label="Age")
