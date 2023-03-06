import numpy as np

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView, TemplateView

from score.models import ScoreBoardModel
from sea_battle.single_player import SinglePlayer
from utils import wrap_data


class SinglePlayerView(LoginRequiredMixin, TemplateView):
    template_name = "single_player/index.html"

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)

        game = SinglePlayer(self.request.user.id)
        game_table = game.get_table_game()
        config = game.config

        context["table"] = wrap_data.get_template_game_table(
            game_table=game_table,
            is_ship_hide=True,
            row=config["row"],
            col=config["col"],
        )
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

    cells = wrap_data.add_css_data_to_cells_when_attack_select(cells)

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

    cells = wrap_data.add_css_data_to_cells_when_radar_select(cells)

    data = {
        "cells": cells,
    }

    return JsonResponse(data)
