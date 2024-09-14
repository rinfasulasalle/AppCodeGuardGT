from flask import Blueprint, jsonify, request
from models.docente import Docente
from models.administracion import Administracion
from models.estudiante import Estudiante
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors

docentes = Blueprint('docentes', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos

@docentes.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    docentes_list = Docente.query.all()
    docentes_data = [docente.to_dict() for docente in docentes_list]
    return jsonify(docentes_data), 200

@docentes.route("/get_by_dni/<dni>", methods=['GET'])
@handle_errors
def get_by_dni(dni):
    docente = Docente.query.filter_by(dni_usuario=dni).first()
    if docente:
        return jsonify(docente.to_dict()), 200
    else:
        return jsonify({'error': 'Docente no encontrado'}), 404

@docentes.route("/create", methods=['POST'])
@handle_errors
def create_docente():
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
    
    # Crea el nuevo docente
    nuevo_docente = Docente(dni)
    db.session.add(nuevo_docente)
    db.session.commit()
    
    return jsonify({'message': 'Docente agregado exitosamente', 'dni': dni}), 201

@docentes.route("/delete/<dni>", methods=['DELETE'])
@handle_errors
def delete(dni):
    docente = Docente.query.filter_by(dni_usuario=dni).first()

    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404

    db.session.delete(docente)
    db.session.commit()

    return jsonify({'message': 'Docente eliminado exitosamente', 'dni_usuario': docente.dni_usuario}), 200

# --------------------------------------------------------
