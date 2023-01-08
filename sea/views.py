from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .logic import SeaBattle, Cell


@login_required
def single_player(request):
    sea_battle = SeaBattle(request.user.id)

    context = {
        "table": sea_battle.get_table_game(),
        "row": sea_battle.row,
        "column": sea_battle.column,
        "empty": Cell.empty.value,
        "taget": Cell.target.value,
        "select": Cell.select.value,
    }

    return render(request, "sea/single_player.html", context=context)


@login_required
def select(request, cell):
    sea_battle = SeaBattle(request.user.id)

    return HttpResponse(sea_battle.select_cell(cell))


@login_required
def new_game(request):
    sea_battle = SeaBattle(request.user.id)
    sea_battle.start_new_game()
    return redirect("single_player")
