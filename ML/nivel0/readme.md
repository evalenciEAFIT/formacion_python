# 🐍 Curso Práctico de Python para Gestión de Datos y Machine Learning
Nivel 0 - nivelación

## Tabla de Contenidos

1. Cómo pasar parámetros por CLI al inicio
2. Buenas Prácticas de Programación en Python (incluyendo `main`)
3. Entornos Virtuales: Definición y Justificación
4. Estructuras de Datos Básicas: Ventajas y Desventajas
5. Almacenamiento en Archivos Planos
6. Bases de Datos Relacionales (SQLite)
7. Análisis de Datos con Pandas
8. Gestión Avanzada de Archivos
9. Ejemplo Integrado: Sistema de Tareas
10. Preparación de Datos para Machine Learning
11. Bonus: Logging, Configuración y Manejo de Errores
12. Descarga el Proyecto Completo

---

## 1. Cómo pasar parámetros por CLI al inicio

Permitir que tu programa reciba argumentos desde la **línea de comandos (CLI)** es esencial para:
- Automatización
- Scripts reutilizables
- Integración con otros sistemas
- Pruebas sin modificar el código

### Opción 1: Usando `sys.argv` (simple)

```python
# cli_simple.py
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python cli_simple.py <nombre> [edad]")
        sys.exit(1)

    nombre = sys.argv[1]
    edad = sys.argv[2] if len(sys.argv) > 2 else "desconocida"

    print(f"Hola {nombre}, tienes {edad} años.")

if __name__ == "__main__":
    main()
```

**Ejecución:**

```bash
Comando:
python cli_simple.py Ana 25

Salida:
Hola Ana, tienes 25 años.
```

---

### Opción 2: Usando `argparse` (recomendado para proyectos serios)

```python
# cli_avanzado.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="Sistema de gestión de tareas por CLI")
    parser.add_argument("--nombre", "-n", type=str, required=True, help="Tu nombre")
    parser.add_argument("--edad", "-e", type=int, default=0, help="Tu edad (opcional)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar logs detallados")

    args = parser.parse_args()

    if args.verbose:
        print("[INFO] Modo verboso activado")

    print(f"¡Hola {args.nombre}!")
    if args.edad > 0:
        print(f"Tienes {args.edad} años.")

if __name__ == "__main__":
    main()
```

**Ejecución:**

```bash
Comando:
python cli_avanzado.py -n "Carlos" -e 30 -v

Salida:
[INFO] Modo verboso activado
¡Hola Carlos!
Tienes 30 años.
```

---

### Consejos para CLI

- Usa `--help` o `-h` para que argparse genere ayuda automática.
- Valida tipos de datos (`type=int`, `type=float`, etc.).
- Define valores por defecto (`default=...`).
- Agrupa argumentos con `add_argument_group` si son muchos.
- Para ML: recibe rutas de archivos, hiperparámetros, modos (train/test), etc.

---

## 2. Buenas Prácticas de Programación en Python (incluyendo `main`)
### ¿Por qué importa?
- Legibilidad
- Mantenibilidad
- Reusabilidad
- Evitar efectos secundarios al importar

### Recomendaciones

```python
# Buen ejemplo: uso de if __name__ == "__main__"
def saludar(nombre):
    return f"Hola, {nombre}!"

def main():
    nombre = input("Ingresa tu nombre: ")
    print(saludar(nombre))

if __name__ == "__main__":
    main()
```

### Consejos Adicionales

- Usa nombres descriptivos: `calcular_promedio()` mejor que `calc()`
- Divide en módulos y paquetes cuando crezca el proyecto

---

## 3. Entornos Virtuales: Definición y Justificación

### ¿Qué es un entorno virtual?
Un entorno virtual es un espacio aislado donde puedes instalar paquetes sin afectar el sistema global ni otros proyectos.

### ¿Por qué usarlo?
- Evita conflictos de versiones entre proyectos
- Facilita la replicabilidad (`requirements.txt`)
- Ideal para colaboración y despliegue

### Cómo crear uno

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

> **Tip**: Usa `pipenv` o `poetry` para gestión avanzada de dependencias.

---

## 4. Estructuras de Datos Básicas: Ventajas y Desventajas

