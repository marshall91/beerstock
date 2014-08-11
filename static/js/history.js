window.onload = function () {
    var $historyButton = $('._moreHistoryButton');
    $historyButton.on('click', function () {
        $.ajax({
            url: '/beers/more_history/' + $historyButton.val() +'/',
            type: 'get',
            success: function (data) {
                $('._moreHistory').before(data).val(parseInt($historyButton.val())+1);
            },
            failure: function (data) {
                alert('AJAX failed');
            }
        });
    });
};