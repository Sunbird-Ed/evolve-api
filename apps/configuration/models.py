from django.db import models



class State(models.Model):
    
    state = models.CharField(max_length=200)
    state_logo=models.ImageField(upload_to='logos/',
			blank=True,
			null=True,)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = "States"

    def __str__(self):
        return self.state
    
class Medium(models.Model):
    
    medium = models.CharField(max_length=200)
    state=models.ForeignKey(State,on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "Medium"
        verbose_name_plural = "Medium"

    def __str__(self):
        return self.medium

class Grade(models.Model):
    
    grade = models.CharField(max_length=200)
    medium=models.ForeignKey(Medium,on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

    def __str__(self):
        return self.grade

class Subject(models.Model):

    Subject = models.CharField(max_length=200)
    grade=models.ForeignKey(Grade,on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name='Subject'
        verbose_name_plural='Subjects'

    def __str__(self):
        return self.Subject

class Book(models.Model):   
    book = models.CharField(max_length=200)
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name='Book'
        verbose_name_plural='Books'
    def __str__(self):
        return self.book