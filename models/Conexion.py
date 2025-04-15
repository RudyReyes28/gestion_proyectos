import pyodbc

class Conexion:
    def __init__(self):
        self.conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=DESKTOP-OAP2EF6;"
            "Database=GestionProyectos;"
            'UID=Alessandro;'
            'PWD=1234'
        )
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

    
    def close(self):
        self.cursor.close()
        self.conn.close()
