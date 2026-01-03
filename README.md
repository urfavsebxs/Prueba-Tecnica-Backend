# API REST de Tareas con FastAPI

Este proyecto es una API REST para gestionar tareas (crear, leer, actualizar y eliminar). Lo hice como prueba técnica. Incluye un sistema de login con usuarios y contraseñas, y todas las operaciones básicas que necesita una aplicación de tareas.

## ¿Qué es esto?

Es un backend (la parte del servidor) que permite:
- Registrar usuarios y hacer login
- Crear tareas con título y descripción
- Ver todas las tareas
- Actualizar tareas existentes
- Eliminar tareas
- Todo esto con autenticación (necesitas estar logueado)

## Tecnologías que usé

- **Python 3.11.8** - El lenguaje de programación
- **FastAPI** - Un framework (herramienta) para crear APIs en Python
- **SQLAlchemy** - Para comunicarnos con la base de datos
- **PostgreSQL** - La base de datos donde guardamos todo
- **Alembic** - Para crear y actualizar las tablas de la base de datos
- **JWT (JSON Web Tokens)** - Para manejar la autenticación (login)
- **Bcrypt** - Para guardar las contraseñas de forma segura
- **Docker** - Para instalar PostgreSQL sin complicaciones
- **pytest** - Para hacer tests y verificar que todo funciona

## Estructura del Proyecto

El proyecto está organizado en carpetas para que sea más fácil encontrar las cosas:

```
app/
├── api/v1/
│   ├── endpoints/
│   │   ├── auth.py         # Aquí está el código del login
│   │   └── tasks.py        # Aquí están todas las operaciones de tareas
│   └── api.py              
├── core/
│   ├── config.py           # Configuraciones del proyecto
│   ├── security.py         # Código para encriptar contraseñas y crear tokens
│   └── dependencies.py     # Verificación de que el usuario está logueado
├── models/
│   ├── user.py             # Define cómo se ve un usuario en la base de datos
│   └── task.py             # Define cómo se ve una tarea en la base de datos
├── schemas/
│   ├── user.py             # Validaciones para usuarios
│   ├── task.py             # Validaciones para tareas
│   └── token.py            # Validaciones para tokens
├── services/
│   ├── auth_service.py     # Funciones para manejar login y usuarios
│   └── task_service.py     # Funciones para manejar tareas
└── main.py                 # Archivo principal que inicia la aplicación
```

## Requisitos previos

Antes de empezar, necesitas tener instalado en tu computadora:

- Python 3.11.8 (puedes descargarlo de python.org)
- Docker Desktop (para la base de datos)
- Git (para clonar el proyecto)

## Cómo ejecutar el proyecto paso a paso

### Paso 1: Descargar el proyecto

Abre tu terminal (cmd, PowerShell o Git Bash) y escribe:

```bash
git clone <url-del-repositorio>
cd Prueba-Tecnica-Backend
```

Esto descarga el proyecto y entra a la carpeta.

### Paso 2: Crear un entorno virtual

Un entorno virtual es como una caja separada donde instalamos las librerías de Python solo para este proyecto.

```bash
python -m venv .venv
```

Ahora actívalo:

**En Windows:**
```bash
.venv\Scripts\activate
```

**En Linux/Mac:**
```bash
source .venv/bin/activate
```

Verás que en tu terminal aparece `(.venv)` al inicio. Eso significa que está activado.

### Paso 3: Instalar las dependencias

Las dependencias son las librerías que el proyecto necesita para funcionar.

```bash
pip install -r requirements.txt
```

Este comando lee el archivo `requirements.txt` e instala todo lo necesario.

### Paso 4: Configurar las variables de entorno

Las variables de entorno son configuraciones secretas como contraseñas y claves.

Primero, copia el archivo de ejemplo:

**En Windows:**
```bash
copy .env.example .env
```

**En Linux/Mac:**
```bash
cp .env.example .env
```

