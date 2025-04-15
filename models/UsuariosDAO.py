from werkzeug.security import generate_password_hash, check_password_hash

"""
CREATE TABLE Usuarios (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre_usuario NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    contraseña NVARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT GETDATE(),
    biografia NVARCHAR(500) NULL
);
"""


class UsuariosDAO:
    def __init__ (self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
    
    def create_user(self, nombre_usuario, email, contraseña, biografia=None):
        query = "INSERT INTO Usuarios (nombre_usuario, email, contraseña, biografia) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (nombre_usuario, email, contraseña, biografia))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def update_user(self, user_id, nombre_usuario=None, email=None, contraseña=None, biografia=None):
        query = "UPDATE Usuarios SET "
        params = []
        if nombre_usuario:
            query += "nombre_usuario = ?, "
            params.append(nombre_usuario)
        if email:
            query += "email = ?, "
            params.append(email)
        if contraseña:
            query += "contraseña = ?, "
            params.append(contraseña)
        if biografia:
            query += "biografia = ? "
            params.append(biografia)
        else:
            query = query.rstrip(", ")
        query += "WHERE id = ?"
        params.append(user_id)
        self.cursor.execute(query, tuple(params))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def update_password(self, user_id, contraseña):
        contraseña = generate_password_hash(contraseña)
        query = "UPDATE Usuarios SET contraseña = ? WHERE id = ?"
        self.cursor.execute(query, (contraseña, user_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_user(self, user_id):
        query = "DELETE FROM Usuarios WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.connection.commit() 
        return self.cursor.rowcount > 0
    
    def get_user_by_id(self, user_id):
        query = "SELECT * FROM Usuarios WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def authenticate_user(self, email, contraseña):
        query = "SELECT * FROM Usuarios WHERE email = ?"
        self.cursor.execute(query, (email,))
        user = self.cursor.fetchone()
        if user and check_password_hash(user[3], contraseña):
            return user
        return None
    
    def get_users(self):
        query = "SELECT * FROM Usuarios"
        self.cursor.execute(query)
        return self.cursor.fetchall()