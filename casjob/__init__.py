import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = '48df99608259875f92817227bfe26e54'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Configure Flask-Mail for Gmail SMTP with SSL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'demoolutayo@gmail.com'
app.config['MAIL_PASSWORD'] = '2Omatoes#'

mail = Mail(app)

# Import routes after configuring extensions
from casjob import routes
