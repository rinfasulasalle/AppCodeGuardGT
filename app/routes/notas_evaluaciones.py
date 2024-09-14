from flask import Blueprint, jsonify, request
from models.nota_evaluacion import NotaEvaluacion
from models.estudiante import Estudiante
from models.evaluacion import Evaluacion
from utils.db import db
from utils.error_handler import handle_errors

notas_evaluaciones = Blueprint('notas_evaluaciones', __name__)

@notas_evaluaciones.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    notas = NotaEvaluacion.query.all()
    notas_list = [nota.to_dict() for nota in notas]
    return jsonify(notas_list), 200

@notas_evaluaciones.route("/get_by_id/<int:id>", methods=['GET'])
@handle_errors
def get_by_id(id):
    nota = NotaEvaluacion.query.get(id)
    if nota:
        return jsonify(nota.to_dict()), 200
    else:
        return jsonify({'error': 'Nota no encontrada'}), 404

@notas_evaluaciones.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    
    dni_estudiante = data.get('dni_estudiante')
    id_evaluacion = data.get('id_evaluacion')
    nota = data.get('nota')
    
    if dni_estudiante is None or id_evaluacion is None or nota is None:
        return jsonify({'error': 'dni_estudiante, id_evaluacion y nota son requeridos'}), 400

    try:
        nota = float(nota)  # Convertir nota a float
    except ValueError:
        return jsonify({'error': 'Nota debe ser un número decimal válido'}), 400

    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    # Verificar si la evaluación existe
    evaluacion = Evaluacion.query.get(id_evaluacion)
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    # Verificar si ya existe una nota para el estudiante en la misma evaluación
    existing_nota = NotaEvaluacion.query.filter_by(dni_estudiante=dni_estudiante, id_evaluacion=id_evaluacion).first()
    if existing_nota:
        return jsonify({'error': 'El estudiante ya tiene una nota para esta evaluación'}), 400

    nueva_nota = NotaEvaluacion(dni_estudiante, id_evaluacion, nota)
    db.session.add(nueva_nota)
    db.session.commit()
    
    return jsonify({'message': 'Nota creada exitosamente', 'nota': nueva_nota.to_dict()}), 201

@notas_evaluaciones.route("/update/<int:id>", methods=['PATCH'])
@handle_errors
def update(id):
    data = request.get_json()
    nota = NotaEvaluacion.query.get(id)
    
    if not nota:
        return jsonify({'error': 'Nota no encontrada'}), 404

    if 'dni_estudiante' in data:
        estudiante = Estudiante.query.filter_by(dni_usuario=data['dni_estudiante']).first()
        if not estudiante:
            return jsonify({'error': 'Estudiante no encontrado'}), 404
        nota.dni_estudiante = data['dni_estudiante']
        
    if 'id_evaluacion' in data:
        evaluacion = Evaluacion.query.get(data['id_evaluacion'])
        if not evaluacion:
            return jsonify({'error': 'Evaluación no encontrada'}), 404
        nota.id_evaluacion = data['id_evaluacion']
        
    if 'nota' in data:
        try:
            nota.nota = float(data['nota'])  # Convertir nota a float
        except ValueError:
            return jsonify({'error': 'Nota debe ser un número decimal válido'}), 400
    
    db.session.commit()
    
    return jsonify({'message': 'Nota actualizada exitosamente', 'nota': nota.to_dict()}), 200

@notas_evaluaciones.route("/delete/<int:id>", methods=['DELETE'])
@handle_errors
def delete(id):
    nota = NotaEvaluacion.query.get(id)
    if not nota:
        return jsonify({'error': 'Nota no encontrada'}), 404
    
    db.session.delete(nota)
    db.session.commit()
    
    return jsonify({'message': 'Nota eliminada exitosamente'}), 200
