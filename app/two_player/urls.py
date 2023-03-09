from django.urls import path
from . import views


app_name = "two_player"
urlpatterns = [
    path("", views.TwoPlayerView.as_view(), name="two_player"),
    path("search-user/", views.SearchUserView.as_view(), name="search_user"),
    path("exit-game/", views.ExitGameView.as_view(), name="exit_game"),
    path("new-game/", views.NewGameView.as_view(), name="new_game"),
]
