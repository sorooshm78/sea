function disableButtons() {
    $('.cell').prop('disabled', true);
}

function enableButtons() {
    $('.cell').prop('disabled', false);
}

function select(cell) {
    disableButtons();
}

