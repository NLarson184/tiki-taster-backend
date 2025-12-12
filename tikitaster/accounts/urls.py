from django.urls import path, include
from accounts.views import CurrentUserView

urlpatterns = [
    path('details', CurrentUserView.as_view(), name='current-user')
]