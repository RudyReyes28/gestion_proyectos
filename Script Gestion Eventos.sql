
CREATE DATABASE GESTION_EVENTOS;

USE GESTION_EVENTOS

-- Tabla ROL_USUARIO
CREATE TABLE ROL_USUARIO (
    id_rol INT PRIMARY KEY IDENTITY(1,1),
    tipo_usuario VARCHAR(50) NOT NULL
);

-- Tabla USUARIO
CREATE TABLE USUARIO (
    id_usuario INT PRIMARY KEY IDENTITY(1,1),
    id_rol INT NOT NULL,
    user_name VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    FOREIGN KEY (id_rol) REFERENCES ROL_USUARIO(id_rol)
);

-- Tabla USUARIO_PUBLICADOR
CREATE TABLE USUARIO_PUBLICADOR (
    id_usuario_publicador INT PRIMARY KEY IDENTITY(1,1),
    id_usuario INT NOT NULL,
    cant_publicaciones INT DEFAULT 0,
    estado_ban BIT DEFAULT 0,
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

-- Tabla PUBLICACION
CREATE TABLE PUBLICACION (
    id_publicacion INT PRIMARY KEY IDENTITY(1,1),
    lugar VARCHAR(255),
    fecha DATE,
    hora TIME,
    id_usuario_publicador INT NOT NULL,
    asistencias INT DEFAULT 0,
    cant_cupo INT,
    tipo_publico VARCHAR(50),
    cant_reportes INT DEFAULT 0,
    estado VARCHAR(50),
    FOREIGN KEY (id_usuario_publicador) REFERENCES USUARIO_PUBLICADOR(id_usuario_publicador)
);

-- Tabla ELEMENTO_PUBLICACION
CREATE TABLE ELEMENTO_PUBLICACION (
    id_elemento_publicacion INT PRIMARY KEY IDENTITY(1,1),
    id_publicacion INT NOT NULL,
    tipo_elemento VARCHAR(50),
    contenido VARBINARY(MAX),
    FOREIGN KEY (id_publicacion) REFERENCES PUBLICACION(id_publicacion)
);

-- Tabla ASISTIR_EVENTO
CREATE TABLE ASISTIR_EVENTO (
    id_evento INT PRIMARY KEY IDENTITY(1,1),
    id_publicacion INT NOT NULL,
    id_usuario INT NOT NULL,
    estado_evento VARCHAR(50),
    FOREIGN KEY (id_publicacion) REFERENCES PUBLICACION(id_publicacion),
    FOREIGN KEY (id_usuario) REFERENCES USUARIO(id_usuario)
);

-- Tabla REPORTE_PUBLICACION
CREATE TABLE REPORTE_PUBLICACION (
    id_reporte_publicacion INT PRIMARY KEY IDENTITY(1,1),
    id_publicacion INT NOT NULL,
    id_usuario_participante INT NOT NULL,
    motivo_reporte VARCHAR(255),
    estado_reporte VARCHAR(50),
    FOREIGN KEY (id_publicacion) REFERENCES PUBLICACION(id_publicacion),
    FOREIGN KEY (id_usuario_participante) REFERENCES USUARIO(id_usuario)
);

