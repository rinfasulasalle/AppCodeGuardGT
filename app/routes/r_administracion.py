from flask import Blueprint, jsonify, request
from models.administracion import Administracion
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors
import re

administracion = Blueprint('administracion', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de administración

@administracion.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    administradores = Administracion.query.all()
    administradores_list = []
    for admin in administradores:
        usuario = Usuario.query.filter_by(dni=admin.dni_usuario).first()
        if usuario:
            administradores_list.append({
                'dni': usuario.dni,
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'fecha_registro': usuario.fecha_registro
            })

    return jsonify(administradores_list), 200

@administracion.route("/get_by_dni_usuario/<dni_usuario>", methods=['GET'])
@handle_errors
def get_by_dni_usuario(dni_usuario):
    if not dni_usuario or not isinstance(dni_usuario, str):
        return jsonify({'error': 'DNI de usuario inválido'}), 400

    admin = Administracion.query.filter_by(dni_usuario=dni_usuario).first()
    if admin:
        usuario = Usuario.query.filter_by(dni=admin.dni_usuario).first()
        if usuario:
            admin_data = {
                'dni': usuario.dni,
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo,
                'telefono': usuario.telefono,
                'fecha_registro': usuario.fecha_registro
            }
            return jsonify(admin_data), 200
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    else:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

@administracion.route("/create", methods=['POST'])
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

    # Verificar si el administrador ya existe
    if Administracion.query.filter_by(dni_usuario=dni_usuario).first():
        return jsonify({'error': 'El administrador ya existe'}), 409

    # Crear el nuevo administrador
    nuevo_admin = Administracion(dni_usuario=dni_usuario)

    db.session.add(nuevo_admin)
    db.session.commit()

    return jsonify({'message': 'Administrador agregado exitosamente', 'dni_usuario': nuevo_admin.dni_usuario}), 201

@administracion.route("/delete/<dni_usuario>", methods=['DELETE'])
@handle_errors
def delete(dni_usuario):
    if not dni_usuario or not isinstance(dni_usuario, str):
        return jsonify({'error': 'DNI de usuario inválido'}), 400

    admin = Administracion.query.filter_by(dni_usuario=dni_usuario).first()

    if not admin:
        return jsonify({'error': 'Administrador no encontrado'}), 404

    db.session.delete(admin)
    db.session.commit()

    return jsonify({'message': 'Administrador eliminado exitosamente', 'dni_usuario': dni_usuario}), 200
# --------------------------------------------------------
@administracion.route("/count", methods=['GET'])
@handle_errors
def count():
    # Contar la cantidad de usuarios en la base de datos
    cantidad_usuarios = Administracion.query.count()
    
    return jsonify({'cantidad': cantidad_usuarios}), 200