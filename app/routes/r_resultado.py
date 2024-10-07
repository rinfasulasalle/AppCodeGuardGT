from flask import Blueprint, jsonify, request
from models.resultado import Resultado
from models.codigo import Codigo
from utils.db import db
from utils.error_handler import handle_errors

resultado = Blueprint('resultado', __name__)

# --------------------------------------------------------
# Rutas para manejo de resultados

# Obtener todos los resultados
@resultado.route("/get_all", methods=['GET'])
@handle_errors
def get_all_resultados():
    resultados = Resultado.query.all()
    resultados_list = [resultado.to_dict() for resultado in resultados]
    return jsonify(resultados_list), 200

# Obtener un resultado por su ID
@resultado.route("/get_by_id/<int:id_resultado>", methods=['GET'])
@handle_errors
def get_resultado_by_id(id_resultado):
    resultado = Resultado.query.filter_by(id_resultado=id_resultado).first()
    if resultado:
        return jsonify(resultado.to_dict()), 200
    else:
        return jsonify({'error': 'Resultado no encontrado'}), 404

# Crear un nuevo resultado
@resultado.route("/create", methods=['POST'])
@handle_errors
def create_resultado():
    data = request.get_json()
    
    # Validar que los datos están presentes
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400

    id_codigo = data.get('id_codigo')
    calificacion = data.get('calificacion')

    # Verificar que el código exista
    codigo = Codigo.query.filter_by(id_codigo=id_codigo).first()
    if not codigo:
        return jsonify({'error': 'El código no existe'}), 404

    # Validar que no exista un resultado para el mismo código
    resultado_existente = Resultado.query.filter_by(id_codigo=id_codigo).first()
    if resultado_existente:
        return jsonify({'error': 'Ya existe un resultado para este código'}), 409

    # Validar la calificación
    if calificacion is None or not (0 <= calificacion <= 20):
        return jsonify({'error': 'La calificación debe ser un número decimal entre 0 y 20'}), 400

    # Crear nuevo resultado
    nuevo_resultado = Resultado(id_codigo=id_codigo, calificacion=calificacion)

    db.session.add(nuevo_resultado)
    db.session.commit()

    return jsonify({'message': 'Resultado creado exitosamente', 'resultado': nuevo_resultado.to_dict()}), 201

# Eliminar un resultado
@resultado.route("/delete/<int:id_resultado>", methods=['DELETE'])
@handle_errors
def delete_resultado(id_resultado):
    resultado = Resultado.query.filter_by(id_resultado=id_resultado).first()

    if not resultado:
        return jsonify({'error': 'Resultado no encontrado'}), 404

    db.session.delete(resultado)
    db.session.commit()

    return jsonify({'message': 'Resultado eliminado exitosamente', 'id_resultado': id_resultado}), 200

# Actualizar un resultado
@resultado.route("/update/<int:id_resultado>", methods=['PUT'])
@handle_errors
def update_resultado(id_resultado):
    data = request.get_json()
    
    # Buscar el resultado
    resultado = Resultado.query.filter_by(id_resultado=id_resultado).first()
    if not resultado:
        return jsonify({'error': 'Resultado no encontrado'}), 404

    id_codigo = data.get('id_codigo')
    calificacion = data.get('calificacion')

    # Validar que el código exista
    if id_codigo and not Codigo.query.filter_by(id_codigo=id_codigo).first():
        return jsonify({'error': 'El código no existe'}), 404

    # Validar la calificación
    if calificacion is not None and not (0 <= calificacion <= 20):
        return jsonify({'error': 'La calificación debe ser un número decimal entre 0 y 20'}), 400

    # Actualizar datos
    if id_codigo:
        resultado.id_codigo = id_codigo
    if calificacion is not None:
        resultado.calificacion = calificacion

    db.session.commit()

    return jsonify({'message': 'Resultado actualizado exitosamente', 'resultado': resultado.to_dict()}), 200
