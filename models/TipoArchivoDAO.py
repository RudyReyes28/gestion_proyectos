class TipoArchivoDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all_file_types(self):
        query = "EXEC Obtener_Todos_Tipo_Archivo"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_file_type_by_id(self, file_type_id):
        query = "EXEC Obtener_Tipo_Archivo_Por_ID ?"
        self.cursor.execute(query, (file_type_id,))
        return self.cursor.fetchone()

    def create_file_type(self, name, extension):
        try:
            query = "EXEC Crear_Tipo_Archivo ?, ?"
            self.cursor.execute(query, (name, extension))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error al crear tipo de archivo: {e}")
            return False

    def update_file_type(self, file_type_id, name, extension):
        query = "EXEC Actualizar_Tipo_Archivo ?, ?, ?"
        self.cursor.execute(query, (file_type_id, name, extension))
        self.connection.commit()
        return self.cursor.rowcount > 0
    