$(document).ready(function() {
    var totalAmount = 0;
    // Вызываем функцию для обновления общей суммы при загрузке страницы
    updateTotalAmount();

    

    // Обработчик события для увеличения количества товара в сессии
    $('.increase-quantity').on('click', function(e) {
        e.preventDefault();
        var pid = $(this).data('pid');
        var price = $(this).data('price');
        var $countElement = $(this).siblings('.count');
        var count = parseInt($countElement.text());
        count++;
        $countElement.text(count);

        updateQuantityInSession(pid, count);
        updateTotalAmount();
    });

    // Обработчик события для уменьшения количества товара в сессии
    $('.decrease-quantity').on('click', function(e) {
        e.preventDefault();
        var pid = $(this).data('pid');
        var price = $(this).data('price');
        var $countElement = $(this).siblings('.count');
        var count = parseInt($countElement.text());
        if (count > 1) {
            count--;
            $countElement.text(count);
            updateQuantityInSession(pid, count);
            updateTotalAmount();
        }
    });

    // Функция для обновления общей суммы в сессии
    function updateTotalAmount() {
        totalAmount = 0;
        $('.product-box').each(function() {
            var price = parseFloat($(this).find('.increase-quantity').data('price'));
            var count = parseInt($(this).find('.count').text());
            totalAmount += price * count;
        });
        $('#total-amount').text(totalAmount.toFixed(2));
        $('#total-amount2').text(totalAmount.toFixed(2));
        updateSummInSession();
    }

    // Функция для обновления количества в сессии
    function updateQuantityInSession(pid, count) {
        updateTotalAmount();
        $.ajax({
            type: 'POST',
            url: '/update_quantity_in_basket',
            data: {'pid': pid, 'count': count},
            success: function(response) {
                var basketData = response.basket;
                console.log(basketData);
            }
        });
    }

    // Функция для удаления всех нецифровых символов из строки
    function updateSummInSession(sum) {    
        $.ajax({
            type: 'POST',
            url: '/update_sum',
            data: {'totalAmount': totalAmount},
            success: function(response) {
                // var basketData = response.basket;
                // console.log(basketData);
            }
        });
    }
});
