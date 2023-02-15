from django.urls import path
from . import views


urlpatterns = [
    path("", views.two_player, name="two_player"),
]
