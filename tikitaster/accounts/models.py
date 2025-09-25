from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.URLField
    is_official = models.BooleanField

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
