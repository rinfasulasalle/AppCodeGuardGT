from flask import Blueprint, render_template
from flask_login import login_required, current_user
home = Blueprint('home', __name__)

def check_access(role):
    if current_user.role != role:
        return render_template('home/access_denied.html')

@home.route('/')
@login_required
def get_home():
    # Redirigir a la plantilla correspondiente según el rol del usuario
    if current_user.role == 'Administracion':
        return render_template('home/admin/index.html')
    elif current_user.role == 'Docente':
        return render_template('home/docente/index.html')
    elif current_user.role == 'Estudiante':
        return render_template('home/estudiante/index.html')
    else:
        return render_template('home/index.html')
    
@home.route('/profile')
@login_required
def get_profile():
    return render_template('home/profile.html')

@home.route('/admin_change_password')
@login_required
def admin_change_password():
    if current_user.role == 'Administracion':
        return render_template('home/admin/admin_change_password.html')
    return check_access('Administracion')

@home.route('/gestion_usuarios')
@login_required
def get_gestion_usuarios():
    if current_user.role == 'Administracion':
        return render_template('home/admin/gestion_usuarios.html')
    return check_access('Administracion')

@home.route('/gestion_roles')
@login_required
def get_gestion_roles():
    if current_user.role == 'Administracion':
        return render_template('home/admin/gestion_roles.html')
    return check_access('Administracion')
@home.route('/gestion_cursos')
@login_required
def get_gestion_cursos():
    if current_user.role == 'Administracion':
        return render_template('home/admin/gestion_cursos.html')
    return check_access('Administracion')



# ----------------------------------
# Para estudiantes
@home.route('/mis_cursos')
@login_required
def mis_cursos():
    if current_user.role == 'Estudiante':
        return render_template('home/estudiante/mis_cursos.html')
    return check_access('Estudiante')


# ----------------------------------
# PARA DOCENTES
@home.route('/docente_cursos')
@login_required
def docente_cursos():
    if current_user.role == 'Docente':
        return render_template('home/docente/docente_cursos.html')
    return check_access('Docente')

@home.route('/docente_evaluaciones')
@login_required
def docente_evaluaciones():
    if current_user.role == 'Docente':
        return render_template('home/docente/docente_evaluaciones.html')
    return check_access('Docente')

@home.route('/docente_clasroom')
@login_required
def docente_clasroom():
    if current_user.role == 'Docente':
        return render_template('home/docente/docente_clasroom.html')
    return check_access('Docente')