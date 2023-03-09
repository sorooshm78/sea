function disableAllOpponentTableCells() {
    $("button", "#opponent_table").prop('disabled', true);
}

function enableEmptyOpponentTableCells() {
    $('.empty, .radar-ship, .radar-empty', "#opponent_table").prop('disabled', false);
}

function showUserInfo(user_info) {
    $("#user_info").text(user_info);
}

function showReportShips(report) {
    $('#4-ships').text(report['4_ships']);
    $('#3-ships').text(report['3_ships']);
    $('#2-ships').text(report['2_ships']);
    $('#1-ships').text(report['1_ships']);
}

function showAttackCount(attack_count) {
    $('#liner_count').text(attack_count['liner']);
    $('#explosion_count').text(attack_count['explosion']);
    $('#radar_count').text(attack_count['radar']);
}

function showOpponentCells(cells) {
    for (index in cells) {
        cell = cells[index];
        $(`#${cell.x}${cell.y}`).removeClass('empty')
            .removeClass('radar-empty')
            .removeClass('radar-ship')
            .removeClass('ship')
            .addClass(cell.class);
    }
}

function showMyCells(cells) {
    for (index in cells) {
        cell = cells[index];
        $(`#my_${cell.x}${cell.y}`).removeClass('empty')
            .removeClass('radar-empty')
            .removeClass('radar-ship')
            .removeClass('ship')
            .addClass(cell.class);
    }
}

function showTurn(who) {
    var turn_text = `<i class="fa-regular fa-circle-dot"></i> turn`;
    if (who == "my_turn") {
        enableEmptyOpponentTableCells();
        $("#turn", "#opponent_table").html(turn_text);
        $("#turn", "#my_table").empty();
    }
    if (who == "opponent_turn") {
        disableAllOpponentTableCells();
        $("#turn", "#my_table").html(turn_text);
        $("#turn", "#opponent_table").empty();
    }
}

function receiveData(data) {
    if (data['user_info']) {
        showUserInfo(data.user_info);
    }
    if (data['report']) {
        showReportShips(data.report);
    }
    if (data['attack_count']) {
        showAttackCount(data.attack_count);
    }
    if (data['opponent_cells']) {
        showOpponentCells(data.opponent_cells);
    }
    if (data['my_cells']) {
        showMyCells(data.my_cells);
    }
    if (data['turn']) {
        showTurn(data.turn);
    }
    if (data['redirect']) {
        if (data.redirect) {
            disableAllOpponentTableCells();
            window.location.replace(data.redirect);
        }
    }
}

function reduceAttackCount(attackType) {
    var attackCountBadge = $(`#${attackType}_count`);
    count = attackCountBadge.text();
    if (count != 0) {
        count--;
        attackCountBadge.text(count);
        if (count == 0) {
            $(`#${attackType}_btn`).attr('disabled', true);
        }
    }
}

function select(x, y) {
    var attackType = $("input[name='attack']:checked").val();
    gameSocket.send(JSON.stringify({
        "select": {
            'x': x,
            'y': y,
            'attack_type': attackType,
        },
    }))
    reduceAttackCount(attackType);
}

$(document).ready(function () {
    gameSocket = new WebSocket("ws://" + window.location.host + "/ws/game");

    gameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        receiveData(data);
    };
});
