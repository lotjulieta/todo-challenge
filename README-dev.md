## Requisitos e Instalación

### Requisitos Previos

Necesitarás tener instalado **Docker & Docker Compose** (método recomendado) o **Python 3.10+**.

### Instalación y Ejecución (Método Docker)

1.  **Clonar el repositorio:**

    ```bash
    git clone [URL_REPO]
    cd [nombre_del_proyecto]
    ```

2.  **Configurar Variables de Entorno (.env):**

    ```bash
    cp .env-sample .env
    # Abre .env y modifica POSTGRES_DB, POSTGRES_USER, y POSTGRES_PASSWORD
    ```

3.  **Construir y levantar contenedores:**

    ```bash
    docker-compose up --build
    ```

4.  **Ejecutar Migraciones:**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Recolectar Archivos Estáticos:**

    ```bash
    docker-compose exec web python manage.py collectstatic --noinput
    ```

6.  **Crear Superusuario (Opcional):**

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

7.  **Ejecuta el siguiente comando para correr todos los tests en la aplicación tasks:**
    ```bash
    docker-compose exec web python manage.py test tasks
    ```
