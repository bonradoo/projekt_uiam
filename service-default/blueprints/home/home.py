from flask import Blueprint, render_template, redirect, url_for, session, request
from pymongo import MongoClient

home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static')

URI = "mongodb+srv://vsc:vsc@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority"

@home_bp.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@home_bp.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
        client = MongoClient(URI)
        db = client.main
        contact_collection = db.contact_collection
        contact_collection.insert_one({'name':name, 'email':email, 'message':message, 'status':'unread'})
        client.close()
    except Exception as e:
        print(e)
        error = 'There was an error sending your message. Please try again.'
        return render_template('home.html', error=error)
    
    return redirect(url_for('home.home'))