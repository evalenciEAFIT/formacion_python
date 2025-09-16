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

# ELIMINAR: Borrar tarea por ID
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

### 8.0.  Manejo de fechas en nombres de archivos

```python
from datetime import datetime

hoy = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre = f"backup_{hoy}.zip"
print(nombre)  # backup_20250405_103045.zip
```


###  8.1. Recorrer Directorios (con `pathlib` — forma moderna y recomendada)

###  Ejemplo: `listar_csv_en_directorio.py`

```python
from pathlib import Path

def listar_archivos_csv(ruta_directorio="datasets"):
    """
    Lista todos los archivos .csv en un directorio.
    Si el directorio no existe, lo crea vacío.
    """
    directorio = Path(ruta_directorio)
    
    # Crear directorio si no existe
    directorio.mkdir(exist_ok=True)
    print(f" Buscando archivos CSV en: '{directorio.absolute()}'\n")

    # Obtener todos los .csv
    archivos_csv = list(directorio.glob("*.csv"))
    
    if not archivos_csv:
        print(" No se encontraron archivos .csv")
        return []

    print(f" Encontrados {len(archivos_csv)} archivos CSV:")
    print("-" * 50)
    for i, archivo in enumerate(archivos_csv, 1):
        # archivo.name → solo nombre
        # archivo.stem → nombre sin extensión
        # archivo.suffix → extensión
        print(f"{i:2}. {archivo.name} (Tamaño: {archivo.stat().st_size} bytes)")

    return archivos_csv

#  Ejecutar ejemplo
if __name__ == "__main__":
    listar_archivos_csv()
```

###  Salida esperada (si tienes `ventas.csv`, `personas.csv`):

```
 Buscando archivos CSV en: 'C:\tu_proyecto\datasets'

 Encontrados 2 archivos CSV:
--------------------------------------------------
 1. ventas.csv (Tamaño: 128 bytes)
 2. personas.csv (Tamaño: 85 bytes)
```

---

###  8.2. Crear Directorios (con estructura anidada)

###  Ejemplo: `crear_estructura_proyecto.py`

```python
from pathlib import Path

def crear_estructura_datos():
    """
    Crea una estructura típica para gestión de datos.
    """
    estructura = [
        "data/raw",
        "data/processed",
        "data/external",
        "backups",
        "logs",
        "exports"
    ]

    print("Creando estructura de directorios...")
    for carpeta in estructura:
        Path(carpeta).mkdir(parents=True, exist_ok=True)
        print(f" {carpeta}/ creado")

    print("\n Estructura final:")
    for item in Path(".").glob("data*/"):
        print(f"  └── {item}")
```

###  Salida esperada:

```
Creando estructura de directorios...
 data/raw/ creado
 data/processed/ creado
 data/external/ creado
 backups/ creado
 logs/ creado
 exports/ creado

 Estructura final:
  └── data/
```

---

###  8.3. Comprimir Archivos en ZIP (con manejo de errores)

###  Ejemplo: `comprimir_csvs.py`

```python
from pathlib import Path
import zipfile
from datetime import datetime

def comprimir_archivos_csv(origen="datasets", destino="backups"):
    """
    Comprime todos los .csv de un directorio en un ZIP con timestamp.
    """
    directorio_origen = Path(origen)
    directorio_destino = Path(destino)
    
    # Crear directorio de destino
    directorio_destino.mkdir(exist_ok=True)

    # Buscar CSVs
    archivos_csv = list(directorio_origen.glob("*.csv"))
    if not archivos_csv:
        print(f"⚠ No hay archivos .csv en '{origen}' para comprimir.")
        return None

    # Nombre con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_zip = directorio_destino / f"backup_csv_{timestamp}.zip"

    print(f" Creando backup: {nombre_zip.name}")
    print("-" * 50)

    try:
        with zipfile.ZipFile(nombre_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for archivo in archivos_csv:
                zf.write(archivo, arcname=archivo.name)  # arcname evita rutas largas
                print(f"   + {archivo.name} ({archivo.stat().st_size} bytes)")

        print(f"\n ¡Compresión exitosa! Tamaño total: {nombre_zip.stat().st_size} bytes")
        return nombre_zip

    except Exception as e:
        print(f" Error al comprimir: {e}")
        return None

# Ejecutar ejemplo
if __name__ == "__main__":
    comprimir_archivos_csv()
```

