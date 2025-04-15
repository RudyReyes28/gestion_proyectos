"""
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
"""

class ComentariosDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def create_comment(self, contenido, id_usuario, id_proyecto, id_archivo=None, linea_codigo=None):
        query = "INSERT INTO Comentarios (contenido, id_usuario, id_proyecto, id_archivo, linea_codigo) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (contenido, id_usuario, id_proyecto, id_archivo, linea_codigo))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def update_comment(self, contenido, comment_id):
        query = "UPDATE Comentarios SET contenido = ? WHERE id = ?"
        self.cursor.execute(query, (contenido, comment_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_comment(self, comment_id):
        query = "DELETE FROM Comentarios WHERE id = ?"
        self.cursor.execute(query, (comment_id,))
        self.connection.commit() 
        return self.cursor.rowcount > 0
    
    def get_comment_by_id(self, comment_id):
        query = "SELECT * FROM Comentarios WHERE id = ?"
        self.cursor.execute(query, (comment_id,))
        return self.cursor.fetchone()
    
    def get_comment_by_user_id(self, user_id):
        query = "SELECT * FROM Comentarios WHERE id_usuario = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_comment_by_project_id(self, project_id):
        query = "SELECT * FROM Comentarios WHERE id_proyecto = ?"
        self.cursor.execute(query, (project_id,))
        return self.cursor.fetchall()
    
    def get_comment_by_file_id(self, file_id):
        query = "SELECT * FROM Comentarios WHERE id_archivo = ?"
        self.cursor.execute(query, (file_id,))
        return self.cursor.fetchall()
    
    