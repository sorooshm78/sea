$(document).ready(function () {
    gameSocket = new WebSocket("ws://" + window.location.host + "/ws/search-user");

    gameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        $("#user_info").text(data.user_info);
        setTimeout(function () {
            window.location.replace(data.redirect);
        }, 3000)
    };
});