###  Salida esperada:

```
Creando backup: backup_csv_20250504_123045.zip
--------------------------------------------------
   + ventas.csv (128 bytes)
   + personas.csv (85 bytes)

¡Compresión exitosa! Tamaño total: 427 bytes
```


### 8.4. Descomprimir Archivos ZIP (con manejo de errores y limpieza)

###  Ejemplo: `descomprimir_backup.py`

```python
from pathlib import Path
import zipfile

def descomprimir_zip(ruta_zip, destino="restaurado"):
    """
    Descomprime un archivo .zip en una carpeta específica.
    """
    archivo_zip = Path(ruta_zip)
    directorio_destino = Path(destino)

    # Verificar que el ZIP existe
    if not archivo_zip.exists():
        print(f" El archivo {ruta_zip} no existe.")
        return False

    # Crear carpeta de destino
    directorio_destino.mkdir(exist_ok=True)

    try:
        with zipfile.ZipFile(archivo_zip, "r") as zf:
            print(f" Descomprimiendo {archivo_zip.name} en '{directorio_destino}/'...")
            zf.extractall(directorio_destino)
            
            # Listar archivos extraídos
            extraidos = list(directorio_destino.iterdir())
            print(f" {len(extraidos)} archivos extraídos:")
            for archivo in extraidos:
                print(f"   - {archivo.name}")
                
        return True

    except zipfile.BadZipFile:
        print(" El archivo no es un ZIP válido.")
        return False
    except Exception as e:
        print(f" Error al descomprimir: {e}")
        return False

#  Ejecutar ejemplo
if __name__ == "__main__":
    # Suponiendo que ya ejecutaste el ejemplo anterior y generaste un .zip
    backups = list(Path("backups").glob("*.zip"))
    if backups:
        ultimo_backup = sorted(backups)[-1]  # el más reciente
        descomprimir_zip(ultimo_backup, "datos_restaurados")
    else:
        print(" No hay backups disponibles para restaurar.")
```

### Salida esperada:

```
 Descomprimiendo backup_csv_20250504_123045.zip en 'datos_restaurados/'...
 2 archivos extraídos:
   - ventas.csv
   - personas.csv
```

---

### 8.5. Bonus: Copiar, Mover y Eliminar Archivos

### Ejemplo: `gestion_archivos_bonus.py`

```python
from pathlib import Path
import shutil

def copiar_csv_a_procesados(origen="datasets", destino="data/processed"):
    """Copia todos los .csv al directorio 'processed'."""
    Path(destino).mkdir(parents=True, exist_ok=True)
    
    for csv in Path(origen).glob("*.csv"):
        destino_path = Path(destino) / csv.name
        shutil.copy2(csv, destino_path)  # copy2 copia también metadatos
        print(f" Copiado: {csv.name} → {destino_path}")

def mover_csv_a_raw(origen="datasets", destino="data/raw"):
    """Mueve (no copia) los CSVs al directorio 'raw'."""
    Path(destino).mkdir(parents=True, exist_ok=True)
    
    for csv in Path(origen).glob("*.csv"):
        destino_path = Path(destino) / csv.name
        shutil.move(csv, destino_path)
        print(f" Movido: {csv.name} → {destino_path}")

def limpiar_directorio_vacio(ruta):
    """Elimina un directorio si está vacío."""
    carpeta = Path(ruta)
    if carpeta.exists() and not any(carpeta.iterdir()):
        carpeta.rmdir()
        print(f" Directorio vacío eliminado: {ruta}")
```


