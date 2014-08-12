window.onload = function () {
    var $updateButtons = $('._updateButton');
    $.each($updateButtons, function () {
        $(this).on('click', function () {
            var id = $(this).val();
            var $modal = $('._updateModal');
            var $modalBody = $modal.find('.modal-body');
            $modalBody.load('/static/html/loading.html');
            $modal.modal();
            $.ajax({
                url: '/beers/update_beer/' + id + '/',
                type: 'get',
                success: function (data) {
                    $modalBody.html(data);
                    $('._updateSubmit').on('click', function () {
                        $modal.find('form').submit();
                    });
                }
            });
        });
    });

    var $checkoutButtons = $('._checkoutButton');
    $.each($checkoutButtons, function () {
        $(this).on('click', function () {
            var id = $(this).val();
            var $modal = $('._checkoutModal');
            var $modalBody = $modal.find('.modal-body');
            $modalBody.load('/static/html/loading.html');
            $modal.modal();
            $.ajax({
                url: '/beers/checkout_beer/' + id + '/',
                type: 'get',
                success: function (data) {
                    $modalBody.html(data);
                    $('._checkoutSubmit').on('click', function () {
                            $modal.find('form').submit();
                    });
                }
            });
        })
    });

    var $historyButton = $('._moreHistoryButton');
    $historyButton.on('click', function () {
        $('._loading').load('/static/html/loading.html');
        $.ajax({
            url: '/beers/more_history/' + $historyButton.val() +'/',
            type: 'get',
            success: function (data) {
                $('._loadingIndicator').remove();
                $('._moreHistory').before(data);
                $historyButton.val(parseInt($historyButton.val())+1);
            }
        });
    });
};