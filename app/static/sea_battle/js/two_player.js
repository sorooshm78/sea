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
