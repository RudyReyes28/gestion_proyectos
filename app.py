from flask import Flask, render_template, request, redirect, url_for, session

from models.Conexion import Conexion
from models.ArchivosDAO import ArchivosDAO
from models.ColaboradorDAO import ColaboradorDAO
from models.ComentariosDAO import ComentariosDAO
from models.ProyectosDAO import ProyectosDAO
from models.UsuariosDAO import UsuariosDAO

conexion = Conexion()
archivosDao = ArchivosDAO(conexion)
colaboradorDao = ColaboradorDAO(conexion)
comentariosDao = ComentariosDAO(conexion)
proyectosDao = ProyectosDAO(conexion)
usuariosDao = UsuariosDAO(conexion)


app = Flask(__name__)
app.secret_key = 'clave_super_secreta'


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/home")
def home():
    if "user_id" in session:
        proyectos = proyectosDao.get_projects_by_user(session["user_id"])
        return render_template("home.html", proyectos=proyectos)
    else:
        return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form["email"]
    password = request.form["password"]
    user = usuariosDao.authenticate_user(username, password)
    if user:
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        session["user_email"] = user[2]
        session["user_biografia"] = user[5]
        return redirect(url_for("home"))
    else:
        error = "Invalid username or password"
        return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register", methods=["POST"])
def register():
    nombre = request.form["nombre"]
    email = request.form["email"]
    password = request.form["password"]
    biografia = request.form["biografia"]
    if usuariosDao.create_user(nombre, email, password, biografia):
        return redirect(url_for("index"))
    else:
        error = "Error creating user"
        return render_template("login.html", error=error)
    

#manejo de proyectos
@app.route("/home/create_project", methods=["POST"])
def create_project():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    visibilidad = request.form["visibilidad"]
    id_creador = session["user_id"]
    
    if proyectosDao.create_project(nombre, descripcion, visibilidad, id_creador):
        return redirect(url_for("home"))
    else:
        error = "Error creating project"
        return render_template("home.html", error=error)

@app.route("/home/edit_project/<int:project_id>")
def edit_project(project_id):
    if "user_id" in session:
        project = proyectosDao.get_project_by_id(project_id)
        return render_template("edit_project.html", project=project)
    else:
        return redirect(url_for("index"))
    

@app.route("/home/update_project/<int:project_id>", methods=["POST"])
def update_project(project_id):
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    visibilidad = request.form["visibilidad"]
    
    if proyectosDao.update_project(project_id, nombre, descripcion, visibilidad):
        return redirect(url_for("home"))
    else:
        error = "Error updating project"
        return render_template("home.html", error=error)
    
@app.route("/home/delete_project/<int:project_id>")
def delete_project(project_id):
    if proyectosDao.delete_project(project_id):
        return redirect(url_for("home"))
    else:
        error = "Error deleting project"
        return render_template("home.html", error=error)


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
