import random
from enum import Enum

import numpy as np

from django.core.cache import cache


MAX_RANGE_LOOP = 20000


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


class Direct(Enum):
    up = "up"
    down = "down"
    right = "right"
    left = "left"


class Ship:
    def __init__(self, point, length, direct):
        self.points = self.get_points_by_direct(point, length, direct)
        self.area = self.get_area_points()
        self.health = length
        self.length = length

    def is_alive(self):
        if self.health == 0:
            return False
        return True

    def get_points_by_direct(self, point, length, direct):
        if direct == Direct.up.value:
            return Point(
                slice(point.x - length + 1, point.x + 1), slice(point.y, point.y + 1)
            )

        elif direct == Direct.down.value:
            return Point(slice(point.x, point.x + length), slice(point.y, point.y + 1))

        elif direct == Direct.right.value:
            return Point(slice(point.x, point.x + 1), slice(point.y, point.y + length))

        elif direct == Direct.left.value:
            return Point(
                slice(point.x, point.x + 1), slice(point.y - length + 1, point.y + 1)
            )

    def get_area_points(self):
        return Point(
            slice(max(0, self.points.x.start - 1), max(0, self.points.x.stop + 1)),
            slice(max(0, self.points.y.start - 1), max(0, self.points.y.stop + 1)),
        )

    def is_inside(self, x, y):
        if x in range(self.points.x.start, self.points.x.stop) and y in range(
            self.points.y.start, self.points.y.stop
        ):
            return True
        return False

    def damage(self):
        if self.is_alive():
            self.health -= 1


class Sea:
    def __init__(self, row, col, list_lenght_ships):
        self.row = row
        self.col = col
        self.list_lenght_ships = list_lenght_ships
        self.coordinates = np.full((self.row, self.col), Cell.empty.value)
        self.make_ships()

    def make_ships(self):
        self.ships = []
        for length in self.list_lenght_ships:
            self.ships.append(self.make_ship(length))

    def make_ship(self, length):
        for _ in range(MAX_RANGE_LOOP):
            point = self.get_random_empty_point()
            directs = np.array([direct.value for direct in Direct])
            random.shuffle(directs)
            for direct in directs:
                ship = self.get_random_ship(point, length, direct)
                if ship is not None:
                    self.coordinates[ship.points.x, ship.points.y] = Cell.ship.value
                    return ship

    def get_random_empty_point(self):
        for _ in range(MAX_RANGE_LOOP):
            x = random.randrange(self.row)
            y = random.randrange(self.col)
            if self.coordinates[x, y] == Cell.empty.value:
                return Point(x, y)

    def is_points_valid(self, points):
        if points.x.start < 0 or points.y.start < 0:
            return False

        if points.x.stop > self.row - 1 or points.y.stop > self.col - 1:
            return False

        return True

    def is_area_ship_valid(self, area):
        if Cell.ship.value in self.coordinates[area.x, area.y]:
            return False
        return True

    def get_random_ship(self, point, length, direct):
        ship = Ship(point, length, direct)

        if self.is_points_valid(ship.points) and self.is_area_ship_valid(ship.area):
            return ship
        return None

    def target_ship(self, point):
        for ship in self.ships:
            if ship.is_inside(point.x, point.y):
                ship.damage()
                if not ship.is_alive():
                    self.coordinates[ship.area.x, ship.area.y] = Cell.select.value
                    self.coordinates[ship.points.x, ship.points.y] = Cell.target.value
                    return ship.area
                else:
                    self.coordinates[point.x, point.y] = Cell.target.value
                    return Point(
                        slice(point.x, point.x + 1), slice(point.y, point.y + 1)
                    )

    def get_changes(self, point):
        selected_cell = self.coordinates[point.x, point.y]

        if selected_cell == Cell.ship.value:
            point = self.target_ship(point)
            return point

        elif selected_cell == Cell.empty.value:
            self.coordinates[point.x, point.y] = Cell.select.value
            return Point(slice(point.x, point.x + 1), slice(point.y, point.y + 1))

    def get_count_ships_by_length(self, length):
        count = 0
        for ship in self.ships:
            if ship.is_alive() and ship.length == length:
                count += 1

        return count


class SeaBattleGame:
    row = 10
    col = 10
    list_lenght_ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    def __init__(self, user_id):
        self.user_id = user_id
        if cache.get(user_id) is not None:
            self.sea = cache.get(user_id)

        else:
            self.start_new_game()

    def start_new_game(self):
        self.sea = Sea(self.row, self.col, self.list_lenght_ships)
        self.save_game_data()

    def get_table_game(self):
        return self.sea.coordinates

    def get_changes(self, x, y):
        points = self.sea.get_changes(Point(x, y))
        self.save_game_data()

        data = []
        for x in range(points.x.start, points.x.stop):
            for y in range(points.y.start, points.y.stop):
                data.append(
                    {
                        "x": x,
                        "y": y,
                        "result": self.sea.coordinates[x, y],
                    }
                )
        return data

    def save_game_data(self):
        cache.set(self.user_id, self.sea)

    def is_end_game(self):
        if Cell.ship.value not in self.sea.coordinates:
            return True
        return False

    def get_report_game(self):
        return {
            "4_ships": self.sea.get_count_ships_by_length(4),
            "3_ships": self.sea.get_count_ships_by_length(3),
            "2_ships": self.sea.get_count_ships_by_length(2),
            "1_ships": self.sea.get_count_ships_by_length(1),
        }

    def get_score_game(self):
        return np.count_nonzero(self.sea.coordinates == Cell.empty.value)
