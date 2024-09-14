from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from utils.db import db

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SQLAlchemyError as e:
            db.session.rollback()  # Revertir cambios en caso de error en la base de datos
            return jsonify({'error': 'Error en la base de datos', 'details': str(e)}), 500
        except Exception as e:
            return jsonify({'error': 'Error inesperado', 'details': str(e)}), 500
    return decorated_function
