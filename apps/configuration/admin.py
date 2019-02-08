from django.contrib import admin

# Register your models here.
from .models import Book,State,Subject,Grade,Medium


admin.site.register([Book,State,Subject,Grade,Medium])