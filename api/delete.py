from flask import Flask,request,jsonify
import sqlite3
from verificaciones import validar_admin,verificacion_company_api_key

#ELIMINAR UNO DE LA TABLA LOCATION
def deletelocation(id,company_api_key):
    api_key = verificacion_company_api_key(company_api_key)
    if api_key == True:
        conn = sqlite3.connect('DB/database.db')
        cursor = conn.cursor()
        query = """DELETE FROM location 
                    WHERE company_id = (
                    SELECT company_id FROM company WHERE company_api_key = {} ) AND location_id = {};""".format(company_api_key, id)
        resultado = cursor.execute(query)
        row_affected = resultado.rowcount
        conn.commit()
        conn.close()
        if row_affected > 0:
            return jsonify({'status':'ready',
                        "message":"Registro eliminado."})
        else:
            return jsonify({'status':'fail',
                        "message":"No se encontró registro alguno para ser eliminado."})
    else:
        return jsonify({'status':'fail',
                        "message":"El company_api_key y el id de la compañia no tienen relación entre si."})

#ELIMINAR UNO DE LA TABLA SENSOR
def deletesensor(id,company_api_key):
    api_key = verificacion_company_api_key(company_api_key)
    if api_key == True:
        conn = sqlite3.connect('DB/database.db')
        cursor = conn.cursor()
        query = """DELETE FROM sensor 
                    WHERE sensor_id = {} AND location_id = (
                    SELECT location_id FROM location WHERE company_id = ( 
                        SELECT company_id FROM company WHERE company_api_key = {} ));""".format(id,company_api_key)
        resultado = cursor.execute(query)
        row_affected = resultado.rowcount
        conn.commit()
        conn.close()
        if row_affected > 0:
            return jsonify({'status':'ready',
                        "message":"Registro eliminado."})
        else:
            return jsonify({'status':'fail',
                        "message":"No se encontró registro alguno para eliminar."})
    else:
        return jsonify({'status':'fail',
                        "message":"El company_api_key y el id de la compañia no tienen relación entre si."})