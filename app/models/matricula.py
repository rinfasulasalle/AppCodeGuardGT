from utils.db import db

class Matricula(db.Model):
    id_matricula = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni_estudiante = db.Column(db.String(20), db.ForeignKey('estudiante.dni_usuario', ondelete='CASCADE'), nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id_curso', ondelete='CASCADE'), nullable=False)

    def __init__(self, dni_estudiante, id_curso):
        self.dni_estudiante = dni_estudiante    
        self.id_curso = id_curso
    
    def to_dict(self):
        return {
            'id_matricula': self.id_matricula,
            'dni_estudiante': self.dni_estudiante,
            'id_curso': self.id_curso
        }
