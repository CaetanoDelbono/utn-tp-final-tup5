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


@app.route('/api/cotizacion')
def obtener_cotizacion():
    response = requests.get('https://dolarapi.com/v1/dolares')

    if response.status_code == 200:
        return jsonify(response.json())  
    else:
        return jsonify({'error': 'No se pudieron obtener los datos'}), 500


@app.route('/historico', methods=['GET'])
def obtener_historico():
    moneda = request.args.get('moneda')
    fecha = request.args.get('fecha')
    
    url = f'https://api.argentinadatos.com/v1/cotizaciones/'
    
    
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'No se pudieron obtener los datos históricos'}), 500


@app.route('/web/email', methods=['GET'])
def show_form():
    return render_template('email.html')  

@app.route('/web/email', methods=['POST'])
def email():
    try:
        nombre = request.form.get("nombre")
        mail_user = request.form.get("email")

        
        url = "https://dolarapi.com/v1/dolares"
        response = requests.get(url)

        
        if response.status_code == 200:
            data = response.json()

            dolar_info = "Cotización del dólar:\n\n"
            for item in data:
                casa = item.get('nombre', 'Sin nombre de casa')
                compra = item.get('compra', 'No disponible')
                dolar_info += f"{casa}: ${compra}\n"
        
            if not dolar_info.strip():
                dolar_info = "No se pudo obtener la información del dólar."
        else: 
            return jsonify({'error': 'No se pudieron obtener los datos del dólar'}), 500

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

if __name__ == '__main__':
    app.run(debug=True)
