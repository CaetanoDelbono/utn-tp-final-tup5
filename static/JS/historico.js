/*document.addEventListener('DOMContentLoaded', function () {
    // Obtener el formulario para la selección de histórico
    const formulario = document.getElementById('seleccion-historico');
    
    // Agregar el evento de envío del formulario
    formulario.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevenir el envío del formulario por defecto
        
        // Obtener los valores de fecha y moneda del formulario
        const fecha = document.getElementById('fecha').value;
        const moneda = document.getElementById('moneda').value;
        
        // Realizar la consulta a la API
        fetch(`http://127.0.0.1:5000/historico?fecha=${fecha}&moneda=${moneda}`)
        .then(response => response.json())  // Convertir la respuesta en formato JSON
        .then(data => {
            console.log(data);  // Ver los datos en la consola para depuración
            
            // Limpiar la tabla antes de agregar nuevos datos
            const tablaCotizaciones = document.getElementById('tabla-cotizaciones');
            tablaCotizaciones.innerHTML = '';  // Limpiar el contenido de la tabla
            
            // Verificar si los datos contienen las cotizaciones
            if (data && data.cotizaciones && Array.isArray(data.cotizaciones) && data.cotizaciones.length > 0) {
                // Insertar cada cotización en la tabla
                data.cotizaciones.forEach(cotizacion => {
                    const fila = document.createElement('tr');
                    
                    // Crear celdas para la fecha y la cotización
                    const celdaFecha = document.createElement('td');
                    celdaFecha.textContent = cotizacion.fecha;
                    
                    const celdaCotizacion = document.createElement('td');
                    celdaCotizacion.textContent = cotizacion.valor;
                    
                    // Añadir las celdas a la fila
                    fila.appendChild(celdaFecha);
                    fila.appendChild(celdaCotizacion);
                    
                    // Añadir la fila a la tabla
                    tablaCotizaciones.appendChild(fila);
                });
            } else {
                // Si no se encuentran cotizaciones, mostrar mensaje
                const fila = document.createElement('tr');
                const celda = document.createElement('td');
                celda.colSpan = 2;  // La celda ocupa dos columnas
                celda.textContent = 'No se encontraron cotizaciones para esta fecha.';
                fila.appendChild(celda);
                tablaCotizaciones.appendChild(fila);
            }
        })
        .catch(error => {
            console.error('Error al obtener las cotizaciones:', error);
            // Puedes agregar un mensaje de error en la interfaz si lo deseas
        });
    });
}); */
