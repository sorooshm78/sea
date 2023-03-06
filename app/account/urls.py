from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "account"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
]
