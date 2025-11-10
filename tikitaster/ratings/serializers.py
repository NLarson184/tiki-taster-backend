from rest_framework import serializers
from ratings.models import Rating, Drink, Bar, Tag
from django.db import transaction


class RatingSerializer(serializers.ModelSerializer):
    # WRITE_ONLY data for incoming string data
    bar_id = serializers.CharField(write_only=True)
    drink_name = serializers.CharField(write_only=True)
    tag_list = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False  # Tags are optional
    )
    
    # READ_ONLY data for output
    creator = serializers.ReadOnlyField(source='creator.email')

    class Meta:
        model = Rating
        fields = [
            'url', 'id', 'created', 'creator', 'overall_rating', 'taste_rating', 'presentation_rating',
            # Output FKs
            'bar', 'drink',
            # Input Custom Fields
            'bar_id', 'drink_name', 'tag_list']
        depth = 1
        read_only_fields = ('bar', 'drink')
        
    # Create a new Rating, while "upserting" (update or insert) Bar, Drink, and Tag objects
    #
    # If the received bar, drink, or tag doesn't exist, we will create an entry before finalizing
    # the rating.
    @transaction.atomic
    def create(self, validated_data):
        bar_id = validated_data.pop('bar_id').strip()
        drink_name = validated_data.pop('drink_name').strip()
        tag_list = validated_data.pop('tag_list', [])
        
        # Get Bar
        bar_instance= Bar.objects.get(
            id=bar_id
        )
        
        # Get or Create Drink
        drink_instance, _ = Drink.objects.get_or_create(
            name__iexact=drink_name,
            bar=bar_instance,
            defaults={'name': drink_name, 'bar': bar_instance}
        )
        
        # Create the Ratings object
        validated_data['bar'] = bar_instance
        validated_data['drink'] = drink_instance
        rating_instance = Rating.objects.create(**validated_data)
        
        # Get or Create Tags and attach to Drink
        tag_instances = []
        for tag_name in tag_list:
            tag_instance, _ = Tag.objects.get_or_create(
                name__iexact=tag_name.strip(),
                defaults={'name': tag_name.strip()}
            )
            tag_instances.append(tag_instance)
        
        drink_instance.tags.add(*tag_instances)
        
        return rating_instance
        
class DrinkSerializer(serializers.ModelSerializer):
    average_overall_rating = serializers.DecimalField(
        max_digits = 3,
        decimal_places = 1,
        source = 'avg_overall',
        read_only = True,
        default = None
    )
    average_taste_rating = serializers.DecimalField(
        max_digits = 3,
        decimal_places = 1,
        source = 'avg_taste',
        read_only = True,
        default = None
    )
    average_presentation_rating = serializers.DecimalField(
        max_digits = 3,
        decimal_places = 1,
        source = 'avg_presentation',
        read_only = True,
        default = None
    )
    
    class Meta:
        model = Drink
        fields = [
            'url', 'id', 'name', 'bar', 'tags', 'ratings',
            # Aggregated Fields
            'average_overall_rating',
            'average_taste_rating',
            'average_presentation_rating'
            ]
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
        fields = ['url', 'id', 'name', 'drinks']
        depth = 1