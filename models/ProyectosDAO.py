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
        try:
            self.cursor.execute("EXEC proc_create_project @nombre=?, @descripcion=?, @visibilidad=?, @id_creador=?", 
                           (nombre, descripcion, visibilidad, id_creador))
        
            self.connection.commit()
            return True 
        
        except Exception as e:
            self.connection.rollback()  
            return False  
    
    def update_project(self, project_id, nombre=None, descripcion=None, visibilidad=None):
        try:
            self.cursor.execute("EXEC proc_update_project @id=?, @nombre=?, @descripcion=?, @visibilidad=?",
                           (project_id, nombre, descripcion, visibilidad))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    def delete_project(self, project_id):
        try:
            self.cursor.execute("EXEC proc_delete_project @id=?", (project_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
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
        query = "SELECT * FROM get_project WHERE id_creador = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_all_projects(self):
        query = "SELECT * FROM get_project"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_projects_by_visibility(self, visibilidad):
        query = "SELECT * FROM get_project WHERE visibilidad = ?"
        self.cursor.execute(query, (visibilidad,))
        return self.cursor.fetchall()
    
    def get_projects_by_user_and_visibility(self, user_id, visibilidad):
        query = "SELECT * FROM get_project WHERE id_creador = ? AND visibilidad = ?"
        self.cursor.execute(query, (user_id, visibilidad))
        return self.cursor.fetchall()
    
    def get_projects_publicos(self):
        query = "SELECT * FROM get_project WHERE visibilidad = 'publico'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_projects_privados(self):
        query = "SELECT * FROM get_project WHERE visibilidad = 'privado'"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_projects_collaborative(self, user_id):
        query = """
            SELECT * FROM get_project_collaborative
            WHERE id_usuario = ?
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_projects_publics_not_myself(self, user_id):
        query = """
            SELECT *
            FROM get_project
            WHERE visibilidad = 'publico' AND id_creador != ?
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def get_project_owner(self, project_id):
        query = "SELECT id_creador, nombre_usuario FROM view_project_owner WHERE id_proyecto = ?"
        self.cursor.execute(query, (project_id,))
        return self.cursor.fetchone()