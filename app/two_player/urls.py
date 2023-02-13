from django.urls import path
from . import views


urlpatterns = [
    path("", views.double_player, name="double_player"),
]
