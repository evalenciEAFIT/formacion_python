# Nivel 1: Manejo Avanzado de Datos
[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Repositorio](https://github.com/evalenciEAFIT/formacion_python)

Este nivel cubre técnicas para trabajar con datos utilizando **SQL (SQLite)**, **Excel**, **archivos planos** y **Pandas**..

## Temas Incluidos
1. **SQL con SQLite**:  
   - Conexión a bases de datos, creación de tablas, inserción/consulta de datos.  
   - Consultas complejas (JOIN, GROUP BY, subconsultas).  

2. **Manejo de Excel**:  
   - Lectura/escritura de archivos `.xlsx`.  
   - Manipulación de hojas y celdas.  

3. **Archivos Planos**:  
   - Trabajo con CSV, TXT y JSON.  
   - Formateo y validación de datos.  

4. **Pandas**:  
   - Estructuras de datos (Series, DataFrames).  
   - Limpieza, transformación y análisis estadístico.  

## Requisitos
- Haber completado el [Nivel 0](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0).  
- Instalar dependencias: `pip install pandas openpyxl sqlite3`.


## Ejemplos de Código
-----------------
# SQL

## 🔧 Comandos Básicos
### 1. **Crear una Base de Datos**
```sql
-- Crea una nueva base de datos (se genera automáticamente al conectarse)
sqlite3 mi_base_de_datos.db
```

```python
# Python: Conectar a una base de datos (crea el archivo si no existe)
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
print("Base de datos creada exitosamente")
conexion.close()
```
---
### 2. **Crear Tablas**
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL CHECK(precio > 0),
    categoria TEXT DEFAULT 'General'
);
```

```python
# Python: Crear una tabla
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
cursor = conexion.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL CHECK(precio > 0),
    categoria TEXT DEFAULT 'General'
)
''')

conexion.commit()  # Guardar cambios
conexion.close()
print("Tabla 'productos' creada")
```

---

### 3. **Insertar Datos**
```sql
INSERT INTO productos (nombre, precio, categoria)
VALUES ('Laptop', 1200.00, 'Electrónica');
```

```python
# Python: Insertar datos (usando parámetros para evitar inyección SQL)
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
cursor = conexion.cursor()

datos = ('Laptop', 1200.00, 'Electrónica')
cursor.execute('''
INSERT INTO productos (nombre, precio, categoria)
VALUES (?, ?, ?)
''', datos)

conexion.commit()
conexion.close()
print("Dato insertado correctamente")
```

---

### 4. **Consultar Datos (SELECT)**
```sql
-- Seleccionar todas las columnas
SELECT * FROM productos;

-- Filtrar resultados
SELECT nombre, precio FROM productos WHERE precio < 500;

-- Ordenar resultados
SELECT * FROM productos ORDER BY precio DESC;
```

```python
# Python: Consultar datos
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
cursor = conexion.cursor()

# 1. Seleccionar todas las columnas
cursor.execute('SELECT * FROM productos')
todos_los_productos = cursor.fetchall()
print("Todos los productos:", todos_los_productos)

# 2. Filtrar resultados
cursor.execute('SELECT nombre, precio FROM productos WHERE precio < ?', (500,))
productos_baratos = cursor.fetchall()
print("Productos baratos:", productos_baratos)

# 3. Ordenar resultados
cursor.execute('SELECT * FROM productos ORDER BY precio DESC')
productos_ordenados = cursor.fetchall()
print("Productos ordenados por precio:", productos_ordenados)

conexion.close()
```

---

## ⚡ Consultas Avanzadas

### 1. **Filtrado con `WHERE`**
```sql
SELECT * FROM productos 
WHERE categoria = 'Electrónica' AND precio BETWEEN 800 AND 1500;
```

```python
# Python: Filtrado avanzado
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
cursor = conexion.cursor()

cursor.execute('''
SELECT * FROM productos 
WHERE categoria = ? AND precio BETWEEN ? AND ?
''', ('Electrónica', 800, 1500))

resultado = cursor.fetchall()
print("Productos electrónicos entre $800-$1500:", resultado)

conexion.close()
```

---

### 2. **Agrupación con `GROUP BY`**
```sql
SELECT categoria, COUNT(*) AS total_productos 
FROM productos 
GROUP BY categoria;
```

```python
# Python: Agrupación con GROUP BY
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
cursor = conexion.cursor()

cursor.execute('''
SELECT categoria, COUNT(*) AS total_productos 
FROM productos 
GROUP BY categoria
''')

for categoria, total in cursor.fetchall():
    print(f"Categoría '{categoria}': {total} productos")

conexion.close()
```

---

### 3. **Unir Tablas (JOIN)**
```sql
SELECT p.nombre, pr.proveedor 
FROM productos p
INNER JOIN proveedores pr ON p.id = pr.producto_id;
```

```python
# Python: JOIN entre tablas
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
cursor = conexion.cursor()

cursor.execute('''
SELECT p.nombre, pr.proveedor 
FROM productos p
INNER JOIN proveedores pr ON p.id = pr.producto_id
''')

for nombre, proveedor in cursor.fetchall():
    print(f"{nombre} - Proveedor: {proveedor}")

conexion.close()
```

---

### 4. **Actualizar y Eliminar**
```sql
-- Actualizar registros
UPDATE productos SET precio = 1150.00 WHERE nombre = 'Laptop';

-- Eliminar registros
DELETE FROM productos WHERE precio < 100;
```

```python
# Python: Actualizar y eliminar datos
import sqlite3

conexion = sqlite3.connect('mi_base_de_datos.db')
cursor = conexion.cursor()

# Actualizar
cursor.execute('''
UPDATE productos SET precio = ? WHERE nombre = ?
''', (1150.00, 'Laptop'))
conexion.commit()

# Eliminar
cursor.execute('DELETE FROM productos WHERE precio < ?', (100,))
conexion.commit()

print("Datos actualizados/eliminados")
conexion.close()
```

---

## 💻 Ejecución Completa desde Python
```python
import sqlite3

def main():
    # Conectar a la base de datos
    conexion = sqlite3.connect('tienda.db')
    cursor = conexion.cursor()
    
    # Crear tabla (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL CHECK(precio > 0),
        categoria TEXT DEFAULT 'General'
    )
    ''')
    
    # Insertar datos de ejemplo
    datos = [
        ('Laptop', 1200.00, 'Electrónica'),
        ('Mouse', 25.50, 'Accesorios'),
        ('Teclado', 45.99, 'Accesorios')
    ]
    
    cursor.executemany('INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)', datos)
    
    # Consultar todos los productos
    cursor.execute('SELECT * FROM productos')
    for fila in cursor.fetchall():
        print(fila)
    
    # Cerrar conexión
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    main()
```

---

## ✅ Práctica Recomendada
1. **Crear un sistema de inventario** con tablas `productos`, `proveedores`, y `ventas`.
2. **Implementar consultas** para:
   - Listar productos con stock bajo.
   - Calcular ingresos totales por categoría.
   - Generar reportes mensuales de ventas.

---

¡Experimenta con estos ejemplos y combina varias consultas para resolver problemas reales! 🚀
-----------------





### Leer Excel con Pandas (ejercicio/excel/leer_excel.py):
```python
import pandas as pd

# Leer archivo Excel
df = pd.read_excel('empleados.xlsx', sheet_name='Hoja1')

# Mostrar primeras filas
print(df.head())
```

---

¡Empieza practicando con los ejercicios y consulta la teoría cuando necesites refuerzo!
```

---

### Pasos para Implementar:
1. **Crea la estructura de carpetas** en tu repositorio local.  
2. **Agrega los archivos de ejercicios y teoría** con ejemplos funcionales.  
3. **Incluye datasets de muestra** en `recursos/datasets/` (ej: `ventas.csv`).  
4. **Sube todo a GitHub** manteniendo la ruta `formacion_python/ML/nivel1`.  

Esta estructura permite un aprendizaje progresivo, combinando teoría con ejercicios prácticos. ¡Listo para empezar! 🚀
