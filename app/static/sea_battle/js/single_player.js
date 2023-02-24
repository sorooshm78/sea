function disableAllButtons() {
    $('.cell').prop('disabled', true);
}

function disableSelectButtons() {
    $('.select,.target').prop('disabled', true);
}

function alertMessage(message) {
    var alert = `<div class="alert alert-warning text-center message" role="alert">${message}</div>`;
    $('#message').html(alert);
}

function goToScoreBoardPage() {
    $('#score_board')[0].click();
}

function reduceAttackCount(attackType) {
    var attackCountBadge = $(`#${attackType}_count`);
    count = attackCountBadge.text();
    if (count != 0) {
        count--;
        attackCountBadge.text(count);
        if (count == 0) {
            $(`#${attackType}_btn`).attr('disabled', true);
        }
    }
}

function disableAttackTypeRadioButton() {
    var typeAttacks = [
        'radar',
        'explosion',
        'liner',
    ];
    for (x in typeAttacks) {
        var attackType = typeAttacks[x];
        var attackCountBadge = $(`#${attackType}_count`);
        count = attackCountBadge.text();
        if (count == 0) {
            $(`#${attackType}_btn`).attr('disabled', true);
        }
    }
}

function select(x, y) {
    var attackType = $("input[name='attack']:checked").val();

    if (attackType == 'radar') {
        $.get(`search/?x=${x}&y=${y}`, function (data, status) {
            if (status === 'success') {
                for (index in data.cells) {
                    cell = data.cells[index];
                    $(`#${cell.x}${cell.y}`).removeClass('empty').addClass(cell.class);
                }
                reduceAttackCount(attackType);
            }
        });
    } else {
        $.get(`attack/?x=${x}&y=${y}&type=${attackType}`, function (data, status) {
            if (status === 'success') {
                // Cells select
                for (index in data.cells) {
                    cell = data.cells[index];
                    $(`#${cell.x}${cell.y}`).removeClass('empty')
                        .removeClass('radar-select')
                        .removeClass('radar-target')
                        .addClass(cell.class);
                }
                disableSelectButtons();

                // Attack count
                reduceAttackCount(attackType);

                // End Game
                if (data.is_end_game == 'true') {
                    goToScoreBoardPage();
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
    disableAttackTypeRadioButton();
});
