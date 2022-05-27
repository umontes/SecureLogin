from flask import Flask, render_template, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import session, sessionmaker, declarative_base
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager

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

## users table creation
class users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = Column('user_id', db.Integer, primary_key=True)
    first_name = Column('first name', db.String, nullable=False)
    last_name = Column('last name', db.String, nullable=False)
    username = Column('username', db.String, unique=True, nullable=False)
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

# login manager stuff
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    return users.query.get(int(id))

## Routes
#the welcome page for any user. users that are not logged in.
@app.route('/') 
def welcome():
    return render_template('welcome.html', user=current_user)

#login page for users to sign in or to be able to go to create account
@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('You are logged in!', category='success')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('User doesn\'t exist', category='error')
            return redirect(url_for('register'))

    return render_template('login.html', user=current_user)

#the home page for the users that have logged in
@app.route('/home') 
@login_required
def home():
    return render_template('home.html', user=current_user)

#the page where new users can create their account
@app.route('/register', methods=['GET', 'POST']) 
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = users.query.filter_by(username=username).first()

        if user:
            flash('User already exists.', category='error')
        elif len(first_name) < 1:
            flash('Enter your first name.', category='error')
        elif len(last_name) < 1:
            flash('Enter your last name.', category='error')
        elif len(username) < 5:
            flash('username must be at least 5 characters long.', category='error')
        elif len(email) < 10:
            flash('email must be at least 10 characters.', category='error')
        elif len(password) < 6:
            flash('password must be at least 6 characters long.', category='error')
        else:
            new_user = users(first_name=first_name, last_name=last_name, username=username, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('You have been registered!', category='success')
            return redirect(url_for('login'))

    return render_template('register.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)