| Estructura | Mutable | Ordenada | Duplicados | Uso típico | Ventajas | Desventajas |
|------------|---------|----------|------------|------------|----------|-------------|
| `list`     | ✅      | ✅       | ✅         | Secuencias | Dinámica, indexada | Lenta en búsquedas grandes |
| `tuple`    | ❌      | ✅       | ✅         | Datos inmutables | Rápida, segura | No modificable |
| `set`      | ✅      | ❌       | ❌         | Eliminar duplicados | Búsquedas O(1) | Sin orden, no indexado |
| `dict`     | ✅      | ✅ (3.7+) | ❌ claves  | Mapeos clave-valor | Acceso rápido por clave | Mayor consumo de memoria |

### Ejemplo práctico

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

## 5. Almacenamiento en Archivos Planos

### Escribir y leer archivos `.txt`

```python
# Escribir
with open("notas.txt", "w", encoding="utf-8") as f:
    f.write("Primera línea\nSegunda línea")

# Leer
with open("notas.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
    print(contenido)
```

### CSV: Comma Separated Values

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

> Usa `csv.DictReader` y `csv.DictWriter` para trabajar con diccionarios.

---

## 6. Bases de Datos Relacionales (SQLite)

### ¿Por qué SQLite?
- Liviana, sin servidor
- Ideal para prototipos y aplicaciones pequeñas
- Soportada nativamente en Python

### Ejemplo práctico: CRUD básico

```python
import sqlite3
from contextlib import contextmanager

# Gestor de contexto para conexión segura
@contextmanager
def obtener_conexion(db_path="tareas.db"):
    """Maneja la conexión a la base de datos de forma segura."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"❌ Error en la base de datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

# Crear tabla si no existe
def crear_tabla():
    with obtener_conexion() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                completada INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("Tabla 'tareas' creada o ya existente.")

# INSERTAR: Crear nueva tarea
def crear_tarea(titulo):
    with obtener_conexion() as conn:
        try:
            cursor = conn.execute(
                "INSERT INTO tareas (titulo) VALUES (?)",
                (titulo,)
            )
            conn.commit()
            print(f"✅ Tarea creada con ID: {cursor.lastrowid} → '{titulo}'")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"❌ Error al crear tarea: {e}")
            return None

# LEER: Listar todas las tareas
def listar_tareas():
    with obtener_conexion() as conn:
        cursor = conn.execute("""
            SELECT id, titulo, completada, fecha_creacion
            FROM tareas
            ORDER BY fecha_creacion DESC
        """)
        tareas = cursor.fetchall()
        
        if not tareas:
            print("No hay tareas registradas.")
            return []
        
        print(f"\nLISTA DE TAREAS ({len(tareas)}):")
        print("-" * 60)
        for tarea in tareas:
            estado = "✅ Completada" if tarea["completada"] else "❌ Pendiente"
            print(f"ID: {tarea['id']} | {tarea['titulo']} | {estado} | Creada: {tarea['fecha_creacion']}")
        print("-" * 60)
        return tareas

# ACTUALIZAR: Marcar tarea como completada
def actualizar_tarea(id_tarea, completada=True):
    with obtener_conexion() as conn:
        cursor = conn.execute(
            "UPDATE tareas SET completada = ? WHERE id = ?",
            (1 if completada else 0, id_tarea)
        )
        conn.commit()
        
        if cursor.rowcount == 0:
            print(f"⚠ No se encontró tarea con ID: {id_tarea}")
            return False
        else:
            estado = "completada" if completada else "marcada como pendiente"
            print(f"Tarea ID {id_tarea} {estado}.")
            return True

# ➖ ELIMINAR: Borrar tarea por ID
def eliminar_tarea(id_tarea):
    with obtener_conexion() as conn:
        cursor = conn.execute("DELETE FROM tareas WHERE id = ?", (id_tarea,))
        conn.commit()
        
        if cursor.rowcount == 0:
            print(f"⚠ No se encontró tarea con ID: {id_tarea}")
            return False
        else:
            print(f"Tarea ID {id_tarea} eliminada.")
            return True

# BUSCAR: Buscar tarea por título (búsqueda parcial)
def buscar_tarea_por_titulo(palabra_clave):
    with obtener_conexion() as conn:
        cursor = conn.execute(
            "SELECT id, titulo, completada, fecha_creacion FROM tareas WHERE titulo LIKE ?",
            (f"%{palabra_clave}%",)
        )
        resultados = cursor.fetchall()
        
        if not resultados:
            print(f"No se encontraron tareas con '{palabra_clave}'.")
            return []
        
        print(f"\nRESULTADOS PARA '{palabra_clave}' ({len(resultados)}):")
        print("-" * 60)
        for tarea in resultados:
            estado = "✅ Completada" if tarea["completada"] else "❌ Pendiente"
            print(f"ID: {tarea['id']} | {tarea['titulo']} | {estado} | Creada: {tarea['fecha_creacion']}")
        print("-" * 60)
        return resultados

# Función principal de demostración
def main():
    print("INICIANDO DEMO CRUD CON SQLITE...\n")
    
    # 1. Crear tabla
    crear_tabla()
    
    # 2. Insertar tareas
    id1 = crear_tarea("Aprender SQL")
    id2 = crear_tarea("Practicar Python")
    id3 = crear_tarea("Hacer ejercicio")
    
    print("\n" + "="*60)
    
    # 3. Listar todas
    listar_tareas()
    
    print("\n" + "="*60)
    
    # 4. Actualizar (marcar como completada)
    actualizar_tarea(id1, completada=True)
    actualizar_tarea(id2, completada=True)
    
    print("\n" + "="*60)
    
    # 5. Listar nuevamente
    listar_tareas()
    
    print("\n" + "="*60)
    
    # 6. Buscar por palabra clave
    buscar_tarea_por_titulo("Python")
    
    print("\n" + "="*60)
    
    # 7. Eliminar una tarea
    eliminar_tarea(id3)
    
    print("\n" + "="*60)
    
    # 8. Listar final
    listar_tareas()

# Ejecutar demo
if __name__ == "__main__":
    main()
```

