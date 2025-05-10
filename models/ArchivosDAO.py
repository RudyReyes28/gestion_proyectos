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
        query = "INSERT INTO Archivos (nombre, id_proyecto, id_usuario_modificador, id_tipo_archivo) VALUES (?, ?, ?, ?)"
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
        query = "DELETE FROM Archivos WHERE id = ?"
        self.cursor.execute(query, (file_id,))
        self.connection.commit() 
        return self.cursor.rowcount > 0
    
    def get_file_by_id(self, file_id):
        query = "SELECT * FROM Archivos WHERE id = ?"
        self.cursor.execute(query, (file_id,))
        return self.cursor.fetchone()
    
    def get_files_by_project_id(self, project_id):
        query = "SELECT * FROM Archivos WHERE id_proyecto = ?"
        self.cursor.execute(query, (project_id,))
        return self.cursor.fetchall()
    
    def get_files_by_user_id(self, user_id):
        query = "SELECT * FROM Archivos WHERE id_usuario_modificador = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def update_content(self, file_id, contenido, id_usuario_modificador):
        query = "UPDATE Archivos SET contenido = ?, ultima_modificacion = GETDATE(), id_usuario_modificador = ? WHERE id = ?"
        self.cursor.execute(query, (contenido, id_usuario_modificador, file_id))
        self.connection.commit()
        return self.cursor.rowcount > 0