from django.urls import path
from flashcards import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home),
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True, success_url="/"),
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/")),
    path("register/", views.register),
]