> Usa parámetros `?` para evitar inyecciones SQL.

---

## 7. Análisis de Datos con Pandas

### Instalación

```bash
pip install pandas matplotlib
```

### Ejemplo: Análisis de ventas

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

### Visualización rápida

```python
import matplotlib.pyplot as plt

df.groupby("Producto")["Ventas"].sum().plot(kind="bar")
plt.title("Ventas por Producto")
plt.show()
```

---

## 8. Gestión Avanzada de Archivos

### Recorrer directorios

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

### Comprimir y descomprimir

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

### Manejo de fechas en nombres de archivos

```python
from datetime import datetime

hoy = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre = f"backup_{hoy}.zip"
print(nombre)  # backup_20250405_103045.zip
```

---

## 9. Ejemplo Integrado: Sistema de Tareas

> Un sistema completo que usa archivos, SQLite, CLI, y buenas prácticas.

📁 Estructura del proyecto:

```
sistema_tareas/
├── main.py
├── database.py
├── models.py
├── utils.py
└── tareas.db
```

### `models.py`

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

### `database.py`

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

### `main.py` (con soporte CLI)

```python
import argparse
from database import TareaDB

def main():
    parser = argparse.ArgumentParser(description="Gestor de Tareas CLI")
    parser.add_argument("--agregar", "-a", type=str, help="Agregar nueva tarea")
    parser.add_argument("--listar", "-l", action="store_true", help="Listar todas las tareas")
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo detallado")

    args = parser.parse_args()
    db = TareaDB()

    if args.agregar:
        db.agregar(args.agregar)
        print(f"Tarea '{args.agregar}' agregada.")
    elif args.listar:
        tareas = db.listar()
        if not tareas:
            print("No hay tareas.")
        else:
            for tarea in tareas:
                print(tarea)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Ejecución:**

```bash
python main.py -a "Terminar reporte"
python main.py -l
```

---

## 10. Preparación de Datos para Machine Learning

### Limpieza de datos con Pandas

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

### Guardar datos procesados

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

## 11. Bonus: Logging, Configuración y Manejo de Errores

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

### Archivo de configuración (`config.ini`)

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

### Manejo de errores

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

==============================================


# 🐍 Curso Práctico de Python para Gestión de Datos y Machine Learning

## Nivel 0 - Nivelación
## Tabla de Contenidos

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

## 1. Buenas Prácticas de Programación en Python (incluyendo `main`)

### ¿Por qué importa?

- Legibilidad
- Mantenibilidad
- Reusabilidad
- Evitar efectos secundarios al importar

### Recomendaciones

```python
# Buen ejemplo: uso de if __name__ == "__main__"
def saludar(nombre):
    return f"Hola, {nombre}!"