Ahora necesitas generar una clave secreta. Ejecuta esto:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Te va a dar algo como: `xK7fG2mP9nR5tY8wZ1bV4cX6hJ0kL3qA`

Abre el archivo `.env` con un editor de texto (Notepad, VSCode, etc.) y pega tu clave en `SECRET_KEY`:

```env
# Configuración de la base de datos PostgreSQL
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/taskdb

# Clave secreta para JWT (cámbiala por la que generaste)
SECRET_KEY=tu-clave-generada-aqui

# Tiempo de expiración del token en minutos
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Paso 5: Levantar PostgreSQL con Docker

PostgreSQL es nuestra base de datos. En vez de instalarlo manualmente, usamos Docker que es más fácil.

**Primero, asegúrate de que Docker Desktop está abierto.**

Luego ejecuta:

```bash
docker-compose up -d
```

Este comando:
- Lee el archivo `docker-compose.yml`
- Descarga PostgreSQL si no lo tienes
- Lo inicia en segundo plano (por eso el `-d`)

Para verificar que está funcionando:

```bash
docker ps
```

Deberías ver algo como esto:
```
CONTAINER ID   IMAGE         COMMAND                  PORTS
abc123def456   postgres:15   "docker-entrypoint.s…"   0.0.0.0:5432->5432/tcp
```

### Paso 6: Crear las tablas en la base de datos

Ahora necesitamos crear las tablas (users, tasks) en PostgreSQL. Usamos Alembic para esto:

```bash
alembic upgrade head
```

Este comando ejecuta las "migraciones" que ya están en el proyecto. Crea automáticamente:
- La tabla `users`
- La tabla `tasks`
- Un usuario admin para que puedas empezar a probar

### Paso 7: Iniciar la aplicación

¡Ya casi! Ahora inicia el servidor:

```bash
uvicorn app.main:app --reload
```

Si todo salió bien, verás algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**¡Felicidades! Tu API está corriendo.**

Puedes abrir tu navegador y visitar:
- `http://localhost:8000/docs` - Documentación interactiva (muy útil)
- `http://localhost:8000/redoc` - Otra vista de la documentación

## Usuario de prueba

Cuando ejecutaste `alembic upgrade head`, se creó automáticamente un usuario para que puedas probar la API:

**Email**: `admin@example.com`  
**Contraseña**: `admin123`

Usa estas credenciales para hacer login y probar los endpoints.

## Cómo usar la API - Ejemplos con cURL

Aquí te muestro cómo usar cada endpoint. Voy a usar cURL (un programa de línea de comandos), pero también puedes usar Postman si prefieres interfaz gráfica.

### 1. Hacer Login

Primero necesitas hacer login para obtener tu token de acceso.

**Con cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"
```

**Respuesta que recibirás:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImV4cCI6MTY0MDk5NTIwMH0.xyz...",
  "token_type": "bearer"
}
```

**Guarda ese `access_token`** porque lo necesitarás para los siguientes pasos. Ese token demuestra que estás logueado.

**Con Postman:**
1. Crea una nueva petición POST
2. URL: `http://localhost:8000/api/v1/auth/login`
3. En la pestaña "Body", selecciona "x-www-form-urlencoded"
4. Agrega:
   - Key: `username`, Value: `admin@example.com`
   - Key: `password`, Value: `admin123`
5. Click en "Send"

### 2. Crear una tarea

Ahora vamos a crear nuestra primera tarea. **Necesitas el token del paso anterior.**

**Con cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Terminar el README",
    "description": "Escribir toda la documentación del proyecto",
    "status": "pending"
  }'
```

Reemplaza `TU_TOKEN_AQUI` con el token que obtuviste en el login.

Los estados posibles para `status` son:
- `pending` (pendiente)
- `in_progress` (en progreso)
- `completed` (completada)

**Respuesta:**
```json
{
  "id": 1,
  "title": "Terminar el README",
  "description": "Escribir toda la documentación del proyecto",
  "status": "pending",
  "created_at": "2026-01-03T10:30:00"
}
```

**Con Postman:**
1. Nueva petición POST
2. URL: `http://localhost:8000/api/v1/tasks/`
3. En "Headers" agrega:
   - Key: `Authorization`, Value: `Bearer TU_TOKEN_AQUI`
