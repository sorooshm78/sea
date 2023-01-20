from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from game.manager import SeaBattleGame
from game.enums import Cell


@login_required
def single_player(request):
    game = SeaBattleGame(request.user.id)

    context = {
        "table": game.get_table_game(),
        "report": game.get_report_game(),
        "score": game.get_score_game(),
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

    game = SeaBattleGame(request.user.id)

    # Wrap cell data for front
    cells = game.get_changes(x, y)
    for cell in cells:
        if cell["result"] == Cell.select.value:
            cell["class"] = "select"
        elif cell["result"] == Cell.target.value:
            cell["class"] = "target"

    # Message for End Game
    message = ""
    if game.is_end_game():
        score = game.get_score_game()
        message = f"End Game Your Score Is {score}"

    # Report count alive ships
    report = game.get_report_game()

    # Data to send to client
    data = {
        "cells": cells,
        "message": message,
        "report": report,
    }

    return JsonResponse(data)


@login_required
def new_game(request):
    game = SeaBattleGame(request.user.id)
    game.start_new_game()
    return redirect("single_player")
