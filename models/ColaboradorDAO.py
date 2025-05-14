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

    
    def remove_colaborador(self, id_proyecto, id_usuario):
        try:
            self.cursor.execute("EXEC remove_colaborador @id_proyecto = ?, @id_usuario = ?", (id_proyecto, id_usuario))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    def get_projects_by_user_id(self, id_usuario):
        query = "SELECT id_proyecto FROM vista_colaboradores_base WHERE id_usuario = ?"
        self.cursor.execute(query, (id_usuario,))
        return self.cursor.fetchall()
    
    def get_users_by_project_id(self, id_proyecto):
        query = "SELECT id_usuario FROM vista_colaboradores_base WHERE id_proyecto = ?"
        self.cursor.execute(query, (id_proyecto,))
        return self.cursor.fetchall()
    
    def get_all_colaboradores(self):
        query = "SELECT id_proyecto, id_usuario FROM vista_colaboradores_base"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_content_projects_by_colaborador(self, id_usuario):
        query = """
            SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, fecha_creacion, visibilidad, id_creador, nombre_usuario FROM vista_colaboradores_detalle
            WHERE id_usuario = ?
        """
        self.cursor.execute(query, (id_usuario,))
        return self.cursor.fetchall()
    
    def get_content_project_by_colaborador(self, id_project, id_usuario):
        query = """
            SELECT id_proyecto, nombre_proyecto, descripcion_proyecto, fecha_creacion, visibilidad, id_creador, nombre_usuario FROM vista_colaboradores_detalle
            WHERE id_proyecto = ? AND id_usuario = ?
        """
        self.cursor.execute(query, (id_project, id_usuario))
        return self.cursor.fetchone()
    
    def get_all_colaboradores_by_project(self, id_proyecto):
        query = """
            SELECT DISTINCT id_usuario, nombre_usuario, email, contraseña ,fecha_registro, biografia
            FROM vista_colaboradores_detalle
            WHERE id_proyecto = ?
        """
        self.cursor.execute(query, (id_proyecto,))
        return self.cursor.fetchall()


    def add_colaborator_gmail(self, id_proyecto, gmail_colaborador, id_colaborador, nombre_proyecto):
        try:
            self.cursor.execute("EXEC add_colaborador @id_proyecto = ?, @id_usuario = ?", (id_proyecto, id_colaborador))
            self.connection.commit()  # Confirmar los cambios
            if True:
                # Enviar correo al colaborador
                enviar_correo(gmail_colaborador,"Colaboración en proyecto","Has sido añadido como colaborador en el proyecto.",nombre_proyecto)
                return True
        except Exception as e:
            self.connection.rollback()
            return False

    