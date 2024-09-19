from flask import Blueprint, jsonify, request
from models.evaluacion import Evaluacion
from models.docente import Docente
from models.usuario import Usuario
from utils.db import db
from utils.error_handler import handle_errors

evaluaciones = Blueprint('evaluaciones', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de evaluaciones

@evaluaciones.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    evaluaciones = Evaluacion.query.all()
    evaluaciones_list = []

    for evaluacion in evaluaciones:
        # Buscar la información del docente
        docente = Docente.query.filter_by(dni_usuario=evaluacion.dni_docente).first()
        if docente:
            usuario = Usuario.query.filter_by(dni=docente.dni_usuario).first()

            # Añadir la información del docente al diccionario de la evaluación
            evaluaciones_list.append({
                'id_evaluacion': evaluacion.id_evaluacion,
                'nombre': evaluacion.nombre,
                'descripcion': evaluacion.descripcion,
                'duracion': evaluacion.duracion,
                'dni_docente': evaluacion.dni_docente,
                'info_docente': {
                    'nombres': usuario.nombres,
                    'apellidos': usuario.apellidos,
                    'correo': usuario.correo
                }
            })
    
    return jsonify(evaluaciones_list), 200

@evaluaciones.route("/get_by_id/<int:id_evaluacion>", methods=['GET'])
@handle_errors
def get_by_id(id_evaluacion):
    # Buscar la evaluación por su ID
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    # Buscar la información del docente asociado
    docente = Docente.query.filter_by(dni_usuario=evaluacion.dni_docente).first()
    if docente:
        usuario = Usuario.query.filter_by(dni=docente.dni_usuario).first()

        return jsonify({
            'id_evaluacion': evaluacion.id_evaluacion,
            'nombre': evaluacion.nombre,
            'descripcion': evaluacion.descripcion,
            'duracion': evaluacion.duracion,
            'dni_docente': evaluacion.dni_docente,
            'info_docente': {
                'nombres': usuario.nombres,
                'apellidos': usuario.apellidos,
                'correo': usuario.correo
            }
        }), 200

    return jsonify({'error': 'Docente asociado no encontrado'}), 404

@evaluaciones.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    duracion = data.get('duracion')
    dni_docente = data.get('dni_docente')

    # Validar que los campos no estén vacíos
    if not nombre or not duracion or not dni_docente:
        return jsonify({'error': 'Faltan datos obligatorios (nombre, duración, dni_docente)'}), 400

    # Validar que el docente exista
    docente = Docente.query.filter_by(dni_usuario=dni_docente).first()
    if not docente:
        return jsonify({'error': 'El DNI del docente no está registrado'}), 404

    # Verificar si el nombre de la evaluación ya existe
    if Evaluacion.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'El nombre de la evaluación ya está en uso'}), 409  # Error 409: Conflicto

    # Crear la nueva evaluación
    nueva_evaluacion = Evaluacion(nombre=nombre, descripcion=descripcion, duracion=duracion, dni_docente=dni_docente)
    db.session.add(nueva_evaluacion)
    db.session.commit()

    return jsonify({'message': 'Evaluación creada exitosamente', 'evaluacion': nueva_evaluacion.to_dict()}), 201

@evaluaciones.route("/update/<int:id_evaluacion>", methods=['PATCH'])
@handle_errors
def update(id_evaluacion):
    data = request.get_json()
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()

    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    # Validar que el nuevo docente exista si se proporciona
    nuevo_dni_docente = data.get('dni_docente')
    if nuevo_dni_docente:
        docente = Docente.query.filter_by(dni_usuario=nuevo_dni_docente).first()
        if not docente:
            return jsonify({'error': 'El nuevo DNI del docente no está registrado'}), 404

    # Actualizar los campos de la evaluación
    if 'nombre' in data:
        evaluacion.nombre = data['nombre']
    if 'descripcion' in data:
        evaluacion.descripcion = data['descripcion']
    if 'duracion' in data:
        evaluacion.duracion = data['duracion']
    
    # Actualizar el dni_docente si se proporciona un nuevo DNI
    if nuevo_dni_docente:
        evaluacion.dni_docente = nuevo_dni_docente

    # Guardar los cambios
    db.session.commit()

    return jsonify({'message': 'Evaluación actualizada exitosamente', 'evaluacion': evaluacion.to_dict()}), 200

@evaluaciones.route("/delete/<int:id_evaluacion>", methods=['DELETE'])
@handle_errors
def delete(id_evaluacion):
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()

    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    db.session.delete(evaluacion)
    db.session.commit()

    return jsonify({'message': 'Evaluación eliminada exitosamente', 'id_evaluacion': id_evaluacion}), 200

# --------------------------------------------------------