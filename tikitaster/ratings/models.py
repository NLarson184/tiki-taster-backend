from django.db import models
from django.contrib.auth.models import AbstractUser

class Rating(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1)
    bar = models.ForeignKey('Bar', related_name='ratings', on_delete=models.CASCADE)
    drink = models.ForeignKey('Drink', related_name='ratings', on_delete=models.CASCADE)
    creator = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

class Bar(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()

    def __str__(self):
        return self.name

class Drink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=60, default='Default Drink')
    bar = models.ForeignKey('Bar', related_name='drinks', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='drinks')
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name
