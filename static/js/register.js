document.addEventListener('DOMContentLoaded', function() {    // Получаем ссылку на кнопку отправки формы регистрации
    const registerButton = document.getElementById('registerButton');  

    // Добавляем обработчик события клика на кнопку отправки формы регистрации    
	registerButton.addEventListener('click', function(event) {

        // Получаем ссылки на все поля формы регистрации        
		const usernameInput = document.getElementById('email');
        const emailInput = document.getElementById('tel');   
		const nameInput = document.getElementById('name');        
		const passwordInputRegister = document.getElementById('passwordInputRegister');
                // Проверяем, заполнены ли все поля формы регистрации
        if (!usernameInput.value || !emailInput.value || !nameInput.value || !passwordInputRegister.value) {            // Если какое-то из полей не заполнено, предотвращаем отправку формы
            event.preventDefault();            // Выводим сообщение об ошибке или предупреждение пользователю
            alert('Пожалуйста, заполните все поля для регистрации.');        
		}
	});
});