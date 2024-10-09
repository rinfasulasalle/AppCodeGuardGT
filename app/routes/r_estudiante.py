from flask import Blueprint, jsonify, request
from models.estudiante import Estudiante
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors
import re

estudiante = Blueprint('estudiante', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de estudiantes

@estudiante.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    # Obtener todos los estudiantes junto con su información de usuario
    estudiantes = Estudiante.query.all()
    estudiantes_list = []

    for est in estudiantes:
        usuario = Usuario.query.filter_by(dni=est.dni_usuario).first()
        if usuario:
            estudiantes_list.append({
                'dni': usuario.dni,
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'fecha_registro': usuario.fecha_registro
            })

    return jsonify(estudiantes_list), 200
@estudiante.route("/get_by_dni_usuario/<dni_usuario>", methods=['GET'])
@handle_errors
def get_by_dni_usuario(dni_usuario):
    if not dni_usuario or not isinstance(dni_usuario, str):
        return jsonify({'error': 'DNI de usuario inválido'}), 400

    estudiante = Estudiante.query.filter_by(dni_usuario=dni_usuario).first()
    if estudiante:
        usuario = Usuario.query.filter_by(dni=estudiante.dni_usuario).first()
        if usuario:
            estudiante_data = {
                'dni': usuario.dni,
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'fecha_registro': usuario.fecha_registro
            }
            return jsonify(estudiante_data), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

@estudiante.route("/create", methods=['POST'])
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

    # Verificar si el estudiante ya existe
    if Estudiante.query.filter_by(dni_usuario=dni_usuario).first():
        return jsonify({'error': 'El estudiante ya existe'}), 409

    # Crear el nuevo estudiante
    nuevo_estudiante = Estudiante(dni_usuario=dni_usuario)

    db.session.add(nuevo_estudiante)
    db.session.commit()

    return jsonify({'message': 'Estudiante agregado exitosamente', 'dni_usuario': nuevo_estudiante.dni_usuario}), 201

@estudiante.route("/delete/<dni_usuario>", methods=['DELETE'])
@handle_errors
def delete(dni_usuario):
    if not dni_usuario or not isinstance(dni_usuario, str):
        return jsonify({'error': 'DNI de usuario inválido'}), 400

    estudiante = Estudiante.query.filter_by(dni_usuario=dni_usuario).first()

    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    db.session.delete(estudiante)
    db.session.commit()

    return jsonify({'message': 'Estudiante eliminado exitosamente', 'dni_usuario': dni_usuario}), 200
# --------------------------------------------------------
@estudiante.route("/count", methods=['GET'])
@handle_errors
def count():
    # Contar la cantidad de usuarios en la base de datos
    cantidad_usuarios = Estudiante.query.count()
    
    return jsonify({'cantidad': cantidad_usuarios}), 200