import random
from enum import Enum

from django.core.cache import cache


class GameDate:
    def __init__(self, table, target_points):
        self.table = table
        self.target_points = target_points


class Cell(Enum):
    empty = "-"
    select = "x"
    target = "*"


class SeaBattle:
    row = 6
    column = 6
    count_target = 5

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
        table = [Cell.empty.value] * self.row * self.column
        target_points = random.sample(range(len(table)), self.count_target)
        self.game_data = GameDate(table, target_points)

    def save_game_data(self):
        cache.set(self.user_id, self.game_data)

    def get_table_game(self):
        return self.game_data.table

    def select_cell(self, point):
        if point in self.game_data.target_points:
            cell = Cell.target.value
        else:
            cell = Cell.select.value

        self.game_data.table[point] = cell
        self.save_game_data()
        return cell
