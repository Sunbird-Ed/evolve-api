from django.contrib import admin

# Register your models here.
# from django.contrib.auth import User

from django.contrib.auth.admin import UserAdmin
from .models import EvolveUser

# admin.site.register(EvolveUser, UserAdmin)
admin.site.register(EvolveUser)