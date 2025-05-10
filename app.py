from flask import Flask, render_template, request, redirect, url_for, session
import os, dotenv
import pyodbc
from models.Conexion import Conexion
from models.ArchivosDAO import ArchivosDAO
from models.ColaboradorDAO import ColaboradorDAO
from models.ComentariosDAO import ComentariosDAO
from models.ProyectosDAO import ProyectosDAO
from models.UsuariosDAO import UsuariosDAO
from models.TipoArchivoDAO import TipoArchivoDAO

dotenv.load_dotenv()
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_driver = os.environ.get('DB_DRIVER')

#conexion = Conexion()
conn_str = (
    f"Driver={db_driver};"
    f"Server={db_host};"
    f"Database={db_name};"
    f"UID={db_user};"
    f"PWD={db_password}"
)

conexion = pyodbc.connect(conn_str)
archivosDao = ArchivosDAO(conexion)
colaboradorDao = ColaboradorDAO(conexion)
comentariosDao = ComentariosDAO(conexion)
proyectosDao = ProyectosDAO(conexion)
usuariosDao = UsuariosDAO(conexion)
TipoArchivoDao = TipoArchivoDAO(conexion)


app = Flask(__name__)
app.secret_key = 'clave_super_secreta'


@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if "user_id" in session:
        proyectos = proyectosDao.get_projects_by_user(session["user_id"])
        return render_template("home.html", proyectos=proyectos)
    else:
        return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["correo"]
        contraseña = request.form["contraseña"]

        user = usuariosDao.authenticate_user(email, contraseña)
        if user:
            session["user_id"] = user[0]
            session["nombre_usuario"] = user[1]
            session["email"] = user[2]
            session["fecha_registro"] = user[4]
            session["biografia"] = user[5]
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials"
            return render_template("login.html", error=error)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre_usuario = request.form["nombre_usuario"]
        email = request.form["email"]
        contraseña = request.form["contraseña"]
        biografia = request.form["biografia"]
        
        if usuariosDao.create_user(nombre_usuario, email, contraseña, biografia):
            return redirect(url_for("index"))
        else:
            error = "Error creating user"
            return render_template("register.html", error=error)
    return render_template("register.html")
    

#manejo de proyectos
@app.route("/home/my_projects")
def my_projects():
    if "user_id" in session:
        proyectos = proyectosDao.get_projects_by_user(session["user_id"])
        return render_template("my_projects.html", proyectos=proyectos)
    else:
        return redirect(url_for("index"))
    


@app.route("/home/my_projects/add_project", methods=["GET","POST"])
def add_project():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        visibilidad = request.form["visibilidad"]
        id_usuario = session["user_id"]
        
        if proyectosDao.create_project(nombre, descripcion, visibilidad, id_usuario):
            return redirect(url_for("home"))
        else:
            error = "Error creating project"
            return render_template("add_project.html", error=error)
    else:
        return render_template("add_project.html")


    

@app.route("/home/my_projects/edit_project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        visibilidad = request.form["visibilidad"]
        
        if proyectosDao.update_project(project_id, nombre, descripcion, visibilidad):
            return redirect(url_for("home"))
        else:
            error = "Error updating project"
            return render_template("edit_project.html", error=error)
    else:
        project = proyectosDao.get_project_by_id(project_id)
        return render_template("edit_project.html", project=project)
    
@app.route("/home/delete_projects/<int:project_id>")
def delete_project(project_id):
    if proyectosDao.delete_project(project_id):
        return redirect(url_for("home"))
    else:
        error = "Error deleting project"
        return render_template("home.html", error=error)



#VER PROYECTOS Y MANEJAR ARCHIVOS
@app.route("/home/view_project/<int:project_id>")
def view_project(project_id):
    if "user_id" in session:
        project = proyectosDao.get_project_by_id(project_id)
        comentarios = comentariosDao.get_comments_by_project(project_id)
        archivos = archivosDao.get_files_by_project(project_id)
        colaboradores = colaboradorDao.get_collaborators_by_project(project_id)
        return render_template("project.html", project=project, comentarios=comentarios, archivos=archivos, colaboradores=colaboradores)
    else:
        return redirect(url_for("index"))


@app.route("/home/view_project/new_file/<int:project_id>", methods=["POST"])
def add_file(project_id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        id_usuario = session["user_id"]
        id_proyecto = project_id
        tipo_archivo = request.form["tipo_archivo"]
        sucess = archivosDao.create_file(nombre, id_usuario, id_proyecto, tipo_archivo)
        if sucess:
            return redirect(url_for("view_project", project_id=project_id))
        else:
            error = "Error creating file"
            return render_template("project.html", error=error)
    else:
        return redirect(url_for("view_project", project_id=project_id))


@app.route("/home/view_project/edit_file/<int:file_id>", methods=["POST"])
def edit_file(file_id):
    if request.method == "POST":
        project_id = request.form["project_id"]
        contenido = request.form["contenido"]
        
        if archivosDao.update_file(file_id, contenido):
            return redirect(url_for("view_project", project_id=project_id))
        else:
            error = "Error updating file"
            return render_template("project.html", error=error)
    else:
        return redirect(url_for("view_project", project_id=project_id))
    
@app.route("/home/view_project/delete_file/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    project_id = request.form["project_id"]
    if archivosDao.delete_file(file_id):
        return redirect(url_for("view_project", project_id=project_id))
    else:
        error = "Error deleting file"
        return render_template("project.html", error=error)



if __name__ == "__main__":
    app.run(debug=True)
