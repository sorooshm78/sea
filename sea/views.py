from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .logic import SeaBattle, Cell


@login_required
def single_player(request):
    sea_battle = SeaBattle(request.user.id)

    context = {
        "table": sea_battle.get_table_game(),
        "report": sea_battle.get_report_game(),
        "empty": Cell.empty.value,
        "target": Cell.target.value,
        "select": Cell.select.value,
        "shape": "o",
    }

    return render(request, "sea/single_player.html", context=context)


@login_required
def select(request):
    x = int(request.GET.get("x"))
    y = int(request.GET.get("y"))

    sea_battle = SeaBattle(request.user.id)

    # Wrap cell data for front
    cells = sea_battle.select_cell(x, y)
    for cell in cells:
        if cell["result"] == Cell.select.value:
            cell["class"] = "select"
        elif cell["result"] == Cell.target.value:
            cell["class"] = "target"

    # Message for End Game
    message = ""
    if sea_battle.is_end_game():
        message = "End Game"

    # Report count alive ships
    report = sea_battle.get_report_game()

    # Data to send to client
    data = {
        "cells": cells,
        "message": message,
        "report": report,
    }

    return JsonResponse(data)


@login_required
def new_game(request):
    sea_battle = SeaBattle(request.user.id)
    sea_battle.start_new_game()
    return redirect("single_player")
