// // Открыть модальное окно
// function openModal() {
//     document.getElementById('myModal').style.display = 'flex';
// }

// // Закрыть модальное окно
// function closeModal() {
//     document.getElementById('myModal').style.display = 'none';
// }

// // Закрыть модальное окно при клике вне окна
// window.onclick = function(event) {
//     var modal = document.getElementById('myModal');
//     if (event.target == modal) {
//         modal.style.display = 'none';
//     }
// };


// Открыть модальное окно
function openModal(orderId) {
	var modalId = 'myModal_' + orderId;    
	document.getElementById(modalId).style.display = 'flex';
}
// Закрыть модальное окно
function closeModal(orderId) {
    var modalId = 'myModal_' + orderId;    
	document.getElementById(modalId).style.display = 'none';
}
// Закрыть модальное окно при клике вне окна
window.onclick = function(event) {
    var modals = document.querySelectorAll('[id^="myModal_"]');    
	modals.forEach(function(modal) {
        if (event.target == modal) {            
			modal.style.display = 'none';
        }    
	});
};