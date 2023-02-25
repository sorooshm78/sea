import numpy as np

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView, TemplateView

from sea_battle.two_player import TwoPlayer
from sea_battle.player import Player


class TwoPlayerView(LoginRequiredMixin, TemplateView):
    template_name = "two_player/index.html"

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)

        username = self.request.user.username
        game = TwoPlayer.get_game(username)
        game_table = game.get_player_by_username(username).get_table_game()

        config = Player.config

        cell_list = []
        for cell in game_table.flatten():
            if cell.is_ship():
                if cell.is_selected:
                    cell_list.append("ship-selected")
                else:
                    cell_list.append("ship")
            else:
                if cell.is_selected:
                    cell_list.append("empty-selected")
                else:
                    cell_list.append("empty")

        my_table = np.array(cell_list).reshape((config["row"], config["col"]))
        table = np.full((config["row"], config["col"]), "empty")

        context["my_table"] = my_table
        context["table"] = table

        return context
