from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors
import pytz

PERU_TZ = pytz.timezone('America/Lima')

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
    required_fields = ['dni', 'nombres', 'apellidos', 'fecha_nacimiento']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': 'Campos faltantes o vacíos', 'missing_fields': missing_fields}), 400

    # Extraer datos del JSON
    dni = data['dni']

    # Validar que el DNI no esté vacío
    if not dni:
        return jsonify({'error': 'El DNI no puede estar vacío'}), 400

    # Validar que el DNI solo contenga números
    if not dni.isdigit():
        return jsonify({'error': 'El DNI solo debe contener números'}), 400

    # Validar que el DNI tenga exactamente 8 dígitos
    if len(dni) != 8:
        return jsonify({'error': 'El DNI debe tener exactamente 8 dígitos'}), 400

    # Validar si el DNI ya existe en la base de datos
    if Usuario.query.filter_by(dni=dni).first():
        return jsonify({'error': 'El DNI ya está registrado'}), 409  # Error 409: Conflicto

    nombres = data['nombres']
    apellidos = data['apellidos'].split()

    # Validar si hay al menos dos apellidos para generar correctamente el correo
    if len(apellidos) < 2:
        return jsonify({'error': 'Se necesitan al menos dos apellidos para generar el correo'}), 400

    fecha_nacimiento = data['fecha_nacimiento']
    
    # Generar correo automáticamente
    correo = f"{nombres[0].lower()}{apellidos[0].lower()}{apellidos[1][0].lower()}@codeguard.pe"

    # La contraseña por defecto será el DNI si no se proporciona
    contrasena = data.get('contrasena', dni)

    # Crear el nuevo usuario
    nuevo_user = Usuario(
        dni=dni,
        nombres=nombres,
        apellidos=" ".join(apellidos),
        correo=correo,
        fecha_nacimiento=fecha_nacimiento,
        contrasena=contrasena
    )

    db.session.add(nuevo_user)
    db.session.commit()

    return jsonify({
        'message': 'Usuario agregado exitosamente',
        'usuario': {
            'dni': nuevo_user.dni,
            'correo': nuevo_user.correo,
            'contrasena': nuevo_user.contrasena  # Para propósitos de confirmación
        }
    }), 201

@usuarios.route("/update/<dni>", methods=['PATCH'])
@handle_errors
def update(dni):
    data = request.get_json()
    usuario = Usuario.query.filter_by(dni=dni).first()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Validar que el DNI no esté vacío
    if not dni:
        return jsonify({'error': 'El DNI no puede estar vacío'}), 400

    # Validar que el DNI solo contenga números
    if not dni.isdigit():
        return jsonify({'error': 'El DNI solo debe contener números'}), 400

    # Validar que el DNI tenga exactamente 8 dígitos
    if len(dni) != 8:
        return jsonify({'error': 'El DNI debe tener exactamente 8 dígitos'}), 400

    # Validar si el nuevo DNI ya existe en la base de datos, si se proporciona
    nuevo_dni = data.get('dni')
    if nuevo_dni and nuevo_dni != dni:
        if Usuario.query.filter_by(dni=nuevo_dni).first():
            return jsonify({'error': 'El DNI ya está registrado'}), 409  # Error 409: Conflicto

    # Validar que los campos no estén vacíos
    for field in ['nombres', 'apellidos', 'correo', 'fecha_nacimiento']:
        if field in data and not data[field]:
            return jsonify({'error': f'El campo {field} no puede estar vacío'}), 400

    # Actualizar campos del usuario
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

    # Actualizar el DNI si se proporciona un nuevo DNI
    if nuevo_dni:
        usuario.dni = nuevo_dni

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
