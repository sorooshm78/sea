from django.urls import path
from . import views


app_name = "history"
urlpatterns = [
    path("", views.GameHistoryView.as_view(), name="game_history"),
]
