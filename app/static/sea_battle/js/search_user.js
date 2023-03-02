$(document).ready(function () {
    gameSocket = new WebSocket("ws://" + window.location.host + "/ws/search-user");

    gameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        window.location.replace(data.redirect);
    };
});
