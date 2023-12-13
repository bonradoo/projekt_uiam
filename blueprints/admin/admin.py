from flask import Blueprint, render_template, redirect, url_for, jsonify
from pymongo.mongo_client import MongoClient

URI = "mongodb+srv://vsc:vsc@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority"

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

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
    return render_template('admin_work.html')

@admin_bp.route('/reports', methods=['GET'])
def reports():
    return render_template('admin_reports.html')

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