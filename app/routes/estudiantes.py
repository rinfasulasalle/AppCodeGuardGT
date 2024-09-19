from flask import Blueprint, jsonify, request
from models.estudiante import Estudiante
from models.usuario import Usuario
from models.administracion import Administracion
from models.docente import Docente
from utils.db import db
from utils.error_handler import handle_errors

estudiantes = Blueprint('estudiantes', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de estudiantes

@estudiantes.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    estudiantes = Estudiante.query.all()
    estudiantes_list = []
    for estudiante in estudiantes:
        usuario = Usuario.query.filter_by(dni=estudiante.dni_usuario).first()

        # Verificar si el usuario existe antes de agregarlo a la lista
        if usuario:
            estudiantes_list.append({
                'dni_usuario': estudiante.dni_usuario,
                'info_usuario': {
                    'nombres': usuario.nombres,
                    'apellidos': usuario.apellidos,
                    'correo': usuario.correo
                }
            })
    return jsonify(estudiantes_list), 200

@estudiantes.route("/get_by_dni/<dni>", methods=['GET'])
@handle_errors
def get_by_dni(dni):
    # Verificar si el usuario existe
    usuario = Usuario.query.filter_by(dni=dni).first()
    if not usuario:
        return jsonify({'error': 'El DNI no está registrado como usuario'}), 404

    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni).first()
    if estudiante:
        return jsonify({
            'dni_usuario': estudiante.dni_usuario,
            'info_usuario': {
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo
            }
        }), 200
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

@estudiantes.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    dni = data.get('dni_usuario')

    # Validar que el DNI no esté vacío
    if not dni:
        return jsonify({'error': 'El DNI no puede estar vacío'}), 400

    # Validar que el DNI solo contenga números
    if not dni.isdigit():
        return jsonify({'error': 'El DNI solo debe contener números'}), 400

    # Validar que el DNI tenga exactamente 8 dígitos
    if len(dni) != 8:
        return jsonify({'error': 'El DNI debe tener exactamente 8 dígitos'}), 400

    # Verificar si el DNI está registrado en la tabla de usuarios
    usuario = Usuario.query.filter_by(dni=dni).first()
    if not usuario:
        return jsonify({'error': 'El DNI no está registrado como usuario'}), 404

    # Verificar si el DNI ya está registrado como administrador o docente
    if Administracion.query.filter_by(dni_usuario=dni).first():
        return jsonify({'error': 'El DNI ya está registrado como administrador'}), 409  # Error 409: Conflicto
    if Docente.query.filter_by(dni_usuario=dni).first():
        return jsonify({'error': 'El DNI ya está registrado como docente'}), 409  # Error 409: Conflicto

    # Verificar si el DNI ya está registrado como estudiante
    if Estudiante.query.filter_by(dni_usuario=dni).first():
        return jsonify({'error': 'El DNI ya está registrado como estudiante'}), 409  # Error 409: Conflicto

    # Crear el nuevo estudiante
    nuevo_estudiante = Estudiante(dni_usuario=dni)
    db.session.add(nuevo_estudiante)
    db.session.commit()

    return jsonify({'message': 'Estudiante agregado exitosamente', 'dni_usuario': nuevo_estudiante.dni_usuario}), 201

@estudiantes.route("/delete/<dni>", methods=['DELETE'])
@handle_errors
def delete(dni):
    # Verificar si el usuario existe
    usuario = Usuario.query.filter_by(dni=dni).first()
    if not usuario:
        return jsonify({'error': 'El DNI no está registrado como usuario'}), 404

    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    db.session.delete(estudiante)
    db.session.commit()

    return jsonify({'message': 'Estudiante eliminado exitosamente', 'dni_usuario': estudiante.dni_usuario}), 200

# --------------------------------------------------------