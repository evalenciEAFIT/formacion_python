## Guía Definitiva: API RESTful con Python, FastAPI y SQLite


[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4) | 
[Nivel 5: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel5) | 
[Nivel 6: Guía: Proyecto de Visualización y Prediccióno](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel6) |  
[Nivel 7: Uso de API, caso práctico](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel7)

Este documento incluye:

  * La explicación de los conceptos y paquetes.
  * La estructura de directorios y los comandos para Windows.
  * El código completo y documentado del backend (API).
  * Un script para generar datos de prueba.
  * Dos ejemplos de cómo consumir la API: una página web y un script de Python.

-----

## 🚀 Guía Completa: Creación de una API RESTful con Flask

Este documento te guiará en la creación de una API completa para gestionar "Tareas", usando Flask, Flask-RESTful y Flask-SQLAlchemy.

-----

### 1\. Conceptos Clave y Paquetes

Antes de escribir código, entiende *por qué* usamos estas herramientas.

#### 📖 Terminología de API

  * **API (Application Programming Interface):** Es un "contrato" o "menú" que un software ofrece a otro. Define las reglas sobre cómo interactuar con él (ej. qué datos enviar, qué datos esperar de vuelta).
  * **REST (REpresentational State Transfer):** Es un estilo de arquitectura para diseñar APIs. Utiliza los métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`) para interactuar con "Recursos" (en nuestro caso, las "Tareas").
  * **Endpoint:** Es una URL específica donde la API espera peticiones. En nuestro proyecto, tendremos dos:
      * `/tareas` (para la lista completa)
      * `/tareas/<id>` (para una tarea individual)
  * **JSON (JavaScript Object Notation):** Es el "idioma" estándar que usan las APIs para intercambiar datos. Es ligero y fácil de leer tanto para humanos como para máquinas.
  * **CORS (Cross-Origin Resource Sharing):** ¡Este es el "CORN" que mencionaste\! Es un mecanismo de seguridad **del navegador**.
      * **El Problema:** Por defecto, un navegador prohíbe que una página web (ej. `index.html`) solicite datos de una API que está en un "origen" (dominio/puerto) diferente. Tu API corre en `http://127.0.0.1:5000` y tu archivo se abre desde `file:///...`. Son orígenes distintos, por lo que el navegador bloquea la petición.
      * **La Solución:** Usamos el paquete `Flask-CORS`. Al añadir `CORS(app)` a nuestra API, el servidor le envía una cabecera al navegador que dice: "Está bien, confío en peticiones de cualquier origen. Deja pasar la solicitud".

#### 📦 "Por Qué" y "Para Qué" de los Paquetes

| Paquete | Para Qué (Propósito) | Por Qué lo Elegimos (Justificación) |
| :--- | :--- | :--- |
| **Flask** | El Framework de la API | Es el motor central. Recibe peticiones HTTP y envía respuestas. Es ligero, flexible y nos da control total. |
| **Flask-RESTful** | Capa de API REST | Simplifica la creación de APIs REST. Nos permite definir **Recursos** (clases) y mapea los métodos (`get`, `post`) a los verbos HTTP automáticamente. |
| **Flask-SQLAlchemy**| ORM (Base de Datos) | Es el "traductor" entre Python y la BBDD. Nos permite definir tablas como clases de Python (`class Tarea`) y evita que escribamos SQL a mano. |
| **Flask-CORS** | Habilitar CORS | Resuelve el problema de seguridad del navegador, permitiendo que nuestro `index.html` consuma la API. |
| **requests** | Cliente Python | (No es para la API, sino para el cliente). Es la librería estándar en Python para realizar peticiones HTTP (consumir APIs). |

-----

### 2\. Estructura y Configuración del Proyecto

#### 2.1. Estructura Final de Archivos

Así se verá tu proyecto. Esta estructura separa las responsabilidades (la lógica de la BBDD, la lógica de la API, etc.).

```
mi_api_flask/
├── app/                  # Núcleo de la aplicación
│   ├── __init__.py       # Fábrica de la app (con CORS)
│   ├── models.py         # Modelos de la BBDD
│   ├── resources.py      # Endpoints (Lógica de la API)
│   └── extensions.py     # Instancias (db, api)
│
├── data/                 # Carpeta para la BBDD
│   └── tareas.db         # Archivo de la BBDD SQLite
│
├── venv/                 # Tu entorno virtual
│
├── index.html            # Cliente web (Frontend)
├── client.py             # Cliente de prueba en Python
├── seed.py               # Script para generar datos
│
├── run.py                # Para iniciar el servidor
└── requirements.txt      # Dependencias
```

