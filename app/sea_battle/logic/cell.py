class Cell:
    def __init__(self, ship=None):
        self.ship = ship
        self.is_selected = False

    def is_ship(self):
        if self.ship is None:
            return False
        return True
