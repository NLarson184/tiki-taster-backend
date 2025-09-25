
from ratings.models import Rating, Drink, Bar
from ratings.serializers import RatingSerializer, DrinkSerializer, BarSerializer
# from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, permissions, renderers, viewsets
from django.contrib.auth.models import User

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ratings': reverse('rating-list', request=request, format=format),
        'bars': reverse('bar-list', request=request, format=format),
        'drinks': reverse('drink-list', request=request, format=format)
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