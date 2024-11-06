from flask import Blueprint, jsonify, request
from models.curso import Curso
from models.docente import Docente
from utils.db import db
from utils.error_handler import handle_errors
import re

curso = Blueprint('curso', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de cursos

@curso.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    cursos = Curso.query.all()
    cursos_list = [curso.to_dict() for curso in cursos]
    return jsonify(cursos_list), 200

@curso.route("/get_by_id/<int:id_curso>", methods=['GET'])
@handle_errors
def get_by_id(id_curso):
    curso = Curso.query.filter_by(id_curso=id_curso).first()
    if curso:
        return jsonify(curso.to_dict()), 200
    else:
        return jsonify({'error': 'Curso no encontrado'}), 404

@curso.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()
    
    # Validar la estructura de los datos
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400

    dni_docente = data.get('dni_docente')
    nombre = data.get('nombre')

    # Validar DNI del docente
    if not dni_docente or not isinstance(dni_docente, str):
        return jsonify({'error': 'DNI del docente es requerido y debe ser una cadena'}), 400

    # Validar que el docente existe
    if not Docente.query.filter_by(dni_usuario=dni_docente).first():
        return jsonify({'error': 'El docente no existe'}), 404

    # Validar nombre del curso
    if not nombre or not isinstance(nombre, str) or len(nombre) < 1 or len(nombre) > 100:
        return jsonify({'error': 'El nombre del curso es requerido y debe tener entre 1 y 100 caracteres(solo caracteres  o números)'}), 400

    # Verificar si el curso ya existe
    if Curso.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'El curso ya existe'}), 409

    # Crear el nuevo curso
    nuevo_curso = Curso(nombre=nombre, dni_docente=dni_docente)

    db.session.add(nuevo_curso)
    db.session.commit()

    return jsonify({'message': 'Curso agregado exitosamente', 'curso': nuevo_curso.to_dict()}), 201

@curso.route("/delete/<int:id_curso>", methods=['DELETE'])
@handle_errors
def delete(id_curso):
    curso = Curso.query.filter_by(id_curso=id_curso).first()

    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404

    db.session.delete(curso)
    db.session.commit()

    return jsonify({'message': 'Curso eliminado exitosamente', 'id_curso': id_curso}), 200

@curso.route("/update/<int:id_curso>", methods=['PUT'])
@handle_errors
def update(id_curso):
    data = request.get_json()
    curso = Curso.query.filter_by(id_curso=id_curso).first()

    if not curso:
        return jsonify({'error': 'Curso no encontrado'}), 404

    dni_docente = data.get('dni_docente')
    nombre = data.get('nombre')

    # Validar DNI del docente
    if dni_docente and not Docente.query.filter_by(dni_usuario=dni_docente).first():
        return jsonify({'error': 'El docente no existe'}), 404

    # Validar nombre del curso
    if nombre and (not isinstance(nombre, str) or len(nombre) < 1 or len(nombre) > 100):
        return jsonify({'error': 'El nombre del curso es requerido y debe tener entre 1 y 100 caracteres'}), 400

    # Actualizar los campos del curso
    if dni_docente:
        curso.dni_docente = dni_docente
    if nombre:
        # Verificar que el nombre no esté duplicado
        if Curso.query.filter_by(nombre=nombre).first():
            return jsonify({'error': 'El curso con este nombre ya existe'}), 409
        curso.nombre = nombre

    db.session.commit()

    return jsonify({'message': 'Curso actualizado exitosamente', 'curso': curso.to_dict()}), 200

# --------------------------------------------------------
@curso.route("/cursos_por_docente/<string:dni_docente>", methods=['GET'])
@handle_errors
def get_cursos_por_docente(dni_docente):
    # Validar que el DNI sea una cadena y tenga exactamente 8 dígitos numéricos
    if not re.match(r'^\d{8}$', dni_docente):
        return jsonify({'error': 'El DNI del docente debe tener exactamente 8 dígitos'}), 400

    # Verificar si el docente existe
    docente = Docente.query.filter_by(dni_usuario=dni_docente).first()
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404

    # Obtener cursos por dni_docente
    cursos = Curso.query.filter_by(dni_docente=dni_docente).all()

    # Crear lista de cursos solo con id_curso y nombre
    cursos_list = [{'id_curso': curso.id_curso, 'nombre': curso.nombre} for curso in cursos]

    return jsonify({'cursos': cursos_list}), 200
