document.addEventListener("DOMContentLoaded", function() {
    //Función para mostrar el modal 
    function manejarModal(mensaje) {
        var modal = document.getElementById('modal');
        var modalMessage = document.getElementById('modal-message');
        var modalClose = document.getElementById('modal-close');

        modalMessage.textContent = mensaje;

        //Mostrar el modal
        modal.style.display = "block";

        modalClose.onclick = function() {
            modal.style.display = "none";
        }
        setTimeout(function() {
            modal.style.display = "none";
        }, 2000);
    }

    //Función para manejar el envío del formulario
    function manejarFormulario(formularioId) {
        var formulario = document.getElementById(formularioId);
        if (formulario) {
            formulario.addEventListener('submit', function(event) {
                event.preventDefault();

                var formData = new FormData(this);

                fetch('/procesar', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        manejarModal(data.message);
                    } else if (data.error) {
                        manejarModal(data.error); 
                    } else {
                        manejarModal("Operación realizada con éxito."); 
                    }
                    formulario.reset();
                })
                .catch(error => {
                    console.error('Error:', error);
                    manejarModal("Hubo un error al procesar la solicitud. Por favor, inténtalo nuevamente.");
                });
            });
        } else {
            console.error("Formulario con ID " + formularioId + " no encontrado.");
        }
    }

    //llamamos a la función manejarFormulario para cada formulario
    manejarFormulario('email-form');
    manejarFormulario('formContacto');
});

