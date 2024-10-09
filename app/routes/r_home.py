from flask import Blueprint, render_template
from flask_login import login_required, current_user
home = Blueprint('home', __name__)

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