function disableAllButtons() {
    $('.empty').prop('disabled', true);
}

function disableSelectButtons() {
    $('.select').prop('disabled', true);
}

function enableEmptyButtons() {
    $('.empty').prop('disabled', false);
}

function select(cell) {
    disableAllButtons();
    $.get(`/select/${cell}`, function (data, status) {
        console.log(status);
        if (status === 'success') {
            cell = $(`#${cell}`);
            cell.text(data);
            cell.removeClass('empty').addClass('select');
            enableEmptyButtons();
        }
    });
}

$(document).ready(function () {
    disableSelectButtons();
});
