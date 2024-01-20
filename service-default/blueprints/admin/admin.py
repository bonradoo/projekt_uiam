from flask import Blueprint, render_template, redirect, url_for, jsonify, request, session
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
import pyodbc
import requests

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
URI = "mongodb+srv://vsc:vsc@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority"

def connect_to_sql():
    server = '34.116.156.230'
    database = 'uiam'
    username = 'sqlserver'
    password = 'sqlserver'
    cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return cnxn

def insert_rfid_data(rfid_tag, reader_id, timestamp):
    cnxn = connect_to_sql()
    cursor = cnxn.cursor()
    cursor.execute('INSERT INTO RFID_Table (RFID_Tag, Reader_ID, Timestamp) VALUES (?, ?, ?)', rfid_tag, reader_id, timestamp)
    cnxn.commit()
    cursor.close()
    cnxn.close()

def select_rfid_data():
    cnxn = connect_to_sql()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM RFID_Table')
    data = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return data

@admin_bp.route('/', methods=['GET'])
def admin():
    return render_template('admin.html')

@admin_bp.route('/weather', methods=['GET'])
def weather():
    lat = 52.2297
    lon = 21.0122
    api = '944381399cf36c796b7f3ac37a3dcd76'
    OWA = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api}'
    weather = requests.get(OWA).json()
    return render_template('admin_weather.html', weather_json=weather)

@admin_bp.route('/workers', methods=['GET'])
def workers():
    client = MongoClient(URI)
    db = client.main
    workers = list(db.user_collection.find({"role": "worker"}))
    for worker in workers:
        jobs = list(db.work_collection.find({"worker": worker["_id"]}))
        worker["jobs"] = jobs
    
    return render_template('admin_workers.html', workers=workers)

@admin_bp.route('/machines', methods=['GET'])
def machines():
    # Ogólne informacje
    try:
        machines_data = MongoClient(URI).main.machines_collection
    except Exception as e:
        return jsonify({'message': e})
    try:
        machines = list(machines_data.find())
    except Exception as e:
        return jsonify({'message': e})
    
    # Lokalizacja
    try:
        rfid = select_rfid_data()
        for machine in machines:
            for element in rfid:
                if machine['rfid'] == element[1]:
                    machine['location'] =  element[2]
            if 'location' not in machine:
                machine['location'] = 'Nieznana'
                
    except Exception as e:
        return jsonify({'message': e})

    # Stan maszyny

    
    return render_template('admin_machines.html', machines=machines)

@admin_bp.route('/work', methods=['GET'])
def work():
    try:
        user_data = MongoClient(URI).main.user_collection
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        workers = user_data.find({'role': 'worker'})
    except Exception as e:
        return jsonify({'message': e})

    return render_template('admin_work.html', workers=workers)

@admin_bp.route('/add_work', methods=['POST'])
def add_work():
    try:
        work_data = MongoClient(URI).main.work_collection
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        worker = request.form.get('worker')
        worker_id = ObjectId(MongoClient(URI).main.user_collection.find_one({'login': worker})['_id'])
        work_name = request.form.get('work_name')
        work_desc = request.form.get('work_desc')
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        to_insert = {
            'worker': worker_id,
            'work_name': work_name,
            'work_desc': work_desc,
            'active': True,
            'done': False,
            'machines': []
        }

        work_data.insert_one(to_insert)
    except Exception as e:
        return jsonify({'message': e})

    return redirect(url_for('admin.work', message='Praca dodana pomyślnie'))

@admin_bp.route('/reports', methods=['GET'])
def reports():
    try:
        logs = MongoClient(URI).main.logs_collection
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        reports_data = list(logs.find())
    except Exception as e:
        return jsonify({'message': e})
    
    return render_template('admin_reports.html', reports_data=reports_data)

# MANAGEMENT

@admin_bp.route('/management', methods=['GET'])
def management():
    try:
        user_data = MongoClient(URI).main.user_collection
        users = list(user_data.find())
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        machines_data = MongoClient(URI).main.machines_collection
        machines = list(machines_data.find())
    except Exception as e:
        return jsonify({'message': e})
    
    return render_template('admin_management.html', users=users, machines=machines)

@admin_bp.route('/delete_user/<login>', methods=['POST'])
def delete_user(login):
    client = MongoClient(URI)
    db = client.main
    # Delete the user with the given login, only if they are a worker
    db.user_collection.delete_one({"login": login, "role": "worker"})
    return redirect(url_for('admin.management'))  # Redirect to the page displaying users

@admin_bp.route('/delete_machine/<id>', methods=['POST'])
def delete_machine(id):
    client = MongoClient(URI)
    db = client.main
    db.machines_collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('admin.management'))  # Redirect to the machine listing page
