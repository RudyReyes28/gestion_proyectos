# API - Sistema de Gestión de Proyectos

Esta API corresponde a un sistema web de gestión de proyectos colaborativos, similar a GitHub, desarrollada con Flask.

## Endpoints

---

### `/`
- **Método:** `GET`
- **Descripción:** Muestra la página de inicio de sesión (`login.html`).

---

### `/home`
- **Método:** `GET`
- **Descripción:** Página de inicio para usuarios autenticados.
  - Si el usuario tiene sesión iniciada, se cargan los proyectos que le pertenecen.
  - Si no hay sesión activa, redirige a la página de login (`/`).

---

### `/login`
- **Métodos:** `GET`, `POST`
- **GET:** Muestra el formulario de inicio de sesión (`login.html`).
- **POST:** Procesa el inicio de sesión:
  - Recibe `email` y `password` del formulario.
  - Verifica las credenciales con `UsuariosDAO`.
  - Si son válidas, guarda los datos en la sesión y redirige a `/home`.
  - Si no son válidas, vuelve a `login.html` con un mensaje de error.

---

### `/logout`
- **Método:** `GET`
- **Descripción:** Cierra la sesión actual del usuario y redirige al inicio (`/`).

---

### `/register`
- **Métodos:** `GET`, `POST`
- **GET:** Muestra el formulario de registro (`register.html`).
- **POST:** Procesa el formulario de registro:
  - Recibe `nombre_usuario`, `email`, `contraseña` y `biografia`.
  - Intenta registrar al usuario con `UsuariosDAO`.
  - Si tiene éxito, redirige al login (`/`).
  - Si falla, muestra un error en el mismo formulario.

---

### `/home/add_project`
- **Métodos:** `GET`, `POST`
- **GET:** Muestra el formulario para crear un nuevo proyecto (`add_project.html`).
- **POST:** Procesa la creación del proyecto:
  - Recibe `nombre`, `descripcion`, `visibilidad`.
  - Obtiene el `user_id` de la sesión como `id_usuario`.
  - Intenta guardar el proyecto con `ProyectosDAO`.
  - Si tiene éxito, redirige a `/home`.
  - Si falla, muestra un error en el formulario.

---

### `/home/edit_project/<int:project_id>`
- **Métodos:** `GET`, `POST`
- **GET:** Muestra el formulario de edición para un proyecto existente.
  - Recupera los datos del proyecto por `id` y los muestra en `edit_project.html`.
- **POST:** Procesa la actualización del proyecto:
  - Recibe `nombre`, `descripcion`, `visibilidad`.
  - Actualiza el proyecto en la base de datos.
  - Si tiene éxito, redirige a `/home`.
  - Si falla, muestra un mensaje de error.

---

### `/home/delete_project/<int:project_id>`
- **Método:** `GET`
- **Descripción:** Elimina el proyecto con el ID dado.
  - Si se elimina correctamente, redirige a `/home`.
  - Si ocurre un error, muestra la página principal con un mensaje de error.

---

### `/home/view_project/<int:project_id>`
- **Método:** `GET`
- **Descripción:** Muestra los detalles del proyecto:
  - Información del proyecto.
  - Comentarios.
  - Archivos.
  - Colaboradores.
- Solo accesible si hay una sesión activa. Si no, redirige a `/`.

---

## Notas
- La mayoría de los endpoints requieren sesión activa.
- Las respuestas son vistas HTML renderizadas con Jinja2.
- La autenticación de usuarios y manejo de proyectos está encapsulado en DAOs.
