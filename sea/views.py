from django.shortcuts import render
from django.http import HttpResponse

# TODO: add this const to settings.py
ROW = 10
COLUMN = 10

class SeaBattle:
    def __init__(self, row=5, column=5):
        self.row = row
        self.column = column

    def get_table_game(self):
        table = [0] * self.row * self.column
        return table


def single_player_view(request):
    sea_battle = SeaBattle(ROW, COLUMN)
    table = sea_battle.get_table_game()
    
    context = {
        'table' : table,
        'row' : ROW,
        'column' : COLUMN,
    } 

    return render(request, "sea/single_player.html", context=context)


def select(request, butten):
    return HttpResponse('ok recive selected')