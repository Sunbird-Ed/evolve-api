from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class EvolveUser(AbstractUser):
    # add additional fields in here
    identifier=models.CharField(max_length=200)

    
    def __str__(self):
        return self.username