import numpy as np


def get_template_game_table(game_table, is_ship_hide, row, col):
    cell_list = []
    for cell in game_table.flatten():
        if cell.is_ship():
            if cell.is_selected:
                cell_list.append("ship-selected")
            else:
                if is_ship_hide:
                    cell_list.append("empty")
                else:
                    cell_list.append("ship")
        else:
            if cell.is_selected:
                cell_list.append("empty-selected")
            else:
                cell_list.append("empty")

    return np.array(cell_list).reshape((row, col))


def add_css_data_to_cells_when_attack_select(cells):
    for cell in cells:
        cell_value = cell.pop("value")
        if cell_value.is_ship():
            if cell_value.is_selected:
                cell["class"] = "ship-selected"
        else:
            if cell_value.is_selected:
                cell["class"] = "empty-selected"

    return cells


def add_css_data_to_cells_when_radar_select(cells):
    for cell in cells:
        cell_value = cell.pop("value")
        if cell_value.is_ship():
            cell["class"] = "radar-ship"
        else:
            cell["class"] = "radar-empty"

    return cells
