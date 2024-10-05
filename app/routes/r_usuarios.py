from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils.db import db
from utils.for_users import validar_telefono,generar_correo_unico, hash_contrasena, verificar_contrasena
from utils.error_handler import handle_errors
import re

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
        'telefono': usuario.telefono,
    } for usuario in usuarios]
    return jsonify(usuarios_list), 200

@usuarios.route("/get_by_dni/<dni>", methods=['GET'])
@handle_errors
def get_by_dni(dni):
    usuario = Usuario.query.filter_by(dni=dni).first()
    if usuario:
        usuario_data = {
            'dni': usuario.dni,
            'nombres': usuario.nombres,
            'apellidos': usuario.apellidos,
            'correo': usuario.correo,
            'telefono': usuario.telefono
        }
        return jsonify(usuario_data), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@usuarios.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    required_fields = ['dni', 'nombres', 'apellidos', 'telefono']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': 'Campos faltantes o vacíos', 'missing_fields': missing_fields}), 400

    dni = data['dni']

    # Validar que el DNI no esté vacío y tenga exactamente 8 dígitos
    if not dni or not dni.isdigit() or len(dni) != 8:
        return jsonify({'error': 'El DNI debe tener exactamente 8 dígitos y solo contener números'}), 400

    # Validar si el DNI ya existe en la base de datos
    if Usuario.query.filter_by(dni=dni).first():
        return jsonify({'error': 'El DNI ya está registrado'}), 409  # Conflicto

    nombres = data['nombres']
    apellidos = data['apellidos']
    
    # Validar que hay al menos dos apellidos
    if len(apellidos.split()) < 2:
        return jsonify({'error': 'Se necesitan al menos dos apellidos para generar el correo'}), 400

    # Validar que nombres y apellidos solo contengan letras
    if not re.match(r'^[A-Za-záéíóúñÑÁÉÍÓÚ ]+$', nombres):
        return jsonify({'error': 'Los nombres solo pueden contener letras y espacios.'}), 400
    
    if not re.match(r'^[A-Za-záéíóúñÑÁÉÍÓÚ ]+$', apellidos):
        return jsonify({'error': 'Los apellidos solo pueden contener letras y espacios.'}), 400

    # Validar el formato del número de teléfono
    telefono = data['telefono'].replace(" ", "")
    if not validar_telefono(telefono):
        return jsonify({'error': 'El formato del número de teléfono es inválido. Debe ser: +código_de_país número.'}), 400

    # Limpiar el número de teléfono (eliminar espacios)
    telefono_limpio = telefono.replace(" ", "")

    # Generar correo único automáticamente
    correo = generar_correo_unico(nombres, apellidos)

    # Hashear la contraseña
    contrasena = data.get('contrasena', dni)  # Usa el DNI como contraseña por defecto si no se proporciona
    contrasena_hash = hash_contrasena(contrasena)

    # Crear el nuevo usuario
    nuevo_user = Usuario(
        dni=dni,
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        contrasena=contrasena_hash,
        telefono=telefono_limpio  # Usar el número limpio
    )

    db.session.add(nuevo_user)
    db.session.commit()

    return jsonify({
        'message': 'Usuario agregado exitosamente',
        'usuario': {
            'dni': nuevo_user.dni,
            'correo': nuevo_user.correo
        }
    }), 201

@usuarios.route("/update/<dni>", methods=['PATCH'])
@handle_errors
def update(dni):
    data = request.get_json()
    usuario = Usuario.query.filter_by(dni=dni).first()

    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Validar si el nuevo DNI ya existe
    nuevo_dni = data.get('dni')
    if nuevo_dni and nuevo_dni != dni and Usuario.query.filter_by(dni=nuevo_dni).first():
        return jsonify({'error': 'El DNI ya está registrado'}), 409  # Conflicto

    # Validar que los campos no estén vacíos
    for field in ['nombres', 'apellidos', 'correo']:
        if field in data and not data[field]:
            return jsonify({'error': f'El campo {field} no puede estar vacío'}), 400

    # Validar que nombres y apellidos solo contengan letras
    if 'nombres' in data and not re.match(r'^[A-Za-záéíóúñÑÁÉÍÓÚ ]+$', data['nombres']):
        return jsonify({'error': 'Los nombres solo pueden contener letras y espacios.'}), 400
    
    if 'apellidos' in data and not re.match(r'^[A-Za-záéíóúñÑÁÉÍÓÚ ]+$', data['apellidos']):
        return jsonify({'error': 'Los apellidos solo pueden contener letras y espacios.'}), 400

    # Actualizar campos del usuario
    if 'nombres' in data:
        usuario.nombres = data['nombres']
    if 'apellidos' in data:
        usuario.apellidos = data['apellidos']
    if 'correo' in data:
        usuario.correo = data['correo']
    
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

@usuarios.route("/change_password/<dni>", methods=['POST'])
@handle_errors
def change_password(dni):
    data = request.get_json()

    # Validar la existencia del usuario
    usuario = Usuario.query.filter_by(dni=dni).first()
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'error': 'La contraseña antigua y la nueva son requeridas'}), 400

    # Verificar si la contraseña actual es correcta
    if not verificar_contrasena(old_password, usuario.contrasena):
        return jsonify({'error': 'La contraseña actual no es correcta'}), 400

    # Hashear la nueva contraseña
    nueva_contrasena_hash = hash_contrasena(new_password)

    # Actualizar la contraseña en la base de datos
    usuario.contrasena = nueva_contrasena_hash
    db.session.commit()

    return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
# --------------------------------------------------------
@usuarios.route("/change_pass/<dni>", methods=['POST'])
@handle_errors
def change_passs(dni):
    data = request.get_json()

    # Validar la existencia del usuario
    usuario = Usuario.query.filter_by(dni=dni).first()
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    # Obtener la nueva contraseña del cuerpo de la solicitud
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'error': 'La nueva contraseña es requerida'}), 400

    # Hashear la nueva contraseña
    nueva_contrasena_hash = hash_contrasena(new_password)

    # Actualizar la contraseña en la base de datos
    usuario.contrasena = nueva_contrasena_hash
    db.session.commit()

    return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
