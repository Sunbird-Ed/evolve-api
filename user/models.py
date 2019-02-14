from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin,AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from apps.configuration.models import State
from django.contrib.auth.models import User
# class EvolveUser(AbstractUser):
#     pass

# class CustomUser(User):
#     username_validator = ASCIIUsernameValidator()
    
class Roles(models.Model):
    rolename=models.CharField(max_length=200)

    def __str__(self):
		return self.rolename

	class Meta:
		verbose_name='Role'


class UserDetails(models.Model):
    state=models.ForeignKey(State,on_delete=models.CASCADE)
    role=models.ForeignKey(Roles,on_delete=models.CASCADE)
    user=models.OneToOneField(User,on_delete=models.CASCADE, to_field='id', primary_key=True)


    def __str__(self):
		return self.user.username

	class Meta:
		verbose_name='user detail'