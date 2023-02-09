import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user_id = "1"
        async_to_sync(self.channel_layer.group_add)(
            self.user_id,
            self.channel_name,
        )

    def disconnect(self, close_code):
        self.user_id = "1"
        async_to_sync(self.channel_layer.group_discard)(
            self.user_id,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.user_id,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))