#### 2.2. Comandos de Generación (Windows PowerShell)

Abre PowerShell, navega a tu carpeta de proyectos y ejecuta:

```powershell
# 1. Crea y activa un entorno virtual
python -m venv venv
.\venv\Scripts\Activate

# 2. Crea la estructura de carpetas y archivos
mkdir mi_api_flask
cd mi_api_flask
mkdir app, data

# 3. Crea los archivos Python vacíos
New-Item -ItemType File run.py, requirements.txt, seed.py, client.py
New-Item -ItemType File app\__init__.py, app\models.py, app\resources.py, app\extensions.py

# 4. Crea el cliente web vacío
New-Item -ItemType File index.html
```

-----

### 3\. Dependencias

Copia esto en tu archivo `requirements.txt`.

**Archivo: `requirements.txt`**

```txt
Flask
Flask-RESTful
Flask-SQLAlchemy
Flask-CORS
requests
```

Ahora, instala todo (asegúrate de tener tu `(venv)` activado):

```powershell
(venv) > pip install -r requirements.txt
```

-----

### 4\. El Corazón de la API (El Backend)

Aquí está el código de cada archivo en tu carpeta `app/`.

#### `app/extensions.py`

*Propósito: Evitar importaciones circulares. Solo creamos las instancias aquí.*

```python
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Creamos las instancias sin vincularlas a una app todavía.
# Esto permite que otros módulos las importen de forma segura.
db = SQLAlchemy()
api = Api()
```

#### `app/models.py`

*Propósito: Definir la estructura de las tablas de la base de datos.*

```python
from .extensions import db

# db.Model es la clase base para todos los modelos de Flask-SQLAlchemy
class Tarea(db.Model):
    # Nombre de la tabla en la base de datos
    __tablename__ = "tareas"
    
    # Definición de las columnas
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False) # No puede estar vacío
    descripcion = db.Column(db.String, nullable=True) # Puede estar vacío
    completada = db.Column(db.Boolean, default=False) # Valor por defecto es Falso

    def to_dict(self):
        """
        Función helper (ayudante).
        Convierte el objeto Tarea (Python) a un diccionario.
        Esto es crucial para que Flask-RESTful pueda convertirlo a JSON.
        """
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'completada': self.completada
        }
```

#### `app/resources.py`

*Propósito: Definir la lógica de los endpoints (qué hacer en `GET`, `POST`, `PUT`, `DELETE`).*

```python
from flask_restful import Resource, reqparse
from .models import Tarea
from .extensions import db

# 1. Parser de Peticiones (reqparse)
# Es el "guardia de seguridad" que valida los datos JSON que entran.
parser = reqparse.RequestParser()
parser.add_argument('titulo', type=str, required=True, help="El título es obligatorio")
parser.add_argument('descripcion', type=str, required=False, default="")
parser.add_argument('completada', type=bool, required=False, default=False)


# 2. Recurso para un Item Específico (GET, PUT, DELETE)
# Maneja las peticiones a: /tareas/<id>
class TareaResource(Resource):
    
    def get(self, tarea_id):
        """Maneja el método GET /tareas/<id>"""
        tarea = Tarea.query.get(tarea_id)
        if not tarea:
            return {'mensaje': 'Tarea no encontrada'}, 404
        return tarea.to_dict(), 200 # 200 OK

    def put(self, tarea_id):
        """Maneja el método PUT /tareas/<id> (Actualizar)"""
        args = parser.parse_args() # Valida la entrada
        tarea = Tarea.query.get(tarea_id)
        if not tarea:
            return {'mensaje': 'Tarea no encontrada'}, 404
        
        # Actualiza los campos
        tarea.titulo = args['titulo']
        tarea.descripcion = args['descripcion']
        tarea.completada = args['completada']
        
        db.session.commit() # Guarda en BBDD
        return tarea.to_dict(), 200 # 200 OK

    def delete(self, tarea_id):
        """Maneja el método DELETE /tareas/<id> (Borrar)"""
        tarea = Tarea.query.get(tarea_id)
        if not tarea:
            return {'mensaje': 'Tarea no encontrada'}, 404
        
        db.session.delete(tarea)
        db.session.commit()
        return '', 204 # 204 No Content


# 3. Recurso para la Colección (Lista) (GET, POST)
# Maneja las peticiones a: /tareas
class TareaListResource(Resource):
    
    def get(self):
        """Maneja el método GET /tareas (Obtener todas)"""
        tareas = Tarea.query.all()
        return [t.to_dict() for t in tareas], 200

    def post(self):
        """Maneja el método POST /tareas (Crear una nueva)"""
        args = parser.parse_args() # Valida la entrada
        
        nueva_tarea = Tarea(
            titulo=args['titulo'],
            descripcion=args['descripcion'],
            completada=args['completada']
        )
        
        db.session.add(nueva_tarea)
        db.session.commit()
        
        return nueva_tarea.to_dict(), 201 # 201 Created
```

