# 🐍 Curso Práctico de Python para Gestión de Datos y Machine Learning

> **Descarga este curso completo en formato `.zip` desde [aquí](#) (enlace simulado)**  
> *Incluye todos los ejemplos prácticos, scripts y datasets listos para ejecutar.*

---

## 📚 Tabla de Contenidos

1. [Buenas Prácticas de Programación en Python (incluyendo `main`)](#-buenas-prácticas-de-programación-en-python-incluyendo-main)
2. [Entornos Virtuales: Definición y Justificación](#-entornos-virtuales-definición-y-justificación)
3. [Estructuras de Datos Básicas: Ventajas y Desventajas](#-estructuras-de-datos-básicas-ventajas-y-desventajas)
4. [Almacenamiento en Archivos Planos](#-almacenamiento-en-archivos-planos)
5. [Bases de Datos Relacionales (SQLite)](#-bases-de-datos-relacionales-sqlite)
6. [Análisis de Datos con Pandas](#-análisis-de-datos-con-pandas)
7. [Gestión Avanzada de Archivos](#-gestión-avanzada-de-archivos)
8. [Ejemplo Integrado: Sistema de Tareas](#-ejemplo-integrado-sistema-de-tareas)
9. [Preparación de Datos para Machine Learning](#-preparación-de-datos-para-machine-learning)
10. [Bonus: Logging, Configuración y Manejo de Errores](#-bonus-logging-configuración-y-manejo-de-errores)

---

## 🧭 1. Buenas Prácticas de Programación en Python (incluyendo `main`)

### ✅ ¿Por qué importa?

- Legibilidad
- Mantenibilidad
- Reusabilidad
- Evitar efectos secundarios al importar

### 🎯 Recomendaciones

```python
# ✅ Buen ejemplo: uso de if __name__ == "__main__"
def saludar(nombre):
    return f"Hola, {nombre}!"

def main():
    nombre = input("Ingresa tu nombre: ")
    print(saludar(nombre))

if __name__ == "__main__":
    main()
```

### 📌 Consejos Adicionales

- Usa nombres descriptivos: `calcular_promedio()` > `calc()`
- Documenta funciones con docstrings
- Usa type hints (Python 3.5+)
- Sigue PEP8 (herramientas: `flake8`, `black`, `isort`)
- Divide en módulos y paquetes cuando crezca el proyecto

---

## 🧪 2. Entornos Virtuales: Definición y Justificación

### ❓ ¿Qué es un entorno virtual?

Un entorno virtual es un espacio aislado donde puedes instalar paquetes sin afectar el sistema global ni otros proyectos.

### 🧩 ¿Por qué usarlo?

- Evita conflictos de versiones entre proyectos
- Facilita la replicabilidad (`requirements.txt`)
- Ideal para colaboración y despliegue

### 🛠️ Cómo crear uno

```bash
# Crear entorno
python -m venv mi_entorno

# Activar (Windows)
mi_entorno\Scripts\activate

# Activar (Linux/Mac)
source mi_entorno/bin/activate

# Instalar paquetes
pip install pandas numpy

# Guardar dependencias
pip freeze > requirements.txt

# Desactivar
deactivate
```

> 💡 **Tip**: Usa `pipenv` o `poetry` para gestión avanzada de dependencias.

---

## 🗃️ 3. Estructuras de Datos Básicas: Ventajas y Desventajas

| Estructura | Mutable | Ordenada | Duplicados | Uso típico | Ventajas | Desventajas |
|------------|---------|----------|------------|------------|----------|-------------|
| `list`     | ✅      | ✅       | ✅         | Secuencias | Dinámica, indexada | Lenta en búsquedas grandes |
| `tuple`    | ❌      | ✅       | ✅         | Datos inmutables | Rápida, segura | No modificable |
| `set`      | ✅      | ❌       | ❌         | Eliminar duplicados | Búsquedas O(1) | Sin orden, no indexado |
| `dict`     | ✅      | ✅ (3.7+) | ❌ claves  | Mapeos clave-valor | Acceso rápido por clave | Mayor consumo de memoria |

### 🧪 Ejemplo práctico

```python
# Lista: agregar tareas
tareas = ["Comprar leche", "Estudiar Python"]
tareas.append("Hacer ejercicio")

# Tupla: coordenadas geográficas
coordenadas = (19.4326, -99.1332)

# Set: eliminar duplicados
emails = ["a@b.com", "c@d.com", "a@b.com"]
unicos = set(emails)  # {'a@b.com', 'c@d.com'}

# Diccionario: perfil de usuario
usuario = {
    "nombre": "Ana",
    "edad": 25,
    "activo": True
}
```

---

## 📁 4. Almacenamiento en Archivos Planos

### ✍️ Escribir y leer archivos `.txt`

```python
# Escribir
with open("notas.txt", "w", encoding="utf-8") as f:
    f.write("Primera línea\nSegunda línea")

# Leer
with open("notas.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
    print(contenido)
```

### 📊 CSV: Comma Separated Values

```python
import csv

# Escribir CSV
datos = [["Nombre", "Edad"], ["Ana", 25], ["Luis", 30]]
with open("personas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(datos)

# Leer CSV
with open("personas.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

> 💡 Usa `csv.DictReader` y `csv.DictWriter` para trabajar con diccionarios.

---

## 💾 5. Bases de Datos Relacionales (SQLite)

### 🐘 ¿Por qué SQLite?

- Liviana, sin servidor
- Ideal para prototipos y aplicaciones pequeñas
- Soportada nativamente en Python

### 🧩 Ejemplo práctico: CRUD básico

```python
import sqlite3

# Conectar (crea si no existe)
conn = sqlite3.connect("tareas.db")
cursor = conn.cursor()

# Crear tabla
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        completada BOOLEAN DEFAULT 0
    )
""")

# Insertar
cursor.execute("INSERT INTO tareas (titulo) VALUES (?)", ("Aprender SQL",))
conn.commit()

# Consultar
cursor.execute("SELECT * FROM tareas")
for row in cursor.fetchall():
    print(row)

# Cerrar
conn.close()
```

> ✅ Usa parámetros `?` para evitar inyecciones SQL.

---

## 📈 6. Análisis de Datos con Pandas

### 🚀 Instalación

```bash
pip install pandas matplotlib
```

### 📊 Ejemplo: Análisis de ventas

```python
import pandas as pd

# Crear DataFrame
data = {
    "Producto": ["A", "B", "C", "A"],
    "Ventas": [100, 150, 200, 120],
    "Mes": ["Ene", "Ene", "Feb", "Feb"]
}
df = pd.DataFrame(data)

# Operaciones comunes
print(df.head())
print(df.groupby("Producto")["Ventas"].sum())
print(df[df["Ventas"] > 130])

# Guardar y cargar
df.to_csv("ventas.csv", index=False)
df_cargado = pd.read_csv("ventas.csv")
```

### 📉 Visualización rápida

```python
import matplotlib.pyplot as plt

df.groupby("Producto")["Ventas"].sum().plot(kind="bar")
plt.title("Ventas por Producto")
plt.show()
```

---

## 🗃️ 7. Gestión Avanzada de Archivos

### 🔄 Recorrer directorios

```python
import os
from pathlib import Path

# Usando pathlib (recomendado)
directorio = Path("datos")
for archivo in directorio.glob("*.csv"):
    print(archivo.name)

# Crear directorios
nuevo_dir = Path("backup")
nuevo_dir.mkdir(exist_ok=True)
```

### 🗜️ Comprimir y descomprimir

```python
import zipfile

# Comprimir
with zipfile.ZipFile("archivos.zip", "w") as zf:
    zf.write("ventas.csv")
    zf.write("personas.csv")

# Descomprimir
with zipfile.ZipFile("archivos.zip", "r") as zf:
    zf.extractall("extraidos")
```

### 🕒 Manejo de fechas en nombres de archivos

```python
from datetime import datetime

hoy = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre = f"backup_{hoy}.zip"
print(nombre)  # backup_20250405_103045.zip
```

---

## 🧩 8. Ejemplo Integrado: Sistema de Tareas

> Un sistema completo que usa archivos, SQLite, y buenas prácticas.

📁 Estructura del proyecto:

```
sistema_tareas/
├── main.py
├── database.py
├── models.py
├── utils.py
└── tareas.db
```

### 🧱 `models.py`

```python
class Tarea:
    def __init__(self, id, titulo, completada=False):
        self.id = id
        self.titulo = titulo
        self.completada = completada

    def __str__(self):
        estado = "✅" if self.completada else "❌"
        return f"{self.id}. {self.titulo} {estado}"
```

### 🗄️ `database.py`

```python
import sqlite3
from models import Tarea

class TareaDB:
    def __init__(self, db_path="tareas.db"):
        self.conn = sqlite3.connect(db_path)
        self.crear_tabla()

    def crear_tabla(self):
        query = """
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            completada INTEGER DEFAULT 0
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def agregar(self, titulo):
        self.conn.execute("INSERT INTO tareas (titulo) VALUES (?)", (titulo,))
        self.conn.commit()

    def listar(self):
        cursor = self.conn.execute("SELECT id, titulo, completada FROM tareas")
        return [Tarea(*row) for row in cursor.fetchall()]
```

### 🚀 `main.py`

```python
from database import TareaDB

def main():
    db = TareaDB()
    
    while True:
        print("\n1. Agregar tarea")
        print("2. Ver tareas")
        print("3. Salir")
        
        opcion = input("Elige opción: ")
        
        if opcion == "1":
            titulo = input("Título: ")
            db.agregar(titulo)
            print("✅ Tarea agregada.")
        elif opcion == "2":
            tareas = db.listar()
            for tarea in tareas:
                print(tarea)
        elif opcion == "3":
            break

if __name__ == "__main__":
    main()
```

---

## 🤖 9. Preparación de Datos para Machine Learning

### 🧹 Limpieza de datos con Pandas

```python
import pandas as pd

df = pd.read_csv("datos_sucios.csv")

# Ver nulos
print(df.isnull().sum())

# Eliminar nulos
df = df.dropna()

# O rellenar
df["edad"].fillna(df["edad"].mean(), inplace=True)

# Codificar categóricas
df = pd.get_dummies(df, columns=["categoria"])

# Escalar (usando sklearn)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[["ingreso", "edad"]] = scaler.fit_transform(df[["ingreso", "edad"]])
```

### 💾 Guardar datos procesados

```python
df.to_csv("datos_limpios.csv", index=False)

# Guardar scaler para usar en producción
import joblib
joblib.dump(scaler, "scaler.pkl")
```

### 📂 Estructura típica para ML

```
proyecto_ml/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
├── models/
├── notebooks/
├── src/
│   ├── data_preprocessing.py
│   └── train_model.py
└── requirements.txt
```

---

## 🧭 10. Bonus: Logging, Configuración y Manejo de Errores

### 📝 Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logging.info("Aplicación iniciada")
logging.error("Error al conectar a la base de datos")
```

### ⚙️ Archivo de configuración (`config.ini`)

```ini
[DATABASE]
path = tareas.db

[LOGGING]
level = INFO
```

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
db_path = config["DATABASE"]["path"]
```

### 🛡️ Manejo de errores

```python
def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logging.error("División por cero intentada")
        return None
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        raise
```

---

## 📥 Descarga el Proyecto Completo

👉 [Descargar curso_completo_python_datos_ml.zip](#) *(simulado)*

Incluye:

- Todos los scripts `.py` listos para ejecutar
- Archivos de ejemplo (CSV, TXT, DB)
- `requirements.txt`
- Estructura de proyecto organizada
- README con instrucciones de instalación

---

## 📚 Recursos Adicionales

- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Documentación oficial de Python](https://docs.python.org/3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLite Python Docs](https://docs.python.org/3/library/sqlite3.html)

---

## ✅ ¡Listo para empezar!

Con este curso tendrás una base sólida en Python para gestión de datos, preparación para machine learning, y buenas prácticas profesionales. ¡Manos a la obra!

> 🐍 *"La simplicidad es la máxima sofisticación." — Leonardo da Vinci (y también la filosofía de Python)*

---

**Autor**: Tu Instructor de Python  
**Versión**: 1.0  
**Última actualización**: Abril 2025  
**Licencia**: MIT — Libre para uso educativo y comercial.

---

> 📬 ¿Encontraste un error? ¿Tienes sugerencias? ¡Abre un issue en nuestro [repositorio de GitHub](#)!
