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
            console.log(data);
            for (index in data.cells) {
                cell = data.cells[index]
                $(`#${cell.x}${cell.y}`).removeClass('empty').addClass(cell.class);
            }

            if (data.message) {
                endGame(data.message);
            } else {
                enableEmptyButtons();
            }

        }
    });
}

$(document).ready(function () {
    disableSelectButtons();
});
