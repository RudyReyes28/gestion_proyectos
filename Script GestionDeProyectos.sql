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



