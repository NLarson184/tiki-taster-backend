
from ratings.models import Rating, Drink, Bar, Tag
from ratings.serializers import RatingSerializer, DrinkSerializer, BarSerializer, FoursquarePlaceSerializer, TagSerializer
# from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
import os
import requests
from urllib.parse import quote_plus
from rest_framework.reverse import reverse
# from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, renderers, viewsets
from django.contrib.auth.models import User

# Helper function to get client's IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Fallback for direct connections
        ip = request.META.get('REMOTE_ADDR')
    return ip

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ratings': reverse('rating-list', request=request, format=format),
        'bars': reverse('bar-list', request=request, format=format),
        'drinks': reverse('drink-list', request=request, format=format),
        'tags': reverse('tag-list', request=request, format=format)
    })

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class DrinkViewSet(viewsets.ModelViewSet):
    # Calculate rating averages to optimize requests
    queryset = Drink.objects.with_average_ratings().all()
    
    serializer_class = DrinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True)
    def drinks_at_bar(self, request, pk):
        try:
            bar = Bar.objects.get(id = pk)
        except Bar.DoesNotExist:
            return Response()
        
        drinks = bar.drinks.with_average_ratings().all()
        serializer = DrinkSerializer(drinks, context={'request': request}, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='geo-search')
    def geoapify_search(self, request):
        bar_name = request.query_params.get('name')
        
        if not bar_name:
            return Response(
                {"error": "Missing required parameter: name."},
                status=status.HTTP_400_BAD_REQUEST
            )

        client_ip = get_client_ip(request)
        if client_ip == '127.0.0.1':
            # Overwrite local IP addresses for testing
            client_ip = '47.151.138.177'
        
        # Pull the API keys from the .env file
        GEOAPIFY_API_KEY = os.getenv('GEOAPIFY_API_KEY')
        FOURSQUARE_API_KEY = os.getenv('FOURSQUARE_API_KEY')
        
        # Get location data of the request
        IP_GEOLOCATION_URL = "https://api.geoapify.com/v1/ipinfo"
        try:
            ip_info_response = requests.get(IP_GEOLOCATION_URL, params={
                'apiKey': GEOAPIFY_API_KEY,
                'ip': client_ip
            })
            ip_info_response.raise_for_status() # throw HTTP error if necessary
            ip_info = ip_info_response.json()
            
            lat = ip_info['location']['latitude']
            lon = ip_info['location']['longitude']
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Location lookup failed: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Run the request with proximity to the request
        PLACES_URL = 'https://places-api.foursquare.com/autocomplete'
        query_params = {
            'query': bar_name,
            'll': f'{lat},{lon}',
            'radius': '100000',
            'session_token': request.session.session_key
        }
        headers = {
            "accept": "application/json",
            "X-Places-Api-Version": "2025-06-17",
            "authorization": f"Bearer {FOURSQUARE_API_KEY}"
        }
        
        try:
            # Call the Foursquare places API
            places_response = requests.get(PLACES_URL, params=query_params, headers=headers)
            places_response.raise_for_status()
            
            # Pull out the list of places from the response
            full_response = places_response.json()
            place_list = [item['place'] for item in full_response.get('results', [])]
            
            # Flatten and filter the data to only show the data we need
            serializer = FoursquarePlaceSerializer(data=place_list, many=True)
            
            # Return the data (or throw exception if it failed validation)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to search: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]