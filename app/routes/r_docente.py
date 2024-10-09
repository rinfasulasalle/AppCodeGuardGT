from flask import Blueprint, jsonify, request
from models.docente import Docente
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors
import re

docente = Blueprint('docente', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de docentes

@docente.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    docentes = Docente.query.all()
    docentes_list = []
    for doce in docentes:
        usuario = Usuario.query.filter_by(dni=doce.dni_usuario).first()
        if usuario:
            docentes_list.append({
                'dni': usuario.dni,
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'fecha_registro': usuario.fecha_registro
            })

    return jsonify(docentes_list), 200

@docente.route("/get_by_dni_usuario/<dni_usuario>", methods=['GET'])
@handle_errors
def get_by_dni_usuario(dni_usuario):
    if not dni_usuario or not isinstance(dni_usuario, str):
        return jsonify({'error': 'DNI de usuario inválido'}), 400

    docente = Docente.query.filter_by(dni_usuario=dni_usuario).first()
    if docente:
        usuario = Usuario.query.filter_by(dni=docente.dni_usuario).first()
        if usuario:
            docente_data = {
                'dni': usuario.dni,
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'fecha_registro': usuario.fecha_registro
            }
            return jsonify(docente_data), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

@docente.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    
    # Validar la estructura de los datos
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400

    dni_usuario = data.get('dni_usuario')

    # Validar el DNI del usuario
    if not dni_usuario:
        return jsonify({'error': 'El DNI del usuario es requerido'}), 400

    if not isinstance(dni_usuario, str) or len(dni_usuario) != 8 or not re.match(r'^\d{8}$', dni_usuario):
        return jsonify({'error': 'DNI del usuario inválido. Debe ser una cadena de texto de exactamente 8 dígitos numéricos.'}), 400

    # Validar que el usuario existe
    if not Usuario.query.filter_by(dni=dni_usuario).first():
        return jsonify({'error': 'El usuario no existe'}), 404

    # Verificar si el docente ya existe
    if Docente.query.filter_by(dni_usuario=dni_usuario).first():
        return jsonify({'error': 'El docente ya existe'}), 409

    # Crear el nuevo docente
    nuevo_docente = Docente(dni_usuario=dni_usuario)

    db.session.add(nuevo_docente)
    db.session.commit()

    return jsonify({'message': 'Docente agregado exitosamente', 'dni_usuario': nuevo_docente.dni_usuario}), 201

@docente.route("/delete/<dni_usuario>", methods=['DELETE'])
@handle_errors
def delete(dni_usuario):
    if not dni_usuario or not isinstance(dni_usuario, str):
        return jsonify({'error': 'DNI de usuario inválido'}), 400

    docente = Docente.query.filter_by(dni_usuario=dni_usuario).first()

    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404

    db.session.delete(docente)
    db.session.commit()

    return jsonify({'message': 'Docente eliminado exitosamente', 'dni_usuario': dni_usuario}), 200
# --------------------------------------------------------
@docente.route("/count", methods=['GET'])
@handle_errors
def count():
    # Contar la cantidad de usuarios en la base de datos
    cantidad_usuarios = Docente.query.count()
    
    return jsonify({'cantidad': cantidad_usuarios}), 200