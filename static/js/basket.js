$(document).ready(function() {
    // Вызываем функцию для обновления общей суммы при загрузке страницы
    updateTotalAmount();

    // Обработчик события для увеличения количества товара
    $('.increase-quantity').on('click', function(e) {
        e.preventDefault();
        var pid = $(this).data('pid');
        var price = $(this).data('price');
        var $countElement = $(this).siblings('.count');
        var count = parseInt($countElement.text());
        count++;
        $countElement.text(count);

        updateQuantityInSession(pid, count, price);
        updateTotalAmount();
    });

    // Обработчик события для уменьшения количества товара
    $('.decrease-quantity').on('click', function(e) {
        e.preventDefault();
        var pid = $(this).data('pid');
        var price = $(this).data('price');
        var $countElement = $(this).siblings('.count');
        var count = parseInt($countElement.text());
        if (count > 1) {
            count--;
            $countElement.text(count);
            updateQuantityInSession(pid, count, price);
            updateTotalAmount();
        }
    });

    // Функция для обновления общей суммы
    function updateTotalAmount() {
        var totalAmount = 0;
        $('.product-box').each(function() {
            var price = parseFloat($(this).find('.increase-quantity').data('price'));
            var count = parseInt($(this).find('.count').text());
            totalAmount += price * count;
        });
        $('#total-amount').text(totalAmount.toFixed(2));
    }

    // Функция для обновления количества в сессии
    function updateQuantityInSession(pid, count, price) {
        $.ajax({
            type: 'POST',
            url: '/update_quantity_in_basket',
            data: {'pid': pid, 'count': count, 'price': price},
            success: function(response) {
                var basketData = response.basket;
                console.log(basketData);
            }
        });
    }

    // Функция для удаления всех нецифровых символов из строки
    function clearString(str) {    
        return str.replace(/\D/g, '');
    }
});
