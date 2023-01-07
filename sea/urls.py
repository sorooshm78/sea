from django.urls import path
from . import views


urlpatterns = [
    path("", views.single_player_view, name="single_player"),
    path("select/<int:cell>", views.select, name="select_cell"),
]
