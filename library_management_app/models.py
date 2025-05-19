from django.db import models


# Create your models here.
class book(models.Model):
    isbn = models.BigIntegerField(13, primary_key=True)
    title = models.TextField()
    genre = models.TextField()
    author = models.TextField()
    summary = models.TextField()
    publisher = models.TextField()
    language = models.TextField()
    edition = models.TextField()


class bookInstance(models.Model):
    isbn = models.ForeignKey(book, on_delete=models.CASCADE)
    purchaseDate = models.DateTimeField()


class user(models.Model):
    userId = models.TextField(primary_key=True)
    firstName = models.TextField()
    lastName = models.TextField()
    age = models.IntegerField()
    createdAt = models.DateTimeField(default=None)


class borrow(models.Model):
    isbn = models.ForeignKey(book, on_delete=models.PROTECT)
    dueDate = models.DateTimeField()
    returnedDate = models.DateTimeField()
    fine = models.FloatField()
    userId = models.ForeignKey(user, on_delete=models.PROTECT)


class login(models.Model):
    username = models.TextField(primary_key=True)
    userId = models.ForeignKey(user, on_delete=models.CASCADE)
    password = models.TextField()
