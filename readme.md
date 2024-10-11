# App CodegGuardGT

CodegGuardGT es una aplicación web desarrollada en Flask que proporciona una plataforma para gestionar usuarios, estudiantes, docentes, y administración, además de manejar incidencias, documentos, plagios, evaluaciones y notas de evaluaciones. El sistema utiliza una base de datos MySQL para el almacenamiento de datos y emplea la autenticación y autorización de usuarios para asegurar el acceso a las funcionalidades.

## Funcionalidades

- **Gestión de Usuarios**: Creación y manejo de usuarios de diferentes tipos (estudiantes, docentes, administración).
- **Incidencias**: Registro y gestión de incidencias relacionadas con estudiantes.
- **Documentos**: Subida y gestión de documentos para estudiantes.
- **Plagios**: Registro y análisis de plagios asociados a documentos.
- **Evaluaciones**: Creación y gestión de evaluaciones con duración en minutos.
- **Notas de Evaluación**: Asignación de notas a estudiantes para evaluaciones específicas.

## Rutas

Las siguientes rutas están disponibles en la aplicación:

- **/usuarios**: Gestión de usuarios.
- **/estudiantes**: Gestión de estudiantes.
- **/docentes**: Gestión de docentes.
- **/administracion**: Gestión de administración.
- **/incidencias**: Gestión de incidencias.
- **/documentos**: Gestión de documentos.
- **/plagios**: Gestión de plagios.
- **/evaluaciones**: Gestión de evaluaciones.
- **/notas_evaluaciones**: Gestión de notas de evaluaciones.

## Contacto

Para cualquier consulta o soporte, por favor contacta a Roger Infa Sánchez en [rogeliosanchez405@gmail.com](mailto:rogeliosanchez405@gmail.com) o al +51977312592.

---

# Instrucciones para levantar el servidor Flask

Este documento describe los pasos para conectarse al servidor y levantar la aplicación Flask.

## Conexión por SSH

1. Abre una terminal en tu máquina local.
2. Conéctate al servidor utilizando SSH con el siguiente comando:

   ```bash
   ssh codeGuard@212.38.95.106
   ```

3. Ingresa tu contraseña cuando se te solicite.

## Levantar el servidor Flask

Una vez que estés conectado al servidor, sigue estos pasos para iniciar la aplicación:

1. Lista los directorios disponibles:

   ```bash
   ls
   ```

   Deberías ver los siguientes directorios:

   ```
   AppCodeGuardGT  flask-adminlte  flask-adminlte1
   ```

2. Cambia al directorio `AppCodeGuardGT`:

   ```bash
   cd AppCodeGuardGT/
   ```

3. Activa el entorno virtual de Python:

   ```bash
   source env/bin/activate
   ```

4. Cambia al directorio `app`:

   ```bash
   cd app/
   ```

5. Ejecuta el servidor Flask:

   ```bash
   python run.py
   ```

   Verás una salida similar a esta:

   ```
   * Serving Flask app 'config'
   * Debug mode: on
   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://212.38.95.106:5000
   Press CTRL+C to quit
   * Restarting with stat
   * Debugger is active!
   * Debugger PIN: 776-389-331
   ```

6. La aplicación Flask estará corriendo en la IP `212.38.95.106` en el puerto `5000`. Puedes acceder a la aplicación desde el navegador en la siguiente URL:

   ```
   http://212.38.95.106:5000
   ```

## Credenciales del Usuario Admin por Defecto

El usuario administrador por defecto es el siguiente:

- **Usuario:** `72190044`
- **Contraseña:** `72190044`

Asegúrate de cambiar estas credenciales en un entorno de producción por razones de seguridad.

## Notas adicionales

- Esta aplicación está corriendo en modo de desarrollo. **No se recomienda usarla en un entorno de producción**. Para entornos de producción, considera usar un servidor WSGI como Gunicorn o uWSGI.
- Para detener el servidor, presiona `CTRL+C` en la terminal.
```