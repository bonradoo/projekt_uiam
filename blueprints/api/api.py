from pymongo.mongo_client import MongoClient
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
import datetime, pprint, json, hashlib
from pymongo.mongo_client import MongoClient
import bson
from bson.json_util import dumps

from blueprints.admin.admin import admin_bp

api_bp = Blueprint('api', __name__)
api_bp.register_blueprint(admin_bp, url_prefix='/admin')


URI = "mongodb+srv://vsc:vsc@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority"

# MISC
## ADD ADMIN

@api_bp.route('/add_admin')
def add_admin():
    name = 'Admin'
    surname = 'Adminowicz'
    login = 'admin'
    email = 'admin@admin.com'
    password = hashlib.sha256('admin'.encode()).hexdigest()
    role = 'admin'
    
    try:
        user_data = MongoClient(URI).main.user_collection
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        if user_data.find_one({'login': login}):
            return jsonify({'message': 'User already exists'})
    
        if user_data.find_one({'email': email}):
            return jsonify({'message': 'Email already exists'})
        
        to_insert = {
            'name': name,
            'surname': surname,
            'login': login,
            'email': email,
            'password': password,
            'role': role
        }

        try:
            user_data.insert_one(to_insert)
        except Exception as e:
            return jsonify({'message': e})
        
    except Exception as e:
        return jsonify({'message': e})
    return jsonify({'message': 'User added successfully'})



# ADMIN
## ADD

@api_bp.route('/add_user', methods=['POST'])
def add_user():
    try:
        name = request.form.get('name')
        surname = request.form.get('surname')
        login = request.form.get('login')
        password = str(request.form.get('password'))
        role = request.form.get('role')

        if request.form.get('email'):
            email = request.form.get('email')
        else:
            email = None
    except Exception as e:
        return jsonify({'message': e})

    try:
        user_data = MongoClient(URI).main.user_collection
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        if user_data.find_one({'login': login}):
            return redirect(url_for('admin.management', error='Użytkownij już istnieje'))
    
        if email is not None and user_data.find_one({'email': email}):
            return redirect(url_for('admin.management', error='Email już istnieje'))
    except Exception as e:
        return redirect(url_for('admin.management', error=e))
    
    try:
        to_insert = {
            'name': name,
            'surname': surname,
            'login': login,
            'email': email,
            'password': hashlib.sha256(password.encode()).hexdigest(),
            'role': role
        }
        user_data.insert_one(to_insert)
    except Exception as e:
        return jsonify({'message': e})
    
    return redirect(url_for('admin.management', success='Użytkownik dodany pomyślnie'))

@api_bp.route('/add_machine', methods=['POST'])
def add_machine():
    try:
        company = request.form.get('company')
        model = request.form.get('model')
        number = request.form.get('number')
        serial_number = request.form.get('serial_number')
        workhours = request.form.get('workhours')
        machine_type = request.form.get('type')
    except Exception as e:
        return redirect(url_for('admin.management', error=e))
    
    try:
        machines_data = MongoClient(URI).main.machines_collection
    except Exception as e:
        return jsonify({'message': e})
    
    
    if machines_data.find_one({'serial_number': serial_number}):
        return redirect(url_for('admin.management', error='Maszyna o podanym numerze seryjnym już istnieje'))

    try:
        to_insert = {
            'company': company,
            'model': model,
            'number': number,
            'serial_number': serial_number,
            'workhours': workhours,
            'type': machine_type
        }
        machines_data.insert_one(to_insert)
    except Exception as e:
        return redirect(url_for('admin.management', error=e))
    
    return redirect(url_for('admin.management', success='Maszyna dodana pomyślnie'))


@api_bp.route('/add_work', methods=['POST'])
def add_work():
    pass


## ASSIGN

@api_bp.route('/assign_worker_work', methods=['POST'])
def assign_worker_work():
    pass

@api_bp.route('/assign_worker_machine', methods=['POST'])
def assign_worker_machine():
    pass


## GET

@api_bp.route('/get_weather', methods=['GET'])
def get_weather():
    pass

@api_bp.route('/get_worker_data', methods=['GET'])
def get_worker_data():
    pass

@api_bp.route('/get_machine_data', methods=['GET'])
def get_machine_data():
    pass

@api_bp.route('/get_workers', methods=['GET'])
def get_workers():
    try:
        user_data = MongoClient(URI).main.user_collection
        users = list(user_data.find())
    except Exception as e:
        return jsonify({'message': e})

    return redirect(url_for('admin.management'), users=users)

@api_bp.route('/get_machines', methods=['GET'])
def get_machines():
    pass


# USER
## ADD

@api_bp.route('/add_fuel', methods=['POST'])
def add_fuel():
    pass

@api_bp.route('/add_start_report', methods=['POST'])
def add_start_report():
    pass

@api_bp.route('/add_end_report', methods=['POST'])
def add_end_report():
    pass
