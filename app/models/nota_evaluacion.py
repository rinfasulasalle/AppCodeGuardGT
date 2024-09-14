from utils.db import db

class NotaEvaluacion(db.Model):

    id_nota_evaluacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni_estudiante = db.Column(db.String(20), db.ForeignKey('estudiante.dni_usuario', ondelete='CASCADE'), nullable=False)
    id_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluacion.id_evaluacion', ondelete='CASCADE'), nullable=False)
    nota = db.Column(db.Numeric(5, 2), nullable=False)

    # Restricción para evitar que un estudiante tenga más de una nota en la misma evaluación
    __table_args__ = (
        db.UniqueConstraint('dni_estudiante', 'id_evaluacion', name='unique_student_evaluation'),
    )

    def __init__(self, dni_estudiante, id_evaluacion, nota):
        self.dni_estudiante = dni_estudiante
        self.id_evaluacion = id_evaluacion
        self.nota = nota

    def to_dict(self):
        return {
            'id_nota_evaluacion': self.id_nota_evaluacion,
            'dni_estudiante': self.dni_estudiante,
            'id_evaluacion': self.id_evaluacion,
            'nota': str(self.nota)  # Asegúrate de convertir la nota a string para evitar problemas con la precisión decimal
        }
