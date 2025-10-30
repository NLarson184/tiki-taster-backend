from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import serializers

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('ratings.urls'))
]

# --- DRFSO2 ENDPOINT ---
urlpatterns += [
    path('auth/', include('drf_social_oauth2.urls', namespace='drf'))
]