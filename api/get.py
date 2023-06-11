from flask import Flask,request,jsonify
import sqlite3
from verificaciones import validar_admin,verificacion_company_api_key


#MOSTRAR TODO DE UNA TABLA
def getall(tabla, company_api_key):
    #print(tabla, company_api_key)
    api_key = verificacion_company_api_key(company_api_key)
    if tabla != 'admin' and tabla != 'company':
        if api_key == True:
            conn = sqlite3.connect('DB/database.db')
            cursor = conn.cursor()
            if tabla == 'location':
                query = """SELECT location_id, location.company_id, location_name, location_country, location_city, location_meta FROM """+tabla+""" JOIN company ON """+tabla+""".company_id = company.company_id WHERE company.company_api_key = {};""".format(company_api_key)
            elif tabla == 'sensor':
                query = """SELECT sensor_id, sensor.location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key FROM """+tabla+""" JOIN location ON """+tabla+""".location_id = location.location_id JOIN company ON location.company_id = company.company_id WHERE company.company_api_key = {};""".format(company_api_key)
            result = cursor.execute(query).fetchall()
            cursor.close()
            if len(result) > 0:
                return jsonify({'status':'ready',
                                tabla:result})
            else:
                return jsonify({'status':'fail',
                                'message':'No se han encontrado registros en el modelo {}'.format(tabla)})
        else:
            return jsonify({'status':'fail',
                            'message':'api_key no está registrada en el sistema'})
    else:
        return jsonify({'status':'fail',
                            'message':'Esta acción no se puede realizar para los datos del modelo {}'.format(tabla)})

#MOSTRAR UNO DE UNA TABLA
def getone(tabla, id, company_api_key):
    #print(tabla, id, company_api_key)
    api_key = verificacion_company_api_key(company_api_key)
    if tabla != 'admin' and tabla != 'company':
        if api_key == True:
            conn = sqlite3.connect('DB/database.db')
            cursor = conn.cursor()
            if tabla == 'location':
                query = """SELECT location_id, location.company_id, location_name, location_country, location_city, location_meta FROM """+tabla+""" JOIN company ON """+tabla+""".company_id = company.company_id WHERE company.company_api_key = {} AND location.{}_id = {};""".format(company_api_key,tabla,id)
            elif tabla == 'sensor':
                query = """SELECT sensor_id, sensor.location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key FROM """+tabla+""" JOIN company ON company.company_id = location.company_id JOIN location ON """+tabla+""".location_id = location.location_id WHERE company.company_api_key = {} AND sensor.{}_id = {};""".format(company_api_key,tabla,id)
            #query = """SELECT * FROM """+tabla+""" WHERE {} = {};""".format(tabla,tabla+'_id',id)
            result = cursor.execute(query).fetchall()
            conn.commit()
            cursor.close()
            if len(result) > 0:
                return jsonify({'status':'ready',
                            tabla:result})
            else:
                return jsonify({'status':'fail',
                                'message':'No se ha encontrado registro en el modelo {} asociado a la id {}'.format(tabla,id)})
        else:
            return jsonify({'status':'fail',
                            'message':'api_key no está registrada en el sistema'})
    else:
        return jsonify({'status':'fail',
                            'message':'Esta acción no se puede realizar para los datos del modelo {}'.format(tabla)})