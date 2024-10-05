from utils.db import db

class Curso(db.Model):
    id_curso = db.Column(db.Integer, primary_key=True, autoincrement= True)
    dni_docente = db.Column(db.String(20), db.ForeignKey('docente.dni_usuario', ondelete='CASCADE'), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, dni_docente, nombre):
        self.dni_docente = dni_docente
        self.nombre = nombre
    
    def to_dict(self):
        return {
            'id_curso': self.id_curso,
            'dni_docente': self.dni_docente,
            'nombre': self.nombre
        }
