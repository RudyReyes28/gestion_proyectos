-- VISTAS Y PROCEDIMIENTOS PARA PROYECTOS
CREATE VIEW get_project AS
SELECT * FROM Proyectos;



CREATE VIEW get_project_collaborative AS
SELECT p.*, c.id_usuario
FROM Colaboradores c
JOIN Proyectos p ON c.id_proyecto = p.id;



CREATE VIEW view_project_owner AS
SELECT 
    p.id AS id_proyecto,
    p.id_creador,
    u.nombre_usuario
FROM 
    Proyectos p
JOIN 
    Usuarios u ON u.id = p.id_creador;



CREATE PROCEDURE proc_create_project
    @nombre NVARCHAR(100),
    @descripcion NVARCHAR(500),
    @visibilidad NVARCHAR(20),
    @id_creador INT
AS
BEGIN
    INSERT INTO Proyectos (nombre, descripcion, visibilidad, id_creador)
    VALUES (@nombre, @descripcion, @visibilidad, @id_creador);

END;


CREATE PROCEDURE proc_update_project
    @id INT,
    @nombre NVARCHAR(100),
    @descripcion NVARCHAR(500),
    @visibilidad NVARCHAR(20)
AS
BEGIN
    UPDATE Proyectos
    SET nombre = @nombre,
        descripcion = @descripcion,
        visibilidad = @visibilidad
    WHERE id = @id;

END;


CREATE PROCEDURE proc_delete_project
    @id INT
AS
BEGIN
    DELETE FROM Proyectos
    WHERE id = @id;

END;


-- VISTAS Y PROCEDIMIENTOS PARA USUARIOS
CREATE VIEW view_usuarios AS
SELECT * FROM Usuarios;

CREATE PROCEDURE proc_create_user
    @nombre_usuario NVARCHAR(50),
    @email NVARCHAR(100),
    @contraseña NVARCHAR(255),
    @biografia NVARCHAR(500) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    INSERT INTO Usuarios (nombre_usuario, email, contraseña, biografia)
    VALUES (@nombre_usuario, @email, @contraseña, @biografia);
END;


CREATE PROCEDURE proc_update_user
    @id INT,
    @nombre_usuario NVARCHAR(50) = NULL,
    @email NVARCHAR(100) = NULL,
    @biografia NVARCHAR(500) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE Usuarios
    SET 
        nombre_usuario = ISNULL(@nombre_usuario, nombre_usuario),
        email = ISNULL(@email, email),
        biografia = ISNULL(@biografia, biografia)
    WHERE id = @id;
END;

-- VISTAS Y PROCEDIMIENTOS PARA tipo_archivo
-- Vista general, filtrar busquedas usando where
CREATE VIEW Vista_Tipo_Archivo AS
SELECT * FROM Tipo_Archivo;
GO

-- Procedimiento: Crear nuevo tipo de archivo
IF OBJECT_ID('Crear_Tipo_Archivo', 'P') IS NOT NULL
    DROP PROCEDURE Crear_Tipo_Archivo;
GO

CREATE PROCEDURE Crear_Tipo_Archivo
    @nombre NVARCHAR(50),
    @extension NVARCHAR(10),
    @resultado BIT OUTPUT
AS
BEGIN
    BEGIN TRY
        INSERT INTO Tipo_Archivo (nombre, extension)
        VALUES (@nombre, @extension);

        -- Si la inserción fue exitosa, devolvemos 1 (true)
        SET @resultado = 1;
    END TRY
    BEGIN CATCH
        -- Si ocurre un error, devolvemos 0 (false)
        SET @resultado = 0;
    END CATCH
END;
GO