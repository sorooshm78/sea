# TODO: add this const to settings.py
# ROW = 10
# COLUMN = 10


class SeaBattle:
    def __init__(self):
        self.row = 5
        self.column = 5

    def get_table_game(self):
        table = [0] * self.row * self.column
        return table
