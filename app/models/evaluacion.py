from utils.db import db

class Evaluacion(db.Model):    
    id_evaluacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    duracion = db.Column(db.Integer, nullable=False)  # Duración en segundos
    
    def __init__(self, nombre, duracion, descripcion=None):
        self.nombre = nombre
        self.duracion = duracion
        self.descripcion = descripcion
    
    def to_dict(self):
        return {
            'id_evaluacion': self.id_evaluacion,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'duracion': self.duracion
        }
