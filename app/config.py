from flask import Flask
from utils.db import db
import os
from dotenv import load_dotenv

from routes.r_usuarios import usuarios
from routes.r_administracion import administracion
from routes.r_docente import docente
from routes.r_estudiante import  estudiante
from routes.r_curso import curso
from routes.r_evaluacion import evaluacion
from routes.r_matricula import matricula

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
    app.register_blueprint(administracion, url_prefix='/administracion')
    app.register_blueprint(docente, url_prefix='/docente')
    app.register_blueprint(estudiante, url_prefix='/estudiante')
    app.register_blueprint(curso, url_prefix='/curso')
    app.register_blueprint(evaluacion, url_prefix='/evaluacion')
    app.register_blueprint(matricula, url_prefix='/matricula')
    return app
