function disableButtons() {
    $('.cell').prop('disabled', true);
}

function enableButtons() {
    $('.cell').prop('disabled', false);
}

function select(cell) {
    disableButtons();
    $.get(`/select/${cell}`, function (data, status) {
        console.log(status);
        if (status === 'success') {
            cell = $(`#${cell}`);
            cell.text(data);
            cell.removeClass('cell').addClass('select');
            enableButtons();
        }
    });
}

