## Guía Definitiva: API RESTful con Python, FastAPI y SQLite


[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4) | 
[Nivel 5: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel5) | 
[Nivel 6: Guía: Proyecto de Visualización y Prediccióno](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel6) |  
[Nivel 7: Uso de API, caso práctico](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel7)

---
### 1. El "Por Qué": Paquetes y Arquitectura

Antes de escribir código, es fundamental entender por qué elegimos estas herramientas. Esto se alinea con las **buenas prácticas de arquitectura de software**.

| Paquete | Propósito | ¿Por Qué lo Elegimos? (La Buena Práctica) |
| :--- | :--- | :--- |
| **FastAPI** | El Framework de la API | **Rendimiento y Modernidad.** Es un framework ASGI (asíncrono), lo que lo hace extremadamente rápido. <br><br> **Documentación Automática.** Genera documentación interactiva (Swagger/ReDoc) a partir de tu código. <br><br> **Validación de Datos.** Se integra nativamente con Pydantic, forzándote a definir tus modelos de datos y validando todas las peticiones (entrantes y salientes) automáticamente. |
| **Uvicorn** | El Servidor | **El "Motor" para ASGI.** FastAPI es un framework, pero no puede "correr" por sí solo. Necesita un servidor ASGI (Interfaz de Pasarela de Servidor Asíncrono) para manejar las peticiones HTTP. Uvicorn es el servidor estándar y recomendado para FastAPI. |
| **Pydantic** | Los Modelos de Datos (Schemas) | **Validación y Serialización.** Es el "guardia de seguridad" de tu API. Define la *forma* (schema) que tus datos JSON deben tener. Si un cliente envía un JSON con campos faltantes o tipos incorrectos, Pydantic lo rechaza automáticamente (con un error 422). También se usa para formatear la *salida* de la API. |
| **SQLAlchemy** | El ORM (Base de Datos) | **Abstracción y Seguridad.** Es el "traductor" entre tus objetos Python y la base de datos SQL. <br><br> **Portabilidad:** Escribes código Python, y SQLAlchemy lo traduce a SQL. Si hoy usas SQLite y mañana quieres cambiar a PostgreSQL, **no tienes que cambiar tu lógica de código**, solo la URL de conexión. <br><br> **Seguridad:** Previene ataques de **Inyección SQL** porque parametriza todas las consultas. |

-----

### 🏗️ 2. Estructura y Configuración del Proyecto

#### 2.1. Estructura de Archivos

Usamos una estructura que sigue el principio de **Separación de Responsabilidades (SoC)**.

```
mi_api_proyecto/
├── app/                  # Núcleo de la aplicación
│   ├── __init__.py       # (Vacío)
│   ├── main.py           # Endpoints (rutas HTTP)
│   ├── crud.py           # Lógica de negocio (C-R-U-D)
│   ├── models.py         # Modelos de la BBDD (SQLAlchemy)
│   ├── schemas.py        # Modelos de la API (Pydantic)
│   └── database.py       # Configuración de la BBDD
│
├── data/                 # Datos (ignorado por git)
│   └── tareas.db         # Nuestra base de datos demo
│
└── requirements.txt      # Dependencias
```

  * `main.py` solo habla con `crud.py` y `schemas.py`.
  * `crud.py` solo habla con `models.py` y `database.py`.
  * Ningún archivo se preocupa por "cómo" funciona el otro, solo por su "qué".

#### 2.2. Generar Estructura (Comandos)   
Puedes crear la estructura de directorios y archivos vacíos abriendo una terminal de **PowerShell** y ejecutando estos comandos uno por uno:

```powershell
# 1. Crea el directorio raíz del proyecto y entra en él
mkdir mi_api_proyecto
cd mi_api_proyecto

# 2. Crea las carpetas 'app' y 'data'
mkdir app, data

# 3. Crea los archivos Python vacíos
# 'New-Item -ItemType File' es el equivalente a 'touch'
New-Item -ItemType File app\__init__.py
New-Item -ItemType File app\main.py
New-Item -ItemType File app\crud.py
New-Item -ItemType File app\models.py
New-Item -ItemType File app\schemas.py
New-Item -ItemType File app\database.py

# 4. Crea el archivo de dependencias (vacío por ahora)
New-Item -ItemType File requirements.txt
```

**Alternativa (Si usas la terminal clásica `CMD.exe`):**

Si prefieres usar el "Símbolo del sistema" (CMD) en lugar de PowerShell, los comandos para crear archivos vacíos son ligeramente diferentes:

