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

## Seguridad

Para mejorar la seguridad de las credenciales:

- Las credenciales de la base de datos se cargan desde variables de entorno.
- Asegúrate de no exponer credenciales en el código fuente.
- Usa HTTPS en producción para asegurar la comunicación entre cliente y servidor.

## Licencia

Este proyecto es propiedad de Roger Infa Sánchez y está protegido por las leyes de propiedad intelectual. No se permite la distribución, modificación o uso sin permiso expreso.

## Contacto

Para cualquier consulta o soporte, por favor contacta a Roger Infa Sánchez en [rogeliosanchez405@gmail.com](mailto:rogeliosanchez405@gmail.com) o al +51977312592.

---
