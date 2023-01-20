from enum import Enum


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
