from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    title = 'Rosario Divisas'
    return render_template('index.html', title=title)

@app.route('/web/mail')
def history():
    title= 'Rosario Divisas'
    return render_template('historicos.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == 'POST':
        return 'You made a POST request'
    
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
        return redirect(url_for('history'))

    else:
        return render_template("email.html")

   

@app.route('/greet/<name>')
def greet(name):
    return f"hello {name}"

@app.route('/add/<int:number1>/<int:number2>')
def add(number1, number2):
    return f'{number1} + {number2} = {number1 + number2}'

@app.route('/handle_url_params')
def handle_params():
    if 'greeting' in request.args.keys() and 'name' in request.args.keys():
        greeting = request.args['greeting']
        name = request.args.get('name')
    else: 
        return 'some parameters are missing'

    return f'{greeting}, {name}'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5555, debug=True)