from utils.db import db
import pytz
from datetime import datetime

# Define la zona horaria de Perú
PERU_TZ = pytz.timezone('America/Lima')

class Plagio(db.Model):
    id_plagio = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_documento = db.Column(db.Integer, db.ForeignKey('documento.id_documento', ondelete='CASCADE'), unique=True)
    porcentaje_plagio = db.Column(db.Numeric(5, 2), nullable=False)
    fecha_analisis = db.Column(db.DateTime, default=datetime.now(PERU_TZ))
    detalles_plagio = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum('sin sanción', 'sancionado', name='estado_plagio'), default='sin sanción')
    
    def __init__(self, id_documento, porcentaje_plagio, detalles_plagio, estado='sin sanción'):
        self.id_documento = id_documento
        self.porcentaje_plagio = porcentaje_plagio
        self.detalles_plagio = detalles_plagio
        self.estado = estado
    
    def to_dict(self):
        return {
            'id_plagio': self.id_plagio,
            'id_documento': self.id_documento,
            'porcentaje_plagio': float(self.porcentaje_plagio),
            'fecha_analisis': self.fecha_analisis.isoformat(),
            'detalles_plagio': self.detalles_plagio,
            'estado': self.estado
        }
