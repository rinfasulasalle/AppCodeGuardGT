from datetime import datetime
import pytz
from utils.db import db

PERU_TZ = pytz.timezone('America/Lima')

class Usuario(db.Model):
    dni = db.Column(db.String(20), primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(15), unique=False, nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP, default=lambda: datetime.now(PERU_TZ))

    def __init__(self, dni, nombres, apellidos, correo, contrasena, telefono):
        self.dni = dni
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.contrasena = contrasena
        self.telefono = telefono
