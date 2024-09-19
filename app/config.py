from flask import Flask
from routes.usuarios import usuarios
from routes.estudiantes import estudiantes
from routes.administradores import administradores
from routes.docentes import docentes
from routes.evaluaciones import evaluaciones
from routes.incidencias import incidencias
from routes.documentos import documentos
from routes.plagios import plagios
from routes.notas_evaluaciones import notas_evaluaciones
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
    app.register_blueprint(estudiantes, url_prefix='/estudiantes')
    app.register_blueprint(administradores, url_prefix='/administradores')
    app.register_blueprint(docentes, url_prefix='/docentes')
    app.register_blueprint(evaluaciones, url_prefix='/evaluaciones')
    app.register_blueprint(incidencias, url_prefix='/incidencias')
    app.register_blueprint(documentos, url_prefix='/documentos')
    app.register_blueprint(plagios, url_prefix='/plagios')
    app.register_blueprint(notas_evaluaciones, url_prefix='/notas_evaluaciones')

    return app
