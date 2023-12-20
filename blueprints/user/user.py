from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session
import datetime, pprint, json, hashlib
from bson import ObjectId
from pymongo.mongo_client import MongoClient

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')
URI = "mongodb+srv://vsc:vsc@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority"

@user_bp.route('/', methods=['GET'])
def user():
    return render_template('user.html')

@user_bp.route('/report', methods=['GET'])
def report():
    return render_template('user_report.html')

@user_bp.route('/add_report', methods=['POST'])
def add_raport():
    machine = request.form.get('machine')
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fuel_state = request.form.get('fuel_state')
    machine_hours = request.form.get('machine_hours')
    oc_done = request.form.get('oc_done')

    try:
        logs = MongoClient(URI).main.logs_collection
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        name = session['name']
        surname = session['surname']
        user = name + ' ' + surname
    except Exception as e:
        return jsonify({'message': e})
    
    try:
        to_insert = {
            'user': user,
            'machine': machine,
            'date_time': date_time,
            'fuel_state': fuel_state,
            'machine_hours': machine_hours,
            'oc_done': oc_done
        }

        logs.insert_one(to_insert)
    except Exception as e:
        return jsonify({'message': e})

    return redirect(url_for('user.user', message='Raport dodany pomyślnie'))


from flask import jsonify, render_template, session
from pymongo import MongoClient

@user_bp.route('/work', methods=['GET'])
def work():
    work_to_do = []
    try:
        work_data = MongoClient(URI).main.work_collection
    except Exception as e:
        return jsonify({'message': str(e)})

    try:
        # Assuming 'user_id' is stored in session upon login
        user = session['login']
        if not user:
            return jsonify({'message': 'User not logged in'}), 401

        # Adjust this query based on your database schema
        work_to_do = work_data.find({'worker': user, 'active': True})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

    # Convert work_to_do to a list and pass it to the template
    work_to_do_list = list(work_to_do)
    return render_template('user_work.html', work_to_do=work_to_do_list)


@user_bp.route('/add_work', methods=['POST'])
def add_work():
    try:
        work_id = request.form.get('work')
    except Exception as e:
        return jsonify({'message': str(e)})

    try:
        work_logs_data = MongoClient(URI).main.work_logs_collection
        to_insert = {
            'work_id': ObjectId(work_id),
            'date_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        work_logs_data.insert_one(to_insert)
    except Exception as e:
        return jsonify({'message': str(e)})

    try:
        work_data = MongoClient(URI).main.work_collection
        # Assuming work_id is stored as a string. If it's an ObjectId, convert it appropriately
        work_data.update_one({'_id': ObjectId(work_id)}, {'$set': {'active': False}})
    except Exception as e:
        return jsonify({'message': str(e)})

    return render_template('user.html', message='Praca wybrana pomyślnie')

