
from ratings.models import Rating, Drink, Bar, Tag
from ratings.serializers import RatingSerializer, DrinkSerializer, BarSerializer, TagSerializer
# from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
# from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, renderers, viewsets
from django.contrib.auth.models import User

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

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BarViewSet(viewsets.ModelViewSet):
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def drinks_at_bar(self, request, pk):
        try:
            bar = Bar.objects.get(pk=pk)
        except Bar.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        drinks = bar.drinks.all()
        serializer = DrinkSerializer(drinks, context={'request': request}, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]