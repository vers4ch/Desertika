$(document).ready(function() {
	$('.sendButton').click(function() {
		var valueToSend = $(this).prev('.hiddenValue').val();
		console.log(valueToSend);
		$.ajax({
			type: 'POST',
			url: '/add_to_basket',
			contentType: 'application/json',
			data: JSON.stringify({value: valueToSend}),
			success: function(response) {
				alert('Товар добавлен в корзину');
			},
			error: function(error) {
				console.error('Произошла ошибка при отправке значения на сервер:', error);
			}
		});
	});
});