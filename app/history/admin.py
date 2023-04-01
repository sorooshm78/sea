from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Q

from .models import GameHistoryModel


class GamePlayersFilter(admin.SimpleListFilter):
    title = "Players"
    parameter_name = "player"

    def lookups(self, request, model_admin):
        return [(user.username, user.username) for user in User.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(player1=self.value()) | Q(player2=self.value()))


class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ("game_players", "win", "left", "time")
    list_filter = (GamePlayersFilter, "time")


admin.site.register(GameHistoryModel, GameHistoryAdmin)
