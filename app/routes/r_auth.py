from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from utils.for_users import verificar_contrasena
from utils.db import db
from models.usuario import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form['dni']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(dni=dni).first()
        if usuario and verificar_contrasena(contrasena, usuario.contrasena):  # Verifica la contraseña hasheada
            login_user(usuario)
            print(current_user.to_dict())
            return redirect(url_for('home.get_home'))  # Redirigir a la página de inicio
        else:
            flash('Credenciales incorrectas', 'error')

    return render_template('auth/login.html')  # Asegúrate de tener un archivo de plantilla HTML

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión con éxito.', 'info')  # Mensaje de cierre de sesión
    return redirect(url_for('auth.login'))  # Redirigir al login
