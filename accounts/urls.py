from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login_user"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout_user"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
]
