from django.core.cache import cache
from django.conf import settings

from .point import Point
from .sea import Sea


CACHE_TTL = settings.CACHE_TTL


class GameRoom:
    def __init__(self, username, sea):
        self.player1 = {
            "username": username,
            "sea": sea,
        }

        self.player2 = dict()

        self.turn = self.get_username_player1()
        self.is_active = True

    def set_another_player(self, username, sea):
        self.player2 = {
            "username": username,
            "sea": sea,
        }

    def has_capacity(self):
        if self.get_username_player1() is None or self.get_sea_player2() is None:
            return True
        return False

    def change_turn(self):
        username1 = self.get_username_player1()
        username2 = self.get_username_player2()

        if self.turn == username1:
            self.turn = username2
        elif self.turn == username2:
            self.turn = username1

    def is_user_exist(self, username):
        if (
            self.get_username_player1() == username
            or self.get_username_player2() == username
        ):
            return True
        return False

    def get_username_player1(self):
        return self.player1.get("username")

    def get_username_player2(self):
        return self.player2.get("username")

    def get_sea_player1(self):
        return self.player1.get("sea")

    def get_sea_player2(self):
        return self.player2.get("sea")


class TwoPlayer:
    config = {
        "row": 10,
        "col": 10,
        "list_length_ships": [4, 3, 3, 2, 2, 2, 1, 1, 1, 1],
        "attack_count": {
            "radar": 2,
            "explosion": 2,
            "liner": 2,
        },
    }

    def __init__(self, user):
        username = user.username
        rooms = cache.get_or_set("rooms", list())
        print(rooms)
        room = self.get_game_room(rooms, username)

        if room is None:
            room = self.create_game_room(rooms, username)

        self.game_room = room

    def get_game_room(self, rooms, username):
        for room in rooms:
            if room.is_user_exist(username):
                return room

    def create_game_room(self, rooms, username):
        sea = Sea(TwoPlayer.config)
        if len(rooms) != 0:
            last_room = rooms[-1]
            if last_room.has_capacity():
                last_room.set_another_player(username, sea)
                rooms.pop()
                rooms.append(last_room)
                cache.set("rooms", rooms)
                return

        new_room = GameRoom(username, sea)
        rooms.append(new_room)
        cache.set("rooms", rooms)
