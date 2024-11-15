document.addEventListener('DOMContentLoaded', () => {
    fetch("http://127.0.0.1:5000/api/cotizacion")
    .then(response => response.json())
    .then(results => {
        results.forEach(moneda => {
        const newMoneda = document.createElement('article');
        newMoneda.classList.add('card');
        
        // Obtener la fecha y hora actual
        const fechaActual = new Date();
        const fechaFormateada = fechaActual.toLocaleDateString(); // Fecha actual
        const horaFormateada = fechaActual.toLocaleTimeString(); // Hora actual
        
        newMoneda.innerHTML = `
        <div class="card-header"> 
            <p class="nombre_casa">${moneda.tipo.moneda}</p>
            <p class="nombre_casa">${moneda.tipo.nombre}</p>
        </div>
        <div class="card-body">
            <div class="precio">
                <span>Compra</span>
                <strong>$${moneda.cotizacion.compra.toLocaleString("es-ES")}</strong>
            </div>
            <div class="precio">
                <span>Venta</span>
                <strong>$${moneda.cotizacion.venta.toLocaleString("es-ES")}</strong>
            </div>
        </div>
        <div class="card-footer"> 
            <p>Fecha actualización: ${fechaFormateada} ${horaFormateada}</p>
        </div>
    `;
        const boxTarjetas = document.querySelector('.cotizaciones .container');
        boxTarjetas.appendChild(newMoneda);
        });
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
    });
});

fetch("http://127.0.0.1:5000/api/cotizaciones")
    .then(response => response.json())
    .then(results => {
        results.forEach(moneda => {
        const newMoneda = document.createElement('article');
        newMoneda.classList.add('card');
        
        const fechaActual = new Date();
        const fechaFormateada = fechaActual.toLocaleDateString();
        const horaFormateada = fechaActual.toLocaleTimeString(); 
        
        newMoneda.innerHTML = `
        <div class="card-header"> 
            <p class="nombre_casa">${moneda.tipo.moneda}</p>
            <p class="nombre_casa">${moneda.tipo.nombre}</p>
        </div>
        <div class="card-body">
            <div class="precio">
                <span>Compra</span>
                <strong>$${moneda.cotizacion.compra.toLocaleString("es-ES")}</strong>
            </div>
            <div class="precio">
                <span>Venta</span>
                <strong>$${moneda.cotizacion.venta.toLocaleString("es-ES")}</strong>
            </div>
        </div>
        <div class="card-footer"> 
            <p>Fecha actualización: ${fechaFormateada} ${horaFormateada}</p>
        </div>
    `;
        const boxTarjetas = document.querySelector('.cotizaciones .container');
        boxTarjetas.appendChild(newMoneda);
        });
    })
    .catch(error => {
        console.error('Error al obtener los datos:', error);
    });


  // Función para verificar si la cotización está actualizada
function verificarFechaActualizada(fecha) {
    const fechaActual = new Date();
    const fechaCotizacion = new Date(fecha);
    const diferenciaEnDias = Math.floor((fechaActual - fechaCotizacion) / (1000 * 3600 * 24));
    
    return diferenciaEnDias <= 1; // Si la cotización es de hace 1 día o menos, la consideramos actualizada
}


const currentPage = window.location.pathname.split("/").pop();

// Obtiene todos los enlaces
const links = document.querySelectorAll(".nav-links a");

// Recorre todos los enlaces y agrega la clase "active" al que corresponde
links.forEach(link => {
if (link.getAttribute("href") === currentPage) {
    link.classList.add("active");
}

const currentLocation = location.pathname;
const menuItems = document.querySelectorAll('nav ul li a');

menuItems.forEach(item => {
if (item.getAttribute('href') === currentLocation) {
    item.classList.add('active');
}
    });
});



