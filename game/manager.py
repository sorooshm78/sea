import numpy as np

from django.core.cache import cache

from .cell import Cell
from .point import Point
from .sea import Sea

# Rename filename to SeaBattleGame
class SeaBattleGame:
    # FIXME 'NoneType' object has no attribute 'is_alive'
    # row = 4
    # col = 20

    row = 10
    col = 10
    list_length_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    def __init__(self, user_id):
        self.user_id = user_id
        if cache.get(user_id) is not None:
            self.sea = cache.get(user_id)

        else:
            self.start_new_game()

    def start_new_game(self):
        self.sea = Sea(self.row, self.col, self.list_length_ships)
        self.save_game_data()

    def get_table_game(self):
        return self.sea.coordinates

    def get_changes(self, x, y):
        points = self.sea.get_changes_by_bomb_attack(Point(x, y))
        self.save_game_data()

        data = []
        for x in range(points.x.start, points.x.stop):
            for y in range(points.y.start, points.y.stop):
                data.append(
                    {
                        "x": x,
                        "y": y,
                        "cell": self.sea.coordinates[x, y],
                    }
                )
        return data

    def save_game_data(self):
        cache.set(self.user_id, self.sea)

    def is_end_game(self):
        for cell in self.sea.coordinates.flatten():
            if cell.is_ship():
                if not cell.is_selected:
                    return False
        return True

    def get_report_game(self):
        return {
            "4_ships": self.sea.get_count_ships_by_length(4),
            "3_ships": self.sea.get_count_ships_by_length(3),
            "2_ships": self.sea.get_count_ships_by_length(2),
            "1_ships": self.sea.get_count_ships_by_length(1),
        }

    def get_score_game(self):
        score = 0

        for cell in self.sea.coordinates.flatten():
            if not cell.is_ship():
                if not cell.is_selected:
                    score += 1

        return score
