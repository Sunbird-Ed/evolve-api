from django.db import models
from apps.configuration.models import Book, Grade, State, Medium, Subject
from django.contrib.auth.models import User
# from user.models import EvolveUser
from apps.dataupload.models import Section,SubSection,Chapter,ChapterKeyword,SectionKeyword,SubSectionKeyword
from apps.hardspot.models import HardSpot
from django.core.validators import MaxValueValidator
# Create your models here.




class ContentContributors(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200, 
		blank=True,
		null=True)
	email = models.EmailField(blank=True, null=True)
	mobile =models.CharField(max_length=10,
		blank=False,
		null=False)

	def __str__(self):
		return self.first_name

	class Meta:
		verbose_name='Content Contributor'

		
class Content(models.Model):

	GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
	chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE,null=True,blank=True)
	section=models.ForeignKey(Section,on_delete=models.CASCADE,null=True,blank=True)
	sub_section=models.ForeignKey(SubSection,on_delete=models.CASCADE,null=True,blank=True)
	content_name = models.CharField(max_length=200)
	video = models.FileField(upload_to='video/',
			blank=True,
			null=True,)
	approved = models.BooleanField(default=False)
	approved_by = models.ForeignKey(User,
		on_delete=models.CASCADE,
		related_name='%(class)s_approved_by',
		null=True,
		blank=True)
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)],
		blank=True,null=True)
	rated_by = models.ForeignKey(User,
		on_delete=models.CASCADE,
		related_name='%(class)s_rated_by',null=True,blank=True)
	comment = models.CharField(max_length=200, null=True, blank=True)
	chapter_keywords=models.ManyToManyField(ChapterKeyword,blank=True)
	section_keywords=models.ManyToManyField(SectionKeyword,blank=True)
	sub_section_keywords=models.ManyToManyField(SubSectionKeyword,blank=True)
	content_contributors=models.ForeignKey(ContentContributors,on_delete=models.CASCADE)
	def __str__(self):
		return self.content_name

	class Meta:
		verbose_name='content'


