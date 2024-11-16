document.addEventListener('DOMContentLoaded', () => {
    // Realiza ambas solicitudes en paralelo
    Promise.all([
        fetch("http://127.0.0.1:5000/api/cotizacion").then(response => response.json()),
        fetch("http://127.0.0.1:5000/api/cotizaciones").then(response => response.json())
    ])
    .then(([cotizacion, cotizaciones]) => {
        const allResults = [...cotizacion, ...cotizaciones]; // Si quieres combinarlas

        // Asegúrate de que el contenedor existe antes de intentar acceder a él
        const boxTarjetas = document.querySelector('.cotizaciones .container');
        console.log("Contenedor encontrado:", boxTarjetas); // Verifica si el contenedor está presente
        if (!boxTarjetas) {
            console.error("No se encontró el contenedor '.cotizaciones .container'");
            return;
        }

        allResults.forEach(moneda => {
            // Verifica que la moneda tenga las propiedades correctas
            if (moneda.tipo && moneda.tipo.moneda && moneda.tipo.nombre && moneda.cotizacion) {
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
            } else {
                console.warn("Datos incompletos en moneda:", moneda); 
            }
        });
    })
    .catch(error => {
        console.error("Error al obtener las cotizaciones:", error);
    });


// Obtén la página actual (último segmento del path)
    // Obtén la URL actual
    const currentUrl = window.location.href;

    const links = document.querySelectorAll(".nav-links a");

    // Itera sobre los enlaces y compara su href con la URL actual
    links.forEach(link => {
        if (currentUrl.includes(link.href)) {
            link.classList.add("active");
        }
    });
});
