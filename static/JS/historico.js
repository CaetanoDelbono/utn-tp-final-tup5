document.getElementById('seleccion-historico').addEventListener('submit', async function(event) {
    event.preventDefault();  // Evitar el envío del formulario y recarga de página
    
    // Obtener la moneda seleccionada y las fechas
    const moneda = document.getElementById('moneda').value;
    const fechaInicio = document.getElementById('fecha_inicio').value;
    const fechaFin = document.getElementById('fecha_fin').value;

    try {
        const response = await fetch(`/historico/${moneda}?fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`);
        
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await response.json();

        if (data.error) {
            document.getElementById('resultado-historico').innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            renderizarTabla(data);
            renderizarGrafico(data);
        }
    } catch (error) {
        console.error("Error al obtener los datos:", error);
        document.getElementById('resultado-historico').innerHTML = `<p style="color: red;">Hubo un problema al obtener los datos. Por favor, intente nuevamente.</p>`;
    }
});

function renderizarTabla(data) {
    const tbody = document.getElementById('tabla-cotizaciones');
    tbody.innerHTML = ''; //limpiamos la tabla

    if (data.length > 0) {
        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${item.casa}</td>
                <td>${item.compra}</td>
                <td>${item.venta}</td>
                <td>${item.fecha}</td>
            `;
            tbody.appendChild(tr);
        });
    } else {
        tbody.innerHTML = '<tr><td colspan="4">No hay datos disponibles para este rango de fechas.</td></tr>';
    }
}

// Función para dibujar el gráfico con los datos
function renderizarGrafico(data) {
    const fechas = data.map(item => item.fecha); 
    const valoresCompra = data.map(item => parseFloat(item.compra)); 
    const valoresVenta = data.map(item => parseFloat(item.venta));

    const ctx = document.getElementById('graficoDolar').getContext('2d'); 
    
    if (window.myChart) {
        window.myChart.destroy();
    }

    
    window.myChart = new Chart(ctx, {
        type: 'line', 
        data: {
            labels: fechas, 
            datasets: [
                {
                    label: 'Compra',
                    data: valoresCompra, 
                    borderColor: 'green', 
                    fill: false, 
                    tension: 0.1 
                },
                {
                    label: 'Venta',
                    data: valoresVenta, 
                    borderColor: 'red', 
                    fill: false, 
                    tension: 0.1 
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Fecha' 
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Precio (USD)' 
                    },
                    beginAtZero: false
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const lastMonth = new Date();
    lastMonth.setMonth(today.getMonth() - 1);

    //Función para formatear la fecha en el formato adecuado (YYYY-MM-DD)
    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const minDate = formatDate(lastMonth);
    const maxDate = formatDate(today);

    //Asignamos el rango de fechas
    document.getElementById('fecha_inicio').setAttribute('min', minDate);
    document.getElementById('fecha_inicio').setAttribute('max', maxDate);
    document.getElementById('fecha_fin').setAttribute('min', minDate);
    document.getElementById('fecha_fin').setAttribute('max', maxDate);
    //Asignamos las fechas 
    document.getElementById('fecha_inicio').value = minDate;
    document.getElementById('fecha_fin').value = maxDate;

    //Limitamos el calendario
    document.querySelectorAll('input[type="date"]').forEach(input => {
        input.addEventListener('focus', (e) => e.target.showPicker()); // Mostrar el calendario al hacer focus
    });
});
