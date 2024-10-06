from utils.db import db

class Evaluacion(db.Model):
    id_evaluacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso', ondelete='CASCADE'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, id_curso, nombre):
        self.id_curso = id_curso
        self.nombre = nombre

    def to_dict(self):
        return {
            'id_evaluacion': self.id_evaluacion,
            'id_curso': self.id_curso,
            'nombre': self.nombre
        }
