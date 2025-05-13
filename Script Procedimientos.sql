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