from flask import Flask, render_template, session, jsonify, flash
from flask_mongoengine import MongoEngine
from functools import wraps
from dotenv import load_dotenv
from flask_cors import CORS
import os

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})  # permite todas las rutas desde cualquier origen

key = os.environ.get("SECRET_KEY")

app.secret_key = f"{key}"# carga la clave secreta desde las variables de entorno
# uri1= "mongodb://localhost:27017/GuiasProfesores"
user = os.environ.get("USER_BD")



uri1 = "mongodb+srv://adsocauca:1061705900@cluster0.pkaaf.mongodb.net/INSTRUCTORES_SENA?retryWrites=true&w=majority&appName=Cluster0"

app.config['SESSION_TYPE'] = 'filesystem' 

app.config["UPLOAD_FOLDER"] = "./static/images"

app.config['MONGODB_SETTINGS'] = [{
    "db": "INSTRUCTORES_SENA",
    "host": uri1,
    # "port": 27017
}]

app.config['CORS_HEADERS'] = 'Content-Type'

db = MongoEngine(app)

from mongoengine.connection import get_db

db_actual = get_db()
print("📌 Conectado a la base de datos:", db_actual.name)


@app.route('/')
def inicio():
    regionales = Regional.objects() 
    return render_template('login.html', regionales=regionales)


from routes.instructorRuta import *
from routes.guiasRuta import *
from routes.regionalRuta import *
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True) 