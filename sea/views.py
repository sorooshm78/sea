import numpy as np

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Window
from django.db.models.functions import Rank

from game.manager import SeaBattleGame
from .models import ScoreBoardModel


@login_required
def single_player(request):
    game = SeaBattleGame(request.user.id)
    game_table = game.get_table_game()

    list_cell = []
    for cell in game_table.flatten():
        if cell.is_ship():
            if cell.is_selected:
                list_cell.append("target")
            else:
                list_cell.append("empty")
        else:
            if cell.is_selected:
                list_cell.append("select")
            else:
                list_cell.append("empty")

    view_table = np.array(list_cell).reshape((game.row, game.col))

    context = {
        "table": view_table,
        "report": game.get_report_game(),
        "shape": "o",
    }

    return render(request, "sea/single_player.html", context=context)


@login_required
def select(request):
    x = int(request.GET.get("x"))
    y = int(request.GET.get("y"))
    type_attack = request.GET.get("type")

    game = SeaBattleGame(request.user.id)

    # Wrap cell data for front
    cells = game.get_changes(x, y, type_attack)
    for cell in cells:
        if cell["cell"].is_ship():
            if cell["cell"].is_selected:
                cell["class"] = "target"
        else:
            if cell["cell"].is_selected:
                cell["class"] = "select"
        cell.pop("cell")

    # End Game
    is_end_game = "false"
    if game.is_end_game():
        score = game.get_score_game()
        ScoreBoardModel.objects.create(user=request.user, score=score)
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

    game = SeaBattleGame(request.user.id)

    # Wrap cell data for front
    cells = game.get_changes(x, y, "radar")
    for cell in cells:
        if cell["cell"].is_ship():
            cell["class"] = "radar-target"
        else:
            cell["class"] = "radar-select"

        cell.pop("cell")

    # Data to send to client
    data = {
        "cells": cells,
    }

    return JsonResponse(data)


@login_required
def new_game(request):
    game = SeaBattleGame(request.user.id)
    game.start_new_game()
    return redirect("single_player")


class ScoreBoardListView(LoginRequiredMixin, ListView):
    model = ScoreBoardModel
    template_name = "sea/score_board.html"
    context_object_name = "scores"
    MAX_SHOW_USER = 10

    def get_queryset(self):
        query = super().get_queryset()
        query = query.order_by("-score").annotate(
            rank=Window(
                expression=Rank(),
                order_by=F("score").desc(),
            )
        )
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        query = self.get_queryset()
        context["last_score"] = (
            query.filter(user=self.request.user).order_by("-time").first()
        )
        context["scores"] = query[: self.MAX_SHOW_USER]
        return context
