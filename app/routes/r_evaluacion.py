from flask import Blueprint, jsonify, request
from models.evaluacion import Evaluacion
from models.curso import Curso
from utils.db import db
from utils.error_handler import handle_errors

evaluacion = Blueprint('evaluacion', __name__)

# --------------------------------------------------------
# Rutas para manejo de evaluaciones

# Obtener todas las evaluaciones
@evaluacion.route("/get_all", methods=['GET'])
@handle_errors
def get_all_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    evaluaciones_list = [evaluacion.to_dict() for evaluacion in evaluaciones]
    return jsonify(evaluaciones_list), 200

# Obtener una evaluación por su ID
@evaluacion.route("/get_by_id/<int:id_evaluacion>", methods=['GET'])
@handle_errors
def get_evaluacion_by_id(id_evaluacion):
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()
    if evaluacion:
        return jsonify(evaluacion.to_dict()), 200
    else:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

# Crear una nueva evaluación
@evaluacion.route("/create", methods=['POST'])
@handle_errors
def create_evaluacion():
    data = request.get_json()
    
    # Validar que los datos están presentes
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400

    id_curso = data.get('id_curso')
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    # Validar curso
    if not id_curso or not isinstance(id_curso, int):
        return jsonify({'error': 'id_curso es requerido y debe ser un número'}), 400
    
    # Verificar si el curso existe
    curso = Curso.query.filter_by(id_curso=id_curso).first()
    if not curso:
        return jsonify({'error': 'El curso no existe'}), 404

    # Validar nombre de evaluación
    if not nombre or not isinstance(nombre, str) or len(nombre) < 1 or len(nombre) > 100:
        return jsonify({'error': 'El nombre de la evaluación es requerido y debe tener entre 1 y 100 caracteres'}), 400

    # Verificar si el nombre de la evaluación ya existe
    if Evaluacion.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'Ya existe una evaluación con ese nombre'}), 409

    # Crear nueva evaluación
    nueva_evaluacion = Evaluacion(id_curso=id_curso, nombre=nombre,descripcion= descripcion)
    db.session.add(nueva_evaluacion)
    db.session.commit()

    return jsonify({'message': 'Evaluación creada exitosamente', 'evaluacion': nueva_evaluacion.to_dict()}), 201

# Eliminar una evaluación
@evaluacion.route("/delete/<int:id_evaluacion>", methods=['DELETE'])
@handle_errors
def delete_evaluacion(id_evaluacion):
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()

    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    db.session.delete(evaluacion)
    db.session.commit()

    return jsonify({'message': 'Evaluación eliminada exitosamente', 'id_evaluacion': id_evaluacion}), 200

# Actualizar una evaluación
@evaluacion.route("/update/<int:id_evaluacion>", methods=['PUT'])
@handle_errors
def update_evaluacion(id_evaluacion):
    data = request.get_json()
    
    # Buscar la evaluación
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    id_curso = data.get('id_curso')
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    # Validar curso
    if id_curso and not Curso.query.filter_by(id_curso=id_curso).first():
        return jsonify({'error': 'El curso no existe'}), 404

    # Validar nombre de la evaluación
    if nombre and (not isinstance(nombre, str) or len(nombre) < 1 or len(nombre) > 100):
        return jsonify({'error': 'El nombre de la evaluación es requerido y debe tener entre 1 y 100 caracteres'}), 400

    # Actualizar datos
    if id_curso:
        evaluacion.id_curso = id_curso
    if nombre:
        # Verificar si el nombre ya existe en otra evaluación
        if Evaluacion.query.filter(Evaluacion.nombre == nombre, Evaluacion.id_evaluacion != id_evaluacion).first():
            return jsonify({'error': 'El nombre de la evaluación ya existe'}), 409
        evaluacion.nombre = nombre
    if descripcion:
        evaluacion.descripcion = descripcion

    db.session.commit()

    return jsonify({'message': 'Evaluación actualizada exitosamente', 'evaluacion': evaluacion.to_dict()}), 200