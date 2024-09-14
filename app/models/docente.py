from utils.db import db

class Docente(db.Model):
    dni_usuario = db.Column(db.String(20), db.ForeignKey('usuario.dni', ondelete='CASCADE'), primary_key=True)

    def __init__(self, dni_usuario):
        self.dni_usuario = dni_usuario

    def to_dict(self):
        return {
            'dni_usuario': self.dni_usuario
        }
