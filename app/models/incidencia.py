from utils.db import db
import pytz
from datetime import datetime

# Define la zona horaria de Perú
PERU_TZ = pytz.timezone('America/Lima')

class Incidencia(db.Model):    
    id_incidencia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni_estudiante = db.Column(db.String(20), db.ForeignKey('estudiante.dni_usuario', ondelete='CASCADE'))
    fecha_incidencia = db.Column(db.DateTime, default=lambda: datetime.now(PERU_TZ))
    descripcion = db.Column(db.Text, nullable=False)
    
    estudiante = db.relationship('Estudiante', backref=db.backref('incidencias', lazy=True))

    def __init__(self, dni_estudiante, descripcion):
        self.dni_estudiante = dni_estudiante
        self.descripcion = descripcion

    def to_dict(self):
        return {
            'id_incidencia': self.id_incidencia,
            'dni_estudiante': self.dni_estudiante,
            'fecha_incidencia': self.fecha_incidencia.isoformat(),
            'descripcion': self.descripcion
        }
