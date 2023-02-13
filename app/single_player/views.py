import numpy as np

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from score.models import ScoreBoardModel
from sea_battle.single_player import SinglePlayer


@login_required
def single_player(request):
    game = SinglePlayer(request.user.id)
    game_table = game.get_table_game()
    config = game.config

    cell_list = []
    for cell in game_table.flatten():
        if cell.is_ship():
            if cell.is_selected:
                cell_list.append("target")
            else:
                cell_list.append("empty")
        else:
            if cell.is_selected:
                cell_list.append("select")
            else:
                cell_list.append("empty")

    view_table = np.array(cell_list).reshape((config["row"], config["col"]))

    context = {
        "table": view_table,
        "report": game.get_report_game(),
        "attack_count": game.get_attack_count(),
    }

    return render(request, "sea_battle/single_player.html", context=context)


@login_required
def attack(request):
    x = int(request.GET.get("x"))
    y = int(request.GET.get("y"))
    type_attack = request.GET.get("type")

    game = SinglePlayer(request.user.id)

    # Wrap cell data for front
    cells = game.get_changes(x, y, type_attack)
    if cells is None:
        return JsonResponse({})
    for cell in cells:
        cell_value = cell.pop("value")
        if cell_value.is_ship():
            if cell_value.is_selected:
                cell["class"] = "target"
        else:
            if cell_value.is_selected:
                cell["class"] = "select"

    # End Game
    is_end_game = "false"
    if game.is_end_game():
        score = game.get_score_game()
        ScoreBoardModel.objects.create(user=request.user, score=score)
        game.start_new_game()
        is_end_game = "true"

    # Report count alive ships
    report = game.get_report_game()

    # Data to send to client
    data = {
        "cells": cells,
        "is_end_game": is_end_game,
        "report": report,
    }

    return JsonResponse(data)


@login_required
def search(request):
    x = int(request.GET.get("x"))
    y = int(request.GET.get("y"))

    game = SinglePlayer(request.user.id)

    # Wrap cell data for front
    cells = game.get_changes(x, y, "radar")
    if cells is None:
        return JsonResponse({})
    for cell in cells:
        cell_value = cell.pop("value")
        if cell_value.is_ship():
            cell["class"] = "radar-target"
        else:
            cell["class"] = "radar-select"

    # Data to send to client
    data = {
        "cells": cells,
    }

    return JsonResponse(data)


@login_required
def new_game(request):
    game = SinglePlayer(request.user.id)
    game.start_new_game()
    return redirect("single_player")
