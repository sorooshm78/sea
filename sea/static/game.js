function disableAllButtons() {
    $('.empty').prop('disabled', true);
}

function disableSelectButtons() {
    $('.select,.target').prop('disabled', true);
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
            cell.removeClass('empty').addClass(data);
            enableEmptyButtons();
        }
    });
}

$(document).ready(function () {
    disableSelectButtons();
});
