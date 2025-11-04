# **GUÍA COMPLETA: API RESTful con Flask + Dashboard Interactivo con Python Dash**  

---

## **Índice**
1. [Nombre Correcto de la API](#nombre-correcto-de-la-api)  
2. [Estructura del Proyecto (Actualizada y Automatizada)](#estructura-del-proyecto)  
3. [Paso 0: Generar Estructura con Script Python](#paso-0-generar-estructura-con-script-python)  
4. [Paso 1: Instalar Dependencias](#paso-1-instalar-dependencias)  
5. [Paso 2: Ejecutar API `api_usuarios`](#paso-2-ejecutar-api-api_usuarios)  
6. [Paso 3: Ejecutar Dashboard Dash](#paso-3-ejecutar-dashboard-dash)  
7. [Códigos Completos (Listos para Copiar)](#códigos-completos-listos-para-copiar)  
8. [Conclusión](#conclusión)

---

<a name="nombre-correcto-de-la-api"></a>
## **1. Nombre Correcto de la API**

> **Incorrecto:** `API RESTful` (genérico)  
> **Correcto:** `api_usuarios`

### **¿Por qué?**
- **Específico**: Describe qué hace (`usuarios`).
- **Escalable**: Puedes tener `api_productos`, `api_ventas`, etc.
- **Profesional**: Así se nombran APIs reales.

---

<a name="estructura-del-proyecto"></a>
## **2. Estructura del Proyecto (Actualizada)**

```
api_usuarios/
│
├── api_usuarios.py             # API REST (Flask)
├── database.py
├── models.py
├── export.py
├── client.py
│
├── dashboard/
│   ├── dash_app.py             # Dashboard Dash
│   └── assets/
│       └── style.css
│
├── static/
│   └── index.html              # Cliente web
│
├── tests/
│   └── api_tests.http          # Pruebas REST Client
│
├── create_structure.py         # Script para generar carpetas
├── requirements.txt
└── database.db                 # (creado al ejecutar)
```

---

<a name="paso-0-generar-estructura-con-script-python"></a>
## **3. Paso 0: Generar Estructura con Script Python**

### **`create_structure.py`** → **Genera toda la estructura automáticamente**

```python
# create_structure.py
# Script para crear la estructura completa del proyecto

import os

# Estructura del proyecto
structure = {
    'api_usuarios': {
        '': ['api_usuarios.py', 'database.py', 'models.py', 'export.py', 'client.py', 'requirements.txt', 'create_structure.py'],
        'dashboard': {
            '': ['dash_app.py'],
            'assets': ['style.css']
        },
        'static': ['index.html'],
        'tests': ['api_tests.http']
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if name:  # Evitar raíz vacía
            os.makedirs(path, exist_ok=True)
            print(f"Creada carpeta: {path}")
        
        if isinstance(content, dict):
            create_structure(path, content)
        else:
            for file in content:
                file_path = os.path.join(path, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        if file.endswith('.py'):
                            f.write("# Archivo generado automáticamente\n")
                        elif file.endswith('.http'):
                            f.write("# Pruebas REST\n")
                        elif file == 'style.css':
                            f.write("/* Estilos personalizados */\n")
                        elif file == 'index.html':
                            f.write("<!-- Cliente web -->\n")
                    print(f"Creado archivo: {file_path}")

# Ejecutar
if __name__ == '__main__':
    print("Generando estructura del proyecto 'api_usuarios'...")
    create_structure('.', structure)
    print("\nEstructura generada con éxito!")
    print("Ejecuta: python create_structure.py")
```

---

### **Ejecutar el Script**

```bash
# 1. Crear carpeta raíz
mkdir api_usuarios
cd api_usuarios

# 2. Crear el script
# (Copia el código de arriba en create_structure.py)

# 3. Ejecutar
python create_structure.py
```

> **Salida:**
```
Generando estructura del proyecto 'api_usuarios'...
Creada carpeta: api_usuarios\dashboard
Creado archivo: api_usuarios\dashboard\dash_app.py
...
Estructura generada con éxito!
```

---

<a name="paso-1-instalar-dependencias"></a>
## **4. Paso 1: Instalar Dependencias**

### `requirements.txt`

```txt
Flask>=2.3.0
Flask-SQLAlchemy>=3.0.0
pandas>=2.0.0
openpyxl>=3.0.0
requests>=2.28.0
dash>=2.14.0
plotly>=5.15.0
```

```bash
pip install -r requirements.txt
```

---

<a name="paso-2-ejecutar-api-api_usuarios"></a>
## **5. Paso 2: Ejecutar API `api_usuarios`**

### **`api_usuarios.py`** → **API con nombre correcto**

```python
# api_usuarios.py
from flask import Flask, request, jsonify, send_file
from database import db
from models import User
from export import export_to_excel, export_to_csv

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# RUTAS CRUD
@app.route('/api/users', methods=['POST'])
def create_user():
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
    return jsonify([u.to_dict() for u in User.query.all()])

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# EXPORTACIÓN
@app.route('/export/excel')
def export_excel_route():
    return export_to_excel()

@app.route('/export/csv')
def export_csv_route():
    return export_to_csv()

# CLIENTE WEB
@app.route('/')
def index():
    return app.send_static_file('index.html')

# INICIO
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada")
    print("API 'api_usuarios' en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
```

---

<a name="paso-3-ejecutar-dashboard-dash"></a>
## **6. Paso 3: Ejecutar Dashboard Dash**

### **`dashboard/dash_app.py`**

```python
# dashboard/dash_app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000/api/users"

app = dash.Dash(__name__, title="Dashboard - api_usuarios")

def fetch_users():
    try:
        r = requests.get(API_URL)
        return pd.DataFrame(r.json())
    except:
        return pd.DataFrame(columns=['id', 'name', 'email', 'age'])

app.layout = html.Div([
    html.H1("Dashboard de Usuarios", style={'textAlign': 'center'}),
    html.Button("Actualizar", id="btn", n_clicks=0),
    html.Div(id="stats"),
    dcc.Graph(id="bar"),
    dcc.Graph(id="pie"),
    html.Div(id="table"),
    dcc.Interval(id="interval", interval=30000, n_intervals=0)
])

@app.callback(
    [Output("stats", "children"), Output("bar", "figure"), Output("pie", "figure"), Output("table", "children")],
    [Input("btn", "n_clicks"), Input("interval", "n_intervals")]
)
def update(n, i):
    df = fetch_users()
    if df.empty:
        return "Sin datos", {}, {}, "API no disponible"

    stats = f"Usuarios: {len(df)} | Edad promedio: {df['age'].mean():.1f}"
    fig_bar = px.bar(df, x='name', y='age', title="Edad por Usuario")
    fig_pie = px.pie(df, names='name', title="Proporción")
    table = html.Table([html.Tr([html.Th(c) for c in df.columns])] + 
                       [html.Tr([html.Td(df.iloc[i][c]) for c in df.columns]) for i in range(len(df))])
    return stats, fig_bar, fig_pie, table

if __name__ == '__main__':
    print("Dashboard en http://127.0.0.1:8050")
    app.run_server(debug=True, port=8050)
```

---

<a name="códigos-completos-listos-para-copiar"></a>
## **7. Códigos Completos (Listos para Copiar)**

### `database.py`
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

### `models.py`
```python
from database import db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'age': self.age}
```

### `export.py`
```python
import pandas as pd
from models import User
from flask import send_file
def export_to_excel():
    df = pd.DataFrame([u.to_dict() for u in User.query.all()])
    df.to_excel('users.xlsx', index=False)
    return send_file('users.xlsx', as_attachment=True)
def export_to_csv():
    df = pd.DataFrame([u.to_dict() for u in User.query.all()])
    df.to_csv('users.csv', index=False)
    return send_file('users.csv', as_attachment=True)
```

---

## **Ejecución Final**

```bash
# Terminal 1
python api_usuarios.py

# Terminal 2
python dashboard/dash_app.py
```

- **API**: [http://127.0.0.1:5000](http://127.0.0.1:5000)  
- **Dashboard**: [http://127.0.0.1:8050](http://127.0.0.1:8050)

