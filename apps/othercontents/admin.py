from django.contrib import admin

from .models import Tags,OtherContributors,OtherContent,SchoolName





class SchoolNames(admin.ModelAdmin):
    model = SchoolName
    list_display = ['id','school_name']

admin.site.register(Tags)
admin.site.register(OtherContributors)
admin.site.register(OtherContent)
admin.site.register(SchoolName,SchoolNames)