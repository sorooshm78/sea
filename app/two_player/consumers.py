import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    
        self.user = self.scope['user']
        self.user_id = self.user.id

        online_users = cache.get_or_set('online_users', set())
        online_users.add(self.user_id)
        cache.set('online_users', online_users)
        
        print('add', self.user_id)
        print('online', online_users)

        async_to_sync(self.channel_layer.group_add)(
            str(self.user_id),
            self.channel_name,
        )

    def disconnect(self, close_code):
        online_users = cache.get('online_users')
        online_users.discard(self.user_id)
        cache.set('online_users', online_users)

        print('del', self.user_id)
        print('online', online_users)

        async_to_sync(self.channel_layer.group_discard)(
            str(self.user_id),
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