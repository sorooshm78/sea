from django.conf import settings

from .point import Point
from .sea import Sea


CACHE_TTL = settings.CACHE_TTL


class Player:
    config = {
        "row": 10,
        "col": 10,
        "list_length_ships": [4, 3, 3, 2, 2, 2, 1, 1, 1, 1],
        "attack_count": {
            "radar": 2,
            "explosion": 2,
            "liner": 2,
        },
    }

    def __init__(self, username):
        self.username = username
        self.sea = Sea(Player.config)

    def start_new_game(self):
        self.sea = Sea(Player.config)

    def get_table_game(self):
        return self.sea.coordinates

    def get_changes(self, x, y, type_attack):
        points = self.sea.get_changes_by_type_attack(Point(x, y), type_attack)
        if points is None:
            return

        change_points = []
        for point in points:
            change_points.append(
                {
                    "x": point.x,
                    "y": point.y,
                    "value": self.sea.coordinates[point.x, point.y],
                }
            )

        return change_points

    def is_end_game(self):
        for cell in self.sea.coordinates.flatten():
            if cell.is_ship():
                if not cell.is_selected:
                    return False
        return True

    def get_report_game(self):
        report_ships = self.sea.get_report_count_ships()
        return {
            "4_ships": report_ships[4],
            "3_ships": report_ships[3],
            "2_ships": report_ships[2],
            "1_ships": report_ships[1],
        }

    def get_score_game(self):
        max_const_score = 120
        return max_const_score - self.sea.move

    def get_attack_count(self):
        return self.sea.attack_count
