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
        try:
            
            hashed_password = generate_password_hash(contraseña)
            self.cursor.execute("EXEC proc_create_user @nombre_usuario=?, @email=?, @contraseña=?, @biografia=?", 
                            (nombre_usuario, email, hashed_password, biografia))
            
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
        
    
    def update_user(self, user_id, nombre_usuario=None, email=None, biografia=None):
        try:
            self.cursor.execute("EXEC proc_update_user @id=?, @nombre_usuario=?, @email=?, @biografia=?",
                            (user_id, nombre_usuario, email, biografia))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    def update_password(self, user_id, old_password, new_password, confirm_password):
        if new_password != confirm_password:
            return False
        query = "SELECT contraseña FROM view_usuarios WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        user = self.cursor.fetchone()
        if not user or not check_password_hash(user[0], old_password):
            return False
        if not new_password:
            return False
        
        new_password = generate_password_hash(new_password)
        query = "UPDATE Usuarios SET contraseña = ? WHERE id = ?"
        self.cursor.execute(query, (new_password, user_id))
        self.connection.commit()
        return self.cursor.rowcount > 0
    
    def delete_user(self, user_id):
        query = "DELETE FROM Usuarios WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.connection.commit() 
        return self.cursor.rowcount > 0
    
    def get_user_by_id(self, user_id):
        query = "SELECT * FROM view_usuarios WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def authenticate_user(self, email, contraseña):
        query = "SELECT * FROM view_usuarios WHERE email = ?"
        self.cursor.execute(query, (email,))
        user = self.cursor.fetchone()
        if user and check_password_hash(user[3], contraseña):
            return user
        return None
    
    def get_users(self):
        query = "SELECT * FROM view_usuarios"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_user_by_email(self, email):
        query = "SELECT * FROM view_usuarios WHERE email = ?"
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone()
    