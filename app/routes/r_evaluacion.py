from flask import Blueprint, jsonify, request
from datetime import datetime
import os
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
from utils.smtpSenderEmail import SmtpSenderEmail

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

# Obtener todos los códigos asociados a una evaluación
@evaluacion.route("/get_codigos_by_evaluacion/<int:id_evaluacion>", methods=['GET'])
@handle_errors
def get_codigos_by_evaluacion(id_evaluacion):
    # Obtener los códigos asociados a la evaluación usando el id_evaluacion
    codigos = (
        db.session.query(
            Codigo.id_codigo,
            Codigo.url_codigo,
            #Codigo.codigo_sql,
            Usuario.dni,
            Usuario.nombres,
            Usuario.apellidos
        )
        .join(Matricula, Codigo.id_matricula == Matricula.id_matricula)
        .join(Usuario, Matricula.dni_estudiante == Usuario.dni)
        .filter(Codigo.id_evaluacion == id_evaluacion)
        .all()
    )

    # Verificar si se encontraron códigos
    if not codigos:
        return jsonify({'message': 'No se encontraron códigos para esta evaluación'}), 404

    # Formatear los datos para la respuesta
    codigos_list = [
        {
            'id_codigo': codigo.id_codigo,
            'url_codigo': codigo.url_codigo,
            #'codigo_sql': codigo.codigo_sql,
            'estudiante': {
                'dni': codigo.dni,
                'nombres': codigo.nombres,
                'apellidos': codigo.apellidos
            }
        }
        for codigo in codigos
    ]

    return jsonify(codigos_list), 200

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
    return jsonify("result"), 200

# Ruta para interactuar con la IA
@evaluacion.route("/make_review_ia_gemini/<int:id_evaluacion>", methods=['POST'])
@handle_errors
def make_review_ia_gemini(id_evaluacion):
    # Obtener el prompt, threshold y métrica del cuerpo de la solicitud
    data = request.json
    prompt_contexto = "Eres un experto en bases de datos SQL para MySQL."
    threshold = data.get('threshold')
    metrica = data.get('metrica')

    # Validar los parámetros obligatorios
    if threshold is None or not metrica:
        return jsonify({'message': '"threshold" y "metrica" son obligatorios.'}), 400

    # Obtener el dni_docente y correo del docente
    docente_info = db.session.query(Curso.dni_docente, Usuario.correo) \
                             .join(Docente, Docente.dni_usuario == Curso.dni_docente) \
                             .join(Usuario, Usuario.dni == Docente.dni_usuario) \
                             .join(Evaluacion, Evaluacion.id_curso == Curso.id_curso) \
                             .filter(Evaluacion.id_evaluacion == id_evaluacion) \
                             .first()

    if not docente_info:
        return jsonify({'message': 'No se encontró al docente o correo asociado a esta evaluación.'}), 404

    dni_docente, correo_docente = docente_info

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
    if len(codigos) < 2:
        return jsonify({'message': 'Debe haber como mínimo 2 códigos para comparar'}), 404

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
        "Determina si existe algún plagio en los códigos proporcionados, y proporciona un análisis detallado de coincidencias sospechosas. "
        "Además, a manera de resumen, muéstralo en una tabla en csv.\n\n"
        f"Códigos para evaluar:\n{datos}"
    )

    # Interactuar con la IA Gemini
    response_text = ask_to_ia_google(prompt_total)
    if response_text is None:
        return jsonify({'message': 'La IA Gemini no pudo procesar la solicitud.'}), 500

    # Obtener la fecha y hora actual para el nombre del archivo
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Nombre del archivo .md basado en el dni_docente y la fecha/hora
    filename = f"reporte_{dni_docente}_{timestamp}.md"
    filepath = os.path.join('reports', filename)

    # Guardar la respuesta de la IA en el archivo .md
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"# Reporte de Evaluación\n\n")
            file.write(f"**Evaluación ID**: {id_evaluacion}\n\n")
            file.write(f"**Resultado de la IA Gemini**:\n\n{response_text}\n")
    except Exception as e:
        return jsonify({'message': f'Error al guardar el archivo: {str(e)}'}), 500

    # Crear el mensaje para el correo
    mensaje = (
        f"Se ha generado un reporte de evaluación para la evaluación ID: {id_evaluacion}.\n"
        f"Fecha del reporte: {datetime.now().strftime('%d-%m-%Y')}\n\n"
        f"Este correo contiene el reporte generado por la IA Gemini.\n\n"
        f"Adjunto encontrarás el archivo con el análisis del plagio."
    )

    # Enviar el correo con el archivo .md adjunto
    smtp = SmtpSenderEmail()  # Instanciamos el sender de correo
    email_sent = smtp.send_email(correo_docente, mensaje, filepath)

    # Verificar si el correo se envió correctamente
    if not email_sent:
        return jsonify({'message': 'Hubo un error al enviar el correo.'}), 500

    # Confirmar que el archivo se ha creado y el correo enviado
    return jsonify({'message': f'Correo enviado exitosamente al docente: {correo_docente}. El archivo {filename} ha sido adjuntado.'}), 200