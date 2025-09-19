from django.db import models
import user

class Rating(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1)
    bar = models.ForeignKey('Bar', on_delete=models.CASCADE)
    drink = models.ForeignKey('Drink', on_delete=models.CASCADE)
    creator = models.ForeignKey(user.User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

class Bar(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()

class Drink(models.Model):
    created = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.TextField()
