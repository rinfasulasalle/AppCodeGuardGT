from flask import Blueprint, jsonify, request
from models.incidencia import Incidencia
from models.estudiante import Estudiante
from utils.db import db
from utils.error_handler import handle_errors
import pytz
from datetime import datetime

# Define la zona horaria de Perú
PERU_TZ = pytz.timezone('America/Lima')

incidencias = Blueprint('incidencias', __name__)

@incidencias.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    incidencias = Incidencia.query.all()
    incidencias_list = [incidencia.to_dict() for incidencia in incidencias]
    return jsonify(incidencias_list), 200

@incidencias.route("/get_by_id/<int:id>", methods=['GET'])
@handle_errors
def get_by_id(id):
    incidencia = Incidencia.query.get(id)
    if incidencia:
        return jsonify(incidencia.to_dict()), 200
    else:
        return jsonify({'error': 'Incidencia no encontrada'}), 404

@incidencias.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    
    dni_estudiante = data.get('dni_estudiante')
    descripcion = data.get('descripcion')
    
    if not dni_estudiante or not descripcion:
        return jsonify({'error': 'DNI del estudiante y descripción son requeridos'}), 400

    # Verifica si el estudiante existe
    estudiante = Estudiante.query.get(dni_estudiante)
    if not estudiante:
        return jsonify({'error': 'El estudiante no existe'}), 404
    
    # Crea la nueva incidencia
    nueva_incidencia = Incidencia(dni_estudiante=dni_estudiante, descripcion=descripcion)
    db.session.add(nueva_incidencia)
    db.session.commit()
    
    return jsonify({'message': 'Incidencia creada exitosamente', 'incidencia': nueva_incidencia.to_dict()}), 201

@incidencias.route("/update/<int:id>", methods=['PATCH'])
@handle_errors
def update(id):
    data = request.get_json()
    incidencia = Incidencia.query.get(id)
    
    if not incidencia:
        return jsonify({'error': 'Incidencia no encontrada'}), 404
    
    if 'descripcion' in data:
        incidencia.descripcion = data['descripcion']
    if 'fecha_incidencia' in data:
        # Convierte la fecha a la zona horaria de Perú
        fecha_incidencia = datetime.fromisoformat(data['fecha_incidencia'])
        fecha_incidencia = PERU_TZ.localize(fecha_incidencia)
        incidencia.fecha_incidencia = fecha_incidencia
    
    db.session.commit()
    
    return jsonify({'message': 'Incidencia actualizada exitosamente', 'incidencia': incidencia.to_dict()}), 200

@incidencias.route("/delete/<int:id>", methods=['DELETE'])
@handle_errors
def delete(id):
    incidencia = Incidencia.query.get(id)
    if not incidencia:
        return jsonify({'error': 'Incidencia no encontrada'}), 404
    
    db.session.delete(incidencia)
    db.session.commit()
    
    return jsonify({'message': 'Incidencia eliminada exitosamente'}), 200
