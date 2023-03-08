from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import GameHistoryModel


class GameHistoryView(LoginRequiredMixin, ListView):
    model = GameHistoryModel
    template_name = "history/game_history.html"
    context_object_name = "games"
    MAX_SHOW_GAME = 10

    def get_queryset(self):
        query = super().get_queryset()
        current_username = self.request.user.username
        query = query.filter(Q(player1=current_username) | Q(player2=current_username))
        query = query.order_by("-time")[: self.MAX_SHOW_GAME]
        return query
