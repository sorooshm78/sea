$(document).ready(function () {
    gameSocket = new WebSocket("ws://" + window.location.host + "/ws/");
    gameSocket.send(JSON.stringify({
        "message": "hi there",
    }));
    gameSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        alert(data.message);
    };
});
