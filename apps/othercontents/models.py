from django.db import models

from apps.configuration.models import Book, Grade, State, Medium, Subject
from django.contrib.auth.models import User
# from user.models import EvolveUser
from apps.dataupload.models import Section,SubSection,Chapter,ChapterKeyword,SectionKeyword,SubSectionKeyword,SubSubSection,SubSubSectionKeyword
from apps.hardspot.models import HardSpot
from django.core.validators import MaxValueValidator
from evolve.custom_storage import MediaStorage
from datetime import datetime


class Tags(models.Model):
    tag_name = models.CharField(max_length=200)
    code_name = models.SlugField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name='Tag'
   




class OtherContributors(models.Model):

    tags = models.ForeignKey(Tags,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, 
        blank=True,
        null=True)
    email = models.EmailField(blank=True, null=True)
    mobile =models.CharField(max_length=10,
        blank=False,
        null=False)
    school_name = models.CharField(max_length=400, 
        blank=True,
        null=True)
    city_name = models.CharField(max_length=200, 
        blank=True,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name='Other Contributor'



class OtherContent(models.Model):

    tags = models.ForeignKey(Tags,on_delete=models.CASCADE)
    hard_spot=models.ForeignKey(HardSpot,on_delete=models.CASCADE,null=True,blank=True)
    chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE,null=True,blank=True)
    section=models.ForeignKey(Section,on_delete=models.CASCADE,null=True,blank=True)
    sub_section=models.ForeignKey(SubSection,on_delete=models.CASCADE,null=True,blank=True)
    sub_sub_section=models.ForeignKey(SubSubSection,on_delete=models.CASCADE,null=True,blank=True)
    content_name = models.CharField(max_length=200)
    video = models.URLField(max_length=1000, blank=True,null=True)
    documents = models.URLField(max_length=1000, blank=True,null=True)
    text = models.TextField(blank=True,null=True)
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
    sub_sub_section_keywords=models.ManyToManyField(SubSubSectionKeyword,blank=True)

    content_contributors=models.ForeignKey(OtherContributors,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.documents == None and self.text == "" and self.video == None:
            raise ValueError("document url, video url and text ,all null values are Not allowed")
        elif self.documents != None and self.text != "" and self.video != None:
            raise ValueError("document url, video url and text ,all values are Not allowed")
        else:
            super().save(*args, **kwargs)
        
     
 
    def __str__(self):
        return self.content_name


    class Meta:
        verbose_name='Other Content'

