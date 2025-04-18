-- Creación de la base de datos
CREATE DATABASE GestionProyectos;

USE GestionProyectos;

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre_usuario NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    contraseña NVARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT GETDATE(),
    biografia NVARCHAR(500) NULL
);

INSERT INTO Usuarios (nombre_usuario, email, contraseña, biografia) VALUES
('juan1', 'user1@example.com', 'scrypt:32768:8:1$CoAKVlX3eG3TCxlg$3ed4a451e10a89b6739c4fced17d0c0efd435fa241f2b535c9102d225956acbcd108618b8f8b805b1335f2851984e62ef188b5ff1f2e4375a0dff724fcbd0ed7', 'Amante de la tecnología y los videojuegos.'),
('juan2', 'user2@example.com', 'scrypt:32768:8:1$CoAKVlX3eG3TCxlg$3ed4a451e10a89b6739c4fced17d0c0efd435fa241f2b535c9102d225956acbcd108618b8f8b805b1335f2851984e62ef188b5ff1f2e4375a0dff724fcbd0ed7', 'Estudiante de informática.');

-- Tabla de Proyectos
CREATE TABLE Proyectos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(500) NULL,
    fecha_creacion DATETIME DEFAULT GETDATE(),
    visibilidad NVARCHAR(20) NOT NULL CHECK (visibilidad IN ('publico', 'privado')),
    id_creador INT NOT NULL,
    FOREIGN KEY (id_creador) REFERENCES Usuarios(id)
);

INSERT INTO Proyectos (nombre, descripcion, visibilidad, id_creador) VALUES
('Sistema de Inventario', 'Aplicación web para gestionar el inventario de una tienda.', 'publico', 7),
('Blog Personal', 'Blog para compartir artículos sobre programación.', 'privado', 7),
('Gestor de Tareas', 'Proyecto colaborativo para manejar tareas de equipo.', 'publico', 7),
('Plataforma de Cursos', 'Sitio para ofrecer cursos en línea.', 'privado', 7),
('Portafolio Profesional', NULL, 'publico', 7);

-- Tabla de Archivos
CREATE TABLE Archivos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(255) NOT NULL,
    contenido NVARCHAR(MAX) NULL,
    ultima_modificacion DATETIME DEFAULT GETDATE(),
    id_proyecto INT NOT NULL,
    id_usuario_modificador INT NOT NULL,
    FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id),
    FOREIGN KEY (id_usuario_modificador) REFERENCES Usuarios(id)
);

-- Tabla de Versiones de Archivos
CREATE TABLE Versiones_Archivo (
    id INT PRIMARY KEY IDENTITY(1,1),
    id_archivo INT NOT NULL,
    contenido NVARCHAR(MAX) NULL,
    fecha_version DATETIME DEFAULT GETDATE(),
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_archivo) REFERENCES Archivos(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

-- Tabla de Colaboradores
CREATE TABLE Colaboradores (
    id_proyecto INT NOT NULL,
    id_usuario INT NOT NULL,
    PRIMARY KEY (id_proyecto, id_usuario),
    FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

-- Tabla de Comentarios
CREATE TABLE Comentarios (
    id INT PRIMARY KEY IDENTITY(1,1),
    contenido NVARCHAR(1000) NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),
    id_usuario INT NOT NULL,
    id_proyecto INT NOT NULL,
    id_archivo INT NULL,
    linea_codigo INT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
    FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id),
    FOREIGN KEY (id_archivo) REFERENCES Archivos(id)
);