#### `app/__init__.py`

*Propósito: Usar el "Patrón de Fábrica" para crear y configurar la aplicación Flask.*

```python
import os
from flask import Flask
from flask_cors import CORS  # Importar CORS
from .extensions import db, api 
from .resources import TareaResource, TareaListResource

def create_app():
    """
    Función Fábrica (Factory Pattern)
    """
    app = Flask(__name__)
    
    # Habilitar CORS para permitir peticiones desde el frontend
    CORS(app)
    
    # --- Configuración de la Base de Datos (SQLite) ---
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'data', 'tareas.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Inicializar Extensiones ---
    db.init_app(app)
    api.init_app(app)

    # --- REGISTRO DE ENDPOINTS ---
    # Conecta las clases (Recursos) a las URLs (Endpoints)
    
    # Endpoint: /tareas
    api.add_resource(TareaListResource, '/tareas')
    
    # Endpoint: /tareas/<id>
    api.add_resource(TareaResource, '/tareas/<int:tarea_id>')

    return app
```

-----

### 5\. El Servidor

Este es el script que ejecutas para iniciar la API.

**Archivo: `run.py`**

```python
from app import create_app
from app.extensions import db

# 1. Crea la aplicación usando la fábrica
app = create_app()

# 2. Entra en el "contexto" de la aplicación
#    Esto es necesario para que Flask-SQLAlchemy sepa 
#    a qué base de datos conectarse.
with app.app_context():
    # 3. Crea todas las tablas definidas en models.py (si no existen)
    db.create_all()

# 4. Inicia el servidor de desarrollo
if __name__ == '__main__':
    # debug=True activa el reinicio automático y los mensajes de error
    app.run(debug=True)
```

-----

### 6\. Explicación: Métodos HTTP y Códigos de Estado

#### Métodos HTTP (Verbos)

| Verbo | Acción | Endpoint de Ejemplo | Método en `resources.py` |
| :--- | :--- | :--- | :--- |
| **`GET`** | **Leer** | `GET /tareas/1` | `get()` |
| **`POST`** | **Crear** | `POST /tareas` | `post()` |
| **`PUT`** | **Actualizar/Reemplazar** | `PUT /tareas/1` | `put()` |
| **`DELETE`**| **Borrar** | `DELETE /tareas/1` | `delete()` |

#### Códigos de Estado (Respuesta)

| Código | Nombre | Cuándo lo Usamos en Nuestra API |
| :--- | :--- | :--- |
| **`200 OK`** | OK | Respuesta estándar para `GET` y `PUT` exitosos. |
| **`201 Created`**| Creado | Respuesta estándar para un `POST` exitoso (creó un recurso). |
| **`204 No Content`** | Sin Contenido | Respuesta estándar para un `DELETE` exitoso (no hay nada que devolver).|
| **`400 Bad Request`**| Petición Incorrecta | `reqparse` lo devuelve automáticamente si faltan datos (ej. no envías `titulo`).|
| **`404 Not Found`** | No Encontrado | Lo devolvemos si se pide un ID que no existe (ej. `GET /tareas/999`).|

-----

### 7\. Generación de Datos de Prueba

Crea este archivo para llenar tu BBDD con datos de ejemplo.

**Archivo: `seed.py`**

