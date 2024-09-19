from utils.db import db

class NotaEvaluacion(db.Model):

    id_nota_evaluacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluacion.id_evaluacion', ondelete='CASCADE'), nullable=False)
    id_documento = db.Column(db.Integer, db.ForeignKey('documento.id_documento', ondelete='CASCADE'), unique=True)
    nota = db.Column(db.Numeric(5, 2), nullable=False)


    def __init__(self, id_evaluacion, id_documento, nota):
        self.id_evaluacion = id_evaluacion
        self.id_documento = id_documento
        self.nota = nota

    def to_dict(self):
        return {
            'id_nota_evaluacion': self.id_nota_evaluacion,
            'id_documento': self.id_documento,
            'id_evaluacion': self.id_evaluacion,
            'nota': str(self.nota)  # Asegúrate de convertir la nota a string para evitar problemas con la precisión decimal
        }
