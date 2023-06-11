from flask import Flask,request,jsonify
import sqlite3
from verificaciones import validar_admin,verificacion_company_api_key

#EDITAR UNO DE LA TABLA LOCATION
def editlocation(id):
    info = request.get_json()
    api_key = verificacion_company_api_key(info['company_api_key'])
    if api_key == True:
        conn = sqlite3.connect('DB/database.db')
        cursor = conn.cursor()
        query = """UPDATE location SET company_id = ?, location_name = ?, 
                    location_country = ?, location_city = ?, location_meta = ?
                    WHERE location_id = """+id+""" AND company_id = (
                        SELECT company_id FROM company WHERE company_api_key = """+info['company_api_key']+"""
                        );"""
        resultado = cursor.execute(query,(info['company_id'],info['location_name'],
                                info['location_country'],info['location_city'],info['location_meta']))
        row_affected = resultado.rowcount
        conn.commit()
        conn.close()
        if row_affected > 0:
            return jsonify({'status':'ready',
                        "message":"Registro modificado."})
        else:
            return jsonify({'status':'fail',
                        "message":"Ningun registro fue modificado."})
    else:
        return jsonify({'status':'fail',
                        "message":"El company_api_key y el id de la compañia no tienen relación entre si."})
        
def editsensor(id):
    info = request.get_json()
    api_key = verificacion_company_api_key(info['company_api_key'])
    if api_key == True:
        conn = sqlite3.connect('DB/database.db')
        cursor = conn.cursor()
        query = """UPDATE sensor SET location_id = ?, sensor_name = ?, 
                    sensor_category = ?, sensor_meta = ?, sensor_api_key = ?
                    WHERE sensor_id = """+id+""" AND location_id = (
                        SELECT location_id FROM location WHERE company_id = (
                            SELECT company_id FROM company WHERE company_api_key = """+info['company_api_key']+"""
                            )
                        );"""
        resultado = cursor.execute(query,(info['location_id'],info['sensor_name'],
                                info['sensor_category'],info['sensor_meta'],info['sensor_api_key']))
        row_affected = resultado.rowcount
        conn.commit()
        conn.close()
        if row_affected > 0:
            return jsonify({'status':'ready',
                        "message":"Registro modificado."})
        else:
            return jsonify({'status':'fail',
                        "message":"Ningun registro fue modificado."})
    else:
        return jsonify({'status':'fail',
                        "message":"El company_api_key y el id de la compañia no tienen relación entre si."})