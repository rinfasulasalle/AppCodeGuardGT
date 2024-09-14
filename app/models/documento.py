from utils.db import db
import pytz
from datetime import datetime

# Define la zona horaria de Perú
PERU_TZ = pytz.timezone('America/Lima')

class Documento(db.Model):    
    id_documento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni_estudiante = db.Column(db.String(20), db.ForeignKey('estudiante.dni_usuario', ondelete='CASCADE'))
    url_documento = db.Column(db.String(255), nullable=False, unique=True)
    fecha_subida = db.Column(db.DateTime, default=datetime.now(PERU_TZ))
    
    def __init__(self, dni_estudiante, url_documento):
        self.dni_estudiante = dni_estudiante
        self.url_documento = url_documento
    
    def to_dict(self):
        return {
            'id_documento': self.id_documento,
            'dni_estudiante': self.dni_estudiante,
            'url_documento': self.url_documento,
            'fecha_subida': self.fecha_subida.isoformat()
        }
