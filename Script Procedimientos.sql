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

-- Vista Colaboradores
CREATE VIEW vista_colaboradores_base AS
SELECT id_usuario, id_proyecto
FROM Colaboradores;
GO

-- Vista 2 colaboradores 
CREATE VIEW vista_colaboradores_detalle AS
SELECT 
    c.id_proyecto,
    c.id_usuario,

    p.id AS id_proyecto_detalle,
    p.nombre AS nombre_proyecto,
    p.descripcion AS descripcion_proyecto,
    p.fecha_creacion,
    p.visibilidad,
    p.id_creador,

    u.id AS id_usuario_detalle,
    u.nombre_usuario,
    u.email,
    u.contraseña,
    u.fecha_registro,
    u.biografia
FROM Colaboradores c
JOIN Proyectos p ON c.id_proyecto = p.id
JOIN Usuarios u ON c.id_usuario = u.id;
GO


-- Procedimiento para ColaboradorDAO
CREATE PROCEDURE add_colaborador 
    @id_proyecto INT,
    @id_usuario INT
AS
BEGIN
    INSERT INTO Colaboradores (id_proyecto, id_usuario) VALUES (@id_proyecto, @id_usuario);
END;
GO

CREATE PROCEDURE remove_colaborador
    @id_proyecto INT,
    @id_usuario INT
AS
BEGIN
    DELETE FROM Colaboradores WHERE id_proyecto = @id_proyecto AND id_usuario = @id_usuario;
END;

