from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/game", consumers.GameConsumer.as_asgi()),
    path("ws/search-user", consumers.SearchUserConsumer.as_asgi()),
]
