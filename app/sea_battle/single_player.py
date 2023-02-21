from django.core.cache import cache
from django.conf import settings

from .player import Player


CACHE_TTL = settings.CACHE_TTL


class SinglePlayer(Player):
    def __init__(self, user_id):
        self.user_id = user_id
        if cache.get(user_id) is not None:
            self.sea = cache.get(user_id)

        else:
            self.start_new_game()

    def start_new_game(self):
        super().start_new_game()
        self.save_game_data()

    def get_changes(self, x, y, type_attack):
        changed_cell = super().get_changes(x, y, type_attack)
        self.save_game_data()
        return changed_cell

    def save_game_data(self):
        cache.set(self.user_id, self.sea, timeout=CACHE_TTL)
