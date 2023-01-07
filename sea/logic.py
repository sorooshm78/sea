import random

from django.core.cache import cache


class SeaBattle:
    row = 6
    column = 6
    count_prize = 5

    def __init__(self, user_id):
        self.user_id = user_id
        if cache.get(user_id) is not None:
            game = cache.get(user_id)

        else:
            game = self._make_game()
            cache.set(user_id, game)

        self.table = game["table"]
        self.ship_points = game["ship_points"]

    def get_table_game(self):
        return self.table

    def select_cell(self, cell):
        if cell in self.ship_points:
            result = "*"
        else:
            result = "x"

        self.table[cell] = result
        self.save_game()
        return result

    def _make_game(self):
        table = [0] * self.row * self.column
        ship_points = random.sample(range(len(table)), self.count_prize)

        return {
            "table": table,
            "ship_points": ship_points,
        }

    def save_game(self):
        game = {
            "table": self.table,
            "ship_points": self.ship_points,
        }
        cache.set(self.user_id, game)

    def load_game(self, game):
        self.table = game["table"]
        self.ship_points = game["ship_points"]
