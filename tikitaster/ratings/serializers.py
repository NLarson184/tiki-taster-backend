from rest_framework import serializers
from ratings.models import Rating, Drink, Bar, Tag


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = Rating
        fields = ['url', 'id', 'created', 'creator', 'overall_rating', 'bar', 'drink']

class DrinkSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
        model = Drink
        fields = ['url', 'name', 'bar', 'tags']

class BarSerializer(serializers.HyperlinkedModelSerializer):
    drinks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='drink-detail')

    class Meta:
        model = Bar
        fields = ['url', 'name', 'drinks']

class TagSerializer(serializers.HyperlinkedModelSerializer):
    drinks = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Tag
        fields = ['url', 'name', 'drinks']