### Ejecución Recomendada (para probar todo en orden)

Crea un script `ejecutar_gestion_archivos.py`:

```python
from pathlib import Path

# 1. Crear estructura
from crear_estructura_proyecto import crear_estructura_datos
crear_estructura_datos()

print("\n" + "="*60 + "\n")

# 2. Listar CSVs
from listar_csv_en_directorio import listar_archivos_csv
listar_archivos_csv()

print("\n" + "="*60 + "\n")

# 3. Comprimir
from comprimir_csvs import comprimir_archivos_csv
zip_creado = comprimir_archivos_csv()

print("\n" + "="*60 + "\n")

# 4. Descomprimir
if zip_creado:
    from descomprimir_backup import descomprimir_zip
    descomprimir_zip(zip_creado, "datos_restaurados")

print("\n" + "="*60 + "\n")

# 5. Copiar a processed
from gestion_archivos_bonus import copiar_csv_a_procesados
copiar_csv_a_procesados()
```
---

### Estructura Final del Proyecto

```
gestion_archivos/
├── datasets/
│   ├── ventas.csv
│   └── personas.csv
├── listar_csv_en_directorio.py
├── crear_estructura_proyecto.py
├── comprimir_csvs.py
├── descomprimir_backup.py
├── gestion_archivos_bonus.py
└── ejecutar_gestion_archivos.py  ← ¡Ejecuta todo en orden!
```

---

## 9. Ejemplo Integrado: Sistema de Tareas

> Un sistema modular, profesional y listo para usar, con SQLite, CLI, logging, validación y buenas prácticas.

---
## 📥 ¿Cómo empezar?

1. Crea la carpeta `sistema_tareas/`
2. Guarda los 4 archivos: `main.py`, `database.py`, `models.py`, `utils.py`
3. Ejecuta:

```bash
python main.py -h
```
---
## 📁 Estructura del Proyecto (Actualizada)

```
sistema_tareas/
├── main.py          ← CLI principal (mejorado)
├── database.py      ← CRUD completo + migraciones
├── models.py        ← Clase Tarea
├── utils.py         ← ¡AHORA INCLUIDO! (validación, logging, ayuda)
└── tareas.db        ← se crea automáticamente
```

---

## 📄 1. `models.py` — Clase Tarea (sin cambios, pero completo)

```python
class Tarea:
    def __init__(self, id, titulo, completada=False):
        self.id = id
        self.titulo = titulo
        self.completada = bool(completada)  # Asegura tipo booleano

    def __str__(self):
        estado = "✅" if self.completada else "❌"
        return f"{self.id:2}. {self.titulo:<30} {estado}"

    def __repr__(self):
        return f"Tarea(id={self.id}, titulo='{self.titulo}', completada={self.completada})"
```

---

## 📄 2. `database.py` — CRUD Completo + Migraciones

