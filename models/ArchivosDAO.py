"""
CREATE TABLE Archivos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(255) NOT NULL,
    contenido NVARCHAR(MAX) NULL,
    ultima_modificacion DATETIME DEFAULT GETDATE(),
    id_proyecto INT NOT NULL,
    id_usuario_modificador INT NOT NULL,
    id_tipo_archivo INT NOT NULL,
    FOREIGN KEY (id_tipo_archivo) REFERENCES Tipo_Archivo(id),
    FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id),
    FOREIGN KEY (id_usuario_modificador) REFERENCES Usuarios(id),
);

"""


class ArchivosDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def create_file(self, nombre, id_proyecto, id_usuario_modificador, id_tipo_archivo):
        query = "EXEC sp_insert_archivos @nombre=?, @id_proyecto=?, @id_usuario_modificador=?, @id_tipo_archivo=?"
        self.cursor.execute(query, (nombre, id_proyecto, id_usuario_modificador, id_tipo_archivo))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    
    def update_file(self, file_id, nombre=None, contenido=None):
        query = "UPDATE Archivos SET "
        params = []
        if nombre:
            query += "nombre = ?, "
            params.append(nombre)
        if contenido:
            query += "contenido = ?, "
            params.append(contenido)
        else:
            query = query.rstrip(", ")
        query += "WHERE id = ?"
        params.append(file_id)
        self.cursor.execute(query, tuple(params))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_file(self, file_id):
        query = "EXEC sp_delete_archivos @id =?"
        self.cursor.execute(query, (file_id,))
        self.connection.commit() 
        return self.cursor.rowcount > 0
    
    def get_file_by_id(self, file_id):
        query = "SELECT * FROM view_archivos WHERE id =?"
        self.cursor.execute(query, (file_id,))
        return self.cursor.fetchone()
    
    def get_files_by_project_id(self, project_id):
        query = "SELECT * FROM view_archivos WHERE id_proyecto =?"
        self.cursor.execute(query, (project_id,))
        return self.cursor.fetchall()
    
    def get_files_by_user_id(self, user_id):
        query = "SELECT * FROM view_archivos WHERE id_usuario_modificador =?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def update_content(self, file_id, contenido, id_usuario_modificador):
        # query = "UPDATE Archivos SET contenido = ?, ultima_modificacion = GETDATE(), id_usuario_modificador = ? WHERE id = ?"
        query = "EXEC sp_update_archivos @contenido=?, @id_usuario_modificador=?, @id=?"
        self.cursor.execute(query, (contenido, id_usuario_modificador, file_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    
    
    def get_file_versions(self, file_id):
        """Obtiene todas las versiones de un archivo"""
        try:
            query = "SELECT * FROM fn_archivos_obtener_versiones(?) ORDER BY fecha_version DESC"
            self.cursor.execute(query, (file_id,))
            versions = self.cursor.fetchall()
            return versions
        except Exception as e:
            print(f"Error al obtener versiones del archivo: {e}")
        return []

    def get_version_by_id(self, version_id):
        """Obtiene una versión específica por su ID"""
        try:
            query = "SELECT * FROM fn_archivos_obtner_version_especifica(?)"
            self.cursor.execute(query, (version_id,))
            version = self.cursor.fetchone()
            return version
        except Exception as e:
            print(f"Error al obtener la versión: {e}")
        return None
