from flask import Blueprint, jsonify, request
from models.plagio import Plagio
from models.documento import Documento
from utils.db import db
from utils.error_handler import handle_errors
import pytz
from datetime import datetime

# Define la zona horaria de Perú
PERU_TZ = pytz.timezone('America/Lima')

plagios = Blueprint('plagios', __name__)

@plagios.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    plagios = Plagio.query.all()
    plagios_list = [plagio.to_dict() for plagio in plagios]
    return jsonify(plagios_list), 200

@plagios.route("/get_by_id/<int:id>", methods=['GET'])
@handle_errors
def get_by_id(id):
    plagio = Plagio.query.get(id)
    if plagio:
        return jsonify(plagio.to_dict()), 200
    else:
        return jsonify({'error': 'Plagio no encontrado'}), 404

@plagios.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    
    id_documento = data.get('id_documento')
    porcentaje_plagio = data.get('porcentaje_plagio')
    detalles_plagio = data.get('detalles_plagio')
    estado = data.get('estado', 'sin sanción')
    
    if not id_documento or not porcentaje_plagio or not detalles_plagio:
        return jsonify({'error': 'ID del documento, porcentaje de plagio y detalles son requeridos'}), 400

    # Verifica si el documento existe
    documento = Documento.query.get(id_documento)
    if not documento:
        return jsonify({'error': 'El documento no existe'}), 404
    
    # Verifica si ya existe un plagio para este documento
    plagio_existente = Plagio.query.filter_by(id_documento=id_documento).first()
    if plagio_existente:
        return jsonify({'error': 'Ya existe un plagio registrado para este documento'}), 400
    
    # Crea el nuevo plagio
    nuevo_plagio = Plagio(
        id_documento=id_documento,
        porcentaje_plagio=porcentaje_plagio,
        detalles_plagio=detalles_plagio,
        estado=estado
    )
    db.session.add(nuevo_plagio)
    db.session.commit()
    
    return jsonify({'message': 'Plagio creado exitosamente', 'plagio': nuevo_plagio.to_dict()}), 201

@plagios.route("/update/<int:id>", methods=['PATCH'])
@handle_errors
def update(id):
    data = request.get_json()
    plagio = Plagio.query.get(id)
    
    if not plagio:
        return jsonify({'error': 'Plagio no encontrado'}), 404
    
    if 'porcentaje_plagio' in data:
        plagio.porcentaje_plagio = data['porcentaje_plagio']
    if 'detalles_plagio' in data:
        plagio.detalles_plagio = data['detalles_plagio']
    if 'estado' in data:
        if data['estado'] not in ['sin sanción', 'sancionado']:
            return jsonify({'error': 'Estado inválido'}), 400
        plagio.estado = data['estado']
    
    db.session.commit()
    
    return jsonify({'message': 'Plagio actualizado exitosamente', 'plagio': plagio.to_dict()}), 200

@plagios.route("/delete/<int:id>", methods=['DELETE'])
@handle_errors
def delete(id):
    plagio = Plagio.query.get(id)
    if not plagio:
        return jsonify({'error': 'Plagio no encontrado'}), 404
    
    db.session.delete(plagio)
    db.session.commit()
    
    return jsonify({'message': 'Plagio eliminado exitosamente'}), 200
