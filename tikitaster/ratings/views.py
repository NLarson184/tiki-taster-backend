
from ratings.models import Rating
from ratings.serializers import RatingSerializer
# from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, permissions, renderers, viewsets
from django.contrib.auth.models import User

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class RatingViewSet(viewsets.modelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)