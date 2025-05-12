from flask import Flask, render_template, request, redirect, url_for, session, send_file, Response
import os, dotenv
import pyodbc
import zipfile
import io
from datetime import datetime
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
        proyectos_colaborativos = proyectosDao.get_projects_collaborative(session["user_id"])
        proyectos_publicos = proyectosDao.get_projects_publics_not_myself(session["user_id"])

        return render_template("home.html", proyectos=proyectos, proyectos_colaborativos=proyectos_colaborativos, proyectos_publicos=proyectos_publicos)
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
        comentarios = comentariosDao.get_comment_by_project_id(project_id)
        archivos = archivosDao.get_files_by_project_id(project_id)
        colaboradores = colaboradorDao.get_all_colaboradores_by_project(project_id)
        project_owner = proyectosDao.get_project_owner(project_id)
        tipos_archivo = TipoArchivoDao.get_all_file_types()
        error = request.args.get("error")
        return render_template("project.html", project=project, comentarios=comentarios, archivos=archivos, colaboradores=colaboradores, tipos_archivo=tipos_archivo, error=error, project_owner=project_owner)
    else:
        return redirect(url_for("index"))


@app.route("/home/view_project_public/<int:project_id>")
def view_project_public(project_id):
    if "user_id" in session:
        project = proyectosDao.get_project_by_id(project_id)
        comentarios = comentariosDao.get_comment_by_project_id(project_id)
        archivos = archivosDao.get_files_by_project_id(project_id)
        colaboradores = colaboradorDao.get_all_colaboradores_by_project(project_id)
        project_owner = proyectosDao.get_project_owner(project_id)
        tipos_archivo = TipoArchivoDao.get_all_file_types()
        error = request.args.get("error")
        return render_template("project_public.html", project=project, comentarios=comentarios, archivos=archivos, colaboradores=colaboradores, tipos_archivo=tipos_archivo, error=error, project_owner=project_owner)
    else:
        return redirect(url_for("index"))
    

