from flask import Blueprint, jsonify, request
from models.documento import Documento
from models.estudiante import Estudiante
from utils.db import db
from utils.error_handler import handle_errors
import pytz
from datetime import datetime

# Define la zona horaria de Perú
PERU_TZ = pytz.timezone('America/Lima')

documentos = Blueprint('documentos', __name__)

@documentos.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    documentos = Documento.query.all()
    documentos_list = [documento.to_dict() for documento in documentos]
    return jsonify(documentos_list), 200

@documentos.route("/get_by_id/<int:id>", methods=['GET'])
@handle_errors
def get_by_id(id):
    documento = Documento.query.get(id)
    if documento:
        return jsonify(documento.to_dict()), 200
    else:
        return jsonify({'error': 'Documento no encontrado'}), 404

@documentos.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    
    dni_estudiante = data.get('dni_estudiante')
    url_documento = data.get('url_documento')
    
    if not dni_estudiante or not url_documento:
        return jsonify({'error': 'DNI del estudiante y URL del documento son requeridos'}), 400

    # Verifica si el estudiante existe
    estudiante = Estudiante.query.get(dni_estudiante)
    if not estudiante:
        return jsonify({'error': 'El estudiante no existe'}), 404
    
    # Crea el nuevo documento
    nuevo_documento = Documento(dni_estudiante=dni_estudiante, url_documento=url_documento)
    db.session.add(nuevo_documento)
    db.session.commit()
    
    return jsonify({'message': 'Documento creado exitosamente', 'documento': nuevo_documento.to_dict()}), 201

@documentos.route("/update/<int:id>", methods=['PATCH'])
@handle_errors
def update(id):
    data = request.get_json()
    documento = Documento.query.get(id)
    
    if not documento:
        return jsonify({'error': 'Documento no encontrado'}), 404
    
    if 'url_documento' in data:
        documento.url_documento = data['url_documento']
    if 'fecha_subida' in data:
        # Convierte la fecha a la zona horaria de Perú
        fecha_subida = datetime.fromisoformat(data['fecha_subida'])
        fecha_subida = PERU_TZ.localize(fecha_subida)
        documento.fecha_subida = fecha_subida
    
    db.session.commit()
    
    return jsonify({'message': 'Documento actualizado exitosamente', 'documento': documento.to_dict()}), 200

@documentos.route("/delete/<int:id>", methods=['DELETE'])
@handle_errors
def delete(id):
    documento = Documento.query.get(id)
    if not documento:
        return jsonify({'error': 'Documento no encontrado'}), 404
    
    db.session.delete(documento)
    db.session.commit()
    
    return jsonify({'message': 'Documento eliminado exitosamente'}), 200
