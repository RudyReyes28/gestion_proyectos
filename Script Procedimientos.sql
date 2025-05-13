
-- 1. Crear tabla Tipo_Archivo si no existe
IF NOT EXISTS (
    SELECT * FROM sys.tables WHERE name = 'Tipo_Archivo'
)
BEGIN
    CREATE TABLE Tipo_Archivo (
        id INT PRIMARY KEY IDENTITY(1,1),
        nombre NVARCHAR(50) NOT NULL UNIQUE,
        extension NVARCHAR(10) NOT NULL UNIQUE
    );
END
GO

-- 2. Crear vista para obtener todos los tipos de archivo
IF OBJECT_ID('Vista_Tipo_Archivo', 'V') IS NOT NULL
    DROP VIEW Vista_Tipo_Archivo;
GO

CREATE VIEW Vista_Tipo_Archivo AS
SELECT id, nombre, extension
FROM Tipo_Archivo;
GO

-- 3. Procedimiento: Obtener todos los tipos de archivo
IF OBJECT_ID('Obtener_Todos_Tipo_Archivo', 'P') IS NOT NULL
    DROP PROCEDURE Obtener_Todos_Tipo_Archivo;
GO

CREATE PROCEDURE Obtener_Todos_Tipo_Archivo
AS
BEGIN
    SELECT * FROM Tipo_Archivo;
END;
GO

-- 4. Procedimiento: Obtener tipo de archivo por ID
IF OBJECT_ID('Obtener_Tipo_Archivo_Por_ID', 'P') IS NOT NULL
    DROP PROCEDURE Obtener_Tipo_Archivo_Por_ID;
GO

CREATE PROCEDURE Obtener_Tipo_Archivo_Por_ID
    @id INT
AS
BEGIN
    SELECT * FROM Tipo_Archivo WHERE id = @id;
END;
GO

-- 5. Procedimiento: Crear nuevo tipo de archivo
IF OBJECT_ID('Crear_Tipo_Archivo', 'P') IS NOT NULL
    DROP PROCEDURE Crear_Tipo_Archivo;
GO

CREATE PROCEDURE Crear_Tipo_Archivo
    @nombre NVARCHAR(50),
    @extension NVARCHAR(10)
AS
BEGIN
    INSERT INTO Tipo_Archivo (nombre, extension)
    VALUES (@nombre, @extension);
END;
GO

-- 6. Procedimiento: Actualizar tipo de archivo
IF OBJECT_ID('Actualizar_Tipo_Archivo', 'P') IS NOT NULL
    DROP PROCEDURE Actualizar_Tipo_Archivo;
GO

CREATE PROCEDURE Actualizar_Tipo_Archivo
    @id INT,
    @nombre NVARCHAR(50),
    @extension NVARCHAR(10)
AS
BEGIN
    UPDATE Tipo_Archivo
    SET nombre = @nombre,
        extension = @extension
    WHERE id = @id;
END;
GO

-- Vista para obtener todos los tipos de archivo
CREATE VIEW Vista_Tipo_Archivo AS
SELECT id, nombre
FROM Tipo_Archivo;
GO