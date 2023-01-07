import random

from django.core.cache import cache


class GameDate:
    def __init__(self, table, ship_points):
        self.table = table
        self.ship_points = ship_points


class SeaBattle:
    row = 6
    column = 6
    count_prize = 5

    def __init__(self, user_id):
        self.user_id = user_id
        if cache.get(user_id) is not None:
            self.game_data = cache.get(user_id)

        else:
            self.start_new_game()

    def start_new_game(self):
        self.make_game()
        self.save_game_data()

    def make_game(self):
        table = ["-"] * self.row * self.column
        ship_points = random.sample(range(len(table)), self.count_prize)
        self.game_data = GameDate(table, ship_points)

    def save_game_data(self):
        cache.set(self.user_id, self.game_data)

    def get_table_game(self):
        return self.game_data.table

    def select_cell(self, cell):
        if cell in self.game_data.ship_points:
            result = "*"
        else:
            result = "x"

        self.game_data.table[cell] = result
        self.save_game_data()
        return result
