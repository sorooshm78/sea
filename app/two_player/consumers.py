import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache
from django.urls import reverse
from django.conf import settings

from sea_battle.two_player import TwoPlayer
from history.models import GameHistoryModel
from utils import wrap_data


CACHE_TTL = settings.CACHE_TTL


class SearchUserConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.current_username = self.scope["user"].username
        self.my_group_name = f"serach_{self.current_username}"

        async_to_sync(self.channel_layer.group_add)(
            self.my_group_name,
            self.channel_name,
        )

        alone_user = cache.get("#alone_user")

        if alone_user is None:
            cache.set("#alone_user", self.current_username)
            return

        if alone_user == self.current_username:
            return

        cache.set(self.current_username, alone_user, CACHE_TTL)
        cache.set(alone_user, self.current_username, CACHE_TTL)
        game = TwoPlayer(self.current_username, alone_user)
        cache.set(
            TwoPlayer.get_game_room_key(self.current_username, alone_user),
            game,
            CACHE_TTL,
        )
        cache.delete("#alone_user")

        # Send to client to redirect game page
        game_url = reverse("two_player:two_player")
        async_to_sync(self.channel_layer.group_send)(
            self.my_group_name,
            {
                "type": "send_to_websocket",
                "redirect": game_url,
                "user_info": alone_user,
            },
        )
        async_to_sync(self.channel_layer.group_send)(
            f"serach_{alone_user}",
            {
                "type": "send_to_websocket",
                "redirect": game_url,
                "user_info": self.current_username,
            },
        )

    def disconnect(self, close_code):
        alone_user = cache.get("#alone_user")
        if alone_user is not None and alone_user == self.current_username:
            cache.delete("#alone_user")

        async_to_sync(self.channel_layer.group_discard)(
            self.my_group_name,
            self.channel_name,
        )

    def send_to_websocket(self, data):
        self.send(text_data=json.dumps(data))


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.current_username = self.scope["user"].username

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.current_username,
            self.channel_name,
        )

        game = TwoPlayer.get_game(self.current_username)

        self.send_data(
            to=self.current_username,
            data={
                "turn": self.get_turn(game, self.current_username),
            },
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.current_username,
            self.channel_name,
        )

    def receive(self, text_data=None):
        game = TwoPlayer.get_game(self.current_username)
        my_player, opponent_player = game.get_my_and_opponent_player_by_username(
            self.current_username
        )

        if not game.is_player_turn(my_player):
            return

        text_data_json = json.loads(text_data)

        select = text_data_json["select"]
        attack_type = select.get("attack_type")
        x = select.get("x")
        y = select.get("y")

        cells = opponent_player.get_changes(x, y, attack_type)
        if cells is None:
            return

        if attack_type == "radar":
            self.search(game, opponent_player, cells)
        else:
            self.attack(game, opponent_player, cells)

        game.save_data()

    def search(self, game, opponent_player, cells):
        cells = wrap_data.add_css_data_to_cells_when_radar_select(cells)

        game.change_turn()

        self.send_data(
            to=self.current_username,
            data={
                "opponent_cells": cells,
                "turn": self.get_turn(game, self.current_username),
            },
        )
        self.send_data(
            to=opponent_player.username,
            data={
                "turn": self.get_turn(game, opponent_player.username),
            },
        )

    def attack(self, game, opponent_player, cells):
        bonus = False

        cells = wrap_data.add_css_data_to_cells_when_attack_select(cells)

        for cell in cells:
            if cell.get("class") == "ship-selected":
                bonus = True
                break

        if not bonus:
            game.change_turn()

        redirect = None
        if opponent_player.is_end_game():
            GameHistoryModel.objects.create(
                player1=game.player1.username,
                player2=game.player2.username,
                status=f"player {self.current_username} win",
            )
            redirect = reverse("history:game_history")
            game.exit(self.current_username)

        self.send_data(
            to=self.current_username,
            data={
                "opponent_cells": cells,
                "report": opponent_player.get_report_game(),
                "redirect": redirect,
                "turn": self.get_turn(game, self.current_username),
            },
        )

        self.send_data(
            to=opponent_player.username,
            data={
                "my_cells": cells,
                "redirect": redirect,
                "turn": self.get_turn(game, opponent_player.username),
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
        return "opponent_turn"
