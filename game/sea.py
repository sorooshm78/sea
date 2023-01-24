import random

import numpy as np

from .enums import Cell, Direct
from .point import Point
from .ship import Ship


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

    def get_posible_points(self):
        posible_points = []
        for y, x in np.ndindex(self.coordinates.shape):
            if self.coordinates[x, y] != Cell.ship.value:
                posible_points.append(Point(x, y))

        return posible_points

    def make_ship(self, length):
        posible_points = self.get_posible_points()
        random.shuffle(posible_points)
        for point in posible_points:
            directs = np.array([direct.value for direct in Direct])
            random.shuffle(directs)
            for direct in directs:
                ship = self.get_random_ship(point, length, direct)
                if ship is not None:
                    self.coordinates[ship.points.x, ship.points.y] = Cell.ship.value
                    return ship

        raise Exception(f"Not Make Ship by length {length}")

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
        # FIXME try to remove for by adding ship to cells
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
            return self.target_ship(point)

        elif selected_cell == Cell.empty.value:
            self.coordinates[point.x, point.y] = Cell.select.value
            return Point(slice(point.x, point.x + 1), slice(point.y, point.y + 1))

    def get_count_ships_by_length(self, length):
        count = 0
        for ship in self.ships:
            if ship.is_alive() and ship.length == length:
                count += 1

        return count
