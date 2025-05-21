from django.db import models
from datetime import datetime


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
    purchase_date = models.DateTimeField()


class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class borrow(models.Model):
    isbn = models.ForeignKey(book, on_delete=models.PROTECT)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField()
    fine = models.FloatField()
    user_id = models.ForeignKey(user, on_delete=models.PROTECT)


class login(models.Model):
    username = models.TextField(primary_key=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    password = models.TextField()
