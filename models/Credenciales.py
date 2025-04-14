import pyodbc
class Credenciales:
    def __init__ (self, conexion):
        self.conexion = conexion
        self.cursor = self.conexion.cursor()

    def verificar_usuario(self, usuario, contrasena):
        consulta = "SELECT u.*, r.tipo_usuario FROM USUARIO u INNER JOIN ROL r ON u.rol_id = r.id WHERE u.usuario = ? AND u.contrasena = ?"
        self.cursor.execute(consulta, (usuario, contrasena))
        resultado = self.cursor.fetchone()
        return resultado
    
    def registrar_usuario(self, user_name, password, nombre, apellido, rol_id):
        consulta = """
        INSERT INTO USUARIO (user_name, password, nombre, apellido, id_rol)
        OUTPUT INSERTED.id_usuario
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(consulta, (user_name, password, nombre, apellido, rol_id))
        self.conexion.commit()
        id_usuario = self.cursor.fetchone()[0]
        if(rol_id == 2):
            consulta = "INSERT INTO USUARIO_PUBLICADOR (id_usuario) VALUES (?)"
            self.cursor.execute(consulta, (id_usuario,))
            self.conexion.commit()
        
        return self.cursor.rowcount
    
