from django.contrib import admin

from .models import Tags,OtherContributors,OtherContent,SchoolName


admin.site.register(Tags)
admin.site.register(OtherContributors)
admin.site.register(OtherContent)
admin.site.register(SchoolName)