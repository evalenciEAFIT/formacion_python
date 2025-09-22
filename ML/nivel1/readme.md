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
# 1. SQL con SQLite

## 🔧 Comandos Básicos (Explicados Simply)

### 1.1. **Crear una Base de Datos**
```sql
-- Crea un archivo de base de datos (.db)
sqlite3 mi_base_de_datos.db
```
**Explicación:** Esto genera un archivo llamado `mi_base_de_datos.db` donde se guardarán tus tablas y datos.

---

### 1.2. **Crear Tablas**

### **Crear Tablas en SQLite: Sintaxis Básica**
La instrucción `CREATE TABLE` define la estructura de una tabla. Su formato general es:

```sql
CREATE TABLE nombre_tabla (
    columna1 tipo_dato restricciones,
    columna2 tipo_dato restricciones,
    ...
);
```

### **Tipos de Datos en SQLite**
SQLite utiliza **tipos dinámicos** (duck typing), pero recomienda usar estos tipos principales:

| Tipo       | Descripción                          | Ejemplo               |
|------------|--------------------------------------|-----------------------|
| **INTEGER** | Números enteros                      | `25`, `-10`           |
| **REAL**    | Números decimales                    | `3.14`, `-0.001`      |
| **TEXT**    | Cadenas de texto                     | `'Juan'`, `'Hola'`    |
| **BLOB**    | Datos binarios (imágenes, archivos) | Datos crudos          |
| **NUMERIC** | Números con precisión fija           | `123.45`              |


###  **restricciones (Reglas Adicionales)**
Los restricciones definen reglas para los datos:

| Constraint       | Descripción                                  | Ejemplo                     |
|------------------|---------------------------------------------|----------------------------|
| `PRIMARY KEY`    | Identificador único (no repetible)           | `id INTEGER PRIMARY KEY`   |
| `AUTOINCREMENT`  | ID se genera automáticamente                | `id INTEGER PRIMARY KEY AUTOINCREMENT` |
| `NOT NULL`       | Campo obligatorio                           | `nombre TEXT NOT NULL`     |
| `UNIQUE`         | Valor único en toda la tabla                | `email TEXT UNIQUE`        |
| `CHECK`          | Validación personalizada                     | `edad INTEGER CHECK(edad >= 18)` |
| `DEFAULT`        | Valor predeterminado si no se especifica    | `estado TEXT DEFAULT 'activo'` |


### **Ejemplo: Crear Tabla de Productos**
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL CHECK(precio > 0),
    stock INTEGER DEFAULT 0,
    fecha_vencimiento DATE
);
```

#### Explicación:
1. **`id`**: Identificador único autoincremental.
2. **`nombre`**: Texto obligatorio (no puede estar vacío).
3. **`precio`**: Número decimal mayor a 0.
4. **`stock`**: Entero con valor predeterminado `0`.
5. **`fecha_vencimiento`**: Fecha en formato `YYYY-MM-DD`.

### **Buenas Prácticas**
- Usa nombres descriptivos para tablas y columnas.
- Define restricciones para mantener la integridad de datos.
- Documenta la estructura de tu base de datos.


---

-------------------
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identificador único automático
    nombre TEXT NOT NULL,                   -- Nombre del producto (obligatorio)
    precio REAL CHECK(precio > 0),          -- Precio (debe ser positivo)
    categoria TEXT DEFAULT 'General'       -- Categoría (por defecto "General")
);
```
**Explicación:** Creamos una tabla llamada `productos` con 4 columnas:
- `id`: Número único para cada producto (se incrementa solo).
- `nombre`: Texto obligatorio (no puede estar vacío).
- `precio`: Número decimal que debe ser mayor a 0.
- `categoria`: Texto con valor predeterminado "General".

---

### 1.3. **Insertar Datos**
```sql
INSERT INTO productos (nombre, precio, categoria)
VALUES ('Laptop', 1200.00, 'Electrónica');
```
**Explicación:** Agregamos un nuevo producto a la tabla `productos`. Especificamos los valores para `nombre`, `precio` y `categoria`.

---

### 1.4. **Consultar Datos (SELECT)**
```sql
-- Ver todos los productos
SELECT * FROM productos;

-- Filtrar productos baratos
SELECT nombre, precio FROM productos WHERE precio < 500;

-- Ordenar por precio descendente
SELECT * FROM productos ORDER BY precio DESC;
```
**Explicación:**
- `SELECT *`: Trae todas las columnas.
- `WHERE precio < 500`: Solo muestra productos con precio menor a $500.
- `ORDER BY precio DESC`: Ordena de mayor a menor precio.

### 2. **Agrupación con `GROUP BY`**
```sql
SELECT categoria, COUNT(*) AS total_productos 
FROM productos 
GROUP BY categoria;
```
**Explicación:** Cuenta cuántos productos hay en cada categoría (ej: 3 en "Electrónica", 2 en "Accesorios").

---

### 3. **Unir Tablas (JOIN)**
```sql
SELECT p.nombre, pr.proveedor 
FROM productos p
INNER JOIN proveedores pr ON p.id = pr.producto_id;
```
**Explicación:** Combina información de dos tablas:
- `productos` (p) y `proveedores` (pr).
- Une filas donde `producto_id` coincide.

---

### 4. **Actualizar y Eliminar**
```sql
-- Cambiar precio de una laptop
UPDATE productos SET precio = 1150.00 WHERE nombre = 'Laptop';

-- Borrar productos baratos
DELETE FROM productos WHERE precio < 100;
```
**Explicación:**
- `UPDATE`: Modifica datos existentes.
- `DELETE`: Borra registros que cumplan una condición.

---

## 💻 Código Python Simplificado

### Conectar a la Base de Datos
```python
import sqlite3

# Crea/conecta a la base de datos
conexion = sqlite3.connect('mi_base_de_datos.db')  
print("Base de datos conectada")
```

### Crear una Tabla
```python
cursor = conexion.cursor()

# Crea tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    precio REAL
)
''')
```

### Insertar Datos Seguros
```python
# Usamos parámetros para evitar errores
datos = ('Mouse', 25.50)
cursor.execute('INSERT INTO productos (nombre, precio) VALUES (?, ?)', datos)
```

### Consultar Datos
```python
# Obtener todos los productos
cursor.execute('SELECT * FROM productos')
productos = cursor.fetchall()  

# Mostrar resultados
for producto in productos:
    print(f"Producto: {producto[1]}, Precio: ${producto[2]}")
```

---

## ✅ Consejos Clave
1. **Seguridad:** Siempre usa parámetros (`?`) en Python para evitar inyecciones SQL.
2. **Practica:** Crea tablas pequeñas y prueba consultas gradualmente.
3. **Documenta:** Comenta tu código para entenderlo luego.

¡Empieza con ejemplos sencillos y ve complejizando! 🚀


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
