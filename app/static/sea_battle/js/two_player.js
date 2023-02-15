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

function showOppositeCells(cells) {
    for (index in cells) {
        cell = cells[index];
        $(`#${cell.x}${cell.y}`).removeClass('empty').addClass(cell.class);
    }
}

function showMyCells(cells) {
    for (index in cells) {
        cell = cells[index];
        $(`#my_${cell.x}${cell.y}`).removeClass('empty').removeClass('ship').addClass(cell.class);
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
    if (data['opposite_cells']) {
        showOppositeCells(data.opposite_cells);
    }
    if (data['my_cells']) {
        showMyCells(data.my_cells);
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
}

$(document).ready(function () {
    gameSocket = new WebSocket("ws://" + window.location.host + "/ws/");

    gameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        receiveData(data);
    };
});
