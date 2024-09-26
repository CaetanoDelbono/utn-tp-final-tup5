//va a estar atento a que descargue bien el dom 
document.addEventListener('DOMContentLoaded', () => {

    fetch("https://dolarapi.com/v1/dolares")
        .then(response => response.json())
        .then(data => {
            console.log(data);

            if (data.length > 0) {
                console.log(data[0].casa);
                const div = document.querySelector('.container');
                let articulos = '';



                for (let i = 0; i < data.length; i++) {
                    const elemento = data[i];

                const fechaActual = new Date();

            
                const fechaFormateada = fechaActual.toLocaleDateString();

            
                const horaFormateada = fechaActual.toLocaleTimeString();

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
                            <strong> ${elemento.venta}</strong>
                        </div>
                    </div>
                    <div class="card-footer">
                        <span>${fechaFormateada} - ${horaFormateada}</span>
                    </div>
                </article> `;


                }
                div.innerHTML = articulos; 
            }
        })
        .catch(error => console.error('Error al obtener los datos:', error));
});


