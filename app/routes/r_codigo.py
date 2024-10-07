from flask import Blueprint, jsonify, request
from models.codigo import Codigo
from models.evaluacion import Evaluacion
from models.matricula import Matricula
from models.curso import Curso
from utils.db import db
from utils.error_handler import handle_errors
import re

codigo = Blueprint('codigo', __name__)

# --------------------------------------------------------
# Rutas para manejo de datos de códigos

# Obtener todos los códigos
@codigo.route("/get_all", methods=['GET'])
@handle_errors
def get_all():
    codigos = Codigo.query.all()
    codigos_list = [codigo.to_dict() for codigo in codigos]
    return jsonify(codigos_list), 200

@codigo.route("/create", methods=['POST'])
@handle_errors
def create():
    data = request.get_json()

    # Validar la estructura de los datos
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400

    id_evaluacion = data.get('id_evaluacion')
    id_matricula = data.get('id_matricula')
    url_codigo = data.get('url_codigo')

    # Verificar que la evaluación y la matrícula existan
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()
    matricula = Matricula.query.filter_by(id_matricula=id_matricula).first()

    if not evaluacion:
        return jsonify({'error': 'La evaluación no existe'}), 404

    if not matricula:
        return jsonify({'error': 'La matrícula no existe'}), 404

    # Validar que no exista un código para la misma evaluación y matrícula
    codigo_existente = Codigo.query.filter_by(id_evaluacion=id_evaluacion, id_matricula=id_matricula).first()
    if codigo_existente:
        return jsonify({'error': 'Ya existe un código para esta evaluación y matrícula'}), 409

    # Validar que el curso relacionado tanto a la evaluación como a la matrícula sea el mismo
    curso_evaluacion = evaluacion.id_curso
    curso_matricula = matricula.id_curso

    if curso_evaluacion != curso_matricula:
        return jsonify({'error': 'El curso asociado a la evaluación y la matrícula no coincide'}), 400

    # Validar que el URL comience con 'https://sqlfiddle.com/mysql/online-compiler?id='
    url_prefix = 'https://sqlfiddle.com/mysql/online-compiler?id='
    if not url_codigo or not url_codigo.startswith(url_prefix):
        return jsonify({'error': 'El URL del código no tiene un formato válido'}), 400

    # Crear el nuevo código
    nuevo_codigo = Codigo(id_evaluacion=id_evaluacion, id_matricula=id_matricula, url_codigo=url_codigo)

    db.session.add(nuevo_codigo)
    db.session.commit()

    return jsonify({'message': 'Código creado exitosamente', 'codigo': nuevo_codigo.to_dict()}), 201

# Eliminar un código por ID
@codigo.route("/delete/<int:id_codigo>", methods=['DELETE'])
@handle_errors
def delete(id_codigo):
    codigo = Codigo.query.filter_by(id_codigo=id_codigo).first()

    if not codigo:
        return jsonify({'error': 'Código no encontrado'}), 404

    db.session.delete(codigo)
    db.session.commit()

    return jsonify({'message': 'Código eliminado exitosamente', 'id_codigo': id_codigo}), 200
