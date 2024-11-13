from flask import Flask, jsonify, render_template , request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
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

@app.route('/web/email', methods=['GET', 'POST'])
def email():
    if request.method == "POST":
        
        asunto = request.form["asunto"]
        email = request.form["email"]
        mensaje = request.form["mensaje"]

  
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login("elias.gk33@gmail.com", "pass")


        msg = MIMEText(f"Asunto: {asunto}\nMensaje: {mensaje}")

        msg["From"] = "elias.gk33@gmail.com"
        msg["To"] = email
        msg["subject"] = asunto 
        servidor.sendmail("elias.gk33@gmail.com", email, msg.as_string())
        servidor.quit()
        return redirect(url_for('historico'))

    else:
        return render_template("email.html")

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
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    # Construye la URL con los parámetros necesarios para la API externa
    url = f'https://api.argentinadatos.com/v1/cotizaciones/dolares/{moneda}/{fecha_inicio}/{fecha_fin}'
    
    # Solicita los datos a la API externa
    response = requests.get(url)

    # Verifica si la respuesta es exitosa
    if response.status_code == 200:
        # Devuelve los datos históricos en formato JSON
        return jsonify(response.json())
    else:
        return jsonify({'error': 'No se pudieron obtener los datos históricos'}), 500

if __name__ == '__main__':
    app.run(debug=True)
