from flask import Flask, jsonify, render_template , request, redirect, url_for, session, flash
import smtplib
import ssl
from clases import  Tipo 
from clases import  Cotizacion 
from email.message import EmailMessage
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "b9d7f2e4a7b8c1f2e5d8f9a2b4c6d8e1"
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/web/email', methods=['GET'])
def show_form():
    return render_template('email.html') 

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



@app.route('/web/email', methods=['POST'])
def save_email():
    try:
        session['nombre'] = request.form.get("nombre", "")
        session['email'] = request.form.get("email", "")
        
        
        return redirect(url_for('index'))  # Redirigir de nuevo al índice
    except Exception as e:
        return jsonify({'error': f'Ocurrió un error: {str(e)}'}), 500
    

@app.route('/enviar_cotizaciones', methods=['POST'])
def enviar_cotizaciones():
    try:
        # Obtener el nombre y el email de la sesión
        nombre = session.get('nombre')
        email_receiver = session.get('email')

        # Verificar si hay datos en la sesión
        if not email_receiver:
            flash("Por favor, complete todos los campos del formulario.", category='error')
            return redirect(url_for('show_form'))

        # Obtener las cotizaciones actuales
        url = "https://dolarapi.com/v1/dolares"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            dolar_info = "Cotización del dólar:\n\n"
            for item in data:
                casa = item.get('nombre', 'Sin nombre de casa')
                compra = item.get('compra', 'No disponible')
                dolar_info += f"{casa}: ${compra}\n"
        else:
            dolar_info = "No se pudo obtener la información del dólar."

        #configuracion del correo 
        email_sender = "cae4569139@gmail.com"
        password = "gmhw qgkk nzdf lmda"
        subject = "Cotizaciones del dólar"
        body = f"Estimado {nombre}, se le envía la cotización del dólar:\n\n{dolar_info}"
        #armamos cuerpo del correo
        em = EmailMessage()
        em["from"] = email_sender
        em["to"] = email_receiver
        em["subject"] = subject
        
        #configuramos el contenido como texto plano
        em.set_content(body, subtype='plain', charset='utf-8')
        
        # Enviar el correo
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        #limpiamos la sesión después de enviar el correo
        session.clear()
        
        flash("El correo se envió correctamente.", category='success')
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
