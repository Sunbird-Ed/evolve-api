from django.contrib import admin

from .models import Tags,OtherContributors,OtherContent


admin.site.register(Tags)
admin.site.register(OtherContributors)
admin.site.register(OtherContent)