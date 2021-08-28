from django.urls import path

from django.contrib.auth import views
from .views import RegisterView, UserDecksView

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('decks/', UserDecksView.as_view(), name='decks'),
]