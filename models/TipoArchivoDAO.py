class TipoArchivoDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all_file_types(self):
        query = "SELECT * FROM Tipo_Archivo"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_file_type_by_id(self, file_type_id):
        query = "SELECT * FROM Tipo_Archivo WHERE id = ?"
        self.cursor.execute(query, (file_type_id,))
        return self.cursor.fetchone()
    
    def create_file_type(self, name):
        query = "INSERT INTO Tipo_Archivo (nombre) VALUES (?)"
        self.cursor.execute(query, (name,))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def update_file_type(self, file_type_id, name):
        query = "UPDATE Tipo_Archivo SET nombre = ? WHERE id = ?"
        self.cursor.execute(query, (name, file_type_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    