4. En "Body", selecciona "raw" y "JSON"
5. Pega el JSON de la tarea
6. Click en "Send"

### 3. Ver todas las tareas

Para listar todas tus tareas:

**Con cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

Puedes agregar paginación:

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?page=1&page_size=10" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Terminar el README",
      "description": "Escribir toda la documentación del proyecto",
      "status": "pending",
      "created_at": "2026-01-03T10:30:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

**Con Postman:**
1. Nueva petición GET
2. URL: `http://localhost:8000/api/v1/tasks/`
3. Agrega el header de Authorization
4. En "Params" puedes agregar `page` y `page_size` si quieres

### 4. Ver una tarea específica

Si quieres ver solo una tarea usando su ID:

**Con cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

El `1` al final es el ID de la tarea.

### 5. Actualizar una tarea

Para cambiar el título, descripción o estado:

**Con cURL:**

```bash
curl -X PUT "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "README terminado",
    "status": "completed"
  }'
```

**No necesitas enviar todos los campos**, solo los que quieres cambiar.

**Con Postman:**
1. Nueva petición PUT
2. URL: `http://localhost:8000/api/v1/tasks/1`
3. Agrega Authorization y Content-Type en Headers
4. En Body (raw, JSON) pon los campos a actualizar

### 6. Eliminar una tarea

Para borrar una tarea:

**Con cURL:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/tasks/1" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Respuesta:** Código 204 (sin contenido) si se eliminó correctamente.

**Con Postman:**
1. Nueva petición DELETE
2. URL: `http://localhost:8000/api/v1/tasks/1`
3. Agrega el header Authorization
4. Click en "Send"

## Resumen de Endpoints

| Método | URL | Descripción | Necesita Auth |
|--------|-----|-------------|---------------|
| POST | `/api/v1/auth/login` | Hacer login y obtener token | No |
| GET | `/api/v1/tasks/` | Listar todas las tareas | Sí |
| GET | `/api/v1/tasks/{id}` | Ver una tarea específica | Sí |
| POST | `/api/v1/tasks/` | Crear una nueva tarea | Sí |
| PUT | `/api/v1/tasks/{id}` | Actualizar una tarea | Sí |
| DELETE | `/api/v1/tasks/{id}` | Eliminar una tarea | Sí |

## Cómo funciona la base de datos

El proyecto tiene dos tablas principales:

### Tabla: tasks (tareas)
- `id` - Número único que identifica cada tarea
- `title` - El título de la tarea (obligatorio)
- `description` - Descripción más larga (opcional)
- `status` - Estado: "pending", "in_progress" o "completed"
- `created_at` - Fecha y hora en que se creó

### Tabla: users (usuarios)
- `id` - Número único del usuario
- `email` - Email del usuario (debe ser único)
- `hashed_password` - La contraseña guardada de forma segura
- `is_active` - Si el usuario está activo o no
- `created_at` - Cuándo se registró el usuario

## Códigos de respuesta HTTP

Cuando haces peticiones a la API, te responde con códigos que indican qué pasó:

- `200 OK` - Todo salió bien
- `201 Created` - Se creó el recurso exitosamente
- `204 No Content` - Se eliminó correctamente (sin datos en la respuesta)
- `400 Bad Request` - Hay algo mal en tu petición
- `401 Unauthorized` - No tienes permiso (token inválido o falta login)
- `404 Not Found` - No se encontró lo que buscas
- `422 Unprocessable Entity` - Los datos que enviaste no son válidos

## Tests (Pruebas)

Incluí tests para verificar que todo funciona correctamente. Son como pruebas automáticas.

**Para ejecutar todos los tests:**

```bash
pytest
```

**Para ver un reporte de qué partes del código están cubiertas:**

