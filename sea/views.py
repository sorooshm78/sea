from django.shortcuts import render
from django.http import HttpResponse


ROW = 6
COLUMN = 4

def make_table_game(row, column):
    table = [0] * row * column
    return table


def single_player_view(request):
    table = make_table_game(ROW, COLUMN)
    
    context = {
        'table' : table,
        'row' : ROW,
        'column' : COLUMN,
    } 

    return render(request, "sea/single_player.html", context=context)


def select(request, butten):
    return HttpResponse('ok recive selected')