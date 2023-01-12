from django.urls import path
from . import views


urlpatterns = [
    path("", views.single_player, name="single_player"),
    path("select/", views.select, name="select_cell"),
    path("new-game/", views.new_game, name="new_game"),
]
