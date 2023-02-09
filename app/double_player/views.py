import numpy as np

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sea_battle.sea_battle_game import SeaBattleGame


@login_required
def double_player(request):
    game = SeaBattleGame(request.user.id)
    game_table = game.get_table_game()
    config = game.config

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
        "report": game.get_report_game(),
        "attack_count": game.get_attack_count(),
    }

    return render(request, "sea_battle/double_player.html", context=context)