## Guía Definitiva: API RESTful con Python, FastAPI y SQLite


[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4) | 
[Nivel 5: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel5) | 
[Nivel 6: Guía: Proyecto de Visualización y Prediccióno](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel6) |  
[Nivel 7: Uso de API, caso práctico](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel7)

-----

# **Guía Completa: API RESTful en Python con Flask, SQLite, Exportación a Excel/CSV y CRUD Total**  
### **Con Comentarios Detallados en Código + Explicación Profunda de "Para Qué" y "Por Qué"**

---

## **Índice**
1. [Introducción a API RESTful](#1-introducción-a-api-restful)  
2. [Tecnologías Utilizadas](#2-tecnologías-utilizadas)  
3. [Estructura del Proyecto](#3-estructura-del-proyecto)  
4. [Paso 1: Configuración del Entorno](#4-paso-1-configuración-del-entorno)  
5. [Paso 2: Base de Datos con SQLite](#5-paso-2-base-de-datos-con-sqlite)  
6. [Paso 3: Modelo de Datos](#6-paso-3-modelo-de-datos)  
7. [Paso 4: API RESTful con Flask (CRUD Completo)](#7-paso-4-api-restful-con-flask-crud-completo)  
8. [Paso 5: Exportar a Excel y CSV](#8-paso-5-exportar-a-excel-y-csv)  
9. [Paso 6: Cliente Web (HTML + JS)](#9-paso-6-cliente-web-html--js)  
10. [Paso 7: Cliente Python](#10-paso-7-cliente-python)  
11. [Paso 8: REST Client y Thunder Client](#11-paso-8-rest-client-y-thunder-client)  
12. [Ejecución Completa](#12-ejecución-completa)  
13. [Conclusión](#13-conclusión)

---

<a name="1-introducción-a-api-restful"></a>
## **1. Introducción a API RESTful**

> **¿Qué es?**  
Una **API RESTful** es un servicio web que permite a aplicaciones comunicarse usando los verbos HTTP (GET, POST, PUT, DELETE) sobre recursos identificados por URLs.

> **¿Por qué usarla?**  
- **Escalabilidad**: Separación clara entre cliente y servidor.  
- **Simplicidad**: Usa estándares web (HTTP, JSON).  
- **Interoperabilidad**: Cualquier lenguaje puede consumirla.  
- **Sin estado (Stateless)**: Cada petición es independiente → más fácil de escalar.

---

<a name="2-tecnologías-utilizadas"></a>
## **2. Tecnologías Utilizadas**

| Tecnología | **Para Qué** | **Por Qué** |
|----------|--------------|-------------|
| **Flask** | Framework web ligero | Ideal para APIs pequeñas, rápido de aprender |
| **Flask-SQLAlchemy** | ORM para SQLite | Simplifica consultas SQL |
| **SQLite** | Base de datos embebida | No requiere servidor externo, ideal para prototipos |
| **pandas + openpyxl** | Generar Excel | Formato ampliamente usado en empresas |
| **csv** | Generar CSV | Formato universal, fácil de importar |
| **HTML + JS (Fetch)** | Cliente web | Pruebas rápidas sin backend adicional |
| **requests** | Cliente HTTP en Python | Consumo de API desde scripts |
| **REST Client / Thunder Client** | Pruebas de endpoints | Integradas en VS Code, rápidas y documentables |

---

<a name="3-estructura-del-proyecto"></a>
## **3. Estructura del Proyecto**

```
api_rest_flask/
│
├── app.py                  # API principal + rutas CRUD
├── database.py             # Configuración de SQLAlchemy
├── models.py               # Modelo User (tabla)
├── export.py               # Lógica de exportación
├── static/
│   └── index.html          # Cliente web (CRUD visual)
├── tests/
│   └── api_tests.http      # Pruebas con REST Client
├── client.py               # Cliente Python (requests)
├── database.db             # (creado al ejecutar)
└── requirements.txt
```

---

<a name="4-paso-1-configuración-del-entorno"></a>
## **4. Paso 1: Configuración del Entorno**

```bash
mkdir api_rest_flask && cd api_rest_flask
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows
```

### **¿Por qué entorno virtual?**
- Aísla dependencias del proyecto.
- Evita conflictos entre versiones.
- Mejora reproducibilidad.

```bash
pip install flask flask-sqlalchemy pandas openpyxl requests
```

---

<a name="5-paso-2-base-de-datos-con-sqlite"></a>
## **5. Paso 2: Base de Datos con SQLite**

### `database.py` — **Configuración global de la BD**

```python
# database.py
from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy
# Esto permite usarla en múltiples archivos
db = SQLAlchemy()
```

> **¿Por qué no `sqlite:///:memory:`?**  
> → `:memory:` es volátil. Usamos archivo para persistencia.

---

<a name="6-paso-3-modelo-de-datos"></a>
## **6. Paso 3: Modelo de Datos**

### `models.py` — **Definición de la tabla `User`**

```python
# models.py
from database import db

class User(db.Model):
    # ID único autoincremental
    id = db.Column(db.Integer, primary_key=True)
    
    # Nombre obligatorio, max 100 caracteres
    name = db.Column(db.String(100), nullable=False)
    
    # Email único y obligatorio
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Edad opcional
    age = db.Column(db.Integer)

    # Método para convertir objeto a diccionario (JSON)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age
        }
```

> **¿Por qué `to_dict()`?**  
> → Flask necesita JSON. Este método serializa el objeto fácilmente.

---

<a name="7-paso-4-api-restful-con-flask-crud-completo"></a>
## **7. Paso 4: API RESTful con Flask (CRUD Completo)**

### `app.py` — **Corazón del proyecto**

```python
# app.py
from flask import Flask, request, jsonify, send_file
from database import db
from models import User
from export import export_to_excel, export_to_csv
import os

# Crear aplicación Flask
app = Flask(__name__, static_folder='static')

# Configurar SQLite como archivo local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita overhead

# Vincular SQLAlchemy con Flask
db.init_app(app)

# === CREAR TABLAS ANTES DE LA PRIMERA PETICIÓN ===
@app.before_first_request
def create_tables():
    db.create_all()  # Crea tablas si no existen

# ==================== CRUD API ====================

# CREATE - POST /api/users
@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Crea un nuevo usuario.
    Requiere: name y email en JSON.
    Valida duplicados por email.
    """
    data = request.get_json()
    
    # Validación básica
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    
    # Evitar emails duplicados
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Crear instancia del modelo
    user = User(
        name=data['name'],
        email=data['email'],
        age=data.get('age')  # opcional
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201  # 201 = Created

# READ - GET /api/users
@app.route('/api/users', methods=['GET'])
def get_users():
    """Devuelve todos los usuarios en formato JSON"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# READ - GET /api/users/<id>
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    """Obtiene un usuario por ID. 404 si no existe"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

# UPDATE - PUT /api/users/<id>
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    """Actualiza campos permitidos. No requiere todos los datos"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Actualizar solo lo que venga
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    
    db.session.commit()
    return jsonify(user.to_dict())

# DELETE - DELETE /api/users/<id>
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Elimina un usuario por ID"""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# ==================== EXPORTACIONES ====================

@app.route('/export/excel')
def export_excel():
    """Descarga todos los usuarios en Excel"""
    return export_to_excel()

@app.route('/export/csv')
def export_csv():
    """Descarga todos los usuarios en CSV"""
    return export_to_csv()

# ==================== CLIENTE WEB ====================

@app.route('/')
def index():
    """Sirve la página web estática"""
    return app.send_static_file('index.html')

# === INICIAR SERVIDOR ===
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Asegura tablas al iniciar
    app.run(debug=True, port=5000)
```

> **¿Por qué `debug=True`?**  
> → Recarga automática y logs detallados (solo en desarrollo).

---

<a name="8-paso-5-exportar-a-excel-y-csv"></a>
## **8. Paso 5: Exportar a Excel y CSV**

### `export.py` — **Generación de archivos**

```python
# export.py
import pandas as pd
from models import User
from flask import send_file
import os

def get_all_users():
    """Obtiene todos los usuarios como lista de diccionarios"""
    users = User.query.all()
    return [user.to_dict() for user in users]

def export_to_excel():
    """
    Genera un archivo Excel con todos los usuarios.
    Usa pandas + openpyxl.
    """
    users = get_all_users()
    df = pd.DataFrame(users)
    
    filename = 'users_export.xlsx'
    df.to_excel(filename, index=False, engine='openpyxl')
    
    return send_file(
        filename,
        as_attachment=True,
        download_name='usuarios.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def export_to_csv():
    """
    Genera un archivo CSV.
    Formato universal.
    """
    users = get_all_users()
    df = pd.DataFrame(users)
    
    filename = 'users_export.csv'
    df.to_csv(filename, index=False, encoding='utf-8')
    
    return send_file(
        filename,
        as_attachment=True,
        download_name='usuarios.csv',
        mimetype='text/csv'
    )
```

> **¿Por qué `encoding='utf-8'`?**  
> → Soporta caracteres especiales (ñ, acentos).

---

<a name="9-paso-6-cliente-web-html--js"></a>
## **9. Paso 6: Cliente Web (HTML + JS)**

### `static/index.html` — **Interfaz visual**

```html
<!-- static/index.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRUD API REST - Usuarios</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f9f9f9; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
        th { background-color: #007bff; color: white; }
        .form-group { margin: 15px 0; }
        input { padding: 8px; margin: 5px; width: 180px; }
        button { 
            padding: 8px 15px; margin: 5px; 
            background: #007bff; color: white; border: none; cursor: pointer;
        }
        button:hover { background: #0056b3; }
        .actions button { background: #28a745; }
        .actions button:last-child { background: #dc3545; }
    </style>
</head>
<body>
    <h1>Gestión de Usuarios (API REST)</h1>

    <!-- Formulario para crear -->
    <h2>Crear Usuario</h2>
    <div class="form-group">
        <input type="text" id="name" placeholder="Nombre" />
        <input type="email" id="email" placeholder="Email" />
        <input type="number" id="age" placeholder="Edad" />
        <button onclick="createUser()">Crear</button>
    </div>

    <!-- Controles y tabla -->
    <h2>Lista de Usuarios</h2>
    <button onclick="loadUsers()">Actualizar</button>
    <button onclick="exportExcel()">Exportar Excel</button>
    <button onclick="exportCSV()">Exportar CSV</button>

    <table id="usersTable">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Email</th>
                <th>Edad</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        const API = '/api/users';

        // Cargar usuarios
        async function loadUsers() {
            const res = await fetch(API);
            const users = await res.json();
            const tbody = document.querySelector('#usersTable tbody');
            tbody.innerHTML = '';
            users.forEach(user => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${user.id}</td>
                    <td><input type="text" value="${user.name}" id="name-${user.id}"></td>
                    <td><input type="email" value="${user.email}" id="email-${user.id}"></td>
                    <td><input type="number" value="${user.age || ''}" id="age-${user.id}"></td>
                    <td class="actions">
                        <button onclick="updateUser(${user.id})">Actualizar</button>
                        <button onclick="deleteUser(${user.id})">Eliminar</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Crear
        async function createUser() {
            const user = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                age: parseInt(document.getElementById('age').value) || null
            };
            await fetch(API, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(user)
            });
            loadUsers();
            document.getElementById('name').value = '';
            document.getElementById('email').value = '';
            document.getElementById('age').value = '';
        }

        // Actualizar
        async function updateUser(id) {
            const user = {
                name: document.getElementById(`name-${id}`).value,
                email: document.getElementById(`email-${id}`).value,
                age: parseInt(document.getElementById(`age-${id}`).value) || null
            };
            await fetch(`${API}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(user)
            });
            loadUsers();
        }

        // Eliminar
        async function deleteUser(id) {
            if (confirm('¿Eliminar usuario?')) {
                await fetch(`${API}/${id}`, { method: 'DELETE' });
                loadUsers();
            }
        }

        // Exportar
        function exportExcel() { window.location.href = '/export/excel'; }
        function exportCSV() { window.location.href = '/export/csv'; }

        // Cargar al iniciar
        loadUsers();
    </script>
</body>
</html>
```

> **¿Por qué `static_folder='static'`?**  
> → Flask sirve archivos estáticos desde esta carpeta.

---

<a name="10-paso-7-cliente-python"></a>
## **10. Paso 7: Cliente Python**

### `client.py` — **Consumo desde scripts**

```python
# client.py
import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api/users'

def create_user(name, email, age=None):
    """Crea usuario y muestra respuesta"""
    data = {'name': name, 'email': email}
    if age: data['age'] = age
    r = requests.post(BASE_URL, json=data)
    print("CREATE:", r.status_code, r.json())

def get_users():
    """Lista todos los usuarios"""
    r = requests.get(BASE_URL)
    print("GET ALL:", json.dumps(r.json(), indent=2, ensure_ascii=False))

def get_user(id):
    r = requests.get(f'{BASE_URL}/{id}')
    print("GET ONE:", r.json())

def update_user(id, name=None, email=None, age=None):
    data = {}
    if name: data['name'] = name
    if email: data['email'] = email
    if age is not None: data['age'] = age
    r = requests.put(f'{BASE_URL}/{id}', json=data)
    print("UPDATE:", r.status_code, r.json())

def delete_user(id):
    r = requests.delete(f'{BASE_URL}/{id}')
    print("DELETE:", r.status_code, r.json())

# === DEMO AUTOMÁTICA ===
if __name__ == '__main__':
    print("=== CREANDO USUARIOS ===")
    create_user("Ana", "ana@mail.com", 25)
    create_user("Luis", "luis@mail.com", 30)

    print("\n=== LISTA DE USUARIOS ===")
    get_users()

    print("\n=== ACTUALIZANDO USUARIO 1 ===")
    update_user(1, age=26)

    print("\n=== ELIMINANDO USUARIO 2 ===")
    delete_user(2)

    print("\n=== LISTA FINAL ===")
    get_users()
```

> **¿Para qué?**  
> → Automatización, pruebas, integración con otros sistemas.

---

<a name="11-paso-8-rest-client-y-thunder-client"></a>
## **11. Paso 8: REST Client y Thunder Client**

### `tests/api_tests.http`

```http
### CREATE
POST http://127.0.0.1:5000/api/users
Content-Type: application/json

{
  "name": "Pedro",
  "email": "pedro@test.com",
  "age": 35
}

### READ ALL
GET http://127.0.0.1:5000/api/users

### READ ONE
GET http://127.0.0.1:5000/api/users/1

### UPDATE
PUT http://127.0.0.1:5000/api/users/1
Content-Type: application/json

{
  "age": 36
}

### DELETE
DELETE http://127.0.0.1:5000/api/users/1

### EXPORT EXCEL
GET http://127.0.0.1:5000/export/excel

### EXPORT CSV
GET http://127.0.0.1:5000/export/csv
```

> **¿Por qué `.http`?**  
> → Archivo versionable, ejecutable, documentable.

---

<a name="12-ejecución-completa"></a>
## **12. Ejecución Completa**

```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Iniciar API
python app.py

# 3. Abrir en navegador
http://127.0.0.1:5000

# 4. Probar cliente Python
python client.py

# 5. Usar REST Client / Thunder Client en VS Code
```

---

<a name="13-conclusión"></a>
## **13. Conclusión**

| Característica | Implementada | Beneficio |
|---------------|--------------|---------|
| CRUD Completo | Yes | Gestión total |
| SQLite | Yes | Persistencia sin servidor |
| Exportar Excel/CSV | Yes | Informes empresariales |
| Cliente Web | Yes | Pruebas visuales |
| Cliente Python | Yes | Automatización |
| REST Client | Yes | Pruebas documentadas |
| Thunder Client | Yes | GUI rápida |

---

**¡Listo para producción básica!**  
Puedes escalar con:
- JWT para autenticación
- Docker
- PostgreSQL
- Paginación
- Validación con Pydantic

**¿Quieres la versión Dockerizada o con login?** ¡Dímelo!
