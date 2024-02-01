from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = '48df99608259875f92817227bfe26e54'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from casjob import routes