from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin,AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from apps.configuration.models import State

class EvolveUser(AbstractUser):
    pass
    
class Roles(models.Model):
    rolename=models.CharField(max_length=200)



class UserDetails(models.Model):
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    role=models.ForeignKey(Roles,on_delete=models.CASCADE)
    user=models.OneToOneField(EvolveUser,on_delete=models.CASCADE, to_field='id', primary_key=True)


