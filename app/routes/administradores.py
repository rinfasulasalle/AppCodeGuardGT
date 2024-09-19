from flask import Blueprint, jsonify, request
from models.estudiante import Estudiante
from models.usuario import Usuario
from models.administracion import Administracion
from models.docente import Docente
from utils.db import db
from utils.error_handler import handle_errors

administradores = Blueprint('administradores', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de estudiantes

@administradores.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    administradores = Administracion.query.all()
    administradores_list = []
    for administrador in administradores:
        usuario = Usuario.query.filter_by(dni= administrador.dni_usuario).first()

        # Verificar si el usuario existe antes de agregarlo a la lista
        if usuario:
            administradores_list.append({
                'dni_usuario': administrador.dni_usuario,
                'info_usuario': {
                    'nombres': usuario.nombres,
                    'apellidos': usuario.apellidos,
                    'correo': usuario.correo
                }
            })
    return jsonify(administradores_list), 200

@administradores.route("/get_by_dni/<dni>", methods=['GET'])
@handle_errors
def get_by_dni(dni):
    # Verificar si el usuario existe
    usuario = Usuario.query.filter_by(dni=dni).first()
    if not usuario:
        return jsonify({'error': 'El DNI no está registrado como usuario'}), 404
    
    # Verificar si el estudiante existe
    administrador = Administracion.query.filter_by(dni_usuario=dni).first()
    if administrador:
        return jsonify({
            'dni_usuario': administrador.dni_usuario,
            'info_usuario': {
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo
            }
        }), 200
    else:
        return jsonify({'error': 'Administrador no encontrado'}), 404
    
@administradores.route("/create", methods=['POST'])
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
    
    # Verificar si el DNI ya está registrado como estudiante o docente
    if Estudiante.query.filter_by(dni_usuario=dni).first():
        return jsonify({'error': 'El DNI ya está registrado como Estudiante'}), 409  # Error 409: Conflicto
    if Docente.query.filter_by(dni_usuario=dni).first():
            return jsonify({'error': 'El DNI ya está registrado como docente'}), 409  # Error 409: Conflicto

    # Verificar si el DNI ya está registrado como administrador
    if Administracion.query.filter_by(dni_usuario=dni).first():
        return jsonify({'error': 'El DNI ya está registrado como administrador'}), 409  # Error 409: Conflicto
    
    # Crear el nuevo administrador
    nuevo_administrador = Administracion(dni_usuario= dni)
    db.session.add(nuevo_administrador)
    db.session.commit()

    return jsonify({'message': 'Administrador agregado exitosamente', 'dni_usuario': nuevo_administrador.dni_usuario}), 201

@administradores.route("/delete/<dni>", methods=['DELETE'])
@handle_errors
def delete(dni):
    # Verificar si el usuario existe
    usuario = Usuario.query.filter_by(dni=dni).first()
    if not usuario:
        return jsonify({'error': 'El DNI no está registrado como usuario'}), 404

    # Verificar si el administrador existe
    administrador = Administracion.query.filter_by(dni_usuario=dni).first()
    if not administrador:
        return jsonify({'error': 'Administrador no encontrado'}), 404

    db.session.delete(administrador)
    db.session.commit()

    return jsonify({'message': 'Administrador eliminado exitosamente', 'dni_usuario': administrador.dni_usuario}), 200

# --------------------------------------------------------