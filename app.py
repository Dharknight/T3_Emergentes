from flask import Flask, jsonify,request
from flask_cors import CORS
from flask_login import login_required, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from DB.database import get_db, create_tables
from flask_sqlalchemy import SQLAlchemy

import os
from config import config

app = Flask(__name__)
#app.config['SECRET_KEY'] = ''
db = SQLAlchemy(app)
#db = get_db()
#cursor = db.cursor()
#create_tables(db,cursor)

#login_manager_app=LoginManager(app)

#INICIO API
@app.route('/', methods=['GET'])
def index():
    print('Ingresar datos\n')
    username = input("Username: ")
    password = input("Password: ")
    statement = "INSERT INTO ADMIN(username,password) VALUES (?,?)"
    cursor.execute(statement, [username, password])
    db.commit()
    return 'Welcome to the API'

#CREAR COMPAÑIA
@app.route('/new_company')

#LOGIN ADMIN
@app.route('/login',methods=['POST'])
def registro_admin():
    cursor = db.cursor()
    info = request.get_json()
    username = info['username']
    password = info['password']
    password_hash = generate_password_hash(password)

    if not username:
        return jsonify({"message": "Se requiere username"})
    if not password:
        return jsonify({"message": "Se requiere password"})
    
    statement = "SELECT * FROM admin WHERE username = ? AND password = ?"
    logeado = cursor.execute(statement, [username, password])
    if logeado is not None:
        print(logeado)
        login_user(logeado)
        return jsonify({"message": "Admin existente"})
        














if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
