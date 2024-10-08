from flask import Flask
from flask_login import LoginManager
from models.usuario import Usuario
from models.administracion import Administracion
from models.docente import Docente
from models.estudiante import Estudiante
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
from routes.r_codigo import codigo
from routes.r_resultado import resultado
from routes.r_auth import auth
from routes.r_home import home

def create_app():
    app = Flask(__name__)
    
    # Carga variables de entorno
    load_dotenv()

    # Configuraciones de la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Inicializa la base de datos con la aplicación
    db.init_app(app)

    # Inicializamos el LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    # Cargar el usuario
    @login_manager.user_loader
    def load_user(dni):
        user = db.session.get(Usuario, str(dni))  # Cargar el usuario por dni
        if user:
            # Consultar el rol del usuario
            role = None

            # Verificar si es Docente
            if db.session.query(Docente).filter_by(dni_usuario=dni).first():
                role = 'Docente'
            # Verificar si es Estudiante
            elif db.session.query(Estudiante).filter_by(dni_usuario=dni).first():
                role = 'Estudiante'
            # Verificar si es Administrador
            elif db.session.query(Administracion).filter_by(dni_usuario=dni).first():
                role = 'Administracion'

            # Si se encontró un rol, asignarlo a una propiedad del usuario
            user.role = role
        return user

    # Registra los Blueprints
    app.register_blueprint(usuarios, url_prefix='/usuarios')
    app.register_blueprint(administracion, url_prefix='/administracion')
    app.register_blueprint(docente, url_prefix='/docente')
    app.register_blueprint(estudiante, url_prefix='/estudiante')
    app.register_blueprint(curso, url_prefix='/curso')
    app.register_blueprint(evaluacion, url_prefix='/evaluacion')
    app.register_blueprint(matricula, url_prefix='/matricula')
    app.register_blueprint(codigo, url_prefix='/codigo')
    app.register_blueprint(resultado, url_prefix='/resultado')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(home, url_prefix = '/')
    
    return app
