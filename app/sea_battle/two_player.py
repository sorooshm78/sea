from django.core.cache import cache
from django.conf import settings

from .point import Point
from .sea import Sea


CACHE_TTL = settings.CACHE_TTL


class Player:
    def __init__(self, username, config):
        self.username = username
        self.sea = Sea(config)

    def get_username(self):
        return self.username

    def get_sea(self):
        return self.sea

    def __str__(self):
        return self.username


class GameRoom:
    def __init__(self, player):
        self.player1 = player
        self.player2 = None

        self.turn = self.player1

    def set_another_player(self, player):
        self.player2 = player

    def has_capacity(self):
        if self.player1 is None or self.player2 is None:
            return True
        return False

    def change_turn(self):
        if self.turn == self.player1:
            self.turn = self.player2
        elif self.turn == self.player2:
            self.turn = self.player1

    def get_player_by_username(self, username):
        if self.player1.get_username() == username:
            return self.player1
        return self.player2

    def get_opposite_player_by_username(self, username):
        if self.player1.get_username() == username:
            return self.player2
        return self.player1


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

    def __init__(self, username):
        self.game_room = self.get_game_room(username)

    def get_game_room(self, username):
        # Chack exist room
        exist_room = [cache.get(key) for key in cache.keys(f"*{username}*")]
        if exist_room:
            return exist_room[0]

        # Check empty room
        empty_room = cache.get("empty_room")
        if empty_room is None:
            new_room = GameRoom(Player(username, TwoPlayer.config))
            cache.set("empty_room", new_room)
            return new_room

        if empty_room.player1.get_username() == username:
            return empty_room

        empty_room.set_another_player(Player(username, TwoPlayer.config))
        cache.set(
            f"{empty_room.player1.get_username()}_{empty_room.player2.get_username()}",
            empty_room,
        )
        cache.delete("empty_room")
        print("rooms ", cache.keys("*_*"))
        return empty_room

    def deactive_room(self, username):
        exist_room = cache.keys(f"*{username}*")
        if exist_room:
            cache.delete(exist_room[0])
            print("rooms ", cache.keys("*_*"))
            return

        empty_room = cache.get("empty_room")
        if empty_room is not None and empty_room.player.username == username:
            cache.delete("empty_room")
            return

    def is_game_ready(self):
        return self.game_room.has_capacity()

    def get_table_game(self, username):
        player = self.game_room.get_player_by_username(username)
        return player.sea.coordinates

    def get_report_game(self, username):
        player = self.game_room.get_player_by_username(username)
        report_ships = player.sea.get_report_count_ships()
        return {
            "4_ships": report_ships[4],
            "3_ships": report_ships[3],
            "2_ships": report_ships[2],
            "1_ships": report_ships[1],
        }

    def get_opposite_username(self, username):
        opposite_player = self.game_room.get_opposite_player_by_username(username)
        return opposite_player.get_username()

    def get_attack_count(self, username):
        player = self.game_room.get_player_by_username(username)
        return player.sea.attack_count

    def get_changes(self, username, x, y, attack_type):
        opposite_player = self.game_room.get_opposite_player_by_username(username)

        points = opposite_player.sea.get_changes_by_type_attack(
            Point(x, y), attack_type
        )
        if points is None:
            return

        change_points = []
        for point in points:
            change_points.append(
                {
                    "x": point.x,
                    "y": point.y,
                    "value": opposite_player.sea.coordinates[point.x, point.y],
                }
            )

        return change_points
