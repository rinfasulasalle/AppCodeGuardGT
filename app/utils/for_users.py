import unicodedata
import bcrypt
from models.usuario import Usuario
import re

# Función para validar el número de teléfono
def validar_telefono(telefono):
    # Ejemplo de patrón: +51 123456789
    patron = re.compile(r'^\+\d{1,3} \d{7,15}$')  # Código de país y número
    return bool(patron.match(telefono))

# Función para normalizar nombres (eliminar tildes y caracteres especiales)
def normalizar_texto(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    ).lower()

# Función para generar un correo único
def generar_correo_unico(nombres, apellidos):
    nombres_normalizado = normalizar_texto(nombres)
    apellidos_normalizado = normalizar_texto(apellidos)

    # Obtener iniciales de los nombres y apellidos
    correo_base = f"{nombres_normalizado[0]}{apellidos_normalizado.split()[0]}{apellidos_normalizado.split()[1][0]}@codeguard.pe"

    # Verificar si ya existe el correo en la base de datos
    contador = 1
    correo_unico = correo_base
    while Usuario.query.filter_by(correo=correo_unico).first():
        correo_unico = f"{correo_base.split('@')[0]}{contador}@{correo_base.split('@')[1]}"
        contador += 1

    return correo_unico

# Función para hashear una contraseña
def hash_contrasena(contrasena):
    contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
    return contrasena_hash.decode('utf-8')

# Función para comparar contraseñas (ver si son iguales)
def verificar_contrasena(contrasena, contrasena_hash):
    return bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_hash.encode('utf-8'))
