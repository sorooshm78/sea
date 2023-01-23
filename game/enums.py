from enum import Enum


# FIXME Relocate to other files


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