```bash
pytest --cov=app --cov-report=html
```

Luego abre el archivo `htmlcov/index.html` en tu navegador para ver el reporte visual.

**Tests de partes específicas:**

```bash
# Pruebas de autenticación (login, tokens)
pytest tests/test_auth.py -v

# Pruebas de endpoints de tareas
pytest tests/test_tasks.py -v

# Pruebas de la lógica de negocio
pytest tests/test_services.py -v

# Pruebas de seguridad
pytest tests/test_security.py -v
```

**Prueba rápida de toda la API (sin pytest):**

```bash
python test_api.py
```

Este script hace un recorrido completo: login → crear tarea → listar → actualizar → eliminar

## Comandos útiles

**Ver qué está pasando en PostgreSQL:**
```bash
docker-compose logs -f db
```

**Detener PostgreSQL:**
```bash
docker-compose down
```

**Borrar todo y empezar de cero:**
```bash
docker-compose down -v        # Borra la base de datos
docker-compose up -d           # Inicia PostgreSQL de nuevo
alembic upgrade head           # Recrea las tablas
```

**Si algo sale mal:**
1. Verifica que Docker está corriendo
2. Verifica que el entorno virtual está activado (deberías ver `(.venv)`)
3. Verifica que el archivo `.env` existe y tiene la SECRET_KEY
4. Revisa los logs: `docker-compose logs db`

## Problemas comunes

**Error: "ModuleNotFoundError"**
- Solución: Asegúrate de activar el entorno virtual y ejecutar `pip install -r requirements.txt`

**Error: "Connection refused" o "database does not exist"**
- Solución: PostgreSQL no está corriendo. Ejecuta `docker-compose up -d`

**Error: "401 Unauthorized"**
- Solución: Tu token expiró (duran 30 min) o es inválido. Haz login de nuevo.

**Error: "Address already in use" en el puerto 8000**
- Solución: Ya hay algo corriendo en ese puerto. Puedes:
  - Matar ese proceso
  - O ejecutar en otro puerto: `uvicorn app.main:app --reload --port 8001`

## Notas importantes

- El usuario admin (`admin@example.com` / `admin123`) se crea automáticamente
- Los tokens de autenticación expiran en 30 minutos
- La paginación permite máximo 100 elementos por página
- Todos los endpoints de tareas necesitan que estés logueado
- Las contraseñas nunca se devuelven en las respuestas (solo el hash se guarda)

## Resumen del proyecto

Este proyecto incluye:
- ✅ Sistema de autenticación con JWT
- ✅ CRUD completo de tareas (Crear, Leer, Actualizar, Eliminar)
- ✅ Paginación en el listado
- ✅ Base de datos PostgreSQL con Docker
- ✅ Migraciones automáticas con Alembic
- ✅ Usuario inicial creado automáticamente
- ✅ Contraseñas encriptadas con bcrypt
- ✅ Validación de datos con Pydantic
- ✅ Documentación interactiva con Swagger
- ✅ Manejo correcto de errores
- ✅ Tests unitarios

## Tecnologías y por qué las usé

**FastAPI**: Es rápido y genera documentación automática. Perfecto para APIs modernas.

**PostgreSQL**: Base de datos muy confiable y robusta. La más usada en producción.

**Docker**: Evita tener que instalar PostgreSQL manualmente. Todo en contenedores.

**JWT**: Los tokens son stateless (no se guardan en el servidor), lo que hace el sistema más escalable.

**Bcrypt**: Algoritmo muy seguro para encriptar contraseñas. Es prácticamente imposible desencriptarlas.

**Alembic**: Permite hacer cambios en la base de datos de forma controlada, con historial.

**Pydantic**: Valida automáticamente que los datos que llegan sean correctos.

---

¿Quieres algo más interactivo? Revisa `http://localhost:8000/docs` o `http://127.0.0.1:8000/docs`cuando tengas el servidor corriendo para que tengas una documentación con un Swagger interactivo.