@app.route("/home/view_project/new_file/<int:project_id>", methods=["POST"])
def add_file(project_id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        id_usuario = session["user_id"]
        id_proyecto = project_id
        tipo_archivo = request.form["tipo_archivo"]
        sucess = archivosDao.create_file(nombre, id_proyecto, id_usuario, tipo_archivo)
        if sucess:
            return redirect(url_for("view_project", project_id=project_id))
        else:
            error = "Error creating file"
            return redirect(url_for("view_project", project_id=project_id, error=error))
    else:
        return redirect(url_for("view_project", project_id=project_id))


@app.route("/home/view_project/edit_file/<int:file_id>", methods=["POST"])
def edit_file(file_id):
    if request.method == "POST":
        project_id = request.form["project_id"]
        contenido = request.form["contenido"]
        id_usuario = session["user_id"]
        
        if archivosDao.update_content(file_id, contenido, id_usuario):
            return redirect(url_for("view_project", project_id=project_id))
        else:
            error = "Error updating file"
            return redirect(url_for("view_project", project_id=project_id, error=error))
    else:
        return redirect(url_for("view_project", project_id=project_id))
    
@app.route("/home/view_project/delete_file/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    project_id = request.form["project_id"]
    if archivosDao.delete_file(file_id):
        return redirect(url_for("view_project", project_id=project_id))
    else:
        error = "Error deleting file"
        return redirect(url_for("view_project", project_id=project_id))



#COLABORADORES
@app.route("/home/view_project/add_colaborator/<int:project_id>", methods=["POST"])
def add_collaborator(project_id):
    if request.method == "POST":
        gmail_colaborador = request.form["collaborator_email"]
        id_colaborador = usuariosDao.get_user_by_email(gmail_colaborador)
        project_name = proyectosDao.get_project_by_id(project_id)[1]
        if id_colaborador:
            #revisar si el colaborador ya existe en el proyecto
            colaborador_existente = colaboradorDao.get_content_project_by_colaborador(project_id, id_colaborador[0])
            if colaborador_existente:
                error = "Collaborator already exists in the project"
                return redirect(url_for("view_project", project_id=project_id, error=error))
            colaboradorDao.add_colaborator_gmail(project_id, gmail_colaborador, id_colaborador[0], project_name)
            return redirect(url_for("view_project", project_id=project_id))
        else:
            error = "Error adding collaborator"
            return redirect(url_for("view_project", project_id=project_id, error=error))
    else:
        return redirect(url_for("view_project", project_id=project_id))
    
@app.route("/home/view_project/delete_colaborator/<int:colaborador_id>", methods=["POST"])
def delete_collaborator(colaborador_id):
    project_id = request.form["project_id"]
    sucess = colaboradorDao.remove_colaborador(project_id, colaborador_id)
    if sucess:
        return redirect(url_for("view_project", project_id=project_id))
    else:
        error = "Error deleting collaborator"
        return redirect(url_for("view_project", project_id=project_id))


#COMENTARIOS
@app.route("/home/view_project/add_comment", methods=["POST"])
def add_comment():
    if request.method == "POST":
        id_usuario = session["user_id"]
        id_proyecto = request.form["project_id"]
        contenido = request.form["contenido"]
        id_archivo = request.form["id_archivo"]
        linea_codigo = request.form["linea_codigo"]
        
        if comentariosDao.create_comment(contenido, id_usuario, id_proyecto, id_archivo, linea_codigo):
            return redirect(url_for("view_project", project_id=id_proyecto))
        else:
            error = "Error creating comment"
            return redirect(url_for("view_project", project_id=id_proyecto, error=error))
    else:
        return redirect(url_for("home"))


#VERSIONES DE ARCHIVOS
@app.route("/home/view_project/version_file/<int:file_id>", methods=["GET"])
def view_file_version(file_id):
    if "user_id" in session:
        file = archivosDao.get_file_by_id(file_id)
        project_id = file[4]
        versions = archivosDao.get_file_versions(file_id)
        return render_template("file_version.html", file=file, versions=versions, project_id=project_id)
    else:
        return redirect(url_for("index"))



#DESCARGAS
@app.route("/home/view_project/download_file/<int:file_id>")
def download_file(file_id):
    if "user_id" in session:
        file = archivosDao.get_file_by_id(file_id)
        if file:
            # Crear archivo en memoria
            file_data = io.BytesIO()
            file_data.write(file[2].encode('utf-8'))
            file_data.seek(0)
            
            # Enviar archivo como descarga
            return send_file(
                file_data,
                as_attachment=True,
                download_name=file[1],
                mimetype='text/plain'
            )
        return redirect(url_for('view_project', project_id=file[4], error="Archivo no encontrado"))
    else:
        return redirect(url_for("index"))
    


@app.route("/home/view_project/download_version/<int:version_id>")
def download_version(version_id):
    if "user_id" in session:
        version = archivosDao.get_version_by_id(version_id)
        if version:
            # Obtener el archivo principal para su nombre
            file = archivosDao.get_file_by_id(version[0])
            
            # Crear archivo en memoria
            file_data = io.BytesIO()
            file_data.write(version[1].encode('utf-8'))
            file_data.seek(0)
            
            # Nombre con timestamp para diferenciar versión
            version_date = version[2].strftime('%Y%m%d_%H%M')
            filename = f"{file[1].split('.')[0]}_{version_date}.{file[1].split('.')[-1]}"
            
            # Enviar archivo como descarga
            return send_file(
                file_data,
                as_attachment=True,
                download_name=filename,
                mimetype='text/plain'
            )
        return redirect(url_for('index', error="Versión no encontrada"))
    else:
        return redirect(url_for("index"))
    

@app.route("/home/view_project/download_project/<int:project_id>")
def download_project(project_id):
    if "user_id" in session:
        project = proyectosDao.get_project_by_id(project_id)
        archivos = archivosDao.get_files_by_project_id(project_id)
        
        if project:
            # Crear el archivo ZIP en memoria
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Agregar README.md como primer archivo si existe
                readme_file = None
                for archivo in archivos:
                    if archivo[1].lower() == 'readme.md':
                        readme_file = archivo
                        break
                
                if readme_file:
                    zipf.writestr(readme_file[1], readme_file[2])
                
                # Agregar el resto de archivos
                for archivo in archivos:
                    if archivo != readme_file:  # Evita duplicar el README
                        zipf.writestr(archivo[1], archivo[2])
            
            # Preparar el archivo para su descarga
            memory_file.seek(0)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            zipname = f"{project[1].replace(' ', '_')}_{timestamp}.zip"
            
            return send_file(
                memory_file,
                mimetype='application/zip',
                as_attachment=True,
                download_name=zipname
            )
            
        return redirect(url_for('home', error="Proyecto no encontrado"))
    else:
        return redirect(url_for("index"))



#DESCARGAS PROYECTOS PUBLICOS
@app.route("/home/view_project_public/download_file/<int:file_id>")
def download_file_public(file_id):
    if "user_id" in session:
        file = archivosDao.get_file_by_id(file_id)
        if file:
            # Crear archivo en memoria
            file_data = io.BytesIO()
            file_data.write(file[2].encode('utf-8'))
            file_data.seek(0)
            
            # Enviar archivo como descarga
            return send_file(
                file_data,
                as_attachment=True,
                download_name=file[1],
                mimetype='text/plain'
            )
        return redirect(url_for('view_project_public', project_id=file[4], error="Archivo no encontrado"))
    else:
        return redirect(url_for("index"))


#MI PERFIL 
@app.route("/home/profile", methods=["GET", "POST"])
def profile():
    if "user_id" in session:
        if request.method == "POST":
            nombre_usuario = request.form["nombre_usuario"]
            email = request.form["email"]
            biografia = request.form["biografia"]
            contraseña = None
            
            if usuariosDao.update_user(session["user_id"], nombre_usuario, email, contraseña, biografia):
                user = usuariosDao.get_user_by_id(session["user_id"])
                if user:
                    
                    session["nombre_usuario"] = user[1]
                    session["email"] = user[2]
                    session["biografia"] = user[5]
                    return redirect(url_for("home"))
            else:
                error = "Error updating profile"
                return render_template("profile.html", error=error)
        else:
            user = usuariosDao.get_user_by_id(session["user_id"])
            error = request.args.get("error")
            return render_template("profile.html", user=user, error=error)
    else:
        return redirect(url_for("index"))

@app.route("/home/profile/change_password", methods=["POST"])
def change_password():
    if "user_id" in session:
        if request.method == "POST":
            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]
            if usuariosDao.update_password(session["user_id"], old_password, new_password, confirm_password):
                return redirect(url_for("home"))
            else:
                error = "Error updating password"
                return redirect(url_for("profile", error=error))
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
