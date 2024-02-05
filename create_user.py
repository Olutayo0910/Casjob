from casjob import app, db
from casjob.models import User

def create_tables():
    # Use app context to work with the database
    with app.app_context():
        # Create tables
        db.create_all()

        # Your user creation logic
        new_user = User(
            firstname='John',
            lastname='Doe',
            username='john_doe',
            phone_number='1234567890',
            email='john.doe@example.com',
            password='your_password_here'
        )

        # Add user to the session
        db.session.add(new_user)

        # Commit changes to the database
        db.session.commit()

    print('Successful')

# Run the script
create_tables()
