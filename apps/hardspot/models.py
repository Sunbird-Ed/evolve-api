from django.db import models
from apps.configuration.models import Book, Grade, State, Medium, Subject
# from django.contrib.auth.models import User
from user.models import EvolveUser
from apps.dataupload.models import Chapter,Section,SubSection
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


class HardSpotContributors(models.Model):
	


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
		verbose_name='Hardspot Contributor'


class HardSpot(models.Model):
	TARGET_CHOICES = (
        ('Teachers', 'Teachers'),
        ('Students', 'Students'),
        ('Both', 'Both'),
    )
	chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE,null=True, blank=True)
	section=models.ForeignKey(Section,on_delete=models.CASCADE,null=True, blank=True)
	sub_section=models.ForeignKey(SubSection,on_delete=models.CASCADE,null=True, blank=True)
	hard_spot = models.TextField()
	description = models.TextField()
	points_to_be_covered = models.TextField()
	useful_to = models.CharField(max_length=20, choices=TARGET_CHOICES, default='Students')
	approved = models.BooleanField(default=False)
	rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)],
		blank=True,null=True)
	approved_by = models.ForeignKey(EvolveUser,
		on_delete=models.CASCADE,null=True,blank=True)
	comment = models.CharField(max_length=200, blank=True, null=True)
	hardspot_contributor=models.ForeignKey(HardSpotContributors,on_delete=models.CASCADE)
	def __str__(self):
		return self.hard_spot

	class Meta:
		verbose_name='Hard Spot'
		verbose_name_plural='Hard Spots'
