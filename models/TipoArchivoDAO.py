class TipoArchivoDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all_file_types(self):
        query = "SELECT * FROM Vista_Tipo_Archivo"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_file_type_by_id(self, file_type_id):
        query = "SELECT * FROM Vista_Tipo_Archivo WHERE id = ?"
        self.cursor.execute(query, (file_type_id,))
        return self.cursor.fetchone()

    def create_file_type(self, name, extension):
        try:
            query = "DECLARE @resultado BIT; EXEC Crear_Tipo_Archivo ?, ?, @resultado OUTPUT; SELECT @resultado;"
            self.cursor.execute(query, (name, extension))
            result = self.cursor.fetchone()[0] 
            self.connection.commit()
            return bool(result)
        except Exception as e:
            print(f"Error al crear tipo de archivo: {e}")
            return False

    def update_file_type(self, file_type_id, name, extension):
        query = "UPDATE Tipo_Archivo SET nombre = ?, extension = ? WHERE id = ?"
        self.cursor.execute(query, (file_type_id, name, extension))
        self.connection.commit()
        return self.cursor.rowcount > 0
    