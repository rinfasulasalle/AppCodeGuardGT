import unicodedata
import bcrypt
from models.usuario import Usuario
import re

# Función para validar el número de teléfono
def validar_telefono(telefono):
    # Patrón general para código de país y número, permite espacios
    patron_general = re.compile(r'^\+\d{1,3}\s*\d{1,3}[\s\d]*$')

    # Verificar si el número cumple con el patrón general
    if not patron_general.match(telefono):
        return False

    # Validación específica para Perú (+51)
    if telefono.startswith("+51"):
        # Eliminar espacios y contar solo los dígitos después de +51
        telefono_sin_espacios = telefono.replace(" ", "")
        # Asegurarse de que tenga exactamente 12 caracteres: +51 seguido de 9 dígitos
        if len(telefono_sin_espacios) != 12:
            return False

    return True


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

    # Verificar si ya existe el correo en la base de datos, en caso de homonimos
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
