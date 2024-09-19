from flask import Blueprint, jsonify, request
from models.documento import Documento
from models.estudiante import Estudiante
from utils.db import db
from utils.error_handler import handle_errors

documentos = Blueprint('documentos', __name__)

# Crear un nuevo documento
@documentos.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    dni_estudiante = data.get('dni_estudiante')
    url_documento = data.get('url_documento')

    # Validar que el DNI del estudiante exista
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'El DNI del estudiante no está registrado'}), 404

    # Validar que la URL del documento no esté vacía
    if not url_documento:
        return jsonify({'error': 'La URL del documento no puede estar vacía'}), 400

    # Crear el nuevo documento
    nuevo_documento = Documento(dni_estudiante=dni_estudiante, url_documento=url_documento)
    db.session.add(nuevo_documento)
    db.session.commit()

    return jsonify({
        'message': 'Documento agregado exitosamente',
        'documento': nuevo_documento.to_dict()
    }), 201

# Obtener todos los documentos
@documentos.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    documentos = Documento.query.all()
    documentos_list = [doc.to_dict() for doc in documentos]
    return jsonify(documentos_list), 200

# Obtener documento por ID
@documentos.route("/get_by_id/<int:id_documento>", methods=['GET'])
@handle_errors
def get_by_id(id_documento):
    documento = Documento.query.get(id_documento)
    if not documento:
        return jsonify({'error': 'Documento no encontrado'}), 404
    return jsonify(documento.to_dict()), 200

# Actualizar un documento
@documentos.route("/update/<int:id_documento>", methods=['PATCH'])
@handle_errors
def update(id_documento):
    data = request.get_json()
    documento = Documento.query.get(id_documento)

    if not documento:
        return jsonify({'error': 'Documento no encontrado'}), 404

    # Actualizar campos
    if 'dni_estudiante' in data:
        estudiante = Estudiante.query.filter_by(dni_usuario=data['dni_estudiante']).first()
        if not estudiante:
            return jsonify({'error': 'El DNI del estudiante no está registrado'}), 404
        documento.dni_estudiante = data['dni_estudiante']

    if 'url_documento' in data:
        documento.url_documento = data['url_documento']

    db.session.commit()
    return jsonify({'message': 'Documento actualizado exitosamente', 'documento': documento.to_dict()}), 200

# Eliminar un documento
@documentos.route("/delete/<int:id_documento>", methods=['DELETE'])
@handle_errors
def delete(id_documento):
    documento = Documento.query.get(id_documento)
    if not documento:
        return jsonify({'error': 'Documento no encontrado'}), 404

    db.session.delete(documento)
    db.session.commit()
    return jsonify({'message': 'Documento eliminado exitosamente', 'id_documento': id_documento}), 200

# Obtener documentos por DNI del estudiante
@documentos.route("/get_by_estudiante/<dni_estudiante>", methods=['GET'])
@handle_errors
def get_by_estudiante(dni_estudiante):
    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'El DNI del estudiante no está registrado'}), 404

    documentos = Documento.query.filter_by(dni_estudiante=dni_estudiante).all()
    documentos_list = [doc.to_dict() for doc in documentos]

    return jsonify({
        'dni_estudiante': dni_estudiante,
        'documentos': documentos_list
    }), 200
