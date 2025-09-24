# Invera ToDo-List Challenge: API RESTful con Django y JS

Este proyecto cumple con los requisitos del ToDo-List Challenge de Invera, implementando una aplicación web moderna que utiliza una **API RESTful robusta** (construida con **Django REST Framework**) consumida por una interfaz de usuario minimalista y dinámica (**Single Page Application simplificada** con HTML/CSS/JavaScript).

---

## Características y Valor Añadido

Características y Valor Añadido

    Arquitectura: Separación total de Backend y Frontend. La interfaz es una SPA simple que consume la API vía AJAX/Fetch, lo que demuestra una arquitectura moderna y permite escalabilidad futura (ej., con React/Vue).

    API RESTful: Implementada con Django REST Framework (DRF). Utiliza métodos HTTP estándar: GET (Listar), POST (Crear), PATCH (Actualizar/Marcar), DELETE (Eliminar).

    Seguridad: Uso de SessionAuthentication y CSRF Protection (vía X-CSRFToken en peticiones AJAX) para garantizar un flujo de sesión seguro.

    Filtrado Avanzado: Implementado con la librería DjangoFilterBackend para búsquedas complejas: búsqueda por contenido (title y description) y filtrado por rango de fecha (created_at_after, created_at_before).

    Operaciones: Crear, listar, eliminar y marcar/desmarcar tareas como completadas mediante peticiones asíncronas, ofreciendo una experiencia de usuario fluida sin recargar la página.

    Manejo de Logs: Configuración de LOGGING profesional para registrar eventos importantes (creación, eliminación y cambio de estado de tareas) en consola y en archivo (`logs/django_errors.log`), mejorando la mantenibilidad del sistema.

    Tests: Cobertura con Tests Unitarios (modelo) y Tests de Integración (API REST) para asegurar la funcionalidad y el alcance de usuario.

---

### Acceso a la Aplicación

| URL                             | Función                       |
| :------------------------------ | :---------------------------- |
| `http://localhost:8000/`        | Página de inicio.             |
| `http://localhost:8000/signup/` | Registro de nuevos usuarios.  |
| `http://localhost:8000/admin/`  | Panel de Login y Admin.       |
| `http://localhost:8000/tasks/`  | **Interfaz de Tareas (SPA).** |

---

## Pruebas de la API RESTful (Postman/cURL)

La API se expone bajo el prefijo `/api/`. **Todas las peticiones requieren autenticación por sesión** (debe estar logueado previamente en el navegador o enviar las cookies de sesión).

### Endpoints Principales

1.  **Listar Tareas (GET)**

    ```
    [GET] http://localhost:8000/api/tasks/
    ```

2.  **Crear Tarea (POST)**

    ```
    [POST] http://localhost:8000/api/tasks/

    --- BODY (JSON) ---
    {
      "title": "",
      "description": ""
    }
    ```

3.  **Eliminar Tarea (DELETE)**
    _(Reemplaza `<pk>` con el ID de la tarea, ej: `/api/tasks/5/`)_

    ```
    [DELETE] http://localhost:8000/api/tasks/<pk>/
    ```

4.  **Marcar Tarea como Completada (PATCH)**

    ```
    [PATCH] http://localhost:8000/api/tasks/<pk>/

    --- BODY (JSON) ---
    {
      "is_completed": true
    }
    ```

### Filtrado

5.  **Buscar por Contenido (GET)**
    _(Busca en `title` y `description`)_

    ```
    [GET] http://localhost:8000/api/tasks/?search=documentacion
    ```

6.  **Filtrar por Rango de Fecha (GET)**
    _(Tareas creadas entre las dos fechas, usa `_after` y `_before`)_
    ```
    [GET] http://localhost:8000/api/tasks/?created_at_after=2025-01-01&created_at_before=2025-03-30
    ```

---

## Configuración de Autenticación en Postman

Para probar `GET`, `POST`, `PATCH`, o `DELETE` desde Postman, debe incluir las cookies de sesión y el token CSRF para evitar errores `403 Forbidden`.

| Cabecera (Key) | Valor (Value)                                      |
| :------------- | :------------------------------------------------- |
| `Cookie`       | `csrftoken=<VALOR_CSRF>; sessionid=<VALOR_SESION>` |
| `X-CSRFToken`  | `<VALOR_CSRF>`                                     |
| `Content-Type` | `application/json`                                 |
