function disableAllButtons() {
    $('.empty').prop('disabled', true);
}

function disableSelectButtons() {
    $('.select').prop('disabled', true);
}

function enableEmptyButtons() {
    $('.empty').prop('disabled', false);
}

function select(x, y) {
    disableAllButtons();
    $.get(`/select/?x=${x}&y=${y}`, function (data, status) {
        console.log(status);
        if (status === 'success') {
            cell = $(`#${x}${y}`);
            cell.text(data);
            cell.removeClass('empty').addClass('select');
            enableEmptyButtons();
        }
    });
}

$(document).ready(function () {
    disableSelectButtons();
});
