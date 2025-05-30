from django.db import models


# Create your models here.
class genres(models.Model):
    genre = models.CharField(null=True)

    def __str__(self):
        return self.genre


class book(models.Model):
    isbn = models.BigIntegerField(13, primary_key=True)
    title = models.TextField()
    genre = models.ManyToManyField(genres)
    author = models.TextField()
    summary = models.TextField()
    publisher = models.TextField()
    language = models.TextField()
    edition = models.TextField()
    deleted_at = models.DateTimeField(null=True)


class bookInstance(models.Model):
    isbn = models.ForeignKey(book, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField()
    deleted_at = models.DateTimeField(null=True)


class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)


class borrow(models.Model):
    # isbn is not required
    isbn = models.ForeignKey(book, on_delete=models.PROTECT)
    copy = models.ForeignKey(bookInstance, on_delete=models.PROTECT)
    due_date = models.DateField()
    returned_date = models.DateField(null=True)
    fine = models.FloatField(null=True)
    user_id = models.ForeignKey(user, on_delete=models.PROTECT)


class login(models.Model):
    username = models.TextField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    password = models.TextField()
