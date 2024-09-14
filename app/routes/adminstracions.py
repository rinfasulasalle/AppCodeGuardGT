from flask import Blueprint, jsonify, request
from models.administracion import Administracion
from models.docente import Docente
from models.estudiante import Estudiante
from models.usuario import Usuario
from routes import estudiantes
from utils.db import db
from utils.error_handler import handle_errors

administracion = Blueprint('administracion', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos

@administracion.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    administracions = Estudiante.query.all()
    administracions_list = [{
        'dni_usuario': administracion.dni_usuario
    } for administracion in administracions]
    return jsonify(administracions_list), 200

@administracion.route("/get_by_dni/<dni>", methods=['GET'])
@handle_errors
def get_by_dni(dni):
    administracion = Administracion.query.filter_by(dni_usuario=dni).first()
    if administracion:
        administracion_data = {
            'dni_usuario': administracion.dni_usuario
        }
        return jsonify(administracion_data), 200
    else:
        return jsonify({'error': 'administracion no encontrado'}), 404

@administracion.route("/create", methods=['POST'])
def create_administracion():
    data = request.get_json()
    
    # Verifica que el dni esté en el formato adecuado
    dni = data.get('dni')
    if not dni:
        return jsonify({'error': 'DNI es requerido'}), 400

    # Verifica si el usuario ya está en alguna de las otras tablas
    if Estudiante.query.get(dni) or Docente.query.get(dni) or Administracion.query.get(dni):
        return jsonify({'error': 'El usuario ya está registrado en otra categoría'}), 400
    
    # Verifica si el usuario existe en la tabla de Usuarios
    usuario = Usuario.query.get(dni)
    if not usuario:
        return jsonify({'error': 'El usuario no existe en la tabla de Usuarios'}), 404
    
    # Crea el nuevo administracion
    nuevo_administracion = Administracion(dni)
    db.session.add(nuevo_administracion)
    db.session.commit()
    
    return jsonify({'message': 'Administracion agregado exitosamente', 'dni': dni}), 201
@administracion.route("/delete/<dni>", methods=['DELETE'])
@handle_errors
def delete(dni):
    administracion = Docente.query.filter_by(dni_usuario=dni).first()

    if not administracion:
        return jsonify({'error': 'Administracion no encontrado'}), 404

    db.session.delete(administracion)
    db.session.commit()

    return jsonify({'message': 'Administracion eliminado exitosamente', 'dni_usuario': administracion.dni_usuario}), 200
# --------------------------------------------------------
