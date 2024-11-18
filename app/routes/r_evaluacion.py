from flask import Blueprint, jsonify, request
from models.evaluacion import Evaluacion
from models.curso import Curso
from models.docente import Docente
from models.codigo import  Codigo
from models.usuario import Usuario
from models.matricula import Matricula
from utils.db import db
from utils.error_handler import handle_errors
from utils.plagiarism_checker_tf_idf import plagiarism_checker
from utils.google_ai import GoogleGenerativeAI, ask_to_ia_google

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
def get_by_id(id_evaluacion):
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
    '''if Evaluacion.query.filter_by(nombre=nombre).first():
        return jsonify({'error': 'Ya existe una evaluación con ese nombre'}), 409
    '''
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


# Obtener todas las evaluaciones por id_curso
@evaluacion.route("/get_by_curso/<int:id_curso>", methods=['GET'])
@handle_errors
def get_evaluaciones_by_curso(id_curso):
    # Verificar si el curso existe
    curso = Curso.query.filter_by(id_curso=id_curso).first()
    if not curso:
        return jsonify({'error': 'El curso no existe'}), 404

    # Obtener todas las evaluaciones asociadas a ese curso
    evaluaciones = Evaluacion.query.filter_by(id_curso=id_curso).all()

    if not evaluaciones:
        return jsonify({'message': 'No hay evaluaciones para este curso'}), 200

    evaluaciones_list = [evaluacion.to_dict() for evaluacion in evaluaciones]
    return jsonify(evaluaciones_list), 200


@evaluacion.route("/get_evaluaciones_by_docente/<string:dni_docente>", methods=['GET'])
@handle_errors
def get_evaluaciones_by_docente(dni_docente):
    # Verificar si el docente existe
    docente = Docente.query.filter_by(dni_usuario=dni_docente).first()
    if not docente:
        return jsonify({'error': 'Docente no encontrado'}), 404

    # Obtener todos los cursos que imparte el docente
    cursos = Curso.query.filter_by(dni_docente=dni_docente).all()

    if not cursos:
        return jsonify({'message': 'No hay cursos asociados a este docente'}), 200

    # Preparar la estructura para la respuesta
    response = {
        'cursos': []
    }
    
    for curso in cursos:
        # Obtener todas las evaluaciones asociadas a este curso
        evaluaciones = Evaluacion.query.filter_by(id_curso=curso.id_curso).all()
        
        # Crear la entrada del curso en la respuesta
        curso_info = {
            'curso': {
                # 'dni_docente': curso.dni_docente,
                'id_curso': curso.id_curso,
                'nombre': curso.nombre
            },
            'evaluaciones': []
        }
        
        # Agregar evaluaciones al curso
        for evaluacion in evaluaciones:
            curso_info['evaluaciones'].append(evaluacion.to_dict())

        response['cursos'].append(curso_info)

    return jsonify(response), 200

# Ruta para realizar revision con metodo tf idf
@evaluacion.route("/make_review_tf_idf/<int:id_evaluacion>", methods=['POST'])
@handle_errors
def make_review_tf_idf(id_evaluacion):
    # Verificar si el parámetro 'threshold' está presente en la solicitud
    threshold = request.json.get('threshold')
    if threshold is None:
        return jsonify({'message': 'El parámetro "threshold" es obligatorio.'}), 400

    # Obtener los códigos entregados por la evaluación
    codigos = (
        db.session.query(
            Codigo.id_codigo,
            Codigo.url_codigo,
            Codigo.codigo_sql,
            Usuario.dni,
            Usuario.nombres,
            Usuario.apellidos
        )
        .join(Matricula, Codigo.id_matricula == Matricula.id_matricula)
        .join(Usuario, Matricula.dni_estudiante == Usuario.dni)
        .filter(Codigo.id_evaluacion == id_evaluacion)
        .all()
    )

    # Verificar si existen códigos
    if not codigos:
        return jsonify({'message': 'No se encontraron códigos para esta evaluación'}), 404
    if len(codigos)<2:
        return jsonify({'message': 'Debe haber como minimo 2 códigos para comparar'}), 404

    # Formatear los datos para el verificador de plagio
    datos = [
        {
            'id_codigo': codigo.id_codigo,
            'url_codigo': codigo.url_codigo,
            'codigo_sql': codigo.codigo_sql,
            'estudiante': {
                'dni': codigo.dni,
                'nombres': codigo.nombres,
                'apellidos': codigo.apellidos
            }
        }
        for codigo in codigos
    ]

    # Verificar el plagio con el threshold proporcionado
    result = plagiarism_checker(datos, threshold)

    # Devolver el resultado como JSON
    return jsonify(result), 200

# Ruta para interactuar con la IA
@evaluacion.route("/make_review_ia_gemini/<int:id_evaluacion>", methods=['POST'])
@handle_errors
def make_review_ia_gemini(id_evaluacion):
    # Obtener el prompt, threshold y métrica del cuerpo de la solicitud
    data = request.json
    prompt_contexto = data.get('prompt_contexto', "Eres un experto en bases de datos SQL para MySQL.")
    threshold = data.get('threshold')
    metrica = data.get('metrica')

    if not prompt_contexto or threshold is None or not metrica:
        return jsonify({'message': 'El "prompt_contexto", "threshold" y "metrica" son obligatorios.'}), 400

    # Obtener los códigos entregados por la evaluación
    codigos = (
        db.session.query(
            Codigo.id_codigo,
            Codigo.url_codigo,
            Codigo.codigo_sql,
            Usuario.dni,
            Usuario.nombres,
            Usuario.apellidos
        )
        .join(Matricula, Codigo.id_matricula == Matricula.id_matricula)
        .join(Usuario, Matricula.dni_estudiante == Usuario.dni)
        .filter(Codigo.id_evaluacion == id_evaluacion)
        .all()
    )

    # Verificar si existen códigos
    if not codigos:
        return jsonify({'message': 'No se encontraron códigos para esta evaluación'}), 404
    if len(codigos)<2:
        return jsonify({'message': 'Debe haber como minimo 2 códigos para comparar'}), 404

    # Formatear los datos para enviar a la IA
    datos = [
        {
            'id_codigo': codigo.id_codigo,
            'url_codigo': codigo.url_codigo,
            'codigo_sql': codigo.codigo_sql,
            'estudiante': {
                'dni': codigo.dni,
                'nombres': codigo.nombres,
                'apellidos': codigo.apellidos
            }
        }
        for codigo in codigos
    ]

    # Crear el prompt con el contexto, threshold, métrica y datos de los códigos
    prompt_total = (
        f"{prompt_contexto}\n"
        f"Evalúa los siguientes códigos SQL con un umbral de similitud de {threshold} utilizando la métrica de {metrica}. "
        "Determina si existe algún plagio en los códigos proporcionados, y proporciona un análisis detallado de coincidencias sospechosas asdemás a manera de resumen muestralo en una tabla en ascci.\n\n"
        f"Códigos para evaluar:\n{datos}"
    )

    response_text = ask_to_ia_google(prompt_total)
    if response_text is None:
        return jsonify({'message': 'La IA Gemini no pudo procesar la solicitud.'}), 500
    return jsonify({'result': response_text}), 200
