document.addEventListener('DOMContentLoaded', () => {
    fetch("http://127.0.0.1:5000/api/cotizacion")
        .then(response => response.json())
        .then(data => {
            console.log(data); // Verifica que los datos se reciban correctamente

            if (data.length > 0) {
                const div = document.querySelector('.container');
                let articulos = '';
                for (let i = 0; i < data.length; i++) {
                    const elemento = data[i];
                    //fecha y hora actual
                    const fechaActual = new Date();
                    const fechaFormateada = fechaActual.toLocaleDateString();
                    const horaFormateada = fechaActual.toLocaleTimeString();
                    //HTML para cada artículo
                    articulos += `<article class="card">
                        <div class="card-header">
                            <span>${elemento.nombre.slice(0,15)}:</span>
                            <span class="variation down">- 3,07%</span>
                        </div>
                        <div class="card-body">
                            <div class="precio">
                                <span>COMPRA</span>
                                <strong>${elemento.compra}</strong>
                            </div>
                            <div class="precio">
                                <span>VENTA</span>
                                <strong>${elemento.venta}</strong>
                            </div>
                        </div>
                        <div class="card-footer">
                            <span>${fechaFormateada} - ${horaFormateada}</span>
                        </div>
                    </article>`;
                }

                // Insertamos las tarjetas generadas en el contenedor
                div.innerHTML = articulos;
            }
        })
        .catch(error => console.error('Error al obtener los datos:', error));
});
