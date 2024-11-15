from flask import Flask, jsonify, render_template , request, redirect, url_for, json
from clases import  Tipo 
from clases import  Cotizacion 
from email.message import EmailMessage
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/web/email', methods=['GET'])
def show_form():
    return render_template('email.html') 

#Traemos cotizaciones generales
@app.route('/api/cotizaciones')
def cotizaciones():
    cotizacionArray = []
    try:

        response = requests.get("https://dolarapi.com/v1/cotizaciones")
        if response.status_code == 200:
            datos = response.json()
            
            for moneda in datos:
                cotizacion = Cotizacion(moneda["compra"], moneda["venta"], moneda["fechaActualizacion"])
                tipomoneda = Tipo(moneda["nombre"] ,moneda["moneda"],moneda["casa"])
                cotizacion_data = {
                    "cotizacion": cotizacion.to_dict(),
                    "tipo": tipomoneda.to_dict()
                    }
                cotizacionArray.append(cotizacion_data)

            return jsonify(cotizacionArray)
        else:
            return jsonify({"error": "No se pudo obtener los datos"}), response.status_code
    except requests.exceptions.RequestException as e:
            return jsonify({"error": "Error de conexión"}), 500

#Traemos cotizaciones del dolar
@app.route('/api/cotizacion')
def dolares():
    dolaresArray = []
    try:
        response = response = requests.get("https://dolarapi.com/v1/dolares")
        if response.status_code == 200:
            datos = response.json()
            
            for moneda in datos:
                cotizacion = Cotizacion(moneda["compra"], moneda["venta"], moneda["fechaActualizacion"])
                tipomoneda = Tipo(moneda["nombre"] ,moneda["moneda"],moneda["casa"])
                cotizacion_data = {
                    "cotizacion": cotizacion.to_dict(),
                    "tipo": tipomoneda.to_dict()
                    }
                dolaresArray.append(cotizacion_data)
            return jsonify(dolaresArray)
        else:
            return jsonify({"error": "No se pudo obtener los datos"}), response.status_code
    except requests.exceptions.RequestException as e:
            return jsonify({"error": "Error de conexión"}), 500


@app.route('/historico', methods=['GET'])
def obtener_historico():
    moneda = request.args.get('moneda')
    # fecha = request.args.get('fecha')  # No lo necesitas si no lo estás usando.
    url = f'https://api.argentinadatos.com/v1/cotizaciones/dolares/{moneda}'
    
    try:
        response = requests.get(url)

        if response.status_code == 200:
            datos_historicos = response.json()
            limite = 20
            datos_historicos_limitados = datos_historicos[-limite:]
            return render_template('historico.html', data=datos_historicos_limitados, moneda=moneda)
        else:
            
            return render_template('historico.html', data=None, moneda=moneda, error="No se pudieron obtener los datos históricos")
    except requests.exceptions.RequestException as e:
        return render_template('historico.html', data=None, moneda=moneda, error=f"Error al conectar con la API: {str(e)}")


def generar_cuerpo_mail():
    """Genera el contenido del cuerpo del correo con cotizaciones del dólar y otras monedas."""
    try:
        # Realizamos las dos solicitudes a la API
        response_cotizaciones = requests.get("https://dolarapi.com/v1/cotizaciones")
        response_dolares = requests.get("https://dolarapi.com/v1/dolares")

        # Comprobamos el estado de las respuestas
        if response_cotizaciones.status_code == 200 and response_dolares.status_code == 200:
            cotizaciones = response_cotizaciones.json()
            dolares = response_dolares.json()

            # Generamos el contenido del correo
            email_body = "COTIZACIONES GENERALES\n\n"
            for moneda in cotizaciones:
                email_body += (
                    f"Nombre: {moneda['nombre']}\n"
                    f"Moneda: {moneda['moneda']}\n"
                    f"Compra: {moneda['compra']}\n"
                    f"Venta: {moneda['venta']}\n"
                    f"Casa: {moneda['casa']}\n"
                    f"Fecha de Actualización: {moneda['fechaActualizacion']}\n"
                    + "-" * 30 + "\n"
                )

            email_body += "\nCOTIZACIONES DEL DÓLAR\n\n"
            for moneda in dolares:
                email_body += (
                    f"Nombre: {moneda['nombre']}\n"
                    f"Moneda: {moneda['moneda']}\n"
                    f"Compra: {moneda['compra']}\n"
                    f"Venta: {moneda['venta']}\n"
                    f"Casa: {moneda['casa']}\n"
                    f"Fecha de Actualización: {moneda['fechaActualizacion']}\n"
                    + "-" * 30 + "\n"
                )

            return email_body
        else:
            return "No se pudieron obtener las cotizaciones correctamente."
    except requests.exceptions.RequestException as e:
        return f"Error al obtener las cotizaciones: {str(e)}"


@app.route('/procesar', methods=['POST'])
def procesar():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')

    if nombre and correo:
        print(f"Nombre: {nombre}")
        print(f"Correo: {correo}")

        # Generar el contenido del correo
        mail = generar_cuerpo_mail()

        # Estructura de datos para la API de envío de correos
        data = {
            'service_id': 'RosarioDivisas',
            'template_id': 'CotizacionMonedas',
            'user_id': 'J3P1UbAo9vpiYCfGt',
            'accessToken': 'YrL1rQfoDbiTvFt1bXW_K',
            'template_params': {
                'to_email': correo,
                'from_name': 'RosarioDivisas',
                'user_name': nombre,
                'message': mail
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0',
        }

        try:
            response = requests.post(
                'https://api.emailjs.com/api/v1.0/email/send',
                data=json.dumps(data),
                headers=headers
            )
            response.raise_for_status()
            print('La cotización fue enviada correctamente!')
        except requests.exceptions.RequestException as error:
            print(f'Oops... {error}')
            if error.response is not None:
                print(error.response.text)

        return f'Mensaje enviado correctamente a {correo}', 200
    else:
        return jsonify({'error': "Amigue, completá bien los datos"}), 405


if __name__ == '__main__':
    app.run(debug=True)
