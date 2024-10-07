from utils.db import db

class Resultado(db.Model):
    id_resultado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_codigo = db.Column(db.Integer, db.ForeignKey('codigo.id_codigo', ondelete='CASCADE'), nullable=False)
    calificacion = db.Column(db.Float, nullable=False)

    def __init__(self, id_codigo, calificacion):
        self.id_codigo = id_codigo
        self.calificacion = calificacion

    def to_dict(self):
        return {
            'id_resultado': self.id_resultado,
            'id_codigo': self.id_codigo,
            'calificacion': self.calificacion 
        }
