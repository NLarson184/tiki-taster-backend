from django.urls import path, include
from ratings import views
from rest_framework.urlpatterns import format_suffix_patterns
from ratings.views import api_root, RatingViewSet

rating_list = RatingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

bar_list = RatingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

drink_list = RatingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('', views.api_root),
    path('ratings/', rating_list, name='rating-list'),
    path('bars/', bar_list, name='bar-list'),
    path('drinks/', drink_list, name='drink-list')
]

urlpatterns = format_suffix_patterns(urlpatterns)