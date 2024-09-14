from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors

usuarios = Blueprint('usuarios', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos
@usuarios.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    usuarios = Usuario.query.all()
    usuarios_list = [{
        'dni': usuario.dni,
        'nombres': usuario.nombres,
        'apellidos': usuario.apellidos,
        'correo': usuario.correo,
        'fecha_nacimiento': str(usuario.fecha_nacimiento)
    } for usuario in usuarios]
    return jsonify(usuarios_list), 200

@usuarios.route("get_by_dni/<dni>", methods=['GET'])
@handle_errors
def get_by_dni(dni):
    usuario = Usuario.query.filter_by(dni=dni).first()
    if usuario:
        usuario_data = {
            'dni': usuario.dni,
            'nombres': usuario.nombres,
            'apellidos': usuario.apellidos,
            'correo': usuario.correo,
            'fecha_nacimiento': str(usuario.fecha_nacimiento)
        }
        return jsonify(usuario_data), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@usuarios.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()

    required_fields = ['dni', 'nombres', 'apellidos', 'correo', 'fecha_nacimiento', 'contrasena']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': 'Campos faltantes', 'missing_fields': missing_fields}), 400

    dni = data['dni']
    nombres = data['nombres']
    apellidos = data['apellidos']
    correo = data['correo']
    fecha_nacimiento = data['fecha_nacimiento']
    contrasena = data['contrasena']

    nuevo_user = Usuario(dni, nombres, apellidos, correo, fecha_nacimiento, contrasena)
    
    db.session.add(nuevo_user)
    db.session.commit()

    return jsonify({'message': 'Usuario agregado exitosamente', 'usuario': nuevo_user.dni}), 201

@usuarios.route("/update/<dni>", methods=['PATCH'])
@handle_errors
def update(dni):
    data = request.get_json()
    usuario = Usuario.query.filter_by(dni=dni).first()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    if 'nombres' in data:
        usuario.nombres = data['nombres']
    if 'apellidos' in data:
        usuario.apellidos = data['apellidos']
    if 'correo' in data:
        usuario.correo = data['correo']
    if 'fecha_nacimiento' in data:
        usuario.fecha_nacimiento = data['fecha_nacimiento']
    if 'contrasena' in data:
        usuario.contrasena = data['contrasena']

    db.session.commit()

    return jsonify({'message': 'Usuario actualizado exitosamente', 'usuario': usuario.dni}), 200

@usuarios.route("/delete/<dni>", methods=['DELETE'])
@handle_errors
def delete(dni):
    usuario = Usuario.query.filter_by(dni=dni).first()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario eliminado exitosamente', 'usuario': usuario.dni}), 200
# --------------------------------------------------------