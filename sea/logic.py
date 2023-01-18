import random
from enum import Enum

import numpy as np

from django.core.cache import cache

# FIXME: replace with builtin class
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


class Ship:
    def __init__(self, point, length, direct):
        self.points = self.get_points_by_direct(point, length, direct)
        self.area = self.get_area_points()
        self.health = length
        # FIXME is_alive could be a method based in health being zero or not
        self.is_alive = True

    def get_points_by_direct(self, point, length, direct):
        if direct == "up":
            return Point(
                slice(point.x - length + 1, point.x + 1), slice(point.y, point.y + 1)
            )

        # FIXME: direct should be a Enum not string
        elif direct == "down":
            return Point(slice(point.x, point.x + length), slice(point.y, point.y + 1))

        elif direct == "right":
            return Point(slice(point.x, point.x + 1), slice(point.y, point.y + length))

        elif direct == "left":
            return Point(
                slice(point.x, point.x + 1), slice(point.y - length + 1, point.y + 1)
            )

    def get_area_points(self):
        return Point(
            slice(max(0, self.points.x.start - 1), max(0, self.points.x.stop + 1)),
            slice(max(0, self.points.y.start - 1), max(0, self.points.y.stop + 1)),
        )

    # FIXME is_inside
    def check_inside_of_points(self, x, y):
        if x in range(self.points.x.start, self.points.x.stop) and y in range(
            self.points.y.start, self.points.y.stop
        ):
            return True
        return False

    def damage(self):
        if self.is_alive:
            self.health -= 1
        if self.health == 0:
            self.is_alive = False


class Table:
    row = 10
    col = 10

    # FIXME Table sizes and ships become input of ctor
    def __init__(self):
        self.coordinates = np.full((self.row, self.col), Cell.empty.value)
        self.make_ships()

    def make_ships(self):
        list_lenght_ships = [4, 3, 3, 2, 2, 1, 1]
        self.ships = []
        for length in list_lenght_ships:
            self.ships.append(self.make_ship(length))

    def make_ship(self, length):
        # FIXME infinite loop danger
        while True:
            point = self.get_random_empty_point()
            directs = np.array(["up", "down", "right", "left"])
            random.shuffle(directs)
            for direct in directs:
                ship = self.get_random_ship(point, length, direct)
                if ship is not None:
                    self.coordinates[ship.points.x, ship.points.y] = Cell.ship.value
                    return ship

    def get_random_empty_point(self):
        while True:
            x = random.randrange(self.row)
            y = random.randrange(self.col)
            if self.coordinates[x, y] == Cell.empty.value:
                return Point(x, y)

    # FIXME rename to meaningful names with "is"
    def check_points_valid(self, points):
        if points.x.start < 0 or points.y.start < 0:
            return False

        if points.x.stop > self.row - 1 or points.y.stop > self.col - 1:
            return False

        return True

    def check_area_ship_valid(self, area):
        if Cell.ship.value in self.coordinates[area.x, area.y]:
            return False
        return True

    def get_random_ship(self, point, length, direct):
        ship = Ship(point, length, direct)

        if self.check_points_valid(ship.points) and self.check_area_ship_valid(
            ship.area
        ):
            return ship
        return None

    # FIXME rename
    def select_ship(self, point):
        for ship in self.ships:
            if ship.check_inside_of_points(point.x, point.y):
                ship.damage()
                if not ship.is_alive:
                    self.coordinates[ship.area.x, ship.area.y] = Cell.select.value
                    self.coordinates[ship.points.x, ship.points.y] = Cell.target.value
                    return ship.area
                else:
                    self.coordinates[point.x, point.y] = Cell.target.value
                    return Point(
                        slice(point.x, point.x + 1), slice(point.y, point.y + 1)
                    )

    def select_cell(self, point):
        selecte_cell = self.coordinates[point.x, point.y]

        if selecte_cell == Cell.ship.value:
            point = self.select_ship(point)
            return point

        # FIXME rename
        elif selecte_cell == Cell.empty.value:
            self.coordinates[point.x, point.y] = Cell.select.value
            return Point(slice(point.x, point.x + 1), slice(point.y, point.y + 1))


# Manage Game
class SeaBattle:
    def __init__(self, user_id):
        self.user_id = user_id
        if cache.get(user_id) is not None:
            self.table = cache.get(user_id)

        else:
            self.start_new_game()

    def start_new_game(self):
        self.table = Table()
        self.save_game_data()

    def get_table_game(self):
        return self.table.coordinates

    # FIXME Rename
    def select_cell(self, x, y):
        points = self.table.select_cell(Point(x, y))
        self.save_game_data()

        data = []
        for x in range(points.x.start, points.x.stop):
            for y in range(points.y.start, points.y.stop):
                data.append(
                    {
                        "x": x,
                        "y": y,
                        "result": self.table.coordinates[x, y],
                    }
                )
        return data

    def save_game_data(self):
        cache.set(self.user_id, self.table)

    def is_end_game(self):
        if Cell.ship.value not in self.table.coordinates:
            return True
        return False
