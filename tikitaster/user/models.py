from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_pic = models.URLField()
    is_official = models.BooleanField(default=False)