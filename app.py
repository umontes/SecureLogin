from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import session, sessionmaker, declarative_base
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash

# from sqlalchemy import String, Integer, DateTime, Column, create_engine
# from sqlalchemy.sql import func
# import json

app = Flask(__name__)
DB_NAME = 'app.db'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
app.secret_key = 'viv'
engine = create_engine(f'sqlite:///{DB_NAME}')
db = SQLAlchemy(app)

admin = Admin(app, name='Dashboard', template_mode='bootstrap3')

Base = declarative_base()
Session = sessionmaker(app)
session = Session()

# users table creation
class users(db.Model):
    __tablename__ = 'Users'
    id = Column('user_id', db.Integer, primary_key=True)
    first_name = Column('first name', db.String, nullable=False)
    last_name = Column('last name', db.String, nullable=False)
    username = Column('username', db.String, nullable=False)
    email = Column('email', db.String, unique=True, nullable=False)
    password = Column('password', db.Text, unique=True, nullable=False)

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

db.create_all()
db.session.commit()
admin.add_view(ModelView(users, db.session))

# Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.query.filter_by(username=username).first()

        if user:
            if password == user.password:
                return redirect('/home')
            else:
                return redirect('/register')

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        new_user = users(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)