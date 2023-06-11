from flask import Flask,request,jsonify
from flask_login import login_required, LoginManager, login_user
import sqlite3
from api.post import new_compania,new_location,new_sensor,sensordata
from api.get import getall,getone
from api.put import editlocation,editsensor
from api.delete import deletelocation,deletesensor

app = Flask(__name__)

#CREAR COMPAÑIA CON USUARIO ADMIN
@app.route('/api/v1/admin/new_compania', methods=['POST'])
def init_admin_new_compania():
   return new_compania()

#CREAR LUGAR CON USUARIO ADMIN
@app.route('/api/v1/admin/new_location', methods=['POST'])
def init_admin_new_location():
   return new_location()

#CREAR SENSOR CON USUARIO ADMIN
@app.route('/api/v1/admin/new_sensor', methods=['POST'])
def init_admin_new_sensor():
    return new_sensor()

#MOSTRAR TODO DE UNA TABLA
@app.route('/api/getall/<tabla>&company_api_key=<company_api_key>', methods=['GET'])
def init_getall(tabla,company_api_key):
    return getall(tabla,company_api_key)

#MOSTRAR UNO DE UNA TABLA
@app.route('/api/getone/<tabla>&id=<id>&company_api_key=<company_api_key>', methods=['GET'])
def init_getone(tabla, id, company_api_key):
    return getone(tabla, id, company_api_key)

#EDITAR UNO DE LA TABLA LOCATION
@app.route('/api/edit/location/<id>', methods=['PUT'])
def init_edit_location(id):
    return editlocation(id)

#EDITAR UNO DE LA TABLA SENSOR
@app.route('/api/edit/sensor/<id>', methods=['PUT'])
def init_edit_sensor(id):
    return editsensor(id)

#ELIMINAR UNO DE LA TABLA LOCATION
@app.route('/api/delete/location/<id>&company_api_key=<company_api_key>', methods=['DELETE'])
def init_delete_location(id,company_api_key):
    return deletelocation(id,company_api_key)

#ELIMINAR UNO DE LA TABLA SENSOR
@app.route('/api/delete/sensor/<id>&company_api_key=<company_api_key>', methods=['DELETE'])
def init_delete_sensor(id,company_api_key):
    return deletesensor(id,company_api_key)

#ENVIAR SENSOR_DATA
@app.route('/api/v1/sensor_data/', methods=['POST'])
def init_sensor_data():
    return sensordata()



@app.route('/login', methods=['POST'])
def login():
    info = request.get_json()
    username = info['username']
    password = info['password']
    print(username)
    print(password)
    conn = sqlite3.connect('DB/database.db')
    cursor = conn.cursor()
    statement = "select * from admin where username = ?"
    if cursor.execute(statement, [username]) is not None:
        rows = cursor.fetchall()
        print(rows)
        return jsonify({"message":"Admin already exist"})




#ENVÍO DE DATA DE SENSOR
#@app.route('/api/v1/sensor_data', methods=['POST'])
#def sensor_data():
#    info = request.get_json()
#    sensor_api_key = authorization_sensor(info['api_key'])
#    if sensor_api_key == True:
#        conn = sqlite3.connect('DB/database.db')
#        cursor = conn.cursor()
#        sensor_info = (info['json_data'][],info['json_data'][],info['json_data'][],info['json_data'][])
#        query = """
#               """





#   return 'Hola'

if __name__ == '__main__':
    app.run(debug=True)