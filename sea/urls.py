from django.urls import path
from . import views


urlpatterns = [
    path("", views.single_player, name="single_player"),
    path("attack/", views.attack, name="select_cell"),
    path("search/", views.search, name="search_by_radar"),
    path("new-game/", views.new_game, name="new_game"),
    path("score-board/", views.ScoreBoardListView.as_view(), name="score_board"),
]
