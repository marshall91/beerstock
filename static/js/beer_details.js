window.onload = function () {
    var $updateButtons = $('._updateButton');
    $.each($updateButtons, function () {
        $(this).on('click', function () {
            var id = $(this).val();
            $.ajax({
                url: '/beers/update_beer/' + id + '/',
                type: 'get',
                success: function (data) {
                    var $modal = $('._updateModal' + id);
                    if($modal.length === 0) {
                        $('._beer_box' + id).append(data);
                        $('._updateSubmit' + id).on('click', function () {
                            $modal.find('form').submit();
                        });
                        $modal = $('._updateModal' + id);
                    }
                    $modal.modal();
                }
            });
        });
    });

    var $checkoutButtons = $('._checkoutButton');
    $.each($checkoutButtons, function () {
        $(this).on('click', function () {
            var id = $(this).val();
            $.ajax({
                url: '/beers/checkout_beer/' + id + '/',
                type: 'get',
                success: function (data) {
                    var $modal = $('._checkoutModal' + id);
                    if($modal.length === 0) {
                        $('._beer_box' + id).append(data);
                        $('._checkoutSubmit' + id).on('click', function () {
                            $modal.find('form').submit();
                        });
                        $modal = $('._checkoutModal' + id);
                    }
                    $modal.modal();
                }
            });
        })
    });

    var $historyButton = $('._moreHistoryButton');
    $historyButton.on('click', function () {
        $.ajax({
            url: '/beers/more_history/' + $historyButton.val() +'/',
            type: 'get',
            success: function (data) {
                $('._moreHistory').before(data);
                $historyButton.val(parseInt($historyButton.val())+1);
            },
            failure: function (data) {
                alert('AJAX failed');
            }
        });
    });
};