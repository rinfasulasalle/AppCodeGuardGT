from flask import Blueprint, jsonify, request
from models.administracion import Administracion
from models.docente import Docente
from models.estudiante import Estudiante
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors

estudiantes = Blueprint('estudiantes', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos

@estudiantes.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    estudiantes = Estudiante.query.all()
    estudiantes_list = [{
        'dni_usuario': estudiante.dni_usuario
    } for estudiante in estudiantes]
    return jsonify(estudiantes_list), 200

@estudiantes.route("/get_by_dni/<dni>", methods=['GET'])
@handle_errors
def get_by_dni(dni):
    estudiante = Estudiante.query.filter_by(dni_usuario=dni).first()
    if estudiante:
        estudiante_data = {
            'dni_usuario': estudiante.dni_usuario
        }
        return jsonify(estudiante_data), 200
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

@estudiantes.route("/create", methods=['POST'])
def create_estudiante():
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
    
    # Crea el nuevo estudiante
    nuevo_estudiante = Estudiante(dni)
    db.session.add(nuevo_estudiante)
    db.session.commit()
    
    return jsonify({'message': 'Estudiante agregado exitosamente', 'dni': dni}), 201
@estudiantes.route("/delete/<dni>", methods=['DELETE'])
@handle_errors
def delete(dni):
    estudiante = Estudiante.query.filter_by(dni_usuario=dni).first()

    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    db.session.delete(estudiante)
    db.session.commit()

    return jsonify({'message': 'Estudiante eliminado exitosamente', 'dni_usuario': estudiante.dni_usuario}), 200
# --------------------------------------------------------