from django.contrib import admin

# Register your models here.
# from django.contrib.auth import User
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Roles, UserDetails

from django.contrib.auth.models import Group


class GroupsAdmin(admin.ModelAdmin):
    list_display = ["name", "pk"]
    class Meta:
        model = Group


class UserDetailInline(admin.StackedInline):
    model = UserDetails


    #readonly_fields = ('data', 'user') #Bonus question later


# class ReportingToInline(admin.StackedInline):
#     model = Roles

class UserAdmin(BaseUserAdmin):
    inlines = [
        UserDetailInline,
    ]
    list_display = ['id', 'username','state','role','email', 'is_staff']

    def state(req,self):
        try:
            return self.userdetails.state.state 
        except:
            return None
    def role(req,self):
        try:
            return self.userdetails.role.rolename 
        except:
            return None


# admin.site.register(UserDetails, UserAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Roles)
admin.site.register(UserDetails)
admin.site.unregister(Group)

admin.site.register(Group, GroupsAdmin)
