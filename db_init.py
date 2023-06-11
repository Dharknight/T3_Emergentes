#FUNCIÓN PARA CREAR TABLAS EN LA DB.
def create_tables(cursor):
# CREAR TABLA ADMIN
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')

    #CREAR TABLA COMPANY
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            company_api_key TEXT
        )
    ''')

    #CREAR TABLA LOCATION
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS location (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            location_name TEXT,
            location_country TEXT,
            location_city TEXT,
            location_meta TEXT,
            FOREIGN KEY (company_id) REFERENCES company (company_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
        )
    ''')

    #CREAR TABLA SENSOR
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor (
            sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            sensor_name TEXT,
            sensor_category TEXT,
            sensor_meta TEXT,
            sensor_api_key TEXT,
            FOREIGN KEY (location_id) REFERENCES location (location_id) 
                    ON DELETE CASCADE 
                    ON UPDATE NO ACTION
        )
    ''')

    #CREAR TABLA SENSOR_DATA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_api_key TEXT,
            sensor_category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            FOREIGN KEY (sensor_api_key) REFERENCES sensor(sensor_api_key)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
        )
    ''')