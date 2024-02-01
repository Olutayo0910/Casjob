# your_script.py

from casjob import app, db
from casjob.models import User, Post

# Use app context to create the database tables
with app.app_context():
    user = User.query.all()
    print(user)