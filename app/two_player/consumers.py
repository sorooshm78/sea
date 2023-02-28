import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache
from django.urls import reverse

from sea_battle.two_player import TwoPlayer


class SearchUserConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.my_username = self.scope["user"].username
        self.my_group_name = f"serach_{self.my_username}"

        async_to_sync(self.channel_layer.group_add)(
            self.my_group_name,
            self.channel_name,
        )

        if cache.get(self.my_username) is not None:
            # Redirect to game
            return

        alone_user = cache.get("alone_user")

        if alone_user is None:
            cache.set("alone_user", self.my_username)
            return

        if alone_user == self.my_username:
            return

        cache.set(self.my_username, alone_user)
        cache.set(alone_user, self.my_username)
        game = TwoPlayer(self.my_username, alone_user)
        cache.set(TwoPlayer.get_game_room_key(self.my_username, alone_user), game)
        cache.delete("alone_user")

        game_url = reverse("two_player")
        # Send to client to redirect game page
        async_to_sync(self.channel_layer.group_send)(
            self.my_group_name,
            {
                "type": "send_to_websocket",
                "url": game_url,
            },
        )
        async_to_sync(self.channel_layer.group_send)(
            f"serach_{alone_user}",
            {
                "type": "send_to_websocket",
                "url": game_url,
            },
        )

    def disconnect(self, close_code):
        alone_user = cache.get("alone_user")
        if alone_user is not None and alone_user == self.my_username:
            cache.delete("alone_user")

        async_to_sync(self.channel_layer.group_discard)(
            self.my_group_name,
            self.channel_name,
        )

    def send_to_websocket(self, data):
        self.send(text_data=json.dumps(data))


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.my_username = self.scope["user"].username
        game = TwoPlayer.get_game(self.my_username)
        my_player, opposite_player = game.get_my_and_opposite_player_by_username(
            self.my_username
        )

        if my_player is None or opposite_player is None:
            return

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.my_username,
            self.channel_name,
        )

        # Send user info to my player
        self.send_data(
            to=self.my_username,
            data={
                "report": opposite_player.get_report_game(),
                "attack_count": opposite_player.get_attack_count(),
                "turn": self.get_turn(game, self.my_username),
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
        my_player, opposite_player = game.get_my_and_opposite_player_by_username(
            self.my_username
        )

        print(f"in {self.my_username} cousumer")
        print(f"my player sea {my_player.sea}")
        print(f"oppo player sea {opposite_player.sea}")

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

        print(
            f"in {self.my_username} cousumer and count attack is {opposite_player.get_attack_count()}"
        )
        game.save_data()

    def search(self, game, opposite_player, cells):
        for cell in cells:
            cell_value = cell.pop("value")
            if cell_value.is_ship():
                cell["class"] = "radar-ship"
            else:
                cell["class"] = "radar-empty"

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
                cell["class"] = "ship-selected"
                bonus = True
            else:
                cell["class"] = "empty-selected"

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
