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

## Comandos Básicos (Explicados Simply)

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


###  **Restricciones (Reglas Adicionales)**
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


## Ejemplo completo

```python
import sqlite3  # 1️⃣ Importamos el módulo para conectar con SQLite

# ========================================
# PASO 1: Conectar a la base de datos
# ========================================
# Creamos una conexión a la base de datos 'tienda.db'
# Si el archivo no existe, SQLite lo crea automáticamente
conexion = sqlite3.connect('tienda.db')  
cursor = conexion.cursor()  # Objeto para ejecutar comandos SQL

print("✅ Conexión establecida con 'tienda.db'")

# ========================================
# PASO 2: Crear la tabla con restricciones
# ========================================
# Usamos execute() para enviar el comando SQL
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 👉 Clave única autoincremental
    nombre TEXT NOT NULL,                 -- 👉 Texto obligatorio (no puede ser NULL)
    precio REAL CHECK(precio > 0),         -- 👉 Número real > 0 (evita precios negativos)
    stock INTEGER DEFAULT 0,              -- 👉 Entero con valor predeterminado 0
    fecha_vencimiento DATE                 -- 👉 Fecha en formato AAAA-MM-DD
)
''')

print("✅ Tabla 'productos' creada con éxito!")

# ========================================
# PASO 3: Verificar la estructura (opcional)
# ========================================
# Podemos inspeccionar la tabla para confirmar
cursor.execute("PRAGMA table_info(productos)")
columnas = cursor.fetchall()

print("\n📋 Estructura de la tabla:")
for col in columnas:
    print(f"- {col[1]} ({col[2]})")  # Muestra nombre y tipo de dato

# ========================================
# PASO 4: Guardar cambios y cerrar
# ========================================
conexion.commit()  # ⚠️ ¡Crucial! Confirma los cambios en la base de datos
conexion.close()   # Cierra la conexión para liberar recursos

print("\n🔒 Conexión cerrada. ¡Todo listo!")
```

---

### Explicación Detallada:
1. **Importar SQLite**  
   ```python
   import sqlite3
   ```
   - Necesario para interactuar con bases de datos SQLite.

2. **Conectar a la base de datos**  
   ```python
   conexion = sqlite3.connect('tienda.db')
   cursor = conexion.cursor()
   ```
   - `connect()` crea o abre el archivo `tienda.db`.
   - `cursor` es como un "puntero" para ejecutar comandos SQL.

3. **Crear la tabla**  
   ```python
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS productos (...);
   ''')
   ```
   - `IF NOT EXISTS`: Evita errores si la tabla ya existe.
   - Restricciones clave:
     - `PRIMARY KEY AUTOINCREMENT`: IDs únicos automáticos.
     - `NOT NULL`: Campo obligatorio (no puede quedar vacío).
     - `CHECK(precio > 0)`: Valida que el precio sea positivo.
     - `DEFAULT 0`: Si no se especifica `stock`, usa `0`.

4. **Verificar la estructura**  
   ```python
   cursor.execute("PRAGMA table_info(productos)")
   ```
   - `PRAGMA` es un comando especial de SQLite para obtener metadatos.
   - Muestra detalles de cada columna (nombre, tipo, restricciones).

5. **Guardar y cerrar**  
   ```python
   conexion.commit()  # Guarda los cambios
   conexion.close()   # Libera memoria
   ```

---

### 🚀 Resultado Al Ejecutar:
```
✅ Conexión establecida con 'tienda.db'
✅ Tabla 'productos' creada con éxito!

📋 Estructura de la tabla:
- id (INTEGER)
- nombre (TEXT)
- precio (REAL)
- stock (INTEGER)
- fecha_vencimiento (DATE)

🔒 Conexión cerrada. ¡Todo listo!
```

---

### 1.3. **Insertar Datos**
### **Estructura de `INSERT INTO`**

La sentencia `INSERT INTO` se usa para **agregar nuevos registros (filas) a una tabla**. Su estructura básica es:

```sql
INSERT INTO nombre_tabla (columna1, columna2, ...)
VALUES (valor1, valor2, ...);
```

### **Desglose del Ejemplo**
```sql
INSERT INTO productos (nombre, precio, categoria)
VALUES ('Laptop', 1200.00, 'Electrónica');
```

1. **`INSERT INTO productos`**  
   - Indica que vamos a insertar datos en la tabla llamada `productos`.

2. **`(nombre, precio, categoria)`**  
   - Lista las **columnas** donde queremos insertar datos.  
   - Deben coincidir exactamente con las columnas definidas en la tabla.

3. **`VALUES ('Laptop', 1200.00, 'Electrónica')`**  
   - Proporciona los **valores** para cada columna en el mismo orden:  
     - `'Laptop'` → Valor para la columna `nombre` (texto).  
     - `1200.00` → Valor para la columna `precio` (número decimal).  
     - `'Electrónica'` → Valor para la columna `categoria` (texto).


