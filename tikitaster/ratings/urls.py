from django.urls import path, include
from ratings import views
from rest_framework.urlpatterns import format_suffix_patterns
from ratings.views import api_root, RatingViewSet, BarViewSet, DrinkViewSet, TagViewSet

rating_list = RatingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
rating_detail = RatingViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

bar_list = BarViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
bar_detail = BarViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
drinks_at_bar = BarViewSet.as_view({
    'get': 'drinks_at_bar'
})
search_bars = BarViewSet.as_view({
    'get': 'geoapify_search'
})

drink_list = DrinkViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
drink_detail = DrinkViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

tag_list = TagViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
tag_detail = TagViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', views.api_root),
    path('ratings/', rating_list, name='rating-list'),
    path('ratings/<int:pk>/', rating_detail, name='rating-detail'),
    path('bars/', bar_list, name='bar-list'),
    path('bars/<str:pk>/', bar_detail, name='bar-detail'),
    path('bars/<str:pk>/drinks', drinks_at_bar, name='drinks-at-bar'),
    path('bars/search', search_bars, name='search-bars'),
    path('drinks/', drink_list, name='drink-list'),
    path('drinks/<int:pk>/', drink_detail, name='drink-detail'),
    path('tags/', tag_list, name='tag-list'),
    path('tags/<int:pk>/', tag_detail, name='tag-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)