from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from casjob.models import User
from flask_login import current_user

# List of skills
SKILLS = [
    'Mechanic', 'Electrician', 'Plumber', 'Carpenter', 'Welder',
    'Cleaner', 'Janitor', 'Housekeeper', 'Pool Cleaner',
    'Computer Technician', 'IT Support', 'Appliance Repair Technician',
    'Delivery Driver', 'Courier', 'Taxi/Uber Driver',
    'Event Staff', 'Caterer', 'Bartender', 'Waitstaff',
    'Gardener', 'Landscaper', 'Pool Maintenance',
    'Babysitter', 'Pet Sitter', 'Dog Walker',
    'Fitness Trainer', 'Yoga Instructor', 'Massage Therapist',
    'Graphic Designer', 'Photographer', 'Writer/job_description Creator',
    'Retail Sales Associate', 'Customer Service Representative'
]

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                           validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Try another!')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Try another!')

class LoginForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    
    password = PasswordField('Password',
                           validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    skill_type = SelectField('Skill Type', choices=[(skill, skill) for skill in SKILLS])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Try another!')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken. Try another!')
            
    def validate_phone_number(self, phone_number):
        if phone_number.data != current_user.phone_number:
            user = User.query.filter_by(phone_number=phone_number.data).first()
            if user:
                raise ValidationError('Email is taken. Try another!')

class PostJobForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    skill_type = SelectField('Skill Type', choices=[(skill, skill) for skill in SKILLS])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    submit = SubmitField('Post') 

class ApplicationForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit Application')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first!')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                           validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
