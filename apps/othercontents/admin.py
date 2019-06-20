from django.contrib import admin

from .models import Tags,OtherContributors,OtherContent,SchoolName





class SchoolNames(admin.ModelAdmin):
    model = SchoolName
    list_display = ['id','school_name']
class OtherContents(admin.ModelAdmin):
	model = OtherContent
	list_display = ['id','content_name','file_url']
admin.site.register(Tags)
admin.site.register(OtherContributors)
admin.site.register(OtherContent,OtherContents)
admin.site.register(SchoolName,SchoolNames)