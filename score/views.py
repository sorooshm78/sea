from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Window
from django.db.models.functions import Rank

from .models import ScoreBoardModel


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
