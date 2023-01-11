import random
from enum import Enum

import numpy as np

from django.core.cache import cache


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Cell(Enum):
    empty = "o"
    ship = "#"
    select = "x"
    target = "*"


class SeaBattle:
    row = 10
    col = 10

    def __init__(self, user_id):
        self.user_id = user_id
        if cache.get(user_id) is not None:
            self.table = cache.get(user_id)

        else:
            self.start_new_game()

    def start_new_game(self):
        self.make_table()
        self.make_ships()
        self.save_game_data()

    def make_table(self):
        self.table = np.full((self.row, self.col), Cell.empty.value)

    def make_ships(self):
        self.make_ship(4)
        self.make_ship(3)
        self.make_ship(2)
        self.make_ship(2)
        self.make_ship(1)
        self.make_ship(1)

    def make_ship(self, length):
        while True:
            random_point = self.random_point()
            directs = np.array(["up", "down", "right", "left"])
            random.shuffle(directs)
            for direct in directs:
                condidate_point = self.slice_condidate_ship(
                    random_point, length, direct
                )
                if len(self.table[condidate_point.x, condidate_point.y]) == length:
                    if (
                        Cell.ship.value
                        not in self.table[condidate_point.x, condidate_point.y]
                    ):
                        self.table[
                            condidate_point.x, condidate_point.y
                        ] = Cell.ship.value
                        return

    def random_point(self):
        while True:
            x = random.randrange(self.row)
            y = random.randrange(self.col)
            if self.table[x, y] == Cell.empty.value:
                return Point(x, y)

    def slice_condidate_ship(self, point, length, direct):
        if direct == "up":
            return Point(slice(point.x - length + 1, point.x + 1), point.y)

        if direct == "down":
            return Point(slice(point.x, point.x + length), point.y)

        if direct == "right":
            return Point(point.x, slice(point.y, point.y + length))

        if direct == "left":
            return Point(point.x, slice(point.y - length + 1, point.y + 1))

    def save_game_data(self):
        cache.set(self.user_id, self.table)

    def get_table_game(self):
        return self.table

    def select_cell(self, x, y):
        selecte_cell = self.table[x, y]
        if selecte_cell == Cell.ship.value or selecte_cell == Cell.target.value:
            cell = Cell.target.value
        else:
            cell = Cell.select.value

        self.table[x, y] = cell
        self.save_game_data()
        return cell
