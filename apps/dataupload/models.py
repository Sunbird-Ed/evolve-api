from django.db import models

from apps.configuration.models import Book




class Chapter(models.Model):
	book = models.ForeignKey(Book,
		on_delete=models.CASCADE)
	chapter = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)
	def __str__(self):
		return self.chapter

	class Meta:
		verbose_name='Chapter'
		verbose_name_plural='Chapter'

class Section(models.Model):
	chapter = models.ForeignKey(Chapter,
		on_delete=models.CASCADE,null=False)
	section = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.section

	class Meta:
		verbose_name='Section'
		verbose_name_plural='Sections'

class SubSection(models.Model):
	section = models.ForeignKey(Section,
		on_delete=models.CASCADE,null=False)
	sub_section = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.sub_section

	class Meta:
		verbose_name='Sub section'
		verbose_name_plural='Sub sections'

class SubSubSection(models.Model):
	subsection = models.ForeignKey(SubSection,
		on_delete=models.CASCADE,null=False)
	sub_sub_section = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.sub_sub_section

	class Meta:
		verbose_name='Sub Sub section'
		verbose_name_plural='Sub Sub sections'




class ChapterKeyword(models.Model):
	chapter = models.ForeignKey(Chapter,
		on_delete=models.CASCADE)
	keyword = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.keyword

	class Meta:
		verbose_name='Chapter keyword'
		verbose_name_plural='Chapter keywords'

class SectionKeyword(models.Model):
	section = models.ForeignKey(Section,
		on_delete=models.CASCADE,null=False)
	keyword = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.keyword

	class Meta:
		verbose_name='Section keyword'
		verbose_name_plural='Section keywords'

class SubSectionKeyword(models.Model):
	sub_section = models.ForeignKey(SubSection,
		on_delete=models.CASCADE,null=False)
	keyword = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.keyword

	class Meta:
		verbose_name='Sub section keyword'
		verbose_name_plural='Sub sections keywords'

class SubSubSectionKeyword(models.Model):
	sub_sub_section = models.ForeignKey(SubSubSection,
		on_delete=models.CASCADE,null=False)
	keyword = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.keyword

	class Meta:
		verbose_name='Sub Sub section keyword'
		verbose_name_plural='Sub Sub sections keywords'