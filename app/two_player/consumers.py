import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import GameRoomModel


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.user = self.scope["user"]

        async_to_sync(self.channel_layer.group_add)(
            self.user.username,
            self.channel_name,
        )

        self.room: GameRoomModel = GameRoomModel.rooms.create_room(self.user)
        if not self.room.has_capacity():
            username1 = self.room.user1.username
            username2 = self.room.user2.username

            async_to_sync(self.channel_layer.group_send)(
                self.room.user1.username,
                {
                    "type": "send_game_data",
                    "user_info": username2,
                },
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room.user2.username,
                {
                    "type": "send_game_data",
                    "user_info": username1,
                },
            )

    def disconnect(self, close_code):
        self.room.deactivate_game_room()
        async_to_sync(self.channel_layer.group_discard)(
            self.user.username,
            self.channel_name,
        )

    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

    def send_game_data(self, data):
        self.send(text_data=json.dumps(data))
