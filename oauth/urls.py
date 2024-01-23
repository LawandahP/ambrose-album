from django.urls import path
from .views import GitHubAuthView

urlpatterns = [
    path('github/',  GitHubAuthView.as_view(), name="github"),
]