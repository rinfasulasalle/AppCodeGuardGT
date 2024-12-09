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
from utils.report_td_idf import generate_pdf

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

# Obtener una evaluación por su ID con detalles adicionales
@evaluacion.route("/get_by_id/<int:id_evaluacion>", methods=['GET'])
@handle_errors
def get_by_id(id_evaluacion):
    # Buscar la evaluación por su ID
    evaluacion = Evaluacion.query.filter_by(id_evaluacion=id_evaluacion).first()
    
    if not evaluacion:
        return jsonify({'error': 'Evaluación no encontrada'}), 404
    
    # Obtener información del curso relacionado
    curso = Curso.query.filter_by(id_curso=evaluacion.id_curso).first()
    
    if not curso:
        return jsonify({'error': 'Curso asociado no encontrado'}), 404

    # Obtener información del docente relacionado con el curso
    docente = Docente.query.filter_by(dni_usuario=curso.dni_docente).first()
    if not docente:
        return jsonify({'error': 'Docente asociado no encontrado'}), 404

    # Obtener información del usuario relacionado con el docente
    usuario = Usuario.query.filter_by(dni=docente.dni_usuario).first()
    if not usuario:
        return jsonify({'error': 'Usuario asociado al docente no encontrado'}), 404

    # Formatear la respuesta
    evaluacion_data = evaluacion.to_dict()
    evaluacion_data['curso'] = {
        'id_curso': curso.id_curso,
        'nombre': curso.nombre
    }
    evaluacion_data['docente'] = {
        'dni': usuario.dni,
        'nombres': usuario.nombres,
        'apellidos': usuario.apellidos
    }

    return evaluacion_data

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

# Ruta para realizar revisión de códigos usando el método TF-IDF
@evaluacion.route("/make_review_tf_idf/<int:id_evaluacion>", methods=['POST'])
@handle_errors
def make_review_tf_idf(id_evaluacion):
    try:
        # Obtener el umbral y el correo del cuerpo de la solicitud
        threshold = request.json.get('threshold')
        email = request.json.get('email')

        # Obtener los códigos y formatear los datos
        codigos = obtener_codigos_por_evaluacion(id_evaluacion)
        datos = formatear_datos_codigos(codigos)

        # Realizar la revisión de plagio
        result = plagiarism_checker(datos, threshold)

        # Obtener los datos de la evaluación
        header = get_by_id(id_evaluacion)

        # Generar el PDF con los resultados
        pdf_path = generate_pdf(header, result, "TF-IDF")

        # Configurar el mensaje del correo
        mensaje = (
            f"Estimado/a,\n\n"
            f"Adjunto encontrará el reporte de la evaluación realizada con el método TF-IDF.\n\n"
            f"Detalles de la evaluación:\n"
            f"- Curso: {header['curso']['nombre']}\n"
            f"- Evaluación: {header['nombre']}\n"
            f"- Umbral: {threshold}\n\n"
            f"Saludos,\nCodeGuard"
        )

        # Enviar el correo con el PDF adjunto
        smtp_sender = SmtpSenderEmail()
        smtp_sender.send_email(email, mensaje, pdf_path)

        # Responder indicando éxito
        return jsonify({'message': 'La revisión de códigos SQL utilizando el método TF-IDF se completó con éxito.\nEl reporte ha sido generado en formato PDF y enviado correctamente al correo asociado.'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@evaluacion.route("/make_review_ia_gemini/<int:id_evaluacion>", methods=['POST'])
@handle_errors
def make_review_ia_gemini(id_evaluacion):
    try:
        data = request.json
        threshold, metrica = data.get('threshold'), data.get('metrica')
        email = data.get('email')

        if not all([threshold, metrica, email]):
            return jsonify({'error': 'Faltan datos necesarios: threshold, metrica, o email'}), 400

        # Crear el contexto y preparar los datos
        prompt_contexto = "Eres un experto en bases de datos SQL para MySQL."
        codigos = obtener_codigos_por_evaluacion(id_evaluacion)
        datos = formatear_datos_codigos(codigos)

        # Generar el prompt para IA Gemini
        prompt_total = (
            f"{prompt_contexto}\n"
            f"Evalúa los siguientes códigos SQL con un umbral de similitud de {threshold} "
            f"utilizando la métrica de {metrica}.\n\nCódigos para evaluar:\n{datos}\n\n"
            f"Cuando te refieras a un código de los datos, menciona su ID y a quien le pertenece (nombres y apellidos todo junto). "
            f"Al final, a manera de resumen, plasma el análisis en una tabla en formato md estricto."
        )

        # Obtener la respuesta de IA Gemini
        response_text = ask_to_ia_google(prompt_total)

        # Generar un nombre único para el archivo .md
        os.makedirs("reports_ia", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        md_file_path = os.path.join("reports_ia", f"IA_Gemini_Report_{timestamp}.md")

        # Guardar el contenido en el archivo .md
        with open(md_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(response_text)

        # Configurar el mensaje del correo
        mensaje = (
            f"Estimado/a,\n\n"
            f"Adjunto encontrará el reporte generado para la evaluación utilizando IA Gemini.\n\n"
            f"Detalles de la evaluación:\n"
            f"- Umbral: {threshold}\n"
            f"- Métrica: {metrica}\n\n"
            f"Saludos,\nCodeGuard"
        )

        # Enviar el correo con el archivo adjunto
        smtp_sender = SmtpSenderEmail()
        smtp_sender.send_email(email, mensaje, md_file_path)

        # Retornar confirmación
        return jsonify({
            'message': 'La revisión de códigos SQL utilizando IA Gemini se realizó exitosamente. '
                       'El reporte ha sido guardado y enviado correctamente por correo.',
            'file_path': md_file_path
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    except Exception as e:
        return jsonify({'error': f"Error inesperado: {str(e)}"}), 500

# ------------------------------------------------------------------------------
## AUX
def obtener_codigos_por_evaluacion(id_evaluacion):
    """
    Recupera los códigos SQL asociados a una evaluación específica.
    Verifica que existan al menos dos códigos, de lo contrario lanza un error.
    """
    codigos = db.session.query(
        Codigo.id_codigo,
        Codigo.url_codigo,
        Codigo.codigo_sql,
        Usuario.dni,
        Usuario.nombres,
        Usuario.apellidos
    ).join(Matricula, Codigo.id_matricula == Matricula.id_matricula) \
     .join(Usuario, Matricula.dni_estudiante == Usuario.dni) \
     .filter(Codigo.id_evaluacion == id_evaluacion).all()

    # Validar que haya al menos dos códigos
    if len(codigos) < 2:
        raise ValueError(f"Debe haber al menos dos códigos entregados a la evaluación. Count: {len(codigos)}")
    
    return codigos

def formatear_datos_codigos(codigos):
    """
    Convierte una lista de códigos obtenidos de la base de datos en un formato adecuado para el análisis.
    """
    return [
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
