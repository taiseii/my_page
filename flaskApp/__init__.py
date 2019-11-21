import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from flaskApp.models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SERCRET_KEY')) #use os.environ.get in production
                           
app.config['SQLALCHEMY_DATABASE_URI'] = str(os.environ.get('SQLALCHEMY_DATABASE_URI'))
db = SQLAlchemy(app)

# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Post=Post)


bcrypt = Bcrypt(app) # this is for hasing the password when we create the registration form!
login_manager = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

from flaskApp import routes
from flaskApp import dash_board
