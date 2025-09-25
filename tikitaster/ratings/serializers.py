from rest_framework import serializers
from ratings.models import Rating, Drink, Bar


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = Rating
        fields = ['url', 'id', 'created', 'creator']

class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drink
        fields = ['url', 'name', 'bar']

class BarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bar
        fields = ['url', 'name', 'ratings']