from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    title = 'Rosario Divisas'
    return render_template('index.html', title=title)

@app.route('/historico')
def history():
    title= 'Rosario Divisas'
    return render_template('historicos.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == 'POST':
        return 'You made a POST request'
    
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return 'You made a GET request'
    elif request.method == 'POST':
        return 'You made a POST request'
    else: 
        return 'You will never see this message '
   

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