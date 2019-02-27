from django.contrib import admin

# Register your models here.
from .models import  HardSpot,HardSpotContributors

admin.site.register(HardSpot)
admin.site.register(HardSpotContributors)