```cmd
:: 1. Crear directorios y entrar
mkdir mi_api_proyecto
cd mi_api_proyecto
mkdir app
mkdir data

:: 2. Crear archivos vacíos (usando 'type nul > ...')
type nul > app\__init__.py
type nul > app\main.py
type nul > app\crud.py
type nul > app\models.py
type nul > app\schemas.py
type nul > app\database.py
type nul > requirements.txt
```
-----

#### 2.3. Dependencias

**Archivo: `requirements.txt`**

```
fastapi
uvicorn[standard]
sqlalchemy
```

Instálalas con: `pip install -r requirements.txt`

-----

### 💻 3. El Código Explicado (con "Más Descripción")

#### 3.1. `app/database.py` (La Conexión)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. La URL de nuestra BBDD demo.
SQLALCHEMY_DATABASE_URL = "sqlite:///../data/tareas.db"

# 2. El "Engine" es el punto de entrada principal a la BBDD.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # Requerido solo para SQLite para permitir múltiples hilos
    connect_args={"check_same_thread": False}
)

# 3. La "Session" es la "conversación" con la BBDD.
# Es la que usamos en crud.py para hacer .add(), .commit(), etc.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. La "Base" es la clase de la que heredarán nuestros modelos
# (las tablas) en models.py.
Base = declarative_base()
```

#### 3.2. `app/models.py` (Las Tablas de la BBDD)

```python
from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

# Este es el modelo de SQLAlchemy.
# Representa la TABLA "tareas" en nuestra base de datos.
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String, nullable=True)
    completada = Column(Boolean, default=False)
```

#### 3.3. `app/schemas.py` (Los JSON de la API)

```python
from pydantic import BaseModel
from typing import Optional

# Este es el modelo de Pydantic.
# Representa el JSON que entra y sale de la API.

class TareaBase(BaseModel):
    """Schema base, comparte los campos comunes."""
    titulo: str
    descripcion: Optional[str] = None
    completada: bool = False

class TareaCreate(TareaBase):
    """Schema para la CREACIÓN (entrada). No tiene ID."""
    pass

class Tarea(TareaBase):
    """Schema para la LECTURA (salida). Sí tiene ID."""
    id: int

    class Config:
        orm_mode = True # Le dice a Pydantic que puede leer
                        # datos desde un modelo ORM (SQLAlchemy)
```

#### 3.4. `app/crud.py` (La Lógica de Negocio)

```python
from sqlalchemy.orm import Session
from . import models, schemas

# Esta es la lógica pura. No sabe nada de HTTP, solo de Python y BBDD.
# Recibe una sesión (db) y los datos (schemas).

def get_tarea(db: Session, tarea_id: int):
    """Obtiene una Tarea por su ID."""
    return db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()

