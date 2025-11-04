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

# **GUÍA COMPLETA Y PROFESIONAL: API RESTful en Python con Flask, SQLite, CRUD, Exportación y Pruebas**  
### **Flask 2.3+ Compatible – Con Comentarios, Explicaciones Detalladas y Mejores Prácticas**

---

## **Índice**
1. [¿Qué es una API RESTful? (Explicación Profunda)](#qué-es-una-api-restful-explicación-profunda)  
2. [Arquitectura REST: Principios y Reglas](#arquitectura-rest-principios-y-reglas)  
3. [HTTP: Métodos, Códigos y Headers](#http-métodos-códigos-y-headers)  
4. [Estructura del Proyecto](#estructura-del-proyecto)  
5. [Tecnologías y Justificación](#tecnologías-y-justificación)  
6. [Paso 1: Configuración del Entorno](#paso-1-configuración-del-entorno)  
7. [Paso 2: Base de Datos SQLite](#paso-2-base-de-datos-sqlite)  
8. [Paso 3: Modelo de Datos](#paso-3-modelo-de-datos)  
9. [Paso 4: API RESTful con Flask (CRUD Completo)](#paso-4-api-restful-con-flask-crud-completo)  
10. [Paso 5: Exportación a Excel y CSV](#paso-5-exportación-a-excel-y-csv)  
11. [Paso 6: Cliente Web Interactivo](#paso-6-cliente-web-interactivo)  
12. [Paso 7: Cliente Python con `requests`](#paso-7-cliente-python-con-requests)  
13. [Paso 8: Pruebas con REST Client y Thunder Client](#paso-8-pruebas-con-rest-client-y-thunder-client)  
14. [Ejecución Completa](#ejecución-completa)  
15. [Buenas Prácticas y Escalabilidad](#buenas-prácticas-y-escalabilidad)  
16. [Conclusión](#conclusión)

---

<a name="qué-es-una-api-restful-explicación-profunda"></a>
## **1. ¿Qué es una API RESTful? (Explicación Profunda)**

> **API** = **A**pplication **P**rogramming **I**nterface  
> **REST** = **RE**presentational **S**tate **T**ransfer

### **Definición:**
Una **API RESTful** es un conjunto de reglas y convenciones para construir servicios web que permiten a diferentes sistemas comunicarse usando **HTTP** de forma estandarizada.

---

### **Analogía Real:**
> Imagina que tu API es un **restaurante**:
- **Menú** → Endpoints (`/api/users`)
- **Mesero** → Servidor (Flask)
- **Cliente** → Navegador, app móvil, Python
- **Pedidos** → Métodos HTTP (`GET`, `POST`)
- **Platos** → Datos en JSON

---

### **¿Por qué REST?**
| Característica | Beneficio |
|----------------|---------|
| **Sin estado (Stateless)** | Cada petición es independiente → fácil de escalar |
| **Uso de HTTP** | Infraestructura universal (navegadores, servidores, cachés) |
| **JSON** | Formato ligero y legible |
| **URLs descriptivas** | Fácil de entender y mantener |

---

## **2. Arquitectura REST: Principios y Reglas**

| Principio | Explicación | Ejemplo |
|---------|-------------|--------|
| **1. Recursos** | Todo es un recurso (usuario, producto) | `/api/users/1` |
| **2. URIs únicas** | Cada recurso tiene una URL | `/api/users`, `/api/users/1` |
| **3. Métodos HTTP** | Acciones sobre recursos | `GET`, `POST`, `PUT`, `DELETE` |
| **4. Stateless** | No guarda estado entre peticiones | No usa sesiones |
| **5. Cacheable** | Respuestas pueden guardarse | `Cache-Control` |
| **6. Cliente-Servidor** | Separación clara | Frontend ≠ Backend |

---

## **3. HTTP: Métodos, Códigos y Headers**

### **Métodos HTTP (CRUD)**

| Método | Acción | Idempotente | Ejemplo |
|-------|--------|-------------|--------|
| `GET` | Leer | Yes | `GET /api/users` |
| `POST` | Crear | No | `POST /api/users` |
| `PUT` | Actualizar (completo) | Yes | `PUT /api/users/1` |
| `PATCH` | Actualizar (parcial) | No | *(no usado aquí)* |
| `DELETE` | Eliminar | Yes | `DELETE /api/users/1` |

> **Idempotente** = Repetir la acción no cambia el resultado.

---

### **Códigos de Estado HTTP**

| Código | Significado | Uso |
|-------|-------------|-----|
| `200 OK` | Éxito | `GET`, `PUT`, `DELETE` |
| `201 Created` | Creado | `POST` |
| `400 Bad Request` | Error cliente | Datos inválidos |
| `404 Not Found` | No existe | ID inválido |
| `500 Internal Error` | Error servidor | Excepción |

---

### **Headers Comunes**

| Header | Uso |
|-------|-----|
| `Content-Type: application/json` | Tipo de datos enviados |
| `Accept: application/json` | Tipo esperado en respuesta |
| `Authorization` | Autenticación (JWT, etc.) |

---

## **4. Estructura del Proyecto**

```
api_rest_flask/
│
├── app.py                  # API principal + rutas
├── database.py             # Configuración SQLAlchemy
├── models.py               # Modelo User
├── export.py               # Exportar Excel/CSV
├── client.py               # Cliente Python
├── requirements.txt
│
├── static/
│   └── index.html          # Cliente web
│
├── tests/
│   └── api_tests.http      # Pruebas REST Client
│
└── database.db             # (creado al ejecutar)
```

---

## **5. Tecnologías y Justificación**

| Tecnología | **Para Qué** | **Por Qué** |
|----------|--------------|-------------|
| **Flask** | Framework web | Ligero, flexible, ideal para APIs |
| **Flask-SQLAlchemy** | ORM | Simplifica operaciones DB |
| **SQLite** | Base de datos | Embebida, sin servidor, perfecta para prototipos |
| **pandas + openpyxl** | Excel | Formato empresarial estándar |
| **csv** | CSV | Universal, fácil de importar |
| **HTML + JS (Fetch)** | Cliente web | Pruebas visuales sin herramientas externas |
| **requests** | Cliente HTTP | Consumo desde Python |
| **REST Client / Thunder Client** | Pruebas | Integradas en VS Code |

---

## **6. Paso 1: Configuración del Entorno**

```bash
mkdir api_rest_flask 
cd api_rest_flask 
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac
```

### **¿Por qué entorno virtual?**
- Aísla dependencias.
- Evita conflictos.
- Reproducible en otros equipos.

```bash
pip install flask flask-sqlalchemy pandas openpyxl requests
pip freeze > requirements.txt
```

---

## **7. Paso 2: Base de Datos SQLite**

### `database.py`

```python
# database.py
# Configuración global de SQLAlchemy

from flask_sqlalchemy import SQLAlchemy

# Instancia reutilizable en toda la app
db = SQLAlchemy()
```

> **¿Por qué no `sqlite:///:memory:`?**  
> → Datos se pierden al cerrar. Usamos archivo para persistencia.

---

## **8. Paso 3: Modelo de Datos**

### `models.py`

```python
# models.py
from database import db

class User(db.Model):
    """
    Modelo de usuario.
    Representa la tabla 'user' en SQLite.
    """
    __tablename__ = 'user'  # Opcional: nombre explícito

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)

    def to_dict(self):
        """Serializa el objeto a JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age
        }

    def __repr__(self):
        return f"<User {self.name}>"
```

---

## **9. Paso 4: API RESTful con Flask (CRUD Completo)**

### `app.py` → **Corazón del Sistema**

```python
# app.py
from flask import Flask, request, jsonify, send_file
from database import db
from models import User
from export import export_to_excel, export_to_csv

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ================================
# RUTAS CRUD
# ================================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Crear usuario"""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email required'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email exists'}), 400

    user = User(name=data['name'], email=data['email'], age=data.get('age'))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.route('/api/users', methods=['GET'])
def get_users():
    """Listar todos"""
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    """Obtener uno"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    """Actualizar"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    db.session.commit()
    return jsonify(user.to_dict())


@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Eliminar"""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


# ================================
# EXPORTACIÓN
# ================================

@app.route('/export/excel')
def export_excel_route():
    return export_to_excel()

@app.route('/export/csv')
def export_csv_route():
    return export_to_csv()


# ================================
# CLIENTE WEB
# ================================

@app.route('/')
def index():
    return app.send_static_file('index.html')


# ================================
# INICIO
# ================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada")
    print("API en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
```

---

## **10. Paso 5: Exportación a Excel y CSV**

### `export.py`

```python
# export.py
import pandas as pd
from models import User
from flask import send_file

def get_all_users():
    return [u.to_dict() for u in User.query.all()]

def export_to_excel():
    df = pd.DataFrame(get_all_users())
    file = 'users.xlsx'
    df.to_excel(file, index=False, engine='openpyxl')
    return send_file(file, as_attachment=True, download_name='usuarios.xlsx')

def export_to_csv():
    df = pd.DataFrame(get_all_users())
    file = 'users.csv'
    df.to_csv(file, index=False, encoding='utf-8')
    return send_file(file, as_attachment=True, download_name='usuarios.csv')
```

---

## **11. Paso 6: Cliente Web Interactivo**

### `static/index.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>CRUD API REST</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f8f9fa; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 10px; }
        th { background: #007bff; color: white; }
        input { padding: 8px; width: 150px; margin: 5px; }
        button { padding: 8px 15px; margin: 5px; background: #007bff; color: white; border: none; cursor: pointer; }
        .btn-success { background: #28a745; }
        .btn-danger { background: #dc3545; }
    </style>
</head>
<body>
    <h1>API REST - Gestión de Usuarios</h1>

    <h2>Crear</h2>
    <input id="name" placeholder="Nombre">
    <input id="email" placeholder="Email">
    <input id="age" type="number" placeholder="Edad">
    <button onclick="createUser()">Crear</button>

    <h2>Lista</h2>
    <button onclick="loadUsers()">Actualizar</button>
    <button onclick="exportExcel()">Excel</button>
    <button onclick="exportCSV()">CSV</button>

    <table id="table">
        <thead>
            <tr><th>ID</th><th>Nombre</th><th>Email</th><th>Edad</th><th>Acciones</th></tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        const API = '/api/users';

        async function loadUsers() {
            const res = await fetch(API);
            const users = await res.json();
            const tbody = document.querySelector('#table tbody');
            tbody.innerHTML = '';
            users.forEach(u => {
                tbody.innerHTML += `
                    <tr>
                        <td>${u.id}</td>
                        <td><input value="${u.name}" id="n${u.id}"></td>
                        <td><input value="${u.email}" id="e${u.id}"></td>
                        <td><input value="${u.age||''}" id="a${u.id}"></td>
                        <td>
                            <button class="btn-success" onclick="update(${u.id})">Update</button>
                            <button class="btn-danger" onclick="remove(${u.id})">Delete</button>
                        </td>
                    </tr>`;
            });
        }

        async function createUser() {
            const user = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                age: +document.getElementById('age').value || null
            };
            await fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(user) });
            loadUsers();
        }

        async function update(id) {
            const user = {
                name: document.getElementById(`n${id}`).value,
                email: document.getElementById(`e${id}`).value,
                age: +document.getElementById(`a${id}`).value || null
            };
            await fetch(`${API}/${id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(user) });
            loadUsers();
        }

        async function remove(id) {
            if (confirm('¿Eliminar?')) {
                await fetch(`${API}/${id}`, { method: 'DELETE' });
                loadUsers();
            }
        }

        function exportExcel() { location.href = '/export/excel'; }
        function exportCSV() { location.href = '/export/csv'; }

        loadUsers();
    </script>
</body>
</html>
```

---

## **12. Paso 7: Cliente Python con `requests`**

### `client.py`

```python
# client.py
import requests, json

BASE = 'http://127.0.0.1:5000/api/users'

def demo():
    print("=== CREAR ===")
    requests.post(BASE, json={'name': 'Ana', 'email': 'ana@x.com', 'age': 25})
    requests.post(BASE, json={'name': 'Luis', 'email': 'luis@x.com', 'age': 30})

    print("\n=== LISTA ===")
    print(json.dumps(requests.get(BASE).json(), indent=2))

    print("\n=== ACTUALIZAR ===")
    requests.put(f'{BASE}/1', json={'age': 26})

    print("\n=== ELIMINAR ===")
    requests.delete(f'{BASE}/2')

    print("\n=== FINAL ===")
    print(json.dumps(requests.get(BASE).json(), indent=2))

if __name__ == '__main__':
    demo()
```

---

## **13. Paso 8: Pruebas con REST Client y Thunder Client**

### `tests/api_tests.http`

```http
### CREATE
POST http://127.0.0.1:5000/api/users
Content-Type: application/json

{ "name": "Test", "email": "test@x.com", "age": 20 }

### READ ALL
GET http://127.0.0.1:5000/api/users

### EXPORT EXCEL
GET http://127.0.0.1:5000/export/excel
```

---

<a name="ejecución-completa"></a>
## **14. Ejecución Completa**

```bash
# 1. Activar entorno
venv\Scripts\activate

# 2. Instalar
pip install -r requirements.txt

# 3. Ejecutar API
python app.py

# 4. Probar
# - Web: http://127.0.0.1:5000
# - Python: python client.py
# - VS Code: REST Client / Thunder Client
```

---

<a name="buenas-prácticas-y-escalabilidad"></a>
## **15. Buenas Prácticas y Escalabilidad**

| Tema | Recomendación |
|------|---------------|
| **Validación** | Usa `pydantic` o `marshmallow` |
| **Autenticación** | JWT con `flask-jwt-extended` |
| **Paginación** | `?page=1&limit=10` |
| **Logs** | `logging` |
| **Docker** | Conteneriza |
| **Tests** | `pytest` + `requests` |

---
