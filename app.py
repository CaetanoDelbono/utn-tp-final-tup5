from flask import Flask, jsonify, render_template , request, redirect, url_for
import smtplib
import ssl
from email.message import EmailMessage
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta principal para la página principal (cotizaciones actuales)
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de histórico
@app.route('/historico')
def historico():
    return render_template('historico.html')

# Ruta para obtener los datos de la cotización actual
@app.route('/api/cotizacion')
def obtener_cotizacion():
    # Hacemos la solicitud a la API externa
    response = requests.get('https://dolarapi.com/v1/dolares')

    if response.status_code == 200:
        return jsonify(response.json())  # Devolvemos los datos de la API al frontend
    else:
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500

# Ruta para obtener los datos históricos (puedes usar un endpoint de la API de histórico)
@app.route('/historico', methods=['GET'])
def obtener_historico():
    moneda = request.args.get('moneda')
    fecha = request.args.get('fecha')
    
    # Construye la URL con los parámetros necesarios para la API externa
    url = f'https://api.argentinadatos.com/v1/cotizaciones/'
    
    # Solicita los datos a la API externa
    response = requests.get(url)

    # Verifica si la respuesta es exitosa
    if response.status_code == 200:
        # Devuelve los datos históricos en formato JSON
        return jsonify(response.json())
    else:
        return jsonify({'error': 'No se pudieron obtener los datos históricos'}), 500

# Ruta para mostrar el formulario (GET)
@app.route('/web/email', methods=['GET'])
def show_form():
    return render_template('email.html')  # Este archivo debe contener el formulario HTML

@app.route('/web/email', methods=['POST'])
def email():
    try:
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        mail_user = request.form.get("email")

        # Hacer la petición a la API
        url = "https://dolarapi.com/v1/dolares"
        response = requests.get(url)

        # Verificar si la respuesta es exitosa
        if response.status_code == 200:
            # Extraer los datos de la respuesta de la API
            data = response.json()
            print(f"Datos recibidos: {data}")  # Imprimimos los datos para ver su estructura

            # Iterar sobre la lista directamente
            dolar_info = "Cotización del dólar:\n\n"
            for item in data:
                # Accedemos a la casa y la cotización
                casa = item.get('nombre', 'Sin nombre de casa')
                compra = item.get('compra', 'No disponible')
                dolar_info += f"{casa}: ${compra}\n"
        
            # Si no se pudo obtener ninguna cotización
            if not dolar_info.strip():
                dolar_info = "No se pudo obtener la información del dólar."
        else: 
            return jsonify({'error': 'No se pudieron obtener los datos del dólar'}), 500

        # Datos para el correo electrónico
        email_sender = "cae4569139@gmail.com"
        password = "gmhw qgkk nzdf lmda"  # Cambiar por una variable de entorno
        email_receiver = mail_user

        subject = "Cotizaciones del dólar"
        body = f"Estimado {nombre}, se le envía la cotización del dólar:\n\n{dolar_info}"

        # Crear el mensaje del correo
        em = EmailMessage()
        em["from"] = email_sender
        em["to"] = email_receiver
        em["subject"] = subject
        em.set_content(body)

        # Enviar el correo
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

        # Redirigir al usuario a la página principal después de enviar el correo
        return redirect(url_for('index'))

    except KeyError as e:
        # Si no se encuentra algún campo en el formulario
        return jsonify({'error': f'Error en los datos del formulario: {str(e)}'}), 400

    except Exception as e:
        # Captura cualquier otro error inesperado
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500

# Configurar la aplicación Flask para que se ejecute
if __name__ == '__main__':
    app.run(debug=True)
