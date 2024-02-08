from datetime import datetime
from flask_login import UserMixin
from casjob import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=True)
    lastname = db.Column(db.String(20), unique=False, nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    skill_type = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(300), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    years_of_experience = db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy=True)
    applications = db.relationship('JobApplication', backref='applicant', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    skill_type = db.Column(db.String(50), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"JobApplication('{self.user_id}', '{self.post_id}', '{self.date_applied}')"
