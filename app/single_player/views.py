import numpy as np

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView, TemplateView

from score.models import ScoreBoardModel
from sea_battle.single_player import SinglePlayer


class SinglePlayerView(LoginRequiredMixin, TemplateView):
    template_name = "single_player/index.html"

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)

        game = SinglePlayer(self.request.user.id)
        game_table = game.get_table_game()
        config = game.config

        cell_list = []
        for cell in game_table.flatten():
            if cell.is_ship():
                if cell.is_selected:
                    cell_list.append("ship-selected")
                else:
                    cell_list.append("empty")
            else:
                if cell.is_selected:
                    cell_list.append("empty-selected")
                else:
                    cell_list.append("empty")

        view_table = np.array(cell_list).reshape((config["row"], config["col"]))

        context["table"] = view_table
        context["report"] = game.get_report_game()
        context["attack_count"] = game.get_attack_count()

        return context


class NewGameView(LoginRequiredMixin, RedirectView):
    pattern_name = "single_player:single_player"

    def get(self, request, *args, **kwargs):
        game = SinglePlayer(request.user.id)
        game.start_new_game()
        return super().get(request, *args, **kwargs)


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
                cell["class"] = "ship-selected"
        else:
            if cell_value.is_selected:
                cell["class"] = "empty-selected"

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
            cell["class"] = "radar-ship"
        else:
            cell["class"] = "radar-empty"

    # Data to send to client
    data = {
        "cells": cells,
    }

    return JsonResponse(data)
