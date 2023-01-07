from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .logic import SeaBattle


@login_required
def single_player_view(request):
    sea_battle = SeaBattle(request.user.id)
    table = sea_battle.get_table_game()

    context = {
        "table": table,
        "row": sea_battle.row,
        "column": sea_battle.column,
    }

    return render(request, "sea/single_player.html", context=context)


@login_required
def select(request, cell):
    sea_battle = SeaBattle(request.user.id)

    return HttpResponse(sea_battle.select_cell(cell))
