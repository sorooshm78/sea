import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from sea_battle.two_player import TwoPlayer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.my_username = self.scope["user"].username

        async_to_sync(self.channel_layer.group_add)(
            self.my_username,
            self.channel_name,
        )

        self.game = TwoPlayer(self.my_username)

        if not self.game.is_game_ready():
            opposite_username = self.game.get_opposite_username(self.my_username)

            # Send data to my player
            async_to_sync(self.channel_layer.group_send)(
                self.my_username,
                {
                    "type": "send_game_data",
                    "user_info": opposite_username,
                    "report": self.game.get_report_game(opposite_username),
                    "attack_count": self.game.get_attack_count(opposite_username),
                },
            )

            # Send data to my oppsite player
            async_to_sync(self.channel_layer.group_send)(
                opposite_username,
                {
                    "type": "send_game_data",
                    "user_info": self.my_username,
                    "report": self.game.get_report_game(self.my_username),
                    "attack_count": self.game.get_attack_count(self.my_username),
                },
            )

    def disconnect(self, close_code):
        self.game.deactive_room(self.my_username)
        async_to_sync(self.channel_layer.group_discard)(
            self.my_username,
            self.channel_name,
        )

    def receive(self, text_data=None):
        if not self.game.is_player_turn(self.my_username):
            print(f"not your turn {self.my_username}")
            return

        text_data_json = json.loads(text_data)
        select = text_data_json["select"]

        opposite_username = self.game.get_opposite_username(self.my_username)

        x = select.get("x")
        y = select.get("y")
        attack_type = select.get("attack_type")

        cells = self.game.get_changes(self.my_username, x, y, attack_type)
        if cells is None:
            return

        if attack_type == "radar":
            self.search(cells)
        else:
            self.attack(cells, opposite_username)

        self.game.change_turn()

    def search(self, cells):
        for cell in cells:
            cell_value = cell.pop("value")
            if cell_value.is_ship():
                cell["class"] = "radar-target"
            else:
                cell["class"] = "radar-select"

        async_to_sync(self.channel_layer.group_send)(
            self.my_username,
            {
                "type": "send_game_data",
                "opposite_cells": cells,
            },
        )

    def attack(self, cells, opposite_username):
        for cell in cells:
            cell_value = cell.pop("value")
            if cell_value.is_ship():
                cell["class"] = "target"
            else:
                cell["class"] = "select"

        async_to_sync(self.channel_layer.group_send)(
            self.my_username,
            {
                "type": "send_game_data",
                "opposite_cells": cells,
                "report": self.game.get_report_game(opposite_username),
            },
        )
        async_to_sync(self.channel_layer.group_send)(
            opposite_username,
            {
                "type": "send_game_data",
                "my_cells": cells,
            },
        )

    def send_game_data(self, data):
        self.send(text_data=json.dumps(data))
