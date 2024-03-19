document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevenir el envío del formulario
    var registrationMessage = document.getElementById('registrationMessage');
    registrationMessage.style.display = 'block'; // Mostrar el mensaje de registro
    /*setTimeout(function() {
        registrationMessage.style.display = 'none'; // Ocultar el mensaje después de 3 segundos
    }, 3000);*/
});