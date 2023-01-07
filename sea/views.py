from django.shortcuts import render
from django.http import HttpResponse

from .logic import SeaBattle


def single_player_view(request):
    sea_battle = SeaBattle()
    table = sea_battle.get_table_game()

    context = {
        "table": table,
        "row": sea_battle.row,
        "column": sea_battle.column,
    }

    return render(request, "sea/single_player.html", context=context)


def select(request, cell):
    return HttpResponse("ok recive selected")
