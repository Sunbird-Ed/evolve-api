from django.contrib import admin

# Register your models here.
# from django.contrib.auth import User
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Roles, UserDetails

class UserDetailInline(admin.StackedInline):
    model = UserDetails
    #readonly_fields = ('data', 'user') #Bonus question later


# class ReportingToInline(admin.StackedInline):
#     model = Roles

class UserAdmin(BaseUserAdmin):
    inlines = [
        UserDetailInline,
    ]
    list_display = ['id', 'username', 'email', 'is_staff']
# admin.site.register(UserDetails, UserAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Roles)
admin.site.register(UserDetails)