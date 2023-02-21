from django.core.cache import cache
from django.conf import settings

from .player import Player


CACHE_TTL = settings.CACHE_TTL


class TwoPlayer:
    def __init__(self, room_id, username):
        self.player1 = Player(username)
        self.player2 = None
        self.turn = self.player1.username

        self.room_id = room_id

    def set_another_player(self, username):
        self.player2 = Player(username)

    @classmethod
    def get_game(cls, username):
        # Chack exist rooms
        user_room_id = cache.get(username)
        if user_room_id is not None:
            room = cache.get(user_room_id)
            return room

        # Not empty room
        room = cache.get("empty_room")
        if room is None:
            room_id = cache.get_or_set("room_id", 1)
            new_room = TwoPlayer(room_id, username)
            cache.incr("room_id")
            cache.set("empty_room", new_room)
            return new_room

        if room.player1.username == username:
            return room

        # Exist empty room and set player2
        room.set_another_player(username)

        cache.set(room.room_id, room)
        cache.set(room.player1.username, room.room_id)
        cache.set(room.player2.username, room.room_id)

        cache.delete("room")
        return room

    @classmethod
    def disactive_game(cls, username):
        # Exist room
        room_id = cache.keys(username)
        if room_id is not None:
            cache.delete(room_id)
            return

        # Empty room
        room = cache.get("empty_room")
        if room is not None:
            cache.delete("empty_room")
            return

    def save_data(self):
        cache.set(self.room_id, self)

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
