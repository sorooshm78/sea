from django.core.cache import cache
from django.conf import settings

from .player import Player


CACHE_TTL = settings.CACHE_TTL


class TwoPlayer:
    def __init__(self, username1, username2):
        self.player1 = Player(username1)
        self.player2 = Player(username2)

        self.turn = self.player1.username

    @classmethod
    def get_game_room_key(cls, username1, username2):
        if username1 < username2:
            return f"{username1}_{username2}"
        return f"{username2}_{username1}"

    @classmethod
    def get_game(cls, username):
        oppoite_username = cache.get(username)
        room = cache.get(TwoPlayer.get_game_room_key(username, oppoite_username))
        if room is not None:
            return room

    @classmethod
    def disactive_game(cls, username):
        pass

    def save_data(self):
        cache.set(
            TwoPlayer.get_game_room_key(self.player1.username, self.player2.username),
            self,
        )

    def has_capacity(self):
        if self.player1 is None or self.player2 is None:
            return True
        return False

    def is_game_ready(self):
        return not self.has_capacity()

    def get_player_by_username(self, username):
        if self.player1.username == username:
            return self.player1
        return self.player2

    def get_opposite_player_by_username(self, username):
        if self.player1.username == username:
            return self.player2
        return self.player1

    def get_my_and_opposite_player_by_username(self, username):
        # Return (my_player, opposite_player)
        if self.player1.username == username:
            return (self.player1, self.player2)
        return (self.player2, self.player1)

    def change_turn(self):
        if self.turn == self.player1.username:
            self.turn = self.player2.username
        elif self.turn == self.player2.username:
            self.turn = self.player1.username

    def get_turn(self):
        return self.turn

    def is_player_turn(self, player):
        if self.turn == player.username:
            return True
        return False
