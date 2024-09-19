from flask import Blueprint, jsonify, request
from models.estudiante import Estudiante
from models.nota_evaluacion import NotaEvaluacion
from models.evaluacion import Evaluacion
from models.documento import Documento
from utils.db import db
from utils.error_handler import handle_errors

notas_evaluaciones = Blueprint('notas_evaluaciones', __name__)

# Crear una nueva nota de evaluación
@notas_evaluaciones.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    id_evaluacion = data.get('id_evaluacion')
    id_documento = data.get('id_documento')
    nota = data.get('nota')

    # Verificar si la evaluación existe
    evaluacion = Evaluacion.query.get(id_evaluacion)
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    # Verificar si el documento existe
    documento = Documento.query.get(id_documento)
    if not documento:
        return jsonify({'error': 'Documento no encontrado'}), 404

    # Crear la nueva nota de evaluación
    nueva_nota_evaluacion = NotaEvaluacion(id_evaluacion=id_evaluacion, id_documento=id_documento, nota=nota)
    db.session.add(nueva_nota_evaluacion)
    db.session.commit()

    return jsonify({
        'message': 'Nota de evaluación creada exitosamente',
        'nota_evaluacion': nueva_nota_evaluacion.to_dict()
    }), 201

# Obtener todas las notas de evaluación
@notas_evaluaciones.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    notas = NotaEvaluacion.query.all()
    notas_list = [nota.to_dict() for nota in notas]
    return jsonify(notas_list), 200

# Obtener una nota de evaluación por ID
@notas_evaluaciones.route("/get_by_id/<int:id_nota_evaluacion>", methods=['GET'])
@handle_errors
def get_by_id(id_nota_evaluacion):
    nota = NotaEvaluacion.query.get(id_nota_evaluacion)
    if not nota:
        return jsonify({'error': 'Nota de evaluación no encontrada'}), 404
    return jsonify(nota.to_dict()), 200

# Actualizar una nota de evaluación
@notas_evaluaciones.route("/update/<int:id_nota_evaluacion>", methods=['PATCH'])
@handle_errors
def update(id_nota_evaluacion):
    data = request.get_json()
    nota = NotaEvaluacion.query.get(id_nota_evaluacion)

    if not nota:
        return jsonify({'error': 'Nota de evaluación no encontrada'}), 404

    # Actualizar campos
    if 'id_evaluacion' in data:
        evaluacion = Evaluacion.query.get(data['id_evaluacion'])
        if not evaluacion:
            return jsonify({'error': 'Evaluación no encontrada'}), 404
        nota.id_evaluacion = data['id_evaluacion']

    if 'id_documento' in data:
        documento = Documento.query.get(data['id_documento'])
        if not documento:
            return jsonify({'error': 'Documento no encontrado'}), 404
        nota.id_documento = data['id_documento']

    if 'nota' in data:
        nota.nota = data['nota']

    db.session.commit()
    return jsonify({'message': 'Nota de evaluación actualizada exitosamente', 'nota_evaluacion': nota.to_dict()}), 200

# Eliminar una nota de evaluación
@notas_evaluaciones.route("/delete/<int:id_nota_evaluacion>", methods=['DELETE'])
@handle_errors
def delete(id_nota_evaluacion):
    nota = NotaEvaluacion.query.get(id_nota_evaluacion)
    if not nota:
        return jsonify({'error': 'Nota de evaluación no encontrada'}), 404

    db.session.delete(nota)
    db.session.commit()
    return jsonify({'message': 'Nota de evaluación eliminada exitosamente', 'id_nota_evaluacion': id_nota_evaluacion}), 200

# Obtener todas las notas de una evaluación específica
@notas_evaluaciones.route("/get_by_evaluacion/<int:id_evaluacion>", methods=['GET'])
@handle_errors
def get_by_evaluacion(id_evaluacion):
    evaluacion = Evaluacion.query.get(id_evaluacion)
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404

    notas = NotaEvaluacion.query.filter_by(id_evaluacion=id_evaluacion).all()
    notas_list = [nota.to_dict() for nota in notas]
    
    return jsonify({
        'id_evaluacion': id_evaluacion,
        'notas': notas_list
    }), 200

# Obtener evaluaciones y notas de un estudiante por DNI
@notas_evaluaciones.route("/get_by_estudiante/<dni_estudiante>", methods=['GET'])
@handle_errors
def get_by_estudiante(dni_estudiante):
    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    # Obtener los documentos asociados a este estudiante
    documentos = Documento.query.filter_by(dni_estudiante=dni_estudiante).all()

    if not documentos:
        return jsonify({'error': 'No se encontraron documentos asociados al estudiante'}), 404

    # Lista para almacenar las evaluaciones y sus notas correspondientes
    evaluaciones_notas = []

    for documento in documentos:
        # Obtener la nota de evaluación asociada al documento
        nota = NotaEvaluacion.query.filter_by(id_documento=documento.id_documento).first()

        if nota:
            # Obtener la evaluación asociada a la nota
            evaluacion = Evaluacion.query.get(nota.id_evaluacion)

            if evaluacion:
                # Agregar la evaluación, la nota y el documento al resultado
                evaluaciones_notas.append({
                    'id_evaluacion': evaluacion.id_evaluacion,
                    'nombre_evaluacion': evaluacion.nombre,
                    'descripcion_evaluacion': evaluacion.descripcion,
                    'duracion_evaluacion': evaluacion.duracion,
                    'nota': str(nota.nota),  # Convertir a string para evitar problemas con decimales
                    'documento': {
                        'id_documento': documento.id_documento,
                        'url_documento': documento.url_documento,
                        'fecha_subida': documento.fecha_subida.isoformat()
                    }
                })

    if not evaluaciones_notas:
        return jsonify({'message': 'El estudiante no tiene evaluaciones con notas registradas'}), 404

    return jsonify({
        'dni_estudiante': dni_estudiante,
        'evaluaciones_notas': evaluaciones_notas
    }), 200