```python
from app import create_app
from app.extensions import db
from app.models import Tarea

# 1. Crea una instancia de la app para tener el contexto
app = create_app()

# 2. 'app_context()' conecta el script a la BBDD
with app.app_context():
    
    # 3. Borra todos los datos antiguos
    print("Eliminando datos antiguos...")
    db.session.query(Tarea).delete()
    
    # 4. Crea los nuevos objetos Tarea
    print("Creando nuevos datos de ejemplo...")
    t1 = Tarea(titulo="Comprar leche", descripcion="Recordar que sea deslactosada")
    t2 = Tarea(titulo="Estudiar API con Flask", completada=True)
    t3 = Tarea(titulo="Llamar al cliente")
    
    # 5. Añade los objetos a la sesión y guarda
    db.session.add_all([t1, t2, t3])
    db.session.commit()
    
    print("¡Datos de ejemplo creados exitosamente!")
```

**Para ejecutarlo** (con `(venv)` activado):

```powershell
(venv) > python seed.py
```

-----

### 8\. Los Clientes (Consumiendo la API)

Aquí tienes dos formas de usar tu API.

#### 🌐 8.1. Ejemplo 1: Cliente Web (HTML + JavaScript)

**Archivo: `index.html`**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Cliente de API de Tareas</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #f4f7f6; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        header { background: #007bff; color: white; padding: 20px; border-radius: 8px 8px 0 0; }
        h1 { margin: 0; }
        main { padding: 20px; }
        ul#lista-tareas { list-style: none; padding: 0; }
        ul#lista-tareas li { display: flex; align-items: center; justify-content: space-between; padding: 15px; border-bottom: 1px solid #eee; }
        .tarea-info.completada { text-decoration: line-through; color: #888; }
        .tarea-acciones button { margin-left: 8px; border: none; padding: 8px 12px; border-radius: 5px; cursor: pointer; }
        .btn-completar { background-color: #28a745; color: white; }
        .btn-borrar { background-color: #dc3545; color: white; }
        form#form-nueva-tarea { display: flex; gap: 10px; margin-top: 20px; }
        form#form-nueva-tarea input { flex-grow: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        form#form-nueva-tarea button { padding: 10px 15px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <header><h1>Gestor de Tareas (API con Flask)</h1></header>
        <main>
            <ul id="lista-tareas"></ul>
            <hr>
            <h3>Nueva Tarea</h3>
            <form id="form-nueva-tarea">
                <input type="text" id="input-titulo" placeholder="Título..." required>
                <input type="text" id="input-descripcion" placeholder="Descripción...">
                <button type="submit">Crear</button>
            </form>
        </main>
    </div>

    <script>
        // URL de la API
        const API_URL = 'http://127.0.0.1:5000/tareas';
        
        // Elementos del DOM
        const listaTareas = document.getElementById('lista-tareas');
        const formNuevaTarea = document.getElementById('form-nueva-tarea');
        const inputTitulo = document.getElementById('input-titulo');
        const inputDescripcion = document.getElementById('input-descripcion');

        // 1. OBTENER Y MOSTRAR TAREAS (GET)
        async function cargarTareas() {
            const response = await fetch(API_URL);
            const tareas = await response.json();
            listaTareas.innerHTML = ''; // Limpia la lista
            tareas.forEach(tarea => {
                const li = document.createElement('li');
                li.dataset.id = tarea.id;
                li.dataset.titulo = tarea.titulo;
                li.dataset.descripcion = tarea.descripcion || '';
                li.dataset.completada = tarea.completada;
                li.innerHTML = `
                    <div class="tarea-info ${tarea.completada ? 'completada' : ''}">
                        <strong>${tarea.titulo}</strong>
                    </div>
                    <div class="tarea-acciones">
                        <button class="btn-completar" onclick="toggleCompletar(${tarea.id})">${tarea.completada ? 'Deshacer' : 'Completar'}</button>
                        <button class="btn-borrar" onclick="borrarTarea(${tarea.id})">Borrar</button>
                    </div>
                `;
                listaTareas.appendChild(li);
            });
        }

        // 2. CREAR NUEVA TAREA (POST)
        formNuevaTarea.addEventListener('submit', async (event) => {
            event.preventDefault();
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    titulo: inputTitulo.value,
                    descripcion: inputDescripcion.value,
                    completada: false
                }),
            });
            if (response.status === 201) {
                inputTitulo.value = '';
                inputDescripcion.value = '';
                cargarTareas();
            }
        });

        // 3. BORRAR TAREA (DELETE)
        async function borrarTarea(id) {
            if (!confirm('¿Seguro?')) return;
            const response = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
            if (response.status === 204) cargarTareas();
        }

        // 4. ACTUALIZAR TAREA (PUT)
        async function toggleCompletar(id) {
            const tareaLi = document.querySelector(`li[data-id="${id}"]`);
            const nuevaCompletada = !(tareaLi.dataset.completada === 'true'); 
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    titulo: tareaLi.dataset.titulo,
                    descripcion: tareaLi.dataset.descripcion,
                    completada: nuevaCompletada
                })
            });
            if (response.status === 200) cargarTareas();
        }
        
        // Carga inicial
        document.addEventListener('DOMContentLoaded', cargarTareas);
    </script>
</body>
</html>
```

#### 🐍 8.2. Ejemplo 2: Cliente Python (`requests`)

**Archivo: `client.py`**

```python
import requests

# URL base de la API
BASE_URL = "http://127.0.0.1:5000/tareas"

def print_tarea(tarea):
    """Función helper para imprimir una tarea formateada."""
    estado = "Completada" if tarea.get('completada') else "Pendiente"
    print(f"  ID: {tarea.get('id')} | Título: {tarea.get('titulo')} ({estado})")

def main_loop():
    print("--- Cliente de API en Python ---")
    
    # 1. CREAR una nueva tarea (POST)
    print("\n1. Creando nueva tarea (POST)...")
    nueva_tarea_data = {"titulo": "Hacer demo en Python"}
    try:
        response = requests.post(BASE_URL, json=nueva_tarea_data)
        if response.status_code == 201:
            tarea_creada = response.json()
            print("¡Tarea creada!")
            print_tarea(tarea_creada)
            tarea_id = tarea_creada.get('id')
        else:
            print(f"Error al crear: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] No se pudo conectar a la API.")
        print("Asegúrate de que el servidor (python run.py) esté corriendo.")
        return
        
    # 2. OBTENER todas las tareas (GET)
    print("\n2. Obteniendo lista de tareas (GET)...")
    response = requests.get(BASE_URL)
    tareas = response.json()
    print(f"Total de tareas: {len(tareas)}")
    for tarea in tareas:
        print_tarea(tarea)
        
    # 3. ACTUALIZAR la tarea (PUT)
    print(f"\n3. Actualizando tarea ID {tarea_id} (PUT)...")
    update_data = {"titulo": "Hacer demo en Python", "completada": True}
    response = requests.put(f"{BASE_URL}/{tarea_id}", json=update_data)
    if response.status_code == 200:
        print("¡Tarea actualizada!")
        print_tarea(response.json())

    # 4. BORRAR la tarea (DELETE)
    print(f"\n4. Borrando tarea ID {tarea_id} (DELETE)...")
    response = requests.delete(f"{BASE_URL}/{tarea_id}")
    if response.status_code == 204:
        print("¡Tarea borrada!")
        
    # 5. VERIFICAR
    print("\n5. Verificando la lista final...")
    response = requests.get(BASE_URL)
    tareas = response.json()
    print(f"Total de tareas ahora: {len(tareas)}")
    for tarea in tareas:
        print_tarea(tarea)

if __name__ == "__main__":
    main_loop()
```

-----

### 9\. Resumen de Ejecución

1.  **Terminal 1 (Servidor API):**

      * Activa tu entorno: `.\venv\Scripts\Activate`
      * *(Opcional)* Genera los datos: `python seed.py`
      * **Inicia la API:** `python run.py`
      * *Deja esta terminal abierta. Verás los logs (GET, POST, etc.) aquí.*

2.  **Terminal 2 (Cliente Python):**

      * Abre una **nueva terminal**.
      * Activa el mismo entorno: `.\venv\Scripts\Activate`
      * **Ejecuta el cliente:** `python client.py`
      * *Verás la salida del script creando, leyendo, actualizando y borrando tareas.*

3.  **Navegador Web (Cliente Web):**

      * Ve a la carpeta `mi_api_flask` en tu explorador de archivos.
      * Haz doble clic en `index.html`.
      * *La página se abrirá y podrás interactuar con la API (crear, borrar, etc.) desde tu navegador.*
