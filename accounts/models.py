from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


# class CustomUser(AbstractBaseUser):
#     email = models.EmailField(verbose_name= "email",max_length=100, unique=True)
#     username = models.CharField(max_length=100, unique=True)
#     # profile_image= models.ImageField(max_Length=255, upload_to=,null=True,blank= True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS= ['username']

#     def __str__(self):
#         return self.username
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
#     def has_module_perms(self, app_label):
#         return True