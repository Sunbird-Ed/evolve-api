from django.contrib import admin

# Register your models here.
from .models import Content,ContentContributors



class ContentAdmin(admin.ModelAdmin):
    model = Content
    list_display = ['id','content_name','chapter_state','section_state','subsection_state','subsubsection_state']

    def chapter_state(self,req):
        try:
            return req.chapter.book.subject.grade.medium.state
        except:
            return None
    def section_state(self,req):
        try:
            return req.section.chapter.book.subject.grade.medium.state
        except:
            return None
    def subsection_state(self,req):
        try:
            return req.sub_sub_section.section.chapter.book.subject.grade.medium.state
        except:
            return None

    def subsubsection_state(self,req):
        try:
            return req.sub_sub_section.sub_sub_section.section.chapter.book.subject.grade.medium.state
        except:
            return None

admin.site.register(ContentContributors)
admin.site.register(Content,ContentAdmin)

