from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import UserManager

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    birthday = models.DateField()
    is_active = models.BooleanField(default=True)
    profile_picture = models.URLField(max_length=200, blank=True, null=True)
    is_official = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'birthday']

    def __str__(self):
        return self.email
