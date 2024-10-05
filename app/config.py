from flask import Flask
from routes.r_usuarios import usuarios
from utils.db import db
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    
    # Carga variables de entorno
    load_dotenv()

    # Configuraciones de la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa la base de datos con la aplicación
    db.init_app(app)

    # Registra los Blueprints
    app.register_blueprint(usuarios, url_prefix='/usuarios')

    return app
