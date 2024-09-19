-- Crear la base de datos
CREATE DATABASE db_codeguard;
USE db_codeguard;

-- Tabla principal de Usuarios
CREATE TABLE Usuarios (
    dni VARCHAR(20) PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Estudiantes
CREATE TABLE Estudiantes (
    dni_usuario VARCHAR(20) PRIMARY KEY,
    FOREIGN KEY (dni_usuario) REFERENCES Usuarios(dni) ON DELETE CASCADE
);

-- Tabla de Docentes
CREATE TABLE Docentes (
    dni_usuario VARCHAR(20) PRIMARY KEY,
    FOREIGN KEY (dni_usuario) REFERENCES Usuarios(dni) ON DELETE CASCADE
);

-- Tabla de Administracion
CREATE TABLE Administracion (
    dni_usuario VARCHAR(20) PRIMARY KEY,
    FOREIGN KEY (dni_usuario) REFERENCES Usuarios(dni) ON DELETE CASCADE
);

-- Crear la tabla de Evaluaciones asociando un docente
CREATE TABLE Evaluaciones (
    id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    duracion INT NOT NULL, -- Duración en segundos
    dni_docente VARCHAR(20),
    CHECK (duracion > 0), -- Asegura que la duración sea positiva
    FOREIGN KEY (dni_docente) REFERENCES Docentes(dni_usuario) ON DELETE CASCADE
);

-- Tabla de Documentos (solo para estudiantes)
CREATE TABLE Documentos (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,
    dni_estudiante VARCHAR(20),
    url_documento VARCHAR(255) NOT null UNIQUE,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (dni_estudiante) REFERENCES Estudiantes(dni_usuario) ON DELETE CASCADE
);

-- Tabla de Plagios (relacionada con Documentos)
CREATE TABLE Plagios (
    id_plagio INT AUTO_INCREMENT PRIMARY KEY,
    id_documento INT,
    porcentaje_plagio DECIMAL(5,2) NOT NULL,
    detalles_plagio TEXT NOT NULL,
    estado ENUM('sin sanción', 'sancionado') DEFAULT 'sin sanción',
    FOREIGN KEY (id_documento) REFERENCES Documentos(id_documento) ON DELETE CASCADE
);

-- Tabla de Incidencias (relacionada con estudiantes)
CREATE TABLE Incidencias (
    id_incidencia INT AUTO_INCREMENT PRIMARY KEY,
    dni_estudiante VARCHAR(20),
    descripcion TEXT NOT NULL,
    FOREIGN KEY (dni_estudiante) REFERENCES Estudiantes(dni_usuario) ON DELETE CASCADE
);

-- Crear la tabla de Notas_Evaluaciones con referencia a Estudiantes, Evaluaciones y Documentos
CREATE TABLE Notas_Evaluaciones (
    id_nota_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    id_evaluacion INT,
    id_documento INT, -- Nueva columna que hace referencia a los documentos
    nota DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (id_evaluacion) REFERENCES Evaluaciones(id_evaluacion) ON DELETE CASCADE,
    FOREIGN KEY (id_documento) REFERENCES Documentos(id_documento) ON DELETE CASCADE
);