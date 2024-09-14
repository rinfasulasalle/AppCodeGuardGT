from flask import Blueprint, jsonify, request
from models.evaluacion import Evaluacion
from utils.db import db
from utils.error_handler import handle_errors

evaluaciones = Blueprint('evaluaciones', __name__)

@evaluaciones.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    evaluaciones = Evaluacion.query.all()
    evaluaciones_list = [evaluacion.to_dict() for evaluacion in evaluaciones]
    return jsonify(evaluaciones_list), 200

@evaluaciones.route("/get_by_id/<int:id>", methods=['GET'])
@handle_errors
def get_by_id(id):
    evaluacion = Evaluacion.query.get(id)
    if evaluacion:
        return jsonify(evaluacion.to_dict()), 200
    else:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

@evaluaciones.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    
    nombre = data.get('nombre')
    duracion = data.get('duracion')
    descripcion = data.get('descripcion')
    
    if not nombre or not isinstance(duracion, int) or duracion <= 0:
        return jsonify({'error': 'Nombre y duración positiva son requeridos'}), 400
    
    nueva_evaluacion = Evaluacion(nombre=nombre, duracion=duracion, descripcion=descripcion)
    db.session.add(nueva_evaluacion)
    db.session.commit()
    
    return jsonify({'message': 'Evaluación creada exitosamente', 'evaluacion': nueva_evaluacion.to_dict()}), 201

@evaluaciones.route("/update/<int:id>", methods=['PATCH'])
@handle_errors
def update(id):
    data = request.get_json()
    evaluacion = Evaluacion.query.get(id)
    
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404
    
    if 'nombre' in data:
        evaluacion.nombre = data['nombre']
    if 'descripcion' in data:
        evaluacion.descripcion = data['descripcion']
    if 'duracion' in data:
        if not isinstance(data['duracion'], int) or data['duracion'] <= 0:
            return jsonify({'error': 'Duración debe ser un número positivo'}), 400
        evaluacion.duracion = data['duracion']
    
    db.session.commit()
    
    return jsonify({'message': 'Evaluación actualizada exitosamente', 'evaluacion': evaluacion.to_dict()}), 200

@evaluaciones.route("/delete/<int:id>", methods=['DELETE'])
@handle_errors
def delete(id):
    evaluacion = Evaluacion.query.get(id)
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404
    
    db.session.delete(evaluacion)
    db.session.commit()
    
    return jsonify({'message': 'Evaluación eliminada exitosamente'}), 200
