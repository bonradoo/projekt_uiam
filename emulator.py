import pyodbc
import datetime

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

def main():
    print('[1] Pługownica PLG1234')
    print('[2] Cysternos CSR0023')
    print('[3] Siewnix SWI1234')
    rfid_input = int(input('RFID: '))

    if rfid_input == 1:
        rfid_tag_input = 'P0001'
    elif rfid_input == 2:
        rfid_tag_input = 'C0001'
    elif rfid_input == 3:
        rfid_tag_input = 'S0001'
    else:
        print('Niepoprawny numer RFID')
        exit()

    print('[1] Park maszynowy')
    print('[2] Serwis')
    print('[3] Pole 1')
    print('[4] Pole 2')
    reader_id = int(input('Reader ID: '))

    if reader_id == 1:
        reader_id_input = 'Park maszynowy'
    elif reader_id == 2:
        reader_id_input = 'Serwis'
    elif reader_id == 3:
        reader_id_input = 'Pole 1'
    elif reader_id == 4:
        reader_id_input = 'Pole 2'
    else:
        print('Niepoprawny numer Reader ID')
        exit()

    timestamp_input = datetime.datetime.strptime(input('Timestamp DDMMYYYY HHMMSS: '), '%d%m%Y %H%M%S')
    
    insert_rfid_data(rfid_tag_input, reader_id_input, timestamp_input)

if __name__ == '__main__':
    main()