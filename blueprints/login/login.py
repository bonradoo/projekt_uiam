from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from google.cloud import datastore
import hashlib
from pymongo.mongo_client import MongoClient

from blueprints.api.api import api_bp
login_bp = Blueprint('login', __name__, template_folder='templates', static_folder='static')
login_bp.register_blueprint(api_bp, url_prefix='/api')

URI = "mongodb+srv://vsc:vsc@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority"

@login_bp.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.home'))

@login_bp.route('/verify_login', methods=['POST'])
def verify_login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
    except Exception as e:
        print(e)
        error = 'There was an error retreiving your information. Please try again.'
        return render_template('login.html', error=error)

    try:
        user_collection = MongoClient(URI).main.user_collection
        user = user_collection.find_one({"login":username})
        if user == None:
            error = 'Username does not exist. Please try again.'
            return render_template('login.html', error=error)
        
        if user['password'] != hashlib.sha256(password.encode()).hexdigest():
            error = 'Incorrect password. Please try again.'
            return render_template('login.html', error=error)

        session['login'] = username
        session['name'] = user['name']
        session['surname'] = user['surname']
        session['email'] = user['email']
        session['role'] = user['role']

        if session['role'] == 'admin':
            return redirect(url_for('admin.admin'))
        elif session['role'] == 'user':
            return redirect(url_for('user.user'))
        
        return render_template('login.html', error="Seems like you don't have role assigned. Contact your administrator.")
    except Exception as e:
        print(e)
        error = 'There was an error logging you in. Please try again.'
        return render_template('login.html', error=error)


    
# @login_bp.route('/signup')
# def signup():
#     return render_template('signup.html')

# @login_bp.route('/create_user', methods=['POST'])
# def create_user():
#     try:
#         name = request.form.get('name')
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         birth_date = request.form.get('birth_date')
#     except Exception as e:
#         print(e)
#         return redirect(url_for('login.login'), error=e)
    
#     try:
#         user_data = MongoClient(URI).main.user_collection
#     except Exception as e:
#         print(e)
#         return redirect(url_for('login.login'), error=e)
    
#     if user_data.find_one({"username":username}) != None:
#         return redirect(url_for('login.login'), error="User already exists")

#     if user_data.find_one({"email":email}) != None:
#         return redirect(url_for('login.login'), error="Email already exists")

#     to_insert = {
#         "name":name,
#         "username":username,
#         "email":email,
#         "hashed_password":hashlib.sha256(password.encode()).hexdigest(),
#         "watchlist":[],
#         "reviews":[],
#         "streaming_services":[],
#         "preferences":[],
#         "birth_date":birth_date,
#         "child_to":[],
#         "parent_of":[]
#     }

#     try:
#         user_data.insert_one(to_insert)
#     except Exception as e:
#         print(e)
#         return redirect(url_for('login.login'), error=e)

#     return redirect(url_for('login.login'), message="Account created successfully. Please log in.")
    

if __name__ == '__main__':
    pass
