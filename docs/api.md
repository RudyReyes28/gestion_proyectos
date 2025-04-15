# Documentación de la API y Endpoints

Este documento detalla los endpoints principales de la aplicación Flask para la gestión de proyectos y la autenticación de usuarios. Se incluyen descripciones, rutas y métodos HTTP, así como una breve explicación del comportamiento de cada endpoint.

---

## Tabla de Contenidos

- [Visión General](#visión-general)
- [Endpoints de Autenticación](#endpoints-de-autenticación)
  - [GET `/` - Página de Login](#get--página-de-login)
  - [GET/POST `/login` - Iniciar Sesión](#getpost-login---iniciar-sesión)
  - [GET `/logout` - Cerrar Sesión](#get-logout---cerrar-sesión)
  - [POST `/register` - Registro de Usuario](#post-register---registro-de-usuario)
- [Endpoints de Gestión de Proyectos](#endpoints-de-gestión-de-proyectos)
  - [GET `/home` - Página Principal](#get-home---página-principal)
  - [POST `/home/create_project` - Crear Proyecto](#post-homecreate_project---crear-proyecto)
  - [GET `/home/edit_project/<int:project_id>` - Editar Proyecto](#get-homeedit_projectintproject_id---editar-proyecto)
  - [POST `/home/update_project/<int:project_id>` - Actualizar Proyecto](#post-homeupdate_projectintproject_id---actualizar-proyecto)
  - [GET `/home/delete_project/<int:project_id>` - Eliminar Proyecto](#get-homedelete_projectintproject_id---eliminar-proyecto)
  - [GET `/home/view_project/<int:project_id>` - Ver Detalles del Proyecto](#get-homeview_projectintproject_id---ver-detalles-del-proyecto)
- [Notas Adicionales](#notas-adicionales)

---

## Visión General

La aplicación es un sistema de gestión de proyectos colaborativos inspirado en GitHub. Permite:
- Autenticación y registro de usuarios.
- Gestión básica de proyectos: creación, edición, actualización y eliminación.
- Visualización de detalles de un proyecto, incluyendo comentarios, archivos y colaboradores.

La lógica de negocio se encuentra encapsulada en varios Data Access Objects (DAO) (por ejemplo, `UsuariosDAO`, `ProyectosDAO`, etc.) que se comunican con la base de datos a través de una conexión compartida.

---

## Endpoints de Autenticación

### GET `/`
- **Descripción:**  
  Endpoint principal que muestra la página de login.
- **Método HTTP:** GET
- **Respuesta:** Renderiza la plantilla `login.html`.

---

### GET/POST `/login` - Iniciar Sesión
- **Descripción:**  
  Procesa el inicio de sesión del usuario. Valida email y contraseña a través del DAO de usuarios.  
  - Si la autenticación es exitosa, guarda los datos del usuario en la sesión y redirige a `/home`.
  - En caso contrario, muestra un mensaje de error y vuelve a renderizar `login.html`.
- **Método HTTP:** GET (para renderizar el formulario) y POST (para procesar el login).

---

### GET `/logout` - Cerrar Sesión
- **Descripción:**  
  Cierra la sesión del usuario eliminando los datos guardados en la sesión y redirige a la página de login.
- **Método HTTP:** GET
- **Respuesta:** Redirige a `/`.

---

### POST `/register` - Registro de Usuario
- **Descripción:**  
  Registra un nuevo usuario recibiendo datos del formulario (nombre, email, contraseña, biografía).  
  Si el registro es exitoso, redirige a la página de login; en caso de error, renderiza `login.html` con un mensaje de error.
- **Método HTTP:** POST

---

## Endpoints de Gestión de Proyectos

### GET `/home` - Página Principal
- **Descripción:**  
  Muestra la página principal del usuario autenticado, listando sus proyectos.  
  Si el usuario no está autenticado, se redirige a la página de login.
- **Método HTTP:** GET
- **Respuesta:** Renderiza `home.html` con la lista de proyectos obtenida a partir del ID de usuario almacenado en sesión.

---

### POST `/home/create_project` - Crear Proyecto
- **Descripción:**  
  Permite la creación de un nuevo proyecto. Recibe datos como nombre, descripción y visibilidad del proyecto a través de un formulario.  
  Asocia el proyecto al usuario en sesión.  
  Redirige a `/home` si la creación es exitosa; en caso contrario, muestra un mensaje de error en la misma plantilla.
- **Método HTTP:** POST

---

### GET `/home/edit_project/<int:project_id>` - Editar Proyecto
- **Descripción:**  
  Muestra el formulario para editar un proyecto específico.  
  Requiere que el usuario esté autenticado y utiliza el ID del proyecto para obtener la información actual que será editada.
- **Método HTTP:** GET
- **Respuesta:** Renderiza `edit_project.html` con los detalles del proyecto.

---

### POST `/home/update_project/<int:project_id>` - Actualizar Proyecto
- **Descripción:**  
  Actualiza la información del proyecto basándose en los datos enviados desde el formulario de edición (nombre, descripción, visibilidad).  
  Redirige a `/home` si la actualización es exitosa; en caso contrario, devuelve un mensaje de error.
- **Método HTTP:** POST

---

### GET `/home/delete_project/<int:project_id>` - Eliminar Proyecto
- **Descripción:**  
  Elimina un proyecto utilizando su ID.  
  Redirige a `/home` si la eliminación es exitosa; de lo contrario, muestra un error.
- **Método HTTP:** GET

---

### GET `/home/view_project/<int:project_id>` - Ver Detalles del Proyecto
- **Descripción:**  
  Muestra la vista detallada de un proyecto, incluyendo:
  - Información del proyecto.
  - Comentarios relacionados.
  - Archivos asociados.
  - Colaboradores del proyecto.  
  Requiere que el usuario esté autenticado.
- **Método HTTP:** GET
- **Respuesta:** Renderiza `project.html` con todos los datos del proyecto.

---

## Notas Adicionales

- **Manejo de la Sesión:**  
  Los datos del usuario se almacenan en la sesión para mantener el estado de autenticación entre las solicitudes.

- **Acceso a la Base de Datos:**  
  La lógica de acceso a datos se implementa a través de distintos DAOs (e.g., `UsuariosDAO`, `ProyectosDAO`, etc.) para mantener una separación de responsabilidades.

- **Seguridad:**  
  Se recomienda siempre validar y sanitizar los datos del usuario. La autenticación se realiza utilizando funciones de hash seguras para la contraseña.

---

Esta documentación te servirá para que tú y tu colaborador tengan una referencia clara de la funcionalidad de cada endpoint y cómo interactúa la aplicación con la base de datos y la sesión de usuario.
