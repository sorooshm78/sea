from django.urls import path
from . import views


app_name = "single_player"
urlpatterns = [
    path("", views.SinglePlayerView.as_view(), name="single_player"),
    path("attack/", views.attack, name="attack"),
    path("search/", views.search, name="search"),
    path("new-game/", views.NewGameView.as_view(), name="new_game"),
]
