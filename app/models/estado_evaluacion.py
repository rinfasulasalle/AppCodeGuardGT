from datetime import datetime
import pytz
from utils.db import db

# Zona horaria específica
PERU_TZ = pytz.timezone('America/Lima')

class EstadoEvaluacion(db.Model):
    id_estado_evaluacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluacion.id_evaluacion', ondelete='CASCADE'), nullable=False)
    id_matricula = db.Column(db.Integer, db.ForeignKey('matricula.id_matricula', ondelete='CASCADE'), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='Pendiente')  # Estados: Pendiente, Completada, Calificada
    fecha_actualizacion = db.Column(db.TIMESTAMP, default=lambda: datetime.now(PERU_TZ), onupdate=lambda: datetime.now(PERU_TZ))

    def __init__(self, id_evaluacion, id_matricula, estado='Pendiente'):
        self.id_evaluacion = id_evaluacion
        self.id_matricula = id_matricula
        self.estado = estado

    def to_dict(self):
        return {
            'id_estado_evaluacion': self.id_estado_evaluacion,
            'id_evaluacion': self.id_evaluacion,
            'id_matricula': self.id_matricula,
            'estado': self.estado,
            'fecha_actualizacion': self.fecha_actualizacion
        }
