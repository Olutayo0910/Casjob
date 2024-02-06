from casjob import app, db
from casjob.models import User

def create_tables():
    # Use app context to work with the database
    with app.app_context():
        db.create_all()
    print('succesful')

create_tables()
