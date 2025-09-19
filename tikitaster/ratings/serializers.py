from rest_framework import serializers
from ratings.models import Rating
from django.contrib.auth.models import User


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ['url', 'id', 'created', 'name']
