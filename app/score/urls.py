from django.urls import path
from . import views


app_name = "score"
urlpatterns = [
    path("", views.ScoreBoardListView.as_view(), name="score_board"),
]
