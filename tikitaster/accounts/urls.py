from django.urls import path, include
from accounts.views import CurrentUserView, CreateUserView

urlpatterns = [
    path('details', CurrentUserView.as_view(), name='current-user'),
    path('register', CreateUserView.as_view(), name='create-user')
]