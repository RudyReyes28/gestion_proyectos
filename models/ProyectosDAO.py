"""
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
"""

class ProyectosDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    
    def create_project(self, nombre, descripcion, visibilidad, id_creador):
        query = "INSERT INTO Proyectos (nombre, descripcion, visibilidad, id_creador) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (nombre, descripcion, visibilidad, id_creador))
        self.connection.commit()
        return self.cursor.rowcount >0
    
    def update_project(self, project_id, nombre=None, descripcion=None, visibilidad=None):
        query = "UPDATE Proyectos SET "
        params = []
        if nombre:
            query += "nombre = ?, "
            params.append(nombre)
        if descripcion:
            query += "descripcion = ?, "
            params.append(descripcion)
        if visibilidad:
            query += "visibilidad = ? "
            params.append(visibilidad)
        else:
            query = query.rstrip(", ")
        query += "WHERE id = ?"
        params.append(project_id)
        self.cursor.execute(query, tuple(params))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_project(self, project_id):
        query = "DELETE FROM Proyectos WHERE id = ?"
        self.cursor.execute(query, (project_id,))
        self.connection.commit() 
        return self.cursor.rowcount > 0
    
    def change_visibility(self, project_id, visibilidad):
        query = "UPDATE Proyectos SET visibilidad = ? WHERE id = ?"
        self.cursor.execute(query, (visibilidad, project_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def get_project_by_id(self, project_id):
        query = "SELECT * FROM Proyectos WHERE id = ?"
        self.cursor.execute(query, (project_id,))
        return self.cursor.fetchone()
    
    def get_projects_by_user(self, user_id):
        query = "SELECT * FROM Proyectos WHERE id_creador = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_all_projects(self):
        query = "SELECT * FROM Proyectos"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_projects_by_visibility(self, visibilidad):
        query = "SELECT * FROM Proyectos WHERE visibilidad = ?"
        self.cursor.execute(query, (visibilidad,))
        return self.cursor.fetchall()
    
    def get_projects_by_user_and_visibility(self, user_id, visibilidad):
        query = "SELECT * FROM Proyectos WHERE id_creador = ? AND visibilidad = ?"
        self.cursor.execute(query, (user_id, visibilidad))
        return self.cursor.fetchall()
    
    def get_projects_publicos(self):
        query = "SELECT * FROM Proyectos WHERE visibilidad = 'publico'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_projects_privados(self):
        query = "SELECT * FROM Proyectos WHERE visibilidad = 'privado'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_projects_collaborative(self, user_id):
        query = """
            SELECT Proyectos.*
            FROM Colaboradores
            JOIN Proyectos ON Colaboradores.id_proyecto = Proyectos.id
            WHERE Colaboradores.id_usuario = ?
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_projects_publics_not_myself(self, user_id):
        query = """
            SELECT Proyectos.*
            FROM Proyectos
            WHERE visibilidad = 'publico' AND id_creador != ?
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_project_owner(self, project_id):
        query = "SELECT p.id_creador, u.nombre_usuario FROM Proyectos p JOIN Usuarios u ON u.id = p.id_creador  WHERE p. id = ?"
        self.cursor.execute(query, (project_id,))
        return self.cursor.fetchone()