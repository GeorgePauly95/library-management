from django.contrib import admin

# Register your models here.
from .models import book, bookInstance, user, login, borrow, genres

admin.site.register(book)
admin.site.register(bookInstance)
admin.site.register(user)
admin.site.register(login)
admin.site.register(borrow)
admin.site.register(genres)
