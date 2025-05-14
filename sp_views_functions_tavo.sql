-- INSERT INTO Archivos (nombre, id_proyecto, id_usuario_modificador, id_tipo_archivo) VALUES (?, ?, ?, ?)
CREATE PROCEDURE sp_insert_archivos
    @nombre NVARCHAR(255),
    @id_proyecto INT,
    @id_usuario_modificador INT,
    @id_tipo_archivo INT
AS
BEGIN
    INSERT INTO Archivos (nombre, id_proyecto, id_usuario_modificador, id_tipo_archivo)
    VALUES (@nombre, @id_proyecto, @id_usuario_modificador, @id_tipo_archivo);
END;


-- DELETE FROM Archivos WHERE id = ?
CREATE PROCEDURE sp_delete_archivos
    @id INT
AS
BEGIN
    DELETE FROM Archivos WHERE id = @id;
END;

-- UPDATE Archivos SET contenido = ?, ultima_modificacion = GETDATE(), id_usuario_modificador = ? WHERE id = ?
CREATE PROCEDURE sp_update_archivos
    @id INT,
    @contenido NVARCHAR(max),
    @id_usuario_modificador INT
AS
BEGIN
    UPDATE Archivos
    SET contenido = @contenido
      , ultima_modificacion = GETDATE()
      , id_usuario_modificador = @id_usuario_modificador
    WHERE id = @id;
END;


-- SELECT * FROM Archivos WHERE id = ?
CREATE VIEW view_archivos AS
  SELECT * FROM Archivos;
GO

/*
SELECT v.id, v.contenido, v.fecha_version, v.id_usuario, u.nombre_usuario
FROM Versiones_Archivo v
JOIN Usuarios u ON v.id_usuario = u.id
WHERE v.id_archivo = ?
ORDER BY v.fecha_version DESC
*/
CREATE FUNCTION fn_archivos_obtener_versiones (
  @id_archivo INT
)
RETURNS TABLE AS RETURN (
  SELECT
         v.id, v.contenido
       , v.fecha_version
       , v.id_usuario
       , u.nombre_usuario
  FROM Versiones_Archivo v
    JOIN Usuarios u ON v.id_usuario = u.id
  WHERE v.id_archivo = @id_archivo
);
GO

/*
SELECT id_archivo, contenido, fecha_version, id_usuario
FROM Versiones_Archivo
WHERE id = ?
*/
CREATE FUNCTION fn_archivos_obtner_version_especifica (
  @id INT
)
RETURNS TABLE AS  RETURN (
  SELECT id_archivo, contenido, fecha_version, id_usuario
  FROM Versiones_Archivo
  WHERE id = @id
);
