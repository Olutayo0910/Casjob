from flask import jsonify, render_template, url_for, redirect, flash, redirect
from casjob import app
from casjob.forms import RegistrationForm, LoginForm
from casjob.models import User, Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account { form.username.data } Created Succesfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Account log in Succesfully!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


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
