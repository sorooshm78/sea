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

        game = TwoPlayer.get_game(self.my_username)

        if game.is_game_ready():
            my_player = game.get_player_by_username(self.my_username)
            opposite_player = game.get_opposite_player_by_username(self.my_username)

            # Send user info to my player
            self.send_data(
                to=self.my_username,
                data={
                    "user_info": opposite_player.username,
                    "report": opposite_player.get_report_game(),
                    "attack_count": opposite_player.get_attack_count(),
                    "turn": self.get_turn(game, self.my_username),
                },
            )

            # Send user info to my oppsite player
            self.send_data(
                to=opposite_player.username,
                data={
                    "user_info": self.my_username,
                    "report": my_player.get_report_game(),
                    "attack_count": my_player.get_attack_count(),
                    "turn": self.get_turn(game, opposite_player.username),
                },
            )

    def disconnect(self, close_code):
        TwoPlayer.disactive_game(self.my_username)
        async_to_sync(self.channel_layer.group_discard)(
            self.my_username,
            self.channel_name,
        )

    def receive(self, text_data=None):
        game = TwoPlayer.get_game(self.my_username)
        my_player = game.get_player_by_username(self.my_username)
        opposite_player = game.get_opposite_player_by_username(self.my_username)

        if not game.is_player_turn(my_player):
            print(f"not your turn {self.my_username}")
            return

        text_data_json = json.loads(text_data)

        select = text_data_json["select"]
        attack_type = select.get("attack_type")
        x = select.get("x")
        y = select.get("y")

        cells = opposite_player.get_changes(x, y, attack_type)
        if cells is None:
            return

        if attack_type == "radar":
            self.search(game, opposite_player, cells)
        else:
            self.attack(game, opposite_player, cells)

        game.save_data()

    def search(self, game, opposite_player, cells):
        for cell in cells:
            cell_value = cell.pop("value")
            if cell_value.is_ship():
                cell["class"] = "radar-target"
            else:
                cell["class"] = "radar-select"

        game.change_turn()

        self.send_data(
            to=self.my_username,
            data={
                "opposite_cells": cells,
                "turn": self.get_turn(game, self.my_username),
            },
        )
        self.send_data(
            to=opposite_player.username,
            data={
                "turn": self.get_turn(game, opposite_player.username),
            },
        )

    def attack(self, game, opposite_player, cells):
        bonus = False

        for cell in cells:
            cell_value = cell.pop("value")
            if cell_value.is_ship():
                cell["class"] = "target"
                bonus = True
            else:
                cell["class"] = "select"

        if not bonus:
            game.change_turn()

        winner = None
        if opposite_player.is_end_game():
            winner = self.my_username

        self.send_data(
            to=self.my_username,
            data={
                "opposite_cells": cells,
                "report": opposite_player.get_report_game(),
                "winner": winner,
                "turn": self.get_turn(game, self.my_username),
            },
        )

        self.send_data(
            to=opposite_player.username,
            data={
                "my_cells": cells,
                "winner": winner,
                "turn": self.get_turn(game, opposite_player.username),
            },
        )

    def send_data(self, to, data):
        context = {"type": "send_to_websocket"}
        context.update(data)
        async_to_sync(self.channel_layer.group_send)(
            to,
            context,
        )

    def send_to_websocket(self, data):
        self.send(text_data=json.dumps(data))

    def get_turn(self, game, username):
        turn = game.get_turn()
        if turn == username:
            return "my_turn"
        return "opposite_turn"