### **Reglas Importantes**
1. **Orden de Columnas**  
   Los valores deben ir en el **mismo orden** que las columnas especificadas.  
   Ejemplo correcto:  
   ```sql
   INSERT INTO productos (nombre, precio) VALUES ('Mouse', 25.50);  -- Correcto
   ```
   Ejemplo incorrecto:  
   ```sql
   INSERT INTO productos (nombre, precio) VALUES (25.50, 'Mouse');  -- Error!
   ```

2. **Tipos de Datos**  
   Los valores deben coincidir con el tipo de dato de la columna:  
   - Texto → Entre comillas simples (`' '`).  
   - Números → Sin comillas.  
   - Fechas → Formato `'YYYY-MM-DD'`.

3. **Columnas Opcionales**  
   Si omites columnas, debes:  
   - Usar `DEFAULT` en la definición de la tabla, o  
   - Permitir `NULL` (si la columna no es `NOT NULL`).

---

### **Insertar Múltiples Registros**
Puedes insertar varios registros a la vez:

```sql
INSERT INTO productos (nombre, precio, categoria)
VALUES 
  ('Mouse', 25.50, 'Accesorios'),
  ('Teclado', 45.99, 'Accesorios');
```

### **Buena Práctica: Parámetros Parametrizados**
En aplicaciones reales (con Python, Java, etc.), **nunca concatenes valores directamente** para prevenir ataques de inyección SQL. Usa parámetros:

```python
# Ejemplo en Python (seguro)
cursor.execute(
  "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
  ('Laptop', 1200.00)
)
```

### Resumen Visual
| Componente          | Descripción                              | Ejemplo                     |
|---------------------|------------------------------------------|-----------------------------|
| `INSERT INTO`       | Indica la tabla destino                  | `INSERT INTO productos`     |
| `(columna1, ...)`   | Columnas donde insertar                  | `(nombre, precio)`         |
| `VALUES (...)`      | Valores a insertar (en orden)            | `('Laptop', 1200.00)`      |

---

### 1.4. **Consultar Datos (SELECT)**
La sentencia `SELECT` es la herramienta principal para recuperar datos de una tabla. Su estructura básica es:

```sql
SELECT columnas_a_mostrar
FROM nombre_tabla
[condiciones];
```

### **Ejemplo 1: Ver todos los productos**
```sql
SELECT * FROM productos;
```

- **`SELECT *`**:  
  El asterisco (`*`) significa "**todas las columnas**" de la tabla.  
  Equivalente a pedir: *"Muéstrame todo lo que hay en la tabla"*.

- **Resultado**:  
  Devuelve **todas las filas y columnas** de la tabla `productos`.

---

### **Ejemplo 2: Filtrar productos baratos**
```sql
SELECT nombre, precio FROM productos WHERE precio < 500;
```

- **`SELECT nombre, precio`**:  
  Especifica **qué columnas mostrar** (solo `nombre` y `precio`, no todas).

- **`WHERE precio < 500`**:  
  Agrega una **condición de filtro**. Solo se muestran filas donde el `precio` sea menor a 500.

- **Resultado**:  
  Devuelve **solo los productos económicos** con su nombre y precio.


### **Ejemplo 3: Ordenar por precio descendente**
```sql
SELECT * FROM productos ORDER BY precio DESC;
```

- **`ORDER BY precio`**:  
  Ordena los resultados basándose en la columna `precio`.

- **`DESC`**:  
  Significa "**descendente**" (de mayor a menor).  
  Si omites `DESC`, el orden será ascendente (`ASC`).

- **Resultado**:  
  Devuelve **todos los productos ordenados desde el más caro al más barato**.
---

###  **Conceptos Clave Adicionales**
1. **Columnas vs. `*`**:  
   - Usar `*` es útil para pruebas rápidas, pero en producción **especifica columnas** para mejorar rendimiento.

2. **Múltiples condiciones**:  
   ```sql
   SELECT * FROM productos 
   WHERE precio < 500 AND categoria = 'Electrónica';
   ```

3. **Combinar filtros y órdenes**:  
   ```sql
   SELECT nombre, precio 
   FROM productos 
   WHERE precio > 100 
   ORDER BY precio ASC;
   ```

---

### Resumen
| Comando          | Propósito                               | Ejemplo                          |
|------------------|-----------------------------------------|----------------------------------|
| `SELECT *`       | Todas las columnas                       | `SELECT * FROM productos`        |
| `SELECT col1, col2` | Columnas específicas                   | `SELECT nombre, precio FROM...`  |
| `WHERE condicion` | Filtrar resultados                       | `WHERE precio < 500`             |
| `ORDER BY col`   | Ordenar resultados                      | `ORDER BY precio DESC`          |



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
