from utils.db import db

class Codigo(db.Model):
    id_codigo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluacion.id_evaluacion', ondelete='CASCADE'), nullable=False)
    id_matricula = db.Column(db.Integer, db.ForeignKey('matricula.id_matricula', ondelete='CASCADE'), nullable=False)
    url_codigo = db.Column(db.String(255), nullable=True)
    codigo = db.Column(db.Text, nullable=True)

    def __init__(self, id_evaluacion, id_matricula, url_codigo=None, codigo=None):
        self.id_evaluacion = id_evaluacion
        self.id_matricula = id_matricula
        self.url_codigo = url_codigo
        self.codigo = codigo
    def to_dict(self):
        return {
            'id_codigo': self.id_codigo,
            'id_evaluacion': self.id_evaluacion,
            'id_matricula': self.id_matricula,
            'url_codigo': self.url_codigo,
            'codigo': self.codigo
        }
