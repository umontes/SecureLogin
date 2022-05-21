from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def welcome():
    return render_template('home.html')

@app.route('/register')
def create():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)