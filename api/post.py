from flask import Flask,request,jsonify
import sqlite3
from verificaciones import validar_admin,verificacion_sensor_api_key

#CREAR COMPAÑIA CON USUARIO ADMIN
def new_compania():
    info = request.get_json()
    admin = validar_admin(info['username'], info['password'])
    if admin == True:
        conn = sqlite3.connect('DB/database.db')
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
def new_location():
    info = request.get_json()
    admin = validar_admin(info['username'], info['password'])
    if admin == True:
        conn = sqlite3.connect('DB/database.db')
        cursor = conn.cursor()
        query1 = """SELECT * FROM company WHERE company_id = {};""".format(info['company_id'])
        result1 = cursor.execute(query1).fetchall()
        if len(result1) > 0:
            query = """INSERT INTO Location (company_id, location_name, location_country, location_city, location_meta)
                        SELECT ?, ?, ?, ?, ?
                        WHERE NOT EXISTS (
                        SELECT 1 FROM location WHERE company_id = ? AND location_name = ?);"""
            result = cursor.execute(query,(info['company_id'],info['location_name'],info['location_country'],
                                        info['location_city'] ,info['location_meta'],info['company_id'],
                                        info['location_name']))
        else:
            return jsonify({'status':'fail',
                            "message":"Compañia {} no existe en su modelo.".format(info['company_id'])})
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
def new_sensor():
    info = request.get_json()
    admin = validar_admin(info['username'], info['password'])
    if admin == True:
        conn = sqlite3.connect('DB/database.db')
        cursor = conn.cursor()
        query1 = """SELECT * FROM location WHERE location_id = {};""".format(info['location_id'])
        result1 = cursor.execute(query1).fetchall()
        if len(result1) > 0:
            query = """INSERT INTO sensor(location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
                        SELECT ?, ?, ?, ?, ?
                        WHERE NOT EXISTS (
                        SELECT 1 FROM sensor WHERE location_id = ? AND sensor_name = ?);"""
            result = cursor.execute(query,(info['location_id'],info['sensor_name'],info['sensor_category'],info['sensor_meta']
                            ,info['sensor_api_key'],info['location_id'],info['sensor_name']))
        else:
            return jsonify({'status':'fail',
                            "message":"Localización {} no existe en su modelo.".format(info['location_id'])})
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
    
#ENVIAR SENSOR_DATA
def sensordata():
    info = request.get_json()
    api_key = verificacion_sensor_api_key(info['sensor_api_key'])
    if api_key == True:
        conn = sqlite3.connect('DB/database.db')
        cursor = conn.cursor()
        query = """INSERT INTO  ;"""
        




    return 'HOLA'