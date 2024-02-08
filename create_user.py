from casjob import app, db
from casjob.models import User
from werkzeug.security import generate_password_hash

def create_users():
    try:
        # Use app context to work with the database
        with app.app_context():
            # Create users
            for i in range(1, 21):
                username = f"user{i}"
                email = f"user{i}@example.com"
                firstname = f"User{i}"
                lastname = "Doe"
                phone_number = f"1234567{i:02d}"
                skill_type = "Electrician"  # You can change this as needed
                bio = f"Experienced electrician with {i} years of experience."
                password_hash = generate_password_hash("12345")

                # Create a new user
                new_user = User(
                    username=username,
                    email=email,
                    password=password_hash,
                    firstname=firstname,
                    lastname=lastname,
                    phone_number=phone_number,
                    skill_type=skill_type,
                    bio=bio,
                    years_of_experience=i
                )

                # Add user to the session
                db.session.add(new_user)

            # Commit changes to the database
            db.session.commit()

        print('Users created successfully.')
    except Exception as e:
        print(f'An error occurred: {e}')

# Run the script
create_users()
