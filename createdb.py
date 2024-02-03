from casjob import app, db
from casjob.models import User

def print_all_users():
    # Use app context to work with the database
    with app.app_context():
        # Query all users
        users = User.query.all()

        # Print each user
        for user in users:
            print(user)

if __name__ == "__main__":
    # Call the function to print all users
    print_all_users()
