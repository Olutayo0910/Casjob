from casjob import app, db
from casjob.models import User

def recreate_tables():
    # Use app context to work with the database
    with app.app_context():
        # Drop existing tables
        db.drop_all()

        # Create tables
        db.create_all()

        # Create a new user
        new_user = User(
            firstname='John',
            lastname='Doe',
            username='john_doe',
            phone_number='1234567890',
            email='john.doe@example.com',
            password='your_password_here',
            bio='Some bio information here'
            
        )

        # Add user to the session
        db.session.add(new_user)

        # Commit changes to the database
        db.session.commit()

    print('Successful')

# Run the script
recreate_tables()
