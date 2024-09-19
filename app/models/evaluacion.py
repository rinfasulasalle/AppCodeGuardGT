from utils.db import db

class Evaluacion(db.Model):    
    id_evaluacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    duracion = db.Column(db.Integer, nullable=False)  # Duración en segundos
    dni_docente = db.Column(db.String(20), db.ForeignKey('docente.dni_usuario', ondelete='CASCADE'))

    def __init__(self, nombre, descripcion, duracion, dni_docente):
        self.nombre = nombre
        self.descripcion = descripcion
        self.duracion = duracion
        self.dni_docente = dni_docente
    
    def to_dict(self):
        return {
            'id_evaluacion': self.id_evaluacion,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'duracion': self.duracion,
            'dni_docente': self.dni_docente
        }
