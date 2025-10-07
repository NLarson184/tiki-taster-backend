from rest_framework import serializers
from ratings.models import Rating, Drink, Bar, Tag


class RatingSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = Rating
        fields = ['url', 'id', 'created', 'creator', 'overall_rating', 'bar', 'drink']
        depth = 1

class DrinkSerializer(serializers.ModelSerializer):
   class Meta:
        model = Drink
        fields = ['url', 'id', 'name', 'bar', 'tags', 'ratings']
        depth = 1

class BarSerializer(serializers.ModelSerializer):
    # drinks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='drink-detail')

    class Meta:
        model = Bar
        fields = ['url', 'id', 'name', 'drinks']
        depth = 1

class TagSerializer(serializers.ModelSerializer):
    drinks = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Tag
        fields = ['url', 'name', 'drinks']
        depth = 1