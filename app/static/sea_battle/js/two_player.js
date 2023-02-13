function showUserInfo(user_info) {
    $("#user_info").text(user_info);
}

function receiveData(data) {
    if (data['user_info']) {
        showUserInfo(data.user_info);
    }
}

$(document).ready(function () {
    gameSocket = new WebSocket("ws://" + window.location.host + "/ws/");

    gameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        receiveData(data);
    };
});
