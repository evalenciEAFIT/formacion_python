# Nivel 1: Manejo Avanzado de Datos
[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) |  
[Repositorio](https://github.com/evalenciEAFIT/formacion_python)

Este nivel cubre técnicas para trabajar con datos utilizando **SQL (SQLite)**, **Excel**, **archivos planos** y **Pandas**. Ideal para quienes ya dominan lo básico de Python.

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

## Cómo Usar
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/tu_usuario/formacion_python.git
   ```
2. Navega a `ML/nivel1` y ejecuta los ejercicios en orden.  
3. Consulta la teoría antes de resolver cada ejercicio.

## Ejemplos de Código
### Conexión a SQLite (ejercicio/sql/conexion_db.py):
```python
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('tienda.db')
cursor = conn.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    precio REAL
)
""")

# Insertar datos
cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", 
               ('Laptop', 1200.00))

# Guardar cambios
conn.commit()
conn.close()
```

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
