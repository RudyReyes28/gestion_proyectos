
class ArchivosDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def create_file(self, nombre, id_proyecto, id_usuario_modificador, id_tipo_archivo):
        try:
            self.cursor.execute("EXEC proc_create_file @nombre=?, @id_proyecto=?, @id_usuario_modificador=?, @id_tipo_archivo=?", 
                            (nombre, id_proyecto, id_usuario_modificador, id_tipo_archivo))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    
    def update_file(self, file_id, nombre=None, contenido=None):
        try:
            self.cursor.execute("EXEC proc_update_file @file_id=?, @nombre=?, @contenido=?",
                            (file_id, nombre, contenido))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    def delete_file(self, file_id):
        try:
            self.cursor.execute("EXEC proc_delete_file @file_id=?", (file_id,))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    def get_file_by_id(self, file_id):
        query = "SELECT * FROM view_archivos WHERE id = ?"
        self.cursor.execute(query, (file_id,))
        return self.cursor.fetchone()
    
    def get_files_by_project_id(self, project_id):
        query = "SELECT * FROM view_archivos WHERE id_proyecto = ?"
        self.cursor.execute(query, (project_id,))
        return self.cursor.fetchall()
    
    def get_files_by_user_id(self, user_id):
        query = "SELECT * FROM view_archivos WHERE id_usuario_modificador = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def update_content(self, file_id, contenido, id_usuario_modificador):
        try:
            self.cursor.execute("EXEC proc_update_content @file_id=?, @contenido=?, @id_usuario_modificador=?",
                            (file_id, contenido, id_usuario_modificador))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    
    
    def get_file_versions(self, file_id):
        """Obtiene todas las versiones de un archivo"""
        try:
            query = """
                SELECT id, contenido, fecha_version, id_usuario, nombre_usuario
                FROM view_versiones_archivo 
                WHERE id_archivo = ?
                ORDER BY fecha_version DESC
                """
            self.cursor.execute(query, (file_id,))
            versions = self.cursor.fetchall()
            return versions
        except Exception as e:
            print(f"Error al obtener versiones del archivo: {e}")
        return []

    def get_version_by_id(self, version_id):
        """Obtiene una versión específica por su ID"""
        try:
            query = """
            SELECT id_archivo, contenido, fecha_version, id_usuario
            FROM Versiones_Archivo
            WHERE id = ?
            """
            self.cursor.execute(query, (version_id,))
            version = self.cursor.fetchone()
            return version
        except Exception as e:
            print(f"Error al obtener la versión: {e}")
        return None
