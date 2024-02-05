import os
import secrets
from PIL import Image
from flask import jsonify, render_template, url_for, redirect, flash, redirect, request
from casjob import app, db, bcrypt
from casjob.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostJobForm
from casjob.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Dummy data for demonstration purposes
categories = [
  {
    "id": 1,
    "name": "Construction and Trades",
    "subcategories": ["Carpentry", "Plumbing", "Electrical", "Painting"]
  },
  {
    "id": 2,
    "name": "Information Technology",
    "subcategories": ["Web Development", "Mobile App Development", "Database Administration", "IT Support"]
  },
]


hires = [
    {
        "id": 1,
        "category_id": 1,
        "hire_id": 1,
        "name":"John Doe", 
        "category": "Construction and Trades",
        "subcategory": "Carpentry",
        "profile_picture": "images/man.png",
        "description": "Experienced carpenter dedicated to transforming spaces with precision and passion, crafting exceptional woodwork that stands the test of time",
        "experience": 4
    },
    {
        "id": 2,
        "category_id": 2,
        "hire_id": 2,
        "name":"Jane Smith",
        "category": "Construction and Trades",
        "subcategory": "Electrical",
        "profile_picture": "images/bussiness-man.png",
        "description": "I am an experienced electrician, specializing in precision wiring and delivering top-notch electrical solutions. Committed to illuminating spaces with expertise and ensuring efficient power solutions.",
        "experience": 6
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', hires=hires)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
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
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your job has been created!', 'success')
        return redirect(url_for('job_tank'))
    return render_template('create_job.html', title='Post Jobs', form=form)

@app.route('/jobs')
def job_tank():
    posts = Post.query.all()
    return render_template('job_tank.html', posts=posts)

# Endpoint to fetch all categories with subcategories
@app.route('/categories', methods=['GET'])
def get_all_categories():
    return jsonify(categories)

# Endpoint to fetch information about a specific category with subcategories
@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = next((cat for cat in categories if cat['id'] == category_id), None)
    if category:
        return jsonify(category)
    else:
        return jsonify({"error": "Category not found"}), 404
        
# Endpoint to fetch all subcategories
@app.route('/subcategories', methods=['GET'])
def get_all_subcategories():
    all_subcategories = [subcategory for category in categories for subcategory in category['subcategories']]
    return jsonify(all_subcategories)

# Endpoint to fetch information about hires under a specific category with subcategories
@app.route('/category/<int:category_id>/hires', methods=['GET'])
def get_category_hires(category_id):
    hires_in_category = [hire for hire in hires if hire['category_id'] == category_id]
    return jsonify(hires_in_category)

# Endpoint to fetch all hires with subcategories
@app.route('/hires', methods=['GET'])
def get_all_hires():
    return jsonify(hires)

# Endpoint to fetch hires in each subcategory
@app.route('/subcategory/<string:subcategory_name>/hires', methods=['GET'])
def get_hires_in_subcategory(subcategory_name):
    hires_in_subcategory = [hire for hire in hires if hire['subcategory'] == subcategory_name]
    return jsonify(hires_in_subcategory)

# Endpoint to fetch information about a specific hire
@app.route('/hire/<int:hire_id>', methods=['GET'])
def get_hire(hire_id):
    hire = next((h for h in hires if h['id'] == hire_id), None)
    if hire:
        return jsonify(hire)
    else:
        return jsonify({"error": "Hire not found"}), 404
