from django.urls import path
from . import views


urlpatterns = [
    path("", views.DoublePlayerView.as_view(), name="double_player"),
]
