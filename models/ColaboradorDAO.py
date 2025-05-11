"""
-- Tabla de Colaboradores
CREATE TABLE Colaboradores (
    id_proyecto INT NOT NULL,
    id_usuario INT NOT NULL,
    PRIMARY KEY (id_proyecto, id_usuario),
    FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);
"""
from models.Correos import enviar_correo

class ColaboradorDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add_colaborador(self, id_proyecto, id_usuario):
        query = "INSERT INTO Colaboradores (id_proyecto, id_usuario) VALUES (?, ?)"
        self.cursor.execute(query, (id_proyecto, id_usuario))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def remove_colaborador(self, id_proyecto, id_usuario):
        query = "DELETE FROM Colaboradores WHERE id_proyecto = ? AND id_usuario = ?"
        self.cursor.execute(query, (id_proyecto, id_usuario))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def get_projects_by_user_id(self, id_usuario):
        query = "SELECT id_proyecto FROM Colaboradores WHERE id_usuario = ?"
        self.cursor.execute(query, (id_usuario,))
        return self.cursor.fetchall()
    
    def get_users_by_project_id(self, id_proyecto):
        query = "SELECT id_usuario FROM Colaboradores WHERE id_proyecto = ?"
        self.cursor.execute(query, (id_proyecto,))
        return self.cursor.fetchall()
    
    def get_all_colaboradores(self):
        query = "SELECT * FROM Colaboradores"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_content_projects_by_colaborador(self, id_usuario):
        query = """
            SELECT Proyectos.*, Usuarios.nombre_usuario
            FROM Colaboradores
            JOIN Proyectos ON Colaboradores.id_proyecto = Proyectos.id
            JOIN Usuarios ON Colaboradores.id_usuario = Usuarios.id
            WHERE Colaboradores.id_usuario = ?
        """
        self.cursor.execute(query, (id_usuario,))
        return self.cursor.fetchall()
    
    def get_content_project_by_colaborador(self, id_project, id_usuario):
        query = """
            SELECT Proyectos.*, Usuarios.nombre_usuario
            FROM Colaboradores
            JOIN Proyectos ON Colaboradores.id_proyecto = Proyectos.id
            JOIN Usuarios ON Colaboradores.id_usuario = Usuarios.id
            WHERE Colaboradores.id_proyecto = ? AND Colaboradores.id_usuario = ?
        """
        self.cursor.execute(query, (id_project, id_usuario))
        return self.cursor.fetchone()
    
    def get_all_colaboradores_by_project(self, id_proyecto):
        query = """
            SELECT Usuarios.*
            FROM Colaboradores
            JOIN Usuarios ON Colaboradores.id_usuario = Usuarios.id
            WHERE Colaboradores.id_proyecto = ?
        """
        self.cursor.execute(query, (id_proyecto,))
        return self.cursor.fetchall()

    def add_colaborator_gmail(self, id_proyecto, gmail_colaborador, id_colaborador, nombre_proyecto):
        query = "INSERT INTO Colaboradores (id_proyecto, id_usuario) VALUES (?, ?)"
        self.cursor.execute(query, (id_proyecto, id_colaborador))
        self.connection.commit()
        if self.cursor.rowcount > 0:
            #enviar correo al colaborador
            enviar_correo(gmail_colaborador, "Colaboración en proyecto", "Has sido añadido como colaborador en el proyecto.", nombre_proyecto)
        return self.cursor.rowcount > 0
