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
        elif session['role'] == 'worker':
            return redirect(url_for('user.user'))
        
        return render_template('login.html', error="Seems like you don't have role assigned. Contact your administrator.")
    except Exception as e:
        print(e)
        error = 'There was an error logging you in. Please try again.'
        return render_template('login.html', error=error)

if __name__ == '__main__':
    pass
