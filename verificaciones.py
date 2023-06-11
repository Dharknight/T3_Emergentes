import sqlite3

#FUNCIÓN PARA VALIDAR QUE LA OPERACIÓN LA HAGA UN USUARIO ADMIN
def validar_admin(username, password):
    sqliteConnection = sqlite3.connect('DB/database.db')
    cursor = sqliteConnection.cursor()
    query = "SELECT username, password FROM admin;"
    cursor.execute(query)
    record = cursor.fetchall()
    for i in record:
        if i[0] == username: 
            if i[1] == password:
                cursor.close()
                return True
    cursor.close()
    return False

#FUNCIÓN PARA VALIDAR QUE EXISTE COMPANY_API_KEY
def verificacion_company_api_key(company_api_key):
    sqliteConnection = sqlite3.connect('DB/database.db')
    cursor = sqliteConnection.cursor()
    query = "SELECT company_api_key FROM company;"
    resultado = cursor.execute(query).fetchall()
    if len(resultado) > 0:
        return True
    cursor.close()
    return False

#FUNCIÓN PARA VALIDAR EL SENSOR_API_KEY
def verificacion_sensor_api_key(sensor_api_key):
    sqliteConnection = sqlite3.connect('DB/database.db')
    cursor = sqliteConnection.cursor()
    query = "SELECT * FROM sensor WHERE sensor_api_key = {};".format(sensor_api_key)
    resultado = cursor.execute(query).fetchall()
    if len(resultado) > 0:
        return True
    cursor.close()
    return False