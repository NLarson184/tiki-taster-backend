from django.urls import include, path

urlpatterns = [
    path('', include('ratings.urls'))
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]