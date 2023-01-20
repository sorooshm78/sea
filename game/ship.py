from .enums import Direct
from .point import Point


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
