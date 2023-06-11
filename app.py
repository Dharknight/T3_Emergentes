from flask import Flask,request,jsonify
from flask_login import login_required, LoginManager, login_user
import sqlite3
from db_init import create_tables

app = Flask(__name__)
login_manager_app=LoginManager(app)


@app.route('/login', methods=['POST'])
def login():
    info = request.get_json()
    username = info['username']
    password = info['password']
    print(username)
    print(password)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    statement = "select * from admin where username = ?"
    if cursor.execute(statement, [username]) is not None:
        rows = cursor.fetchall()
        print(rows)
        return jsonify({"message":"Admin already exist"})

#CREAR COMPAÑIA CON USUARIO ADMIN
@app.route('/api/v1/admin/new_compania', methods=['POST'])
def new_compania():
    info = request.get_json()
    admin = validar_admin(info['username'], info['password'])
    if admin == True:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = """INSERT INTO company (company_name, company_api_key)
                    SELECT ?, ?
                    WHERE NOT EXISTS (
                    SELECT 1 FROM company WHERE company_name = ?);"""
        result = cursor.execute(query,(info['company_name'], info['company_api_key'], info['company_name']))
        rows_affected = result.rowcount
        conn.commit()
        cursor.close()
        if rows_affected > 0:
            return jsonify({'status':'ready',
                            "message":"Compañia creada"})
        else:
            return jsonify({'status':'fail',
                            'message':'Compañia ya existente'})
    else:
         return jsonify({"mensaje": 'Credenciales no corresponden a un usuario admin'})

#CREAR LUGAR CON USUARIO ADMIN
@app.route('/api/v1/admin/new_location', methods=['POST'])
def new_location():
    info = request.get_json()
    admin= validar_admin(info['username'], info['password'])
    if admin == True:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = """INSERT INTO Location (company_id, location_name, location_country, location_city, location_meta)
                    SELECT ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                    SELECT 1 FROM location WHERE company_id = ? AND location_name = ?);"""
        result = cursor.execute(query,(info['company_id'],info['location_name'],info['location_country'],
                                       info['location_city'] ,info['location_meta'],info['company_id'],
                                       info['location_name']))
        rows_affected = result.rowcount
        conn.commit()
        cursor.close()
        if rows_affected > 0:
            return jsonify({'status':'ready',
                            "message":"Localización creada"})
        else:
            return jsonify({'status':'fail',
                            'message':'Localización ya existente asociada a la compañia {}'.format(info['company_id'])})
    else:
         return jsonify({"mensaje": 'Credenciales no corresponden a un usuario admin'})

#CREAR SENSOR CON USUARIO ADMIN
@app.route('/api/v1/admin/new_sensor', methods=['POST'])
def new_sensor():
    info = request.get_json()
    admin= validar_admin(info['username'], info['password'])
    if admin == True:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = """INSERT INTO sensor(location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
                    SELECT ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                    SELECT 1 FROM sensor WHERE location_id = ? AND sensor_name = ?);"""
        result = cursor.execute(query,(info['location_id'],info['sensor_name'],info['sensor_category'],info['sensor_meta']
                            ,info['sensor_api_key'],info['location_id'],info['sensor_name']))
        rows_affected = result.rowcount
        conn.commit()
        cursor.close()
        if rows_affected > 0:
            return jsonify({'status':'ready',
                            "message":"Sensor creada"})
        else:
            return jsonify({'status':'fail',
                            'message':'Sensor {} ya existente asociada a la localización {}'.format(info['sensor_name'],info['location_id'])})
    else:
         return jsonify({"mensaje": 'Credenciales no corresponden a un usuario admin'})







#FUNCIÓN PARA VALIDAR QUE LA OPERACIÓN LA HAGA UN USUARIO ADMIN
def validar_admin(username, password):
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()
    query = "select username, password from admin;"
    cursor.execute(query)
    record = cursor.fetchall()
    for i in record:
        if i[0] == username: 
            if i[1] == password:
                cursor.close()
                return True
    cursor.close()
    return False

if __name__ == '__main__':
    app.run(debug=True)