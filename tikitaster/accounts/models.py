from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.URLField
    is_official = models.BooleanField

    def __str__(self):
        return self.email