```python

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from models import Tarea  # ✅ ¡IMPORTANTE! Sin esto, 'Tarea' no existe

@contextmanager
def obtener_conexion(db_path="tareas.db"):
    """Gestiona conexión segura a la base de datos."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    except sqlite3.Error as e:
        print(f"❌ Error en la base de datos: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def crear_tabla():
    """Crea la tabla si no existe."""
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

def agregar_columna_fecha_si_no_existe():
    """Agrega columna 'fecha_creacion' si no existe (migración)."""
    with obtener_conexion() as conn:
        cursor = conn.execute("PRAGMA table_info(tareas)")
        columnas = [col[1] for col in cursor.fetchall()]
        if "fecha_creacion" not in columnas:
            conn.execute("ALTER TABLE tareas ADD COLUMN fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()

class TareaDB:
    def __init__(self, db_path="tareas.db"):
        self.db_path = db_path
        Path(db_path).touch(exist_ok=True)  # Crea archivo si no existe
        crear_tabla()
        agregar_columna_fecha_si_no_existe()

    def agregar(self, titulo):
        with obtener_conexion(self.db_path) as conn:
            cursor = conn.execute("INSERT INTO tareas (titulo) VALUES (?)", (titulo,))
            conn.commit()
            return cursor.lastrowid

    def listar(self):
        with obtener_conexion(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, titulo, completada 
                FROM tareas 
                ORDER BY id DESC
            """)
            # ✅ Ahora 'Tarea' está definido gracias al import
            return [Tarea(row["id"], row["titulo"], row["completada"]) for row in cursor.fetchall()]

    def completar(self, id_tarea):
        with obtener_conexion(self.db_path) as conn:
            cursor = conn.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (id_tarea,))
            conn.commit()
            return cursor.rowcount > 0

    def eliminar(self, id_tarea):
        with obtener_conexion(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM tareas WHERE id = ?", (id_tarea,))
            conn.commit()
            return cursor.rowcount > 0

    def buscar(self, palabra):
        with obtener_conexion(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT id, titulo, completada FROM tareas WHERE titulo LIKE ?",
                (f"%{palabra}%",)
            )
            return [Tarea(row["id"], row["titulo"], row["completada"]) for row in cursor.fetchall()]

```

---

## 📄 3. `utils.py` — ¡FINALMENTE INCLUIDO! ✅

```python
import logging
import argparse

def configurar_logging(nivel=logging.INFO):
    """Configura el sistema de logging para la aplicación."""
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("sistema_tareas.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def validar_titulo(titulo):
    """Valida que el título no esté vacío y tenga longitud razonable."""
    if not titulo or not titulo.strip():
        raise ValueError("❌ El título no puede estar vacío.")
    if len(titulo) > 200:
        raise ValueError("❌ El título es demasiado largo (máx. 200 caracteres).")
    return titulo.strip()

def mostrar_ayuda_personalizada():
    """Muestra una ayuda amigable con emojis y ejemplos."""
    ayuda = """
🌟 SISTEMA DE GESTIÓN DE TAREAS 🌟

Uso:
  python main.py [OPCIÓN]

Opciones:
  -a, --agregar TEXTO     ➕ Agregar nueva tarea
  -l, --listar            📋 Listar todas las tareas
  -c, --completar ID      ✅ Marcar tarea como completada
  -e, --eliminar ID       🗑️  Eliminar tarea por ID
  -b, --buscar PALABRA    🔍 Buscar tareas por palabra clave
  -v, --verbose           📢 Modo detallado (muestra logs)
  -h, --help              ❓ Mostrar esta ayuda

Ejemplos:
  python main.py -a "Estudiar Python"
  python main.py -l
  python main.py -c 1
  python main.py -b "Python"
"""
    print(ayuda)
```

---

## 📄 4. `main.py` — CLI Completo y Mejorado

