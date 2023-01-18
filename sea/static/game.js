function disableAllButtons() {
    $('.empty').prop('disabled', true);
}

function disableSelectButtons() {
    $('.select,.target').prop('disabled', true);
}

function enableEmptyButtons() {
    $('.empty').prop('disabled', false);
}

function endGame(message) {
    $('#msg').text(message);
    $('#msg').addClass('end-game');
}

function select(x, y) {
    disableAllButtons();
    $.get(`/select/?x=${x}&y=${y}`, function (data, status) {
        console.log(status);
        if (status === 'success') {
            // Cells select
            for (index in data.cells) {
                cell = data.cells[index]
                $(`#${cell.x}${cell.y}`).removeClass('empty').addClass(cell.class);
            }

            // End Game
            if (data.message) {
                endGame(data.message);
            } else {
                enableEmptyButtons();
            }

            // Report Game
            $('#4-ships').text(data.report['4_ships']);
            $('#3-ships').text(data.report['3_ships']);
            $('#2-ships').text(data.report['2_ships']);
            $('#1-ships').text(data.report['1_ships']);
        }
    });
}

$(document).ready(function () {
    disableSelectButtons();
});
