from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("attack/", views.attack, name="attack"),
    path("search/", views.search, name="search"),
    path("new-game/", views.new_game, name="new_game"),
]
