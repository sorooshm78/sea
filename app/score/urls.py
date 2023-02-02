from django.urls import path
from . import views


urlpatterns = [
    path("", views.ScoreBoardListView.as_view(), name="score_board"),
]
