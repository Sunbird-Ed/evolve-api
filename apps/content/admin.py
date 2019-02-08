from django.contrib import admin

# Register your models here.
from .models import Content,ContentContributors

admin.site.register(Content)
admin.site.register(ContentContributors)

