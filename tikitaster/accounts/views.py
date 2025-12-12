from django.shortcuts import render
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import UserSerializer

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
        
