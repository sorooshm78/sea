import random

import numpy as np

from .cell import Cell
from .direct import Direct
from .point import Point
from .ship import Ship


class Sea:
    def __init__(self, row, col, list_lenght_ships):
        self.row = row
        self.col = col
        self.list_lenght_ships = list_lenght_ships
        self.make_coordinates()
        self.make_ships()

    def make_coordinates(self):
        self.coordinates = np.empty((self.row, self.col), dtype=object)
        for y, x in np.ndindex(self.coordinates.shape):
            self.coordinates[x, y] = Cell()

    def make_ships(self):
        self.ships = []
        for length in self.list_lenght_ships:
            self.ships.append(self.make_ship(length))

    def get_posible_points(self):
        posible_points = []
        for y, x in np.ndindex(self.coordinates.shape):
            if not self.coordinates[x, y].is_ship():
                posible_points.append(Point(x, y))

        return posible_points

    def mark_cell_as_ship(self, points, ship):
        for cell in self.coordinates[points.x, points.y].flatten():
            cell.ship = ship

    def mark_cell_as_selected(self, points):
        for cell in self.coordinates[points.x, points.y].flatten():
            cell.is_selected = True

    def make_ship(self, length):
        posible_points = self.get_posible_points()
        random.shuffle(posible_points)
        for point in posible_points:
            directs = np.array([direct.value for direct in Direct])
            random.shuffle(directs)
            for direct in directs:
                ship = self.get_random_ship(point, length, direct)
                if ship is not None:
                    self.mark_cell_as_ship(ship.points, ship)
                    return ship

        raise Exception(f"Not Make Ship by length {length}")

    def is_points_valid(self, points):
        if points.x.start < 0 or points.y.start < 0:
            return False

        if points.x.stop > self.row - 1 or points.y.stop > self.col - 1:
            return False

        return True

    def is_area_ship_valid(self, area):
        for cell in self.coordinates[area.x, area.y].flatten():
            if cell.is_ship():
                return False
        return True

    def get_random_ship(self, point, length, direct):
        ship = Ship(point, length, direct)

        if self.is_points_valid(ship.points) and self.is_area_ship_valid(ship.area):
            return ship
        return None

    def get_list_of_point(self, points):
        list_point = []
        for x in range(points.x.start, points.x.stop):
            for y in range(points.y.start, points.y.stop):
                list_point.append(Point(x, y))

        return list_point

    def target_ship(self, point):
        cell = self.coordinates[point.x, point.y]
        ship = cell.ship

        ship.damage()
        if not ship.is_alive():
            self.mark_cell_as_selected(ship.area)
            return self.get_list_of_point(ship.area)
        else:
            cell.is_selected = True
            return [point]

    def get_changes_by_bomb_attack(self, point):
        selected_cell = self.coordinates[point.x, point.y]

        if selected_cell.is_ship():
            return self.target_ship(point)

        else:
            selected_cell.is_selected = True
            return [point]

    def get_changes_by_explosion_attack(self, point):
        explosion_area = Point(
            slice(max(0, point.x - 1), min(self.col, point.x + 2)),
            slice(max(0, point.y - 1), min(self.row, point.y + 2)),
        )
        points = self.get_list_of_point(explosion_area)
        change_cell = []

        for point in points:
            if not self.coordinates[point.x, point.y].is_selected:
                change_cell.extend(self.get_changes_by_bomb_attack(point))

        return change_cell

    def get_changes_by_liner_attack(self, point):
        liner_area = Point(
            slice(point.x, point.x + 1),
            slice(0, self.row),
        )
        points = self.get_list_of_point(liner_area)
        change_cell = []

        for point in points:
            cell = self.coordinates[point.x, point.y]
            if not cell.is_selected:
                if cell.is_ship():
                    change_cell.extend(self.target_ship(point))
                    break

                else:
                    cell.is_selected = True
                    change_cell.append(point)

        return change_cell

    def get_changes_by_radar_attack(self, point):
        radar_area = Point(
            slice(max(0, point.x - 1), min(self.col, point.x + 2)),
            slice(max(0, point.y - 1), min(self.row, point.y + 2)),
        )
        points = self.get_list_of_point(radar_area)
        change_cell = []

        for point in points:
            if not self.coordinates[point.x, point.y].is_selected:
                change_cell.append(point)

        return change_cell

    def get_report_count_ships(self):
        # Map length ship to count alive ship
        report_ships = {
            4: 0,
            3: 0,
            2: 0,
            1: 0,
        }
        for ship in self.ships:
            if ship.is_alive():
                report_ships[ship.length] += 1

        return report_ships

    def is_point_selected(self, point):
        return self.coordinates[point.x, point.y].is_selected
