function disableAllButtons() {
    $('.empty,.radar-select,.radar-target').prop('disabled', true);
}

function disableSelectButtons() {
    $('.select,.target').prop('disabled', true);
}

function enableEmptyButtons() {
    $('.empty,.radar-select,.radar-target').prop('disabled', false);
}

function alertMessage(message) {
    var alert = `<div class="alert alert-warning text-center message" role="alert">${message}</div>`;
    $('#message').html(alert);
}

function select(x, y) {
    var typeAttack = $("input[name='attack']:checked").val();

    if (typeAttack == 'radar') {
        $.get(`/search-by-radar/?x=${x}&y=${y}`, function (data, status) {
            if (status === 'success') {
                for (index in data.cells) {
                    cell = data.cells[index]
                    $(`#${cell.x}${cell.y}`).removeClass('empty').addClass(cell.class);
                }
            }
        });
    } else {
        $.get(`/select/?x=${x}&y=${y}&type=${typeAttack}`, function (data, status) {
            if (status === 'success') {
                // Cells select
                for (index in data.cells) {
                    cell = data.cells[index]
                    $(`#${cell.x}${cell.y}`).removeClass('empty')
                        .removeClass('radar-select')
                        .removeClass('radar-target')
                        .addClass(cell.class);
                }

                // Alert message
                if (data.message) {
                    alertMessage(data.message);
                    disableAllButtons();
                }

                // Report Game
                $('#4-ships').text(data.report['4_ships']);
                $('#3-ships').text(data.report['3_ships']);
                $('#2-ships').text(data.report['2_ships']);
                $('#1-ships').text(data.report['1_ships']);
            }
        });

    }

}

$(document).ready(function () {
    disableSelectButtons();
});
