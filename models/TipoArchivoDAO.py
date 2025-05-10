class TipoArchivoDAO:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def get_all(self):
        query = "SELECT * FROM tipo_archivo"
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def get_by_id(self, id):
        query = "SELECT * FROM tipo_archivo WHERE id = %s"
        cursor = self.db.cursor()
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        return row

    def create(self, nombre):
        query = "INSERT INTO tipo_archivo (nombre) VALUES (%s)"
        cursor = self.db.cursor()
        cursor.execute(query, (nombre,))
        self.db.commit()
        return cursor.lastrowid

    def update(self, id, nombre):
        query = "UPDATE tipo_archivo SET nombre = %s WHERE id = %s"
        cursor = self.db.cursor()
        cursor.execute(query, (nombre, id))
        self.db.commit()

    def delete(self, id):
        query = "DELETE FROM tipo_archivo WHERE id = %s"
        cursor = self.db.cursor()
        cursor.execute(query, (id,))
        self.db.commit()