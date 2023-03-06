import numpy as np

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView, TemplateView
from django.shortcuts import redirect

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from sea_battle.two_player import TwoPlayer
from sea_battle.player import Player


# FIXME Rename to another name, for example "add_css_data"
# FIXME Factor duplicate code of current file methods
# FIXME Add utils and factor duplicate code of app's views in it
def get_view_game_table_with_ship(game_table, row, col):
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

    return np.array(cell_list).reshape((row, col))


def get_view_game_table_hide_ship(game_table, row, col):
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

    return np.array(cell_list).reshape((row, col))


class TwoPlayerView(LoginRequiredMixin, TemplateView):
    template_name = "two_player/index.html"

    def dispatch(self, request, *args, **kwargs):
        self.username = self.request.user.username
        self.game = TwoPlayer.get_game(self.username)
        if self.game is None:
            return redirect("two_player:search_user")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *arg, **kwargs):
        context = super().get_context_data(*arg, **kwargs)

        my_player, opposite_player = self.game.get_my_and_opposite_player_by_username(
            self.username
        )

        config = Player.config

        context["my_table"] = get_view_game_table_with_ship(
            my_player.get_table_game(), config["row"], config["col"]
        )
        context["opposite_table"] = get_view_game_table_hide_ship(
            opposite_player.get_table_game(), config["row"], config["col"]
        )
        context["opposite_username"] = opposite_player.username
        context["report"] = opposite_player.get_report_game()
        context["attack_count"] = opposite_player.get_attack_count()

        return context


class SearchUserView(LoginRequiredMixin, TemplateView):
    template_name = "two_player/search_user.html"

    def dispatch(self, request, *args, **kwargs):
        username = self.request.user.username
        game = TwoPlayer.get_game(username)
        if game is not None:
            return redirect("two_player:two_player")
        return super().dispatch(request, *args, **kwargs)


class ExitGameView(LoginRequiredMixin, RedirectView):
    pattern_name = "home:home"

    def get(self, request, *args, **kwargs):
        my_username = request.user.username
        game = TwoPlayer.get_game(my_username)
        if game is not None:
            game.exit(my_username)
            opposite_player = game.get_opposite_player_by_username(my_username)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                opposite_player.username,
                {
                    "type": "send_to_websocket",
                    "message": f"user {my_username} leave game please start new game",
                },
            )

        return super().get(request, *args, **kwargs)


class NewGameView(ExitGameView):
    pattern_name = "two_player:search_user"