def get_tareas(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista paginada de Tareas."""
    return db.query(models.Tarea).offset(skip).limit(limit).all()

def create_tarea(db: Session, tarea: schemas.TareaCreate):
    """Crea una Tarea en la BBDD."""
    # 1. Convierte el schema (Pydantic) a un modelo (SQLAlchemy)
    db_tarea = models.Tarea(**tarea.dict())
    # 2. Añade, confirma y refresca
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def update_tarea(db: Session, tarea_id: int, tarea: schemas.TareaCreate):
    """Actualiza una Tarea (método PUT)."""
    db_tarea = get_tarea(db, tarea_id)
    if db_tarea:
        db_tarea.titulo = tarea.titulo
        db_tarea.descripcion = tarea.descripcion
        db_tarea.completada = tarea.completada
        db.commit()
        db.refresh(db_tarea)
    return db_tarea

def delete_tarea(db: Session, tarea_id: int):
    """Elimina una Tarea."""
    db_tarea = get_tarea(db, tarea_id)
    if db_tarea:
        db.delete(db_tarea)
        db.commit()
    return db_tarea # Retorna el objeto borrado (o None)
```

#### 3.5. `app/main.py` (El Controlador HTTP)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

# Crea las tablas en la BBDD (si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Tareas v3")

# --- Inyección de Dependencias ---
# Esta es una buena práctica. FastAPI se encarga de:
# 1. Llamar a esta función en cada petición.
# 2. "Inyectar" el valor (db) en el endpoint (ej. `db: Session = Depends(get_db)`)
# 3. Ejecutar el 'finally' cuando la petición termina.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Cierra la sesión, liberando la conexión.

# --- Endpoints ---

@app.post("/tareas/", response_model=schemas.Tarea, status_code=status.HTTP_201_CREATED)
def crear_nueva_tarea(tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    """
    POST (Crear):
    - Body: Recibe un JSON que coincide con TareaCreate.
    - Respuesta: Devuelve un JSON que coincide con Tarea (con ID) y un 201.
    """
    return crud.create_tarea(db=db, tarea=tarea)

@app.get("/tareas/{tarea_id}", response_model=schemas.Tarea)
def leer_una_tarea(tarea_id: int, db: Session = Depends(get_db)):
    """
    GET (Leer Uno):
    - Path: Recibe el ID desde la URL.
    - Respuesta: Devuelve la Tarea o un 404.
    """
    db_tarea = crud.get_tarea(db, tarea_id=tarea_id)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

@app.put("/tareas/{tarea_id}", response_model=schemas.Tarea)
def actualizar_una_tarea(tarea_id: int, tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    """
    PUT (Actualizar/Reemplazar):
    - Path: ID del recurso a reemplazar.
    - Body: Datos completos del recurso (TareaCreate).
    - Respuesta: Devuelve la Tarea actualizada o un 404.
    """
    db_tarea = crud.update_tarea(db, tarea_id=tarea_id, tarea=tarea)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

@app.delete("/tareas/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_una_tarea(tarea_id: int, db: Session = Depends(get_db)):
    """
    DELETE (Borrar):
    - Path: ID del recurso a borrar.
    - Respuesta: Devuelve un 204 (sin contenido) o un 404.
    """
    db_tarea = crud.delete_tarea(db, tarea_id=tarea_id)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    # No se devuelve contenido, solo el código 204
    return
```

-----

### 🚦 4. Guía Detallada de Códigos de Estado HTTP

Estos códigos son la "respuesta emocional" de la API. Le dicen al cliente qué pasó.

#### 🟢 Familia 2xx: Éxito (Todo salió bien)

| Código | Nombre | Cuándo lo Usamos en Nuestra API |
| :--- | :--- | :--- |
| **`200 OK`** | OK | Respuesta estándar para peticiones exitosas que devuelven datos. <br> *(Ej: `GET /tareas/1` y `PUT /tareas/1`)* |
| **`201 Created`**| Creado | Se usa específicamente después de un `POST` exitoso que creó un nuevo recurso. <br> *(Ej: `POST /tareas/`)* |
| **`204 No Content`** | Sin Contenido | Se usa cuando la acción fue exitosa, pero no hay nada que devolver en el cuerpo. <br> *(Ej: `DELETE /tareas/1`)* |

#### 🟡 Familia 4xx: Errores del Cliente (Tú, el cliente, te equivocaste)

| Código | Nombre | Causa Común en Nuestra API |
| :--- | :--- | :--- |
| **`404 Not Found`**| No Encontrado | El cliente pidió un recurso que no existe. <br> *(Ej: `GET /tareas/999`)*. <br> **Nosotros lo lanzamos** con `raise HTTPException(status_code=404)`. |
| **`422 Unprocessable Entity`** | Entidad No Procesable | **¡El más importante de FastAPI\!** El JSON enviado estaba bien formado, pero falló la validación de Pydantic. <br> *(Ej: `POST /tareas/` sin el campo `titulo`, o `completada: "hola"`)*. <br> **FastAPI/Pydantic lo lanzan automáticamente.** |
| **`401 Unauthorized`** | No Autorizado | El cliente no ha proporcionado credenciales (API Key, Token) para un endpoint protegido. (Aún no lo implementamos). |
| **`403 Forbidden`** | Prohibido | El cliente *sí* proporcionó credenciales, pero estas no tienen permiso para realizar esa acción. (Ej. un usuario "invitado" intentando hacer `DELETE`). |
| **`400 Bad Request`** | Petición Incorrecta | Error genérico. Usualmente significa que el JSON estaba mal formado (ej. una coma faltante) y el servidor ni siquiera pudo *intentar* validarlo. |

#### 🔴 Familia 5xx: Errores del Servidor (Nosotros, la API, nos equivocamos)

| Código | Nombre | Causa Común en Nuestra API |
| :--- | :--- | :--- |
| **`500 Internal Server Error`** | Error Interno del Servidor | **El error que debes evitar.** Significa que hubo un bug en nuestro código (ej. `crud.py`), la BBDD se desconectó, o algo inesperado falló. |
| **`503 Service Unavailable`** | Servicio No Disponible | El servidor está vivo, pero temporalmente sobrecargado o en mantenimiento. |

-----

### 🚀 5. Ejecutar y Probar

1.  Desde la carpeta raíz (`mi_api_proyecto/`):
    ```bash
    uvicorn app.main:app --reload
    ```
2.  Abre tu navegador en: **`http://127.0.0.1:8000/docs`**
3.  Usa la interfaz de Swagger para probar tus endpoints `POST`, `GET`, `PUT` y `DELETE`. Intenta crear una tarea, luego obtenerla, actualizarla y finalmente borrarla.

¿Te gustaría que implementemos el método `PATCH` para actualizaciones parciales, que es un poco más complejo que `PUT`, o prefieres añadir autenticación básica?
