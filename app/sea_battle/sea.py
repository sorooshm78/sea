import random

import numpy as np

from .cell import Cell
from .direct import Direct
from .point import Point
from .ship import Ship


class Sea:
    def __init__(self, config):
        self.move = 0
        self.row = config["row"]
        self.col = config["col"]
        self.list_length_ships = config["list_length_ships"]
        self.attack_count = dict(config["attack_count"])
        self.make_coordinates()
        self.make_ships()

    def make_coordinates(self):
        self.coordinates = np.empty((self.row, self.col), dtype=object)
        for x, y in np.ndindex(self.coordinates.shape):
            self.coordinates[x, y] = Cell()

    def make_ships(self):
        self.ships = []
        for length in self.list_length_ships:
            self.ships.append(self.make_ship(length))

    def get_possible_points(self):
        posible_points = []
        for x, y in np.ndindex(self.coordinates.shape):
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
        posible_points = self.get_possible_points()
        random.shuffle(posible_points)
        for point in posible_points:
            directs = np.array([direct.value for direct in Direct])
            random.shuffle(directs)
            for direct in directs:
                ship = self.get_random_ship(point, length, direct)
                if ship is not None:
                    self.mark_cell_as_ship(ship.points, ship)
                    return ship

        raise Exception(f"Could not make a ship with length {length}")

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
        point_list = []
        for x in range(points.x.start, points.x.stop):
            for y in range(points.y.start, points.y.stop):
                point_list.append(Point(x, y))

        return point_list

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

    def is_allow_to_attack(self, point, type_attack):
        if self.is_point_selected(point) or self.attack_count.get(type_attack) == 0:
            return False
        return True

    def get_changes_by_type_attack(self, point, type_attack):
        if not self.is_allow_to_attack(point, type_attack):
            return

        self.move += 1
        if type_attack == "bomb":
            return self.get_changes_by_bomb_attack(point)
        elif type_attack == "explosion":
            return self.get_changes_by_explosion_attack(point)
        elif type_attack == "liner":
            return self.get_changes_by_liner_attack(point)
        elif type_attack == "radar":
            return self.get_changes_by_radar_attack(point)

    def get_changes_by_bomb_attack(self, point):
        selected_cell = self.coordinates[point.x, point.y]

        if selected_cell.is_ship():
            return self.target_ship(point)

        else:
            selected_cell.is_selected = True
            return [point]

    def get_changes_by_explosion_attack(self, point):
        explosion_area = Point(
            slice(max(0, point.x - 1), min(self.row, point.x + 2)),
            slice(max(0, point.y - 1), min(self.col, point.y + 2)),
        )
        points = self.get_list_of_point(explosion_area)
        changed_cell = []

        for point in points:
            if not self.coordinates[point.x, point.y].is_selected:
                changed_cell.extend(self.get_changes_by_bomb_attack(point))

        self.attack_count["explosion"] -= 1
        return changed_cell

    def get_changes_by_liner_attack(self, point):
        liner_area = Point(
            slice(point.x, point.x + 1),
            slice(0, self.col),
        )
        points = self.get_list_of_point(liner_area)
        changed_cell = []

        for point in points:
            cell = self.coordinates[point.x, point.y]
            if not cell.is_selected:
                if cell.is_ship():
                    changed_cell.extend(self.target_ship(point))
                    break

                else:
                    cell.is_selected = True
                    changed_cell.append(point)

        self.attack_count["liner"] -= 1
        return changed_cell

    def get_changes_by_radar_attack(self, point):
        radar_area = Point(
            slice(max(0, point.x - 1), min(self.row, point.x + 2)),
            slice(max(0, point.y - 1), min(self.col, point.y + 2)),
        )
        points = self.get_list_of_point(radar_area)
        changed_cell = []

        for point in points:
            if not self.coordinates[point.x, point.y].is_selected:
                changed_cell.append(point)

        self.attack_count["radar"] -= 1
        return changed_cell

    def get_report_count_ships(self):
        # Map length ship to count alive ship
        # Count alive ship by length
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
