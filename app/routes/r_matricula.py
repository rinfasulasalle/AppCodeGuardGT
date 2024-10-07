from flask import Blueprint, jsonify, request
from models.matricula import Matricula
from models.estudiante import Estudiante
from models.curso import Curso
from utils.db import db
from utils.error_handler import handle_errors
import re

matricula = Blueprint('matricula', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de matrículas

@matricula.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    matriculas = Matricula.query.all()
    matriculas_list = [matricula.to_dict() for matricula in matriculas]
    return jsonify(matriculas_list), 200

@matricula.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()

    # Validar la estructura de los datos
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400

    dni_estudiante = data.get('dni_estudiante')
    id_curso = data.get('id_curso')

    # Validar DNI del estudiante
    if not dni_estudiante or not isinstance(dni_estudiante, str):
        return jsonify({'error': 'DNI del estudiante es requerido y debe ser una cadena'}), 400

    # Validar que el estudiante existe
    if not Estudiante.query.filter_by(dni_usuario=dni_estudiante).first():
        return jsonify({'error': 'El estudiante no existe'}), 404

    # Validar que el curso existe
    if not Curso.query.filter_by(id_curso=id_curso).first():
        return jsonify({'error': 'El curso no existe'}), 404

    # Verificar si el estudiante ya está matriculado en el curso
    if Matricula.query.filter_by(dni_estudiante=dni_estudiante, id_curso=id_curso).first():
        return jsonify({'error': 'El estudiante ya está matriculado en este curso'}), 409

    # Crear la nueva matrícula
    nueva_matricula = Matricula(dni_estudiante=dni_estudiante, id_curso=id_curso)

    db.session.add(nueva_matricula)
    db.session.commit()

    return jsonify({'message': 'Matrícula agregada exitosamente', 'matricula': nueva_matricula.to_dict()}), 201

@matricula.route("/delete/<int:id_matricula>", methods=['DELETE'])
@handle_errors
def delete(id_matricula):
    matricula = Matricula.query.filter_by(id_matricula=id_matricula).first()

    if not matricula:
        return jsonify({'error': 'Matrícula no encontrada'}), 404

    db.session.delete(matricula)
    db.session.commit()

    return jsonify({'message': 'Matrícula eliminada exitosamente', 'id_matricula': id_matricula}), 200

# --------------------------------------------------------
# Ruta para obtener cursos por DNI del estudiante
@matricula.route("/cursos_por_estudiante/<string:dni_estudiante>", methods=['GET'])
@handle_errors
def get_cursos_por_estudiante(dni_estudiante):
    # Validar que el DNI sea una cadena y tenga exactamente 8 dígitos numéricos
    if not re.match(r'^\d{8}$', dni_estudiante):
        return jsonify({'error': 'El DNI del estudiante debe tener exactamente 8 dígitos'}), 400

    # Verificar si el estudiante existe
    estudiante = Estudiante.query.filter_by(dni_usuario=dni_estudiante).first()
    if not estudiante:
        return jsonify({'error': 'Estudiante no encontrado'}), 404

    # Obtener todas las matrículas del estudiante
    matriculas = Matricula.query.filter_by(dni_estudiante=dni_estudiante).all()

    # Crear lista de cursos
    cursos_list = []
    for matricula in matriculas:
        curso = Curso.query.filter_by(id_curso=matricula.id_curso).first()
        if curso:
            cursos_list.append({
                'id_curso': curso.id_curso,
                'nombre': curso.nombre,
                'dni_docente': curso.dni_docente
            })

    return jsonify({'cursos': cursos_list}), 200