def main():
    nombre = input("Ingresa tu nombre: ")
    print(saludar(nombre))

if __name__ == "__main__":
    main()
```

### Consejos Adicionales

- Usa nombres descriptivos: `calcular_promedio()` en lugar de `calc()`
- Documenta funciones
- Divide en módulos y paquetes cuando crezca el proyecto

---

## 2. Entornos Virtuales: Definición y Justificación

### ¿Qué es un entorno virtual?

Un entorno virtual es un espacio aislado donde puedes instalar paquetes sin afectar el sistema global ni otros proyectos.

### ¿Por qué usarlo?

- Evita conflictos de versiones entre proyectos
- Facilita la replicabilidad (`requirements.txt`)
- Ideal para colaboración y despliegue

### Cómo crear uno

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

> **Tip**: Usa `pipenv` o `poetry` para gestión avanzada de dependencias.

---

## 3. Estructuras de Datos Básicas: Ventajas y Desventajas

| Estructura | Mutable | Ordenada | Duplicados | Uso típico | Ventajas | Desventajas |
|------------|---------|----------|------------|------------|----------|-------------|
| `list`     | ✅      | ✅       | ✅         | Secuencias | Dinámica, indexada | Lenta en búsquedas grandes |
| `tuple`    | ❌      | ✅       | ✅         | Datos inmutables | Rápida, segura | No modificable |
| `set`      | ✅      | ❌       | ❌         | Eliminar duplicados | Búsquedas O(1) | Sin orden, no indexado |
| `dict`     | ✅      | ✅ (3.7+) | ❌ claves  | Mapeos clave-valor | Acceso rápido por clave | Mayor consumo de memoria |

### Ejemplo práctico

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

## 4. Almacenamiento en Archivos Planos

### Escribir y leer archivos `.txt`

```python
# Escribir
with open("notas.txt", "w", encoding="utf-8") as f:
    f.write("Primera línea\nSegunda línea")

# Leer
with open("notas.txt", "r", encoding="utf-8") as f:
    contenido = f.read()
    print(contenido)
```

### CSV: Comma Separated Values

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

> Usa `csv.DictReader` y `csv.DictWriter` para trabajar con diccionarios.

---

## 5. Bases de Datos Relacionales (SQLite)

### ¿Por qué SQLite?

- Liviana, sin servidor
- Ideal para prototipos y aplicaciones pequeñas
- Soportada nativamente en Python

### Ejemplo práctico: CRUD básico

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

> Usa parámetros `?` para evitar inyecciones SQL.

---

## 6. Análisis de Datos con Pandas

### Instalación

```bash
pip install pandas matplotlib
```

### Ejemplo: Análisis de ventas

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

### Visualización rápida

```python
import matplotlib.pyplot as plt

df.groupby("Producto")["Ventas"].sum().plot(kind="bar")
plt.title("Ventas por Producto")
plt.show()
```

---

## 7. Gestión Avanzada de Archivos

### Recorrer directorios

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

### Comprimir y descomprimir

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

### Manejo de fechas en nombres de archivos

```python
from datetime import datetime

hoy = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre = f"backup_{hoy}.zip"
print(nombre)  # backup_20250405_103045.zip
```

---

## 8. Ejemplo Integrado: Sistema de Tareas

> Un sistema completo que usa archivos, SQLite, y buenas prácticas.

Estructura del proyecto:

```
sistema_tareas/
├── main.py
├── database.py
├── models.py
├── utils.py
└── tareas.db
```

### `models.py`

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

### `database.py`

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

### `main.py`

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
            print("Tarea agregada.")
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

## 9. Preparación de Datos para Machine Learning

### Limpieza de datos con Pandas

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

### Guardar datos procesados

```python
df.to_csv("datos_limpios.csv", index=False)

# Guardar scaler para usar en producción
import joblib
joblib.dump(scaler, "scaler.pkl")
```

### Estructura típica para ML

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

### Logging

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

### Archivo de configuración (`config.ini`)

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

### 🛡Manejo de errores

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
