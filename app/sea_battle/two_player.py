from django.core.cache import cache
from django.conf import settings

from .player import Player


CACHE_TTL = settings.CACHE_TTL


class TwoPlayer:
    def __init__(self, username):
        self.player1 = Player(username)
        self.player2 = None

        self.turn = self.player1.username

    def set_another_player(self, username):
        self.player2 = Player(username)

    @classmethod
    def get_game(cls, username):
        # Chack exist room
        exist_room = [cache.get(key) for key in cache.keys(f"*{username}*")]
        if exist_room:
            return exist_room[0]

        # Not empty room
        empty_room = cache.get("empty_room")

        if empty_room is None:
            new_room = TwoPlayer(username)
            cache.set("empty_room", new_room)
            return new_room

        if empty_room.player1.username == username:
            return empty_room

        # Exist empty room
        empty_room.set_another_player(username)
        cache.set(
            f"{empty_room.player1.username}_{empty_room.player2.username}", empty_room
        )
        cache.delete("empty_room")
        return empty_room

    @classmethod
    def disactive_game(cls, username):
        # Exist room
        exist_room = cache.keys(f"*{username}*")
        if exist_room:
            cache.delete(exist_room[0])
            return

        # Empty room
        empty_room = cache.get("empty_room")
        if empty_room is not None:
            cache.delete("empty_room")
            return

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

    def change_turn(self):
        if self.turn == self.player1.username:
            self.turn = self.player2.username
        elif self.turn == self.player2.username:
            self.turn = self.player1.username

    def is_player_turn(self, player):
        if self.turn == player.username:
            return True
        return False

    def save_data(self):
        cache.set(f"{self.player1.username}_{self.player2.username}", self)
