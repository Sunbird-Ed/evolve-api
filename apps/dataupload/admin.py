from django.contrib import admin
from . models import Chapter, Section, SubSection,ChapterKeyword,SectionKeyword,SubSectionKeyword,SubSubSection

admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(SubSection)

admin.site.register(ChapterKeyword)
admin.site.register(SectionKeyword)
admin.site.register(SubSectionKeyword)
admin.site.register(SubSubSection)
