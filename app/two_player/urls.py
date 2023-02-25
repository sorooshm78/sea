from django.urls import path
from . import views


urlpatterns = [
    path("", views.TwoPlayerView.as_view(), name="two_player"),
]
