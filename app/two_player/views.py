from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView, TemplateView
from django.shortcuts import redirect

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from sea_battle.two_player import TwoPlayer
from sea_battle.player import Player
from utils import wrap_data


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

        my_player, opponent_player = self.game.get_my_and_opponent_player_by_username(
            self.username
        )

        config = Player.config

        context["my_table"] = wrap_data.get_template_game_table(
            game_table=my_player.get_table_game(),
            is_ship_hide=False,
            row=config["row"],
            col=config["col"],
        )
        context["opponent_table"] = wrap_data.get_template_game_table(
            game_table=opponent_player.get_table_game(),
            is_ship_hide=True,
            row=config["row"],
            col=config["col"],
        )

        context["opponent_username"] = opponent_player.username
        context["report"] = opponent_player.get_report_game()
        context["attack_count"] = opponent_player.get_attack_count()

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
        current_username = request.user.username
        game = TwoPlayer.get_game(current_username)
        if game is not None:
            game.exit(current_username)
            opponent_player = game.get_opponent_player_by_username(current_username)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                opponent_player.username,
                {
                    "type": "send_to_websocket",
                    "message": f"user {current_username} leave game please start new game",
                },
            )

        return super().get(request, *args, **kwargs)


class NewGameView(ExitGameView):
    pattern_name = "two_player:search_user"
