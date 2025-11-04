# **GUÍA COMPLETA: Integrar tu API RESTful con Python Dash y Plotly**  
### **Dashboard Interactivo con Datos de la API Flask + SQLite**

---

## **Índice**
1. [¿Qué es Dash y por qué usarlo?](#qué-es-dash-y-por-qué-usarlo)  
2. [Estructura del Proyecto Actualizada](#estructura-del-proyecto-actualizada)  
3. [Paso 1: Instalar Dash y Dependencias](#paso-1-instalar-dash-y-dependencias)  
4. [Paso 2: Crear el Dashboard con Dash](#paso-2-crear-el-dashboard-con-dash)  
5. [Paso 3: Conectar el Dashboard a la API REST](#paso-3-conectar-el-dashboard-a-la-api-rest)  
6. [Paso 4: Funcionalidades del Dashboard](#paso-4-funcionalidades-del-dashboard)  
7. [Paso 5: Ejecutar API + Dashboard](#paso-5-ejecutar-api--dashboard)  
8. [Paso 6: Mejoras y Buenas Prácticas](#paso-6-mejoras-y-buenas-prácticas)  
9. [Conclusión](#conclusión)

---

<a name="qué-es-dash-y-por-qué-usarlo"></a>
## **1. ¿Qué es Dash y por qué usarlo?**

> **Dash** = Framework de **Python** para crear **dashboards web interactivos** sin escribir JavaScript.

### **Ventajas de Dash**
| Característica | Beneficio |
|----------------|---------|
| **100% Python** | No necesitas HTML/CSS/JS |
| **Plotly** | Gráficos interactivos (zoom, hover, exportar) |
| **React bajo el capó** | Rápido y escalable |
| **Integración con Flask** | Puede correr junto a tu API |
| **Callbacks** | Actualiza gráficos en tiempo real |

---

<a name="estructura-del-proyecto-actualizada"></a>
## **2. Estructura del Proyecto Actualizada**

```
api_rest_flask/
│
├── app.py                  # API REST (Flask)
├── database.py
├── models.py
├── export.py
├── client.py
│
├── dashboard/
│   ├── dash_app.py         # Dashboard principal
│   └── assets/
│       └── style.css       # Estilos personalizados
│
├── static/
│   └── index.html
│
├── tests/
│   └── api_tests.http
│
└── requirements.txt
```

---

<a name="paso-1-instalar-dash-y-dependencias"></a>
## **3. Paso 1: Instalar Dash y Dependencias**

```bash
# Activar entorno
venv\Scripts\activate

# Instalar Dash
pip install dash pandas plotly

# Actualizar requirements.txt
pip freeze > requirements.txt
```

> **Nota**: `pandas` y `requests` ya estaban, pero los mantenemos.

---

<a name="paso-2-crear-el-dashboard-con-dash"></a>
## **4. Paso 2: Crear el Dashboard con Dash**

### **Crear carpeta `dashboard/`**

```bash
mkdir dashboard
mkdir dashboard\assets
```

---

### `dashboard/dash_app.py` → **Dashboard Completo**

```python
# dashboard/dash_app.py
# Dashboard interactivo con Dash + Plotly
# Consume la API REST en http://127.0.0.1:5000

import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import requests
from flask import Flask

# ================================
# CONFIGURACIÓN
# ================================

API_URL = "http://127.0.0.1:5000/api/users"
EXPORT_EXCEL = "http://127.0.0.1:5000/export/excel"
EXPORT_CSV = "http://127.0.0.1:5000/export/csv"

# Inicializar Dash (integrado con Flask si es necesario)
app = dash.Dash(__name__, title="Dashboard Usuarios")

# ================================
# FUNCIONES DE DATOS
# ================================

def fetch_users():
    """Obtiene usuarios desde la API"""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as e:
        print(f"Error al conectar con API: {e}")
        return pd.DataFrame(columns=['id', 'name', 'email', 'age'])

# ================================
# LAYOUT DEL DASHBOARD
# ================================

app.layout = html.Div([
    html.H1("Dashboard de Usuarios - API REST + Dash", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'margin': '20px'}),

    # Botones de control
    html.Div([
        html.Button("Actualizar Datos", id="btn-refresh", n_clicks=0,
                    style={'margin': '10px', 'padding': '10px 20px'}),
        html.A("Exportar Excel", href=EXPORT_EXCEL, target="_blank",
               style={'margin': '10px', 'padding': '10px 20px', 'background': '#27ae60', 'color': 'white', 'textDecoration': 'none'}),
        html.A("Exportar CSV", href=EXPORT_CSV, target="_blank",
               style={'margin': '10px', 'padding': '10px 20px', 'background': '#2980b9', 'color': 'white', 'textDecoration': 'none'}),
    ], style={'textAlign': 'center'}),

    # Estadísticas
    html.Div(id="stats", style={'textAlign': 'center', 'margin': '20px', 'fontSize': '18px'}),

    # Gráfico de barras: Edad promedio por nombre
    dcc.Graph(id="bar-age"),

    # Gráfico de pastel: Distribución de edades
    dcc.Graph(id="pie-age"),

    # Tabla de usuarios
    html.H3("Lista de Usuarios", style={'textAlign': 'center', 'marginTop': '40px'}),
    html.Div(id="table-container"),

    # Intervalo para auto-actualización (opcional)
    dcc.Interval(id="interval", interval=30*1000, n_intervals=0)  # cada 30 seg
], style={'fontFamily': 'Arial', 'backgroundColor': '#ecf0f1', 'padding': '20px'})

# ================================
# CALLBACKS
# ================================

@app.callback(
    [Output("stats", "children"),
     Output("bar-age", "figure"),
     Output("pie-age", "figure"),
     Output("table-container", "children")],
    [Input("btn-refresh", "n_clicks"),
     Input("interval", "n_intervals")]
)
def update_dashboard(n_clicks, n_intervals):
    df = fetch_users()

    if df.empty:
        empty_msg = html.P("No hay datos disponibles. Asegúrate de que la API esté corriendo.")
        return empty_msg, {}, {}, empty_msg

    # Estadísticas
    total = len(df)
    avg_age = df['age'].mean()
    stats = html.Div([
        html.Span(f"Total Usuarios: {total} | ", style={'fontWeight': 'bold'}),
        html.Span(f"Edad Promedio: {avg_age:.1f} años" if pd.notna(avg_age) else "Edad Promedio: N/A")
    ])

    # Gráfico de barras: edad por usuario
    fig_bar = px.bar(df, x='name', y='age', title="Edad por Usuario",
                     labels={'name': 'Nombre', 'age': 'Edad'},
                     color='age', color_continuous_scale='Viridis')
    fig_bar.update_layout(transition_duration=500)

    # Gráfico de pastel: rangos de edad
    if 'age' in df.columns and df['age'].notna().any():
        df['rango_edad'] = pd.cut(df['age'], bins=[0, 18, 30, 50, 100], 
                                  labels=['0-18', '19-30', '31-50', '51+'])
        fig_pie = px.pie(df, names='rango_edad', title="Distribución de Edades",
                         color_discrete_sequence=px.colors.sequential.Plasma)
    else:
        fig_pie = px.pie(names=[], values=[], title="Sin datos de edad")

    # Tabla
    table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(len(df))
        ])
    ], style={'width': '100%', 'border': '1px solid #ddd', 'margin': '20px auto'})

    return stats, fig_bar, fig_pie, table

# ================================
# ESTILOS PERSONALIZADOS
# ================================

with open("dashboard/assets/style.css", "w") as f:
    f.write("""
    body { background-color: #f8f9fa; }
    .dash-table-container { margin: 20px; }
    """)

# ================================
# EJECUTAR
# ================================

if __name__ == '__main__':
    print("Dashboard corriendo en http://127.0.0.1:8050")
    app.run_server(debug=True, port=8050)
```

---

<a name="paso-3-conectar-el-dashboard-a-la-api-rest"></a>
## **5. Paso 3: Conectar el Dashboard a la API REST**

### **Cómo funciona la conexión**
```python
requests.get("http://127.0.0.1:5000/api/users")
```
- El dashboard **consume** la API en tiempo real.
- Cada vez que presionas **"Actualizar Datos"**, se llama a la API.
- También se actualiza **cada 30 segundos** automáticamente.

---

<a name="paso-4-funcionalidades-del-dashboard"></a>
## **6. Paso 4: Funcionalidades del Dashboard**

| Funcionalidad | Descripción |
|--------------|-----------|
| **Actualización manual** | Botón "Actualizar Datos" |
| **Auto-refresh** | Cada 30 segundos |
| **Estadísticas** | Total usuarios, edad promedio |
| **Gráfico de barras** | Edad por usuario |
| **Gráfico de pastel** | Distribución por rangos de edad |
| **Tabla completa** | Todos los usuarios |
| **Exportar** | Botones directos a Excel/CSV |

---

<a name="paso-5-ejecutar-api--dashboard"></a>
## **7. Paso 5: Ejecutar API + Dashboard**

### **Paso a paso (2 terminales)**

#### **Terminal 1: Iniciar API Flask**
```bash
venv\Scripts\activate
python app.py
```
> Salida: `http://127.0.0.1:5000`

#### **Terminal 2: Iniciar Dashboard Dash**
```bash
venv\Scripts\activate
python dashboard/dash_app.py
```
> Salida: `http://127.0.0.1:8050`

---

### **Abrir en el navegador**
- **API + Cliente Web**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Dashboard Dash**: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

<a name="paso-6-mejoras-y-buenas-prácticas"></a>
## **8. Paso 6: Mejoras y Buenas Prácticas**

| Mejora | Cómo implementarla |
|-------|-------------------|
| **Integrar Dash en Flask** | Usa `Dash(app)` en lugar de app separada |
| **Autenticación** | JWT en API + login en Dash |
| **Caching** | `functools.cache` para evitar llamadas repetidas |
| **Filtros** | Dropdowns para filtrar por edad, nombre |
| **Responsive** | Usa `dash-bootstrap-components` |
| **Deploy** | Render, Heroku, Docker |

---

### **Ejemplo: Integrar Dash dentro de Flask (Opcional)**

```python
# En app.py (al final)
from dashboard.dash_app import app as dash_app
dash_app.server = app  # Integra Dash en Flask
```

---

<a name="conclusión"></a>
## **9. Conclusión**

**Has logrado:**

| Logro | Herramienta |
|------|------------|
| API RESTful | Flask + SQLite |
| CRUD completo | GET/POST/PUT/DELETE |
| Exportación | Excel + CSV |
| Cliente web | HTML + JS |
| **Dashboard interactivo** | **Dash + Plotly** |
| **Conexión en tiempo real** | `requests` |

---


---

**¡Tu API ahora tiene un frontend profesional con Dash!**
