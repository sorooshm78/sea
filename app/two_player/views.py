import numpy as np

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sea_battle.two_player import TwoPlayer
from sea_battle.player import Player


@login_required
def two_player(request):
    username = request.user.username
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

    context = {
        "my_table": my_table,
        "table": table,
    }

    return render(request, "two_player/index.html", context=context)
