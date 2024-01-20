from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import pyodbc
import hashlib
app = Flask(__name__)

URI = 'mongodb+srv://admin:admin@production.sz8f5n1.mongodb.net/?retryWrites=true&w=majority'

def connect_to_db(uri):
    client = MongoClient(uri)
    db = client.main
    return db

def connect_to_sql():
    server = '34.116.156.230'
    database = 'uiam'
    username = 'sqlserver'
    password = 'sqlserver'
    cnxn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return cnxn

def select_rfid_data():
    cnxn = connect_to_sql()
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM RFID_Table')
    data = cursor.fetchall()
    cursor.close()
    cnxn.close()
    return data

def insert_rfid_data(rfid_tag, reader_id, timestamp):
    cnxn = connect_to_sql()
    cursor = cnxn.cursor()
    cursor.execute('INSERT INTO RFID_Table (RFID_Tag, Reader_ID, Timestamp) VALUES (?, ?, ?)', rfid_tag, reader_id, timestamp)
    cnxn.commit()
    cursor.close()
    cnxn.close()

def create_rfid_table():
    cnxn = connect_to_sql()
    cursor = cnxn.cursor()
    cursor.execute('''
        CREATE TABLE RFID_Table (
            ID int PRIMARY KEY IDENTITY,
            RFID_Tag nvarchar(50),
            Reader_ID nvarchar(50),
            Timestamp datetime
        )
    ''')
    cnxn.commit()
    cursor.close()
    cnxn.close()


@app.route('/')
def hello_world():
    api_test = 'Welcome to the API!'
    return api_test

# Example 'add_worker/John/Doe/john.doe@domain/worker/123'
@app.route('/add_worker/<name>/<surname>/<email>/<role>/<password>')
def add(name, surname, email, role, password):
    data = {
        'name': name,
        'surname': surname,
        'email': email,
        'role': role,
        'hashed_password': hashlib.sha256(password.encode()).hexdigest()
    }
    try:
        db = connect_to_db(URI)
        db.user_collection.insert_one(data)
        return 'Success!', 200
    except:
        return 'Error!', 400

# Example 'add_machine/John/plough/123'
@app.route('/add_machine/<name>/<type>/<number>/<rfid_tag>')
def add_machine(name, type, number, rfid_tag):
    data = {
        'name': name,
        'type': type,
        'number': number,
        'insert_date': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        'rfid_tag': rfid_tag
    }
    try:
        db = connect_to_db(URI)
        db.machines_collection.insert_one(data)
        return 'Success!', 200
    except:
        return 'Error!', 400

@app.route('/add_rfid/<rfid_tag>/<reader_id>')
def add_rfid(rfid_tag, reader_id):
    print(rfid_tag, reader_id, str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    try:
        insert_rfid_data(rfid_tag, reader_id, str(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        return 'Success!', 200
    except Exception as e:
        print(e)
        return 'Error!', 400

@app.route('/get_rfid')
def get_rfid():
    try:
        data = select_rfid_data()
        result = []
        for element in data:
            result.append({
                'rfid_tag': element[1],
                'reader_id': element[2],
                'timestamp': element[3]
            })
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return 'Error!', 400

if __name__ == '__main__':
    # insert_rfid_data('0003', 'P001', '2023-01-01 00:00:00')
    app.run(debug=True)
