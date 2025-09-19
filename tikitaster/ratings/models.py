from django.db import models
from django.contrib.auth.models import AbstractUser

class Rating(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1)
    bar = models.ForeignKey('Bar', on_delete=models.CASCADE)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)

class Bar(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()

class Drink(models.Model):
    created = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    pass