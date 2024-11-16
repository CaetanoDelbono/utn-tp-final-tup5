from flask import Flask, jsonify, render_template , request, redirect, url_for, json
from clases import  Tipo 
from clases import  Cotizacion 
from datetime import datetime
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
            # Omitimos la primera cotización
            datos = datos[1:]  # Desde la segunda en adelante
            
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
        #realizamos las dos solicitudes a la API
        response_cotizaciones = requests.get("https://dolarapi.com/v1/cotizaciones")
        response_dolares = requests.get("https://dolarapi.com/v1/dolares")

        #comprobamos el estado de las respuestas
        if response_cotizaciones.status_code == 200 and response_dolares.status_code == 200:
            cotizaciones = response_cotizaciones.json()
            dolares = response_dolares.json()
            
            cotizaciones = cotizaciones[1:]  
        

            #Generamos el contenido del correo
            email_body = "COTIZACIONES GENERALES\n\n"
            for moneda in cotizaciones:
                fecha_iso = moneda['fechaActualizacion']
                fecha_obj = datetime.fromisoformat(fecha_iso.replace("Z", "")) 
                fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S ")  
                email_body += (
                    f"Nombre: {moneda['nombre']}\n"
                    f"Moneda: {moneda['moneda']}\n"
                    f"Compra: {moneda['compra']}\n"
                    f"Venta: {moneda['venta']}\n"
                    f"Fecha de Actualización: {fecha_formateada}\n"
                    + "-" * 50 + "\n"
                )

            email_body += "\nCOTIZACIONES DEL DÓLAR\n\n"
            for moneda in dolares:
                fecha_iso = moneda['fechaActualizacion']
                fecha_obj = datetime.fromisoformat(fecha_iso.replace("Z", "")) 
                fecha_formateada = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")  
                email_body += (
                    f"Nombre: {moneda['nombre']}\n"
                    f"Moneda: {moneda['moneda']}\n"
                    f"Compra: {moneda['compra']}\n"
                    f"Venta: {moneda['venta']}\n"
                    f"Fecha de Actualización: {fecha_formateada}\n"
                    + "-" * 50 + "\n"
                )

            return email_body
        else:
            return "No se pudieron obtener las cotizaciones correctamente."
    except requests.exceptions.RequestException as e:
        return f"Error al obtener las cotizaciones: {str(e)}"


@app.route('/procesar', methods=['POST'])
def procesar():
    # Obtener los datos del formulario
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    tipo = request.form.get('tipo')  #tipo de formulario: 'contacto' o 'cotizacion'

    if nombre and correo:
        if tipo == 'contacto':  
            mail = mensaje 
            data = {
                'service_id': 'RosarioDivisas',
                'template_id': 'Contacto',
                'user_id': 'J3P1UbAo9vpiYCfGt',
                'accessToken': 'YrL1rQfoDbiTvFt1bXW_K',
                'template_params': {
                    'user_name': nombre,
                    'message': mail,
                }
            }
        else: 
            mail = generar_cuerpo_mail() 
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
            return jsonify({"message": "Correo enviado correctamente"}), 200
        except requests.exceptions.RequestException as error:
            print(f'Oops... {error}')
            return jsonify({"error": "Error al enviar el correo"}), 500
    else:
        return jsonify({'error': "Por favor, completa todos los datos"}), 400


if __name__ == '__main__':
    app.run(debug=True)
