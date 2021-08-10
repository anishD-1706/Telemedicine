from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.static_folder = 'static'
# for protecting against forgery attacks , cookies
app.config['SECRET_KEY'] = '0f765fa34fc8fac9081b3fd9fc2f6a95'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app) #database Instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_blog import routes
