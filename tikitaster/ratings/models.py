from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import DrinkQuerySet

class Rating(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1)
    taste_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    presentation_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    bar = models.ForeignKey('Bar', related_name='ratings', on_delete=models.CASCADE)
    drink = models.ForeignKey('Drink', related_name='ratings', on_delete=models.CASCADE)
    creator = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    
    class Meta:
        # A user can only make 1 rating per drink
        unique_together = ('creator', 'drink')

class Bar(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    formatted_address = models.TextField(default = '')
    
    # Store the ID from Foursquare's Places API for easy lookup
    foursquare_place_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Drink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=60, default='Default Drink')
    bar = models.ForeignKey('Bar', related_name='drinks', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='drinks')
    
    objects = DrinkQuerySet.as_manager()
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name
