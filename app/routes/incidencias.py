from flask import Blueprint, jsonify, request
from models.incidencia import Incidencia
from utils.db import db
from utils.error_handler import handle_errors
from models.estudiante import Estudiante  # Asegúrate de importar el modelo Estudiante

incidencias = Blueprint('incidencias', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos

@incidencias.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    incidencias = Incidencia.query.all()
    incidencias_list = [incidencia.to_dict() for incidencia in incidencias]
    return jsonify(incidencias_list), 200

@incidencias.route("/get_by_dni/<dni_estudiante>", methods=['GET'])
@handle_errors
def get_by_dni(dni_estudiante):
    incidencias = Incidencia.query.filter_by(dni_estudiante=dni_estudiante).all()
    if not incidencias:
        return jsonify({'error': 'No se encontraron incidencias para este estudiante'}), 404

    incidencias_list = [incidencia.to_dict() for incidencia in incidencias]
    return jsonify(incidencias_list), 200

@incidencias.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    required_fields = ['dni_estudiante', 'descripcion']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({'error': 'Campos faltantes o vacíos', 'missing_fields': missing_fields}), 400

    dni_estudiante = data['dni_estudiante']

    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'El DNI del estudiante no está registrado'}), 404

    descripcion = data['descripcion']

    # Crear la nueva incidencia
    nueva_incidencia = Incidencia(
        dni_estudiante=dni_estudiante,
        descripcion=descripcion
    )

    db.session.add(nueva_incidencia)
    db.session.commit()

    return jsonify({'message': 'Incidencia creada exitosamente', 'incidencia': nueva_incidencia.to_dict()}), 201

@incidencias.route("/update/<int:id_incidencia>", methods=['PATCH'])
@handle_errors
def update(id_incidencia):
    data = request.get_json()
    incidencia = Incidencia.query.filter_by(id_incidencia=id_incidencia).first()

    if not incidencia:
        return jsonify({'error': 'Incidencia no encontrada'}), 404

    # Actualizar campos de la incidencia
    if 'descripcion' in data:
        incidencia.descripcion = data['descripcion']

    db.session.commit()

    return jsonify({'message': 'Incidencia actualizada exitosamente', 'incidencia': incidencia.to_dict()}), 200

@incidencias.route("/delete/<int:id_incidencia>", methods=['DELETE'])
@handle_errors
def delete(id_incidencia):
    incidencia = Incidencia.query.filter_by(id_incidencia=id_incidencia).first()

    if not incidencia:
        return jsonify({'error': 'Incidencia no encontrada'}), 404

    db.session.delete(incidencia)
    db.session.commit()

    return jsonify({'message': 'Incidencia eliminada exitosamente', 'id_incidencia': id_incidencia}), 200

# --------------------------------------------------------
@incidencias.route("/get_by_estudiante/<dni_estudiante>", methods=['GET'])
@handle_errors
def get_by_estudiante(dni_estudiante):
    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'El DNI del estudiante no está registrado'}), 404

    incidencias = Incidencia.query.filter_by(dni_estudiante=dni_estudiante).all()
    incidencias_list = [incidencia.to_dict() for incidencia in incidencias]

    return jsonify({
        'dni_estudiante': dni_estudiante,
        'incidencias': incidencias_list
    }), 200