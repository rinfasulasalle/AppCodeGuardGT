from flask import Blueprint, jsonify, request
from models.estado_evaluacion import EstadoEvaluacion
from models.evaluacion import Evaluacion
from models.matricula import Matricula
from utils.db import db
from utils.error_handler import handle_errors
from datetime import datetime
import pytz

PERU_TZ = pytz.timezone('America/Lima')

estado_evaluacion = Blueprint('estado_evaluacion', __name__)

# Estados permitidos
ESTADOS_VALIDOS = {"Pendiente", "Completada", "Calificada"}

# --------------------------------------------------------
# Rutas para manejo de estados de evaluación

# Obtener todos los estados de evaluación
@estado_evaluacion.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    estados = EstadoEvaluacion.query.all()
    estados_list = [estado.to_dict() for estado in estados]
    return jsonify(estados_list), 200

# Crear un nuevo estado de evaluación
@estado_evaluacion.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()

    # Validar datos proporcionados
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400

    id_evaluacion = data.get('id_evaluacion')
    id_matricula = data.get('id_matricula')
    estado = data.get('estado', 'Pendiente')

    # Verificar que la evaluación y la matrícula existan
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()
    matricula = Matricula.query.filter_by(id_matricula=id_matricula).first()

    if not evaluacion:
        return jsonify({'error': 'La evaluación no existe'}), 404
    if not matricula:
        return jsonify({'error': 'La matrícula no existe'}), 404

    # Verificar si ya existe un estado para esa evaluación y matrícula
    estado_existente = EstadoEvaluacion.query.filter_by(id_evaluacion=id_evaluacion, id_matricula=id_matricula).first()
    if estado_existente:
        return jsonify({'error': 'Ya existe un estado para esta evaluación y matrícula'}), 409

    # Validar que el estado proporcionado sea válido
    if estado not in ESTADOS_VALIDOS:
        return jsonify({'error': f'Estado no válido. Estados permitidos: {ESTADOS_VALIDOS}'}), 400

    # Crear nuevo estado de evaluación
    nuevo_estado = EstadoEvaluacion(
        id_evaluacion=id_evaluacion,
        id_matricula=id_matricula,
        estado=estado
    )

    db.session.add(nuevo_estado)
    db.session.commit()

    return jsonify({'message': 'Estado de evaluación creado exitosamente', 'estado': nuevo_estado.to_dict()}), 201

# Actualizar el estado de una evaluación
@estado_evaluacion.route("/update/<int:id_estado_evaluacion>", methods=['PUT'])
@handle_errors
def update(id_estado_evaluacion):
    data = request.get_json()

    # Validar datos proporcionados
    if not data or 'estado' not in data:
        return jsonify({'error': 'Datos no proporcionados o incompletos'}), 400

    nuevo_estado = data['estado']

    # Validar que el estado proporcionado sea válido
    if nuevo_estado not in ESTADOS_VALIDOS:
        return jsonify({'error': f'Estado no válido. Estados permitidos: {ESTADOS_VALIDOS}'}), 400

    estado_evaluacion = EstadoEvaluacion.query.filter_by(id_estado_evaluacion=id_estado_evaluacion).first()

    if not estado_evaluacion:
        return jsonify({'error': 'Estado de evaluación no encontrado'}), 404

    # Actualizar el estado y la fecha de actualización
    estado_evaluacion.estado = nuevo_estado
    estado_evaluacion.fecha_actualizacion = datetime.now(PERU_TZ)

    db.session.commit()

    return jsonify({'message': 'Estado de evaluación actualizado', 'estado': estado_evaluacion.to_dict()}), 200

# Eliminar un estado de evaluación por ID
@estado_evaluacion.route("/delete/<int:id_estado_evaluacion>", methods=['DELETE'])
@handle_errors
def delete(id_estado_evaluacion):
    estado_evaluacion = EstadoEvaluacion.query.filter_by(id_estado_evaluacion=id_estado_evaluacion).first()

    if not estado_evaluacion:
        return jsonify({'error': 'Estado de evaluación no encontrado'}), 404

    db.session.delete(estado_evaluacion)
    db.session.commit()

    return jsonify({'message': 'Estado de evaluación eliminado', 'id_estado_evaluacion': id_estado_evaluacion}), 200
    