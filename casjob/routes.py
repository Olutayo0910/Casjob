import os
import secrets
from PIL import Image
from flask import jsonify, render_template, url_for, redirect, flash, redirect, request, abort
from casjob import app, db, bcrypt
from casjob.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostJobForm, ApplicationForm
from casjob.models import User, Post, JobApplication
from random import shuffle
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from . import mail


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/hires')
def hire():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    skills = [
    'Mechanic', 'Electrician', 'Plumber', 'Carpenter', 'Welder',
    'Cleaner', 'Janitor', 'Housekeeper', 'Pool Cleaner',
    'Computer Technician', 'IT Support', 'Appliance Repair Technician',
    'Delivery Driver', 'Courier', 'Taxi/Uber Driver',
    'Event Staff', 'Caterer', 'Bartender', 'Waitstaff',
    'Gardener', 'Landscaper', 'Pool Maintenance',
    'Babysitter', 'Pet Sitter', 'Dog Walker',
    'Fitness Trainer', 'Yoga Instructor', 'Massage Therapist',
    'Graphic Designer', 'Photographer', 'Writer',
    'Retail Sales Associate', 'Customer Service Representative'
]
    hires = User.query.paginate(page=page, per_page=per_page)
    shuffled_items = hires.items
    shuffle(shuffled_items)
    return render_template('hires.html', title='Hires', hires=hires, skills=skills)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('job_tank'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account { form.username.data } Created Succesfully, you can now log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('job_tank'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('job_tank'))
        else:
            flash(f'Login Unsuccesfully. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.skill_type = form.skill_type.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_job_post():
    form = PostJobForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, job_description=form.job_description.data, skill_type=form.skill_type.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your job has been created!', 'success')
        return redirect(url_for('job_tank'))
    return render_template('create_job.html', title='Post Jobs', form=form, legend='New Job Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('job.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_job_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostJobForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.skill_type = request.form['skill_type']
        post.job_description = form.job_description.data
        db.session.commit()
        flash('Your job has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.skill_type.data = post.skill_type
        form.job_description.data = post.job_description
    return render_template('create_job.html', title='Update Job', form=form, legend='Update Job Post')

# delete job post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_job_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your job has been deleted', 'success')
    return redirect(url_for('job_tank'))

# view all the job post
@app.route('/jobs')
def job_tank():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('job_tank.html', posts=posts)

@app.route('/user/<username>')
def user_job_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_job_posts.html', posts=posts, user=user)

@app.route('/apply/<int:post_id>', methods=['GET', 'POST'])
@login_required
def apply(post_id):
    post = Post.query.get_or_404(post_id)
    form = ApplicationForm()
    if form.validate_on_submit():
        application = JobApplication(message=form.message.data, post_id=post_id, applicant=current_user)
        db.session.add(application)
        db.session.commit()
        flash('Your application has been sent!', 'success')
        
        # Send email to the poster
        if post.author.email:
            send_email_to_poster(post.author.email, current_user.email)
        
        return redirect(url_for('confirmation'))
    return render_template('apply.html', title='Apply', form=form)

def send_email_to_poster(poster_email, applicant_email):
    subject = 'New Application for your Job Post'
    body = f'Hello,\n\nYou have received a new job application from {applicant_email}.\n\nBest regards,\nYour Application System'
    msg = Message(subject, recipients=[poster_email], body=body)
    mail.send(msg)