```python
import argparse
from database import TareaDB
from models import Tarea
from utils import configurar_logging, validar_titulo, mostrar_ayuda_personalizada
import logging

def main():
    parser = argparse.ArgumentParser(add_help=False)  # Desactivamos ayuda automática
    parser.add_argument("--agregar", "-a", type=str, help="Agregar nueva tarea")
    parser.add_argument("--listar", "-l", action="store_true", help="Listar tareas")
    parser.add_argument("--completar", "-c", type=int, help="Completar tarea por ID")
    parser.add_argument("--eliminar", "-e", type=int, help="Eliminar tarea por ID")
    parser.add_argument("--buscar", "-b", type=str, help="Buscar tareas por palabra clave")
    parser.add_argument("--verbose", "-v", action="store_true", help="Modo detallado")
    parser.add_argument("--help", "-h", action="store_true", help="Mostrar ayuda")

    args = parser.parse_args()

    # Configurar logging
    nivel = logging.INFO if args.verbose else logging.WARNING
    configurar_logging(nivel)

    # Mostrar ayuda personalizada
    if args.help:
        mostrar_ayuda_personalizada()
        return

    # Inicializar base de datos
    db = TareaDB()

    try:
        if args.agregar:
            titulo = validar_titulo(args.agregar)
            id_nueva = db.agregar(titulo)
            print(f"✅ Tarea agregada con ID {id_nueva}: '{titulo}'")
            logging.info(f"Tarea agregada: ID {id_nueva}, '{titulo}'")

        elif args.listar:
            tareas = db.listar()
            if not tareas:
                print("📭 No hay tareas registradas.")
            else:
                print(f"\n📋 LISTA DE TAREAS ({len(tareas)}):")
                print("=" * 60)
                for tarea in tareas:
                    print(tarea)
                print("=" * 60)

        elif args.completar is not None:
            if db.completar(args.completar):
                print(f"✅ Tarea ID {args.completar} marcada como completada.")
                logging.info(f"Tarea completada: ID {args.completar}")
            else:
                print(f"⚠️  No se encontró tarea con ID {args.completar}.")

        elif args.eliminar is not None:
            if db.eliminar(args.eliminar):
                print(f"🗑️  Tarea ID {args.eliminar} eliminada.")
                logging.info(f"Tarea eliminada: ID {args.eliminar}")
            else:
                print(f"⚠️  No se encontró tarea con ID {args.eliminar}.")

        elif args.buscar:
            resultados = db.buscar(args.buscar)
            if not resultados:
                print(f"🔍 No se encontraron tareas con '{args.buscar}'.")
            else:
                print(f"\n🔎 RESULTADOS PARA '{args.buscar}' ({len(resultados)}):")
                print("=" * 60)
                for tarea in resultados:
                    print(tarea)
                print("=" * 60)

        else:
            mostrar_ayuda_personalizada()

    except ValueError as ve:
        print(ve)
        logging.error(f"Error de validación: {ve}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        logging.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
```

---

## 🧪 Ejecución y Salidas Esperadas

### ➕ Agregar tarea

```bash
python main.py -a "Aprender Pandas"
```
```
✅ Tarea agregada con ID 1: 'Aprender Pandas'
```

### 📋 Listar tareas

```bash
python main.py -l
```
```
📋 LISTA DE TAREAS (2):
============================================================
 1. Aprender Pandas                     ✅
 2. Hacer ejercicio                     ❌
============================================================
```

### ✅ Completar tarea

```bash
python main.py -c 2
```
```
✅ Tarea ID 2 marcada como completada.
```

### 🗑️ Eliminar tarea

```bash
python main.py -e 1
```
```
🗑️  Tarea ID 1 eliminada.
```

### 🔍 Buscar tarea

```bash
python main.py -b "Pandas"
```
```
🔎 RESULTADOS PARA 'Pandas' (1):
============================================================
 3. Aprender Pandas                     ✅
============================================================
```

### ❓ Mostrar ayuda

```bash
python main.py -h
```
```
🌟 SISTEMA DE GESTIÓN DE TAREAS 🌟

Uso:
  python main.py [OPCIÓN]

Opciones:
  -a, --agregar TEXTO     ➕ Agregar nueva tarea
  -l, --listar            📋 Listar todas las tareas
  -c, --completar ID      ✅ Marcar tarea como completada
  -e, --eliminar ID       🗑️  Eliminar tarea por ID
  -b, --buscar PALABRA    🔍 Buscar tareas por palabra clave
  -v, --verbose           📢 Modo detallado (muestra logs)
  -h, --help              ❓ Mostrar esta ayuda

Ejemplos:
  python main.py -a "Estudiar Python"
  python main.py -l
  python main.py -c 1
  python main.py -b "Python"
```

---

## 📄 Archivo de Log Generado (`sistema_tareas.log`)

```
2025-05-04 14:30:45,123 - INFO - Tarea agregada: ID 1, 'Aprender Pandas'
2025-05-04 14:31:10,456 - INFO - Tarea completada: ID 2
2025-05-04 14:32:05,789 - INFO - Tarea eliminada: ID 1
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

