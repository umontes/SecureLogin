from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import session, sessionmaker, declarative_base
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# from sqlalchemy import String, Integer, DateTime, Column, create_engine
# from sqlalchemy.sql import func
# import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['FLASK_ADMIN_SWATCH'] = 'sandstone'
app.secret_key = 'viv'
engine = create_engine('sqlite:///app.db')
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

# uriel = users(first_name='uriel', last_name='montes', username='umontes', email='uri.mon99@gmail.com', password='vivian123')
# db.session.add(uriel)
# db.session.commit()

# Routes
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