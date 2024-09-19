from flask import Blueprint, jsonify, request
from models.plagio import Plagio
from models.documento import Documento
from models.estudiante import Estudiante
from utils.db import db
from utils.error_handler import handle_errors

plagios = Blueprint('plagios', __name__)

# Crear un nuevo registro de plagio
@plagios.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    id_documento = data.get('id_documento')
    porcentaje_plagio = data.get('porcentaje_plagio')
    detalles_plagio = data.get('detalles_plagio')

    # Validar que el documento exista
    documento = Documento.query.get(id_documento)
    if not documento:
        return jsonify({'error': 'El documento no está registrado'}), 404

    # Crear el nuevo registro de plagio
    nuevo_plagio = Plagio(id_documento=id_documento, porcentaje_plagio=porcentaje_plagio, detalles_plagio=detalles_plagio)
    db.session.add(nuevo_plagio)
    db.session.commit()

    return jsonify({
        'message': 'Registro de plagio creado exitosamente',
        'plagio': nuevo_plagio.to_dict()
    }), 201

# Obtener todos los registros de plagio
@plagios.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    plagios = Plagio.query.all()
    plagios_list = [plagio.to_dict() for plagio in plagios]
    return jsonify(plagios_list), 200

# Obtener un registro de plagio por ID
@plagios.route("/get_by_id/<int:id_plagio>", methods=['GET'])
@handle_errors
def get_by_id(id_plagio):
    plagio = Plagio.query.get(id_plagio)
    if not plagio:
        return jsonify({'error': 'Registro de plagio no encontrado'}), 404
    return jsonify(plagio.to_dict()), 200

# Actualizar un registro de plagio
@plagios.route("/update/<int:id_plagio>", methods=['PATCH'])
@handle_errors
def update(id_plagio):
    data = request.get_json()
    plagio = Plagio.query.get(id_plagio)

    if not plagio:
        return jsonify({'error': 'Registro de plagio no encontrado'}), 404

    # Actualizar campos
    if 'id_documento' in data:
        documento = Documento.query.get(data['id_documento'])
        if not documento:
            return jsonify({'error': 'El documento no está registrado'}), 404
        plagio.id_documento = data['id_documento']

    if 'porcentaje_plagio' in data:
        plagio.porcentaje_plagio = data['porcentaje_plagio']
    
    if 'detalles_plagio' in data:
        plagio.detalles_plagio = data['detalles_plagio']
    
    if 'estado' in data:
        plagio.estado = data['estado']

    db.session.commit()
    return jsonify({'message': 'Registro de plagio actualizado exitosamente', 'plagio': plagio.to_dict()}), 200

# Eliminar un registro de plagio
@plagios.route("/delete/<int:id_plagio>", methods=['DELETE'])
@handle_errors
def delete(id_plagio):
    plagio = Plagio.query.get(id_plagio)
    if not plagio:
        return jsonify({'error': 'Registro de plagio no encontrado'}), 404

    db.session.delete(plagio)
    db.session.commit()
    return jsonify({'message': 'Registro de plagio eliminado exitosamente', 'id_plagio': id_plagio}), 200

# Obtener registros de plagio por ID del documento
@plagios.route("/get_by_documento/<int:id_documento>", methods=['GET'])
@handle_errors
def get_by_documento(id_documento):
    # Verificar si el documento existe
    documento = Documento.query.get(id_documento)
    if not documento:
        return jsonify({'error': 'El documento no está registrado'}), 404

    plagios = Plagio.query.filter_by(id_documento=id_documento).all()
    plagios_list = [plagio.to_dict() for plagio in plagios]

    return jsonify({
        'id_documento': id_documento,
        'plagios': plagios_list
    }), 200

# Obtener plagios por DNI del estudiante
@plagios.route("/get_by_estudiante/<dni_estudiante>", methods=['GET'])
@handle_errors
def get_plagios_by_estudiante(dni_estudiante):
    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'El DNI del estudiante no está registrado'}), 404

    # Obtener todos los documentos del estudiante
    documentos = Documento.query.filter_by(dni_estudiante=dni_estudiante).all()
    if not documentos:
        return jsonify({'message': 'No se encontraron documentos para este estudiante'}), 404

    plagios_list = []
    
    # Obtener los plagios de cada documento
    for documento in documentos:
        plagios = Plagio.query.filter_by(id_documento=documento.id_documento).all()
        plagios_list.extend([plagio.to_dict() for plagio in plagios])

    if not plagios_list:
        return jsonify({'message': 'No se detectaron plagios en los documentos del estudiante'}), 200

    return jsonify({
        'plagios': plagios_list
    }), 200