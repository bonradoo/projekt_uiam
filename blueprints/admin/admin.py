from flask import Blueprint, render_template, redirect, url_for, jsonify, request, session
import datetime, pprint, json, hashlib
from pymongo.mongo_client import MongoClient

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')
URI = "mongodb+srv://vsc:vsc@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority"

@admin_bp.route('/', methods=['GET'])
def admin():
    return render_template('admin.html')

@admin_bp.route('/workers', methods=['GET'])
def workers():
    return render_template('admin_workers.html')

@admin_bp.route('/machines', methods=['GET'])
def machines():
    return render_template('admin_machines.html')

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
        work_name = request.form.get('work_name')
        work_desc = request.form.get('work_desc')
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        to_insert = {
            'worker': worker,
            'work_name': work_name,
            'work_desc': work_desc,
            'active': True
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

@admin_bp.route('/management', methods=['GET'])
def management():
    return render_template('admin_management.html')