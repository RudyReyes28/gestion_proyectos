# API - Sistema de Gestión de Proyectos

Esta API corresponde a un sistema web de gestión de proyectos colaborativos, similar a GitHub, desarrollada con Flask.

## Índice
- [Autenticación y Registro](#autenticación-y-registro)
- [Gestión de Proyectos](#gestión-de-proyectos)
- [Gestión de Archivos](#gestión-de-archivos)
- [Sistema de Colaboradores](#sistema-de-colaboradores)
- [Sistema de Comentarios](#sistema-de-comentarios)
- [Sistema de Versiones](#sistema-de-versiones)
- [Sistema de Descargas](#sistema-de-descargas)
- [Gestión de Perfil](#gestión-de-perfil)

## Autenticación y Registro

---

### `/`
- **Método:** `GET`
- **Descripción:** Redirige a la página de inicio de sesión.
- **Interacción:** Esta es la ruta base que automáticamente lleva al usuario a la página de login.

---

### `/home`
- **Método:** `GET`
- **Descripción:** Muestra la página principal con los proyectos del usuario autenticado.
- **Interacción:** Requiere autenticación previa. Muestra proyectos propios, proyectos colaborativos y proyectos públicos de otros usuarios.

---

### `/login`
- **Métodos:** `GET`, `POST`
- **Descripción:** Permite al usuario iniciar sesión en el sistema.
- **GET:** Muestra el formulario de inicio de sesión.
- **POST:** Procesa el formulario con estos parámetros:
  - `correo` - Email del usuario
  - `contraseña` - Contraseña del usuario
- **Interacción:** En caso de éxito, establece variables de sesión y redirige a la página principal. En caso de error, muestra un mensaje.

---

### `/logout`
- **Método:** `GET`
- **Descripción:** Cierra la sesión del usuario actual.
- **Interacción:** Elimina todas las variables de sesión y redirige a la página de inicio.

---

### `/register`
- **Métodos:** `GET`, `POST`
- **Descripción:** Permite a los usuarios crear una nueva cuenta.
- **GET:** Muestra el formulario de registro.
- **POST:** Procesa el formulario con estos parámetros:
  - `nombre_usuario` - Nombre del usuario
  - `email` - Correo electrónico
  - `contraseña` - Contraseña elegida
  - `biografia` - Descripción personal del usuario
- **Interacción:** En caso de éxito, redirige al inicio de sesión. En caso de error, muestra un mensaje.

## Gestión de Proyectos

---

### `/home/my_projects`
- **Método:** `GET`
- **Descripción:** Muestra todos los proyectos creados por el usuario autenticado.
- **Interacción:** Requiere autenticación. Lista todos los proyectos donde el usuario es propietario.

---

### `/home/my_projects/add_project`
- **Métodos:** `GET`, `POST`
- **Descripción:** Permite crear un nuevo proyecto.
- **GET:** Muestra el formulario para crear un proyecto.
- **POST:** Procesa el formulario con estos parámetros:
  - `nombre` - Nombre del proyecto
  - `descripcion` - Descripción del proyecto
  - `visibilidad` - Visibilidad del proyecto (público o privado)
- **Interacción:** El ID del usuario se obtiene de la sesión. En caso de éxito, redirige a la página principal.

---

### `/home/my_projects/edit_project/<int:project_id>`
- **Métodos:** `GET`, `POST`
- **Descripción:** Permite editar la información de un proyecto existente.
- **GET:** Muestra el formulario con los datos actuales del proyecto.
- **POST:** Procesa el formulario con estos parámetros:
  - `nombre` - Nombre actualizado
  - `descripcion` - Descripción actualizada
  - `visibilidad` - Visibilidad actualizada
- **Interacción:** En caso de éxito, redirige a la página principal.

---

### `/home/delete_projects/<int:project_id>`
- **Método:** `GET`
- **Descripción:** Permite eliminar un proyecto existente.
- **Interacción:** Elimina el proyecto especificado por el ID y redirige a la página principal.

---

### `/home/view_project/<int:project_id>`
- **Método:** `GET`
- **Descripción:** Muestra la información completa de un proyecto con opciones de edición.
- **Interacción:** Muestra detalles del proyecto, archivos, colaboradores, comentarios y las opciones de edición para propietarios y colaboradores.

---

### `/home/view_project_public/<int:project_id>`
- **Método:** `GET`
- **Descripción:** Muestra la información de un proyecto público sin opciones de edición.
- **Interacción:** Similar a la vista de proyecto normal, pero con permisos limitados para proyectos públicos.

## Gestión de Archivos

---

### `/home/view_project/new_file/<int:project_id>`
- **Método:** `POST`
- **Descripción:** Permite crear un nuevo archivo en un proyecto.
- **Interacción:** Requiere estos parámetros:
  - `nombre` - Nombre del archivo
  - `tipo_archivo` - Tipo de archivo a crear
- El ID del usuario se obtiene de la sesión. En caso de éxito, redirige a la vista del proyecto.

---

### `/home/view_project/edit_file/<int:file_id>`
- **Método:** `POST`
- **Descripción:** Permite editar el contenido de un archivo existente.
- **Interacción:** Requiere estos parámetros:
  - `project_id` - ID del proyecto al que pertenece el archivo
  - `contenido` - Nuevo contenido del archivo
- Cada edición guarda automáticamente una versión del archivo. En caso de éxito, redirige a la vista del proyecto.

---

### `/home/view_project/delete_file/<int:file_id>`
- **Método:** `POST`
- **Descripción:** Permite eliminar un archivo existente.
- **Interacción:** Requiere el parámetro:
  - `project_id` - ID del proyecto al que pertenece el archivo
- En caso de éxito, redirige a la vista del proyecto.

## Sistema de Colaboradores

---

### `/home/view_project/add_colaborator/<int:project_id>`
- **Método:** `POST`
- **Descripción:** Permite añadir un colaborador a un proyecto.
- **Interacción:** Requiere el parámetro:
  - `collaborator_email` - Email del usuario a invitar
- Verifica que el usuario exista y que no sea ya un colaborador. En caso de éxito, redirige a la vista del proyecto.

---

### `/home/view_project/delete_colaborator/<int:colaborador_id>`
- **Método:** `POST`
- **Descripción:** Permite eliminar un colaborador de un proyecto.
- **Interacción:** Requiere el parámetro:
  - `project_id` - ID del proyecto
- En caso de éxito, redirige a la vista del proyecto.

## Sistema de Comentarios

---

### `/home/view_project/add_comment`
- **Método:** `POST`
- **Descripción:** Permite añadir un comentario a un proyecto o archivo específico.
- **Interacción:** Requiere estos parámetros:
  - `project_id` - ID del proyecto
  - `contenido` - Contenido del comentario
  - `id_archivo` - ID del archivo (opcional)
  - `linea_codigo` - Línea específica de código (opcional)
- El ID del usuario se obtiene de la sesión. En caso de éxito, redirige a la vista del proyecto.

## Sistema de Versiones

---

### `/home/view_project/version_file/<int:file_id>`
- **Método:** `GET`
- **Descripción:** Muestra todas las versiones anteriores de un archivo.
- **Interacción:** Muestra una lista de las versiones del archivo con sus fechas y autores.

## Sistema de Descargas

---

### `/home/view_project/download_file/<int:file_id>`
- **Método:** `GET`
- **Descripción:** Permite descargar un archivo individual.
- **Interacción:** Descarga el archivo especificado por el ID con su nombre original.

---

### `/home/view_project/download_version/<int:version_id>`
- **Método:** `GET`
- **Descripción:** Permite descargar una versión específica de un archivo.
- **Interacción:** Descarga la versión del archivo con un nombre que incluye la fecha y hora de la versión.

---

### `/home/view_project/download_project/<int:project_id>`
- **Método:** `GET`
- **Descripción:** Permite descargar todos los archivos de un proyecto como un archivo ZIP.
- **Interacción:** Crea un archivo ZIP con todos los archivos del proyecto, colocando el README.md primero si existe.

---

### `/home/view_project_public/download_file/<int:file_id>`
- **Método:** `GET`
- **Descripción:** Permite a cualquier usuario descargar un archivo de un proyecto público.
- **Interacción:** Similar a la descarga normal pero desde la vista pública del proyecto.

## Gestión de Perfil

---

### `/home/profile`
- **Métodos:** `GET`, `POST`
- **Descripción:** Permite al usuario ver y actualizar su información de perfil.
- **GET:** Muestra el formulario con los datos actuales del usuario.
- **POST:** Procesa el formulario con estos parámetros:
  - `nombre_usuario` - Nombre actualizado
  - `email` - Email actualizado
  - `biografia` - Biografía actualizada
- **Interacción:** En caso de éxito, actualiza los datos de sesión y redirige a la página principal.

---

### `/home/profile/change_password`
- **Método:** `POST`
- **Descripción:** Permite al usuario cambiar su contraseña.
- **Interacción:** Requiere estos parámetros:
  - `old_password` - Contraseña actual
  - `new_password` - Nueva contraseña
  - `confirm_password` - Confirmación de la nueva contraseña
- Verifica que la contraseña actual sea correcta y que las nuevas contraseñas coincidan. En caso de éxito, redirige a la página principal.