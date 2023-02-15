import numpy as np

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sea_battle.two_player import TwoPlayer


@login_required
def two_player(request):
    username = request.user.username
    game = TwoPlayer(username)
    game_table = game.get_table_game(username)
    config = TwoPlayer.config

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

    return render(request, "sea_battle/two_player.html", context=context)
