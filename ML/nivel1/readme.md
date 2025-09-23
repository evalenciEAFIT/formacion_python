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
import sqlite3  # 1Importamos el módulo para conectar con SQLite

# ========================================
# PASO 1: Conectar a la base de datos
# ========================================
# Creamos una conexión a la base de datos 'tienda.db'
# Si el archivo no existe, SQLite lo crea automáticamente
conexion = sqlite3.connect('tienda.db')  
cursor = conexion.cursor()  # Objeto para ejecutar comandos SQL

print("Conexión establecida con 'tienda.db'")

# ========================================
# PASO 2: Crear la tabla con restricciones
# ========================================
# Usamos execute() para enviar el comando SQL
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nombre TEXT NOT NULL, 
    precio REAL CHECK(precio > 0), 
    stock INTEGER DEFAULT 0, 
    fecha_vencimiento DATE
)
''')

print("Tabla 'productos' creada con éxito!")

# ========================================
# PASO 3: Verificar la estructura (opcional)
# ========================================
# Podemos inspeccionar la tabla para confirmar
cursor.execute("PRAGMA table_info(productos)")
columnas = cursor.fetchall()

print("\nEstructura de la tabla:")
for col in columnas:
    print(f"- {col[1]} ({col[2]})")  # Muestra nombre y tipo de dato

# ========================================
# PASO 4: Guardar cambios y cerrar
# ========================================
conexion.commit()  # ¡Crucial! Confirma los cambios en la base de datos
conexion.close()   # Cierra la conexión para liberar recursos

print("\nConexión cerrada. ¡Todo listo!")
```

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

### **1.4. Consultar Datos con `SELECT`**
La sentencia `SELECT` recupera información de una tabla. Su estructura básica es:

```sql
SELECT columnas_a_mostrar
FROM nombre_tabla
[condiciones];
```

---

### **Parámetros Comunes de `SELECT`**
| Parámetro       | Descripción                                      | Ejemplo                          |
|----------------|--------------------------------------------------|----------------------------------|
| `*`            | Todas las columnas                               | `SELECT * FROM productos`        |
| `columna1, columna2` | Columnas específicas                         | `SELECT nombre, precio FROM productos` |
| `WHERE`        | Filtro de condiciones                            | `WHERE precio < 500`             |
| `ORDER BY`     | Ordenamiento de resultados                      | `ORDER BY precio DESC`          |
| `LIMIT`        | Número máximo de filas a devolver                | `LIMIT 10`                       |
| `LIKE`         | Coincidencia de patrones (textuales)             | `WHERE nombre LIKE '%laptop%'`   |

---

### **Ejemplo Completo en Python**
Vamos a crear una base de datos, insertar datos y realizar consultas variadas:

```python
import sqlite3

# ========================================
# 1. Conectar a la base de datos
# ========================================
conexion = sqlite3.connect('tienda.db')
cursor = conexion.cursor()

# ========================================
# 2. Crear tabla (si no existe)
# ========================================
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL CHECK(precio > 0),
    categoria TEXT
)
''')

# ========================================
# 3. Insertar datos de ejemplo
# ========================================
productos = [
    ('Laptop', 1200.00, 'Electrónica'),
    ('Mouse', 25.50, 'Accesorios'),
    ('Teclado', 45.99, 'Accesorios'),
    ('Monitor', 300.00, 'Electrónica'),
    ('Audífonos', 80.00, 'Accesorios')
]

cursor.executemany('INSERT INTO productos (nombre, precio, categoria) VALUES (?, ?, ?)', productos)
conexion.commit()

# ========================================
# 4. Consultas Variadas
# ========================================

# CONSULTA 1: Ver todos los productos
print("=== Todos los productos ===")
cursor.execute('SELECT * FROM productos')
for fila in cursor.fetchall():
    print(fila)

# CONSULTA 2: Filtrar productos baratos (< $100)
print("\n=== Productos baratos (< $100) ===")
cursor.execute('SELECT nombre, precio FROM productos WHERE precio < 100')
for fila in cursor.fetchall():
    print(f"Nombre: {fila[0]}, Precio: ${fila[1]:.2f}")

# CONSULTA 3: Ordenar por precio descendente
print("\n=== Productos ordenados por precio (mayor a menor) ===")
cursor.execute('SELECT nombre, precio FROM productos ORDER BY precio DESC')
for fila in cursor.fetchall():
    print(f"Nombre: {fila[0]}, Precio: ${fila[1]:.2f}")

# CONSULTA 4: Buscar productos con 'ote' en el nombre
print("\n=== Productos con 'ote' en el nombre ===")
cursor.execute("SELECT * FROM productos WHERE nombre LIKE '%ote%'")
for fila in cursor.fetchall():
    print(fila)

# ========================================
# 5. Cerrar conexión
# ========================================
conexion.close()
```


### **Resultados Esperados**
```
=== Todos los productos ===
(1, 'Laptop', 1200.0, 'Electrónica')
(2, 'Mouse', 25.5, 'Accesorios')
(3, 'Teclado', 45.99, 'Accesorios')
(4, 'Monitor', 300.0, 'Electrónica')
(5, 'Audífonos', 80.0, 'Accesorios')

=== Productos baratos (< $100) ===
Nombre: Mouse, Precio: $25.50
Nombre: Teclado, Precio: $45.99
Nombre: Audífonos, Precio: $80.00

=== Productos ordenados por precio (mayor a menor) ===
Nombre: Laptop, Precio: $1200.00
Nombre: Monitor, Precio: $300.00
Nombre: Audífonos, Precio: $80.00
Nombre: Teclado, Precio: $45.99
Nombre: Mouse, Precio: $25.50

=== Productos con 'ote' en el nombre ===
(4, 'Monitor', 300.0, 'Electrónica')
```


### **Explicación del Código**
1. **Conexión y creación de tabla**:  
   ```python
   conexion = sqlite3.connect('tienda.db')
   cursor = conexion.cursor()
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS productos (...);
   ''')
   ```

2. **Inserción masiva de datos**:  
   ```python
   cursor.executemany('INSERT INTO productos (...) VALUES (?, ?, ?)', productos)
   ```

3. **Consultas con parámetros**:  
   - `fetchall()`: Obtiene todos los resultados.
   - `LIKE '%patron%'`: Busca cadenas que contengan el patrón.

4. **Cierre seguro**:  
   ```python
   conexion.commit()
   conexion.close()
   ```
---

### 2. **Agrupación con `GROUP BY`**
La cláusula `GROUP BY` agrupa filas con valores similares en columnas específicas, permitiendo resumir datos mediante funciones agregadas.

---

### **Sintaxis Básica**
```sql
SELECT columna_agrupadora, función_agregada(columna)
FROM nombre_tabla
GROUP BY columna_agrupadora;
```

### **Explicación Detallada**
```sql
SELECT categoria, COUNT(*) AS total_productos 
FROM productos 
GROUP BY categoria;
```

| Componente          | Descripción                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| `SELECT categoria`   | Selecciona la columna por la que se agruparán los datos.                   |
| `COUNT(*)`           | Función agregada que cuenta el número de filas en cada grupo.              |
| `AS total_productos` | Asigna un alias a la columna resultante (`total_productos` para facilitar lectura). |
| `FROM productos`     | Indica la tabla fuente de los datos.                                        |
| `GROUP BY categoria` | Agrupa las filas donde la columna `categoria` tenga el mismo valor.         |

---

### **Ejemplo Práctico**
Supongamos una tabla `productos` con estos datos:

| id | nombre       | precio | categoria   |
|----|--------------|--------|-------------|
| 1  | Laptop       | 1200   | Electrónica |
| 2  | Mouse        | 25     | Accesorios  |
| 3  | Teclado      | 45     | Accesorios  |
| 4  | Monitor      | 300    | Electrónica |
| 5  | Auriculares  | 80     | Accesorios  |

#### **Consulta:**
```sql
SELECT categoria, COUNT(*) AS total_productos 
FROM productos 
GROUP BY categoria;
```

#### **Resultado:**
| categoria   | total_productos |
|-------------|-----------------|
| Electrónica | 2               |
| Accesorios  | 3               |

---

### **Reglas Importantes**
1. **Columnas en `SELECT`**:  
   - Si usas `GROUP BY`, las columnas en `SELECT` deben estar en `GROUP BY` o ser funciones agregadas (`SUM()`, `AVG()`, etc.).

2. **Funciones Agregadas Comunes**:
   | Función       | Descripción                          |
   |---------------|--------------------------------------|
   | `COUNT(*)`    | Cuenta el número de filas en el grupo. |
   | `SUM(campo)`  | Suma los valores de un campo.         |
   | `AVG(campo)`   | Calcula el promedio de un campo.      |
   | `MAX(campo)`   | Encuentra el valor máximo.            |
   | `MIN(campo)`   | Encuentra el valor mínimo.            |

---

### **Ejemplo en Python**
```python
import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tienda.db')
cursor = conexion.cursor()

# Consulta con GROUP BY
cursor.execute('''
SELECT categoria, COUNT(*) AS total_productos 
FROM productos 
GROUP BY categoria
''')

# Mostrar resultados
print("Productos por categoría:")
for fila in cursor.fetchall():
    print(f"Categoría: {fila[0]}, Total: {fila[1]}")

conexion.close()
```

#### **Salida Esperada:**
```
Productos por categoría:
Categoría: Electrónica, Total: 2
Categoría: Accesorios, Total: 3
```

---

###  **Casos de Uso Avanzado**
1. **Filtrar grupos con `HAVING`** (similar a `WHERE` para grupos):  
   ```sql
   SELECT categoria, AVG(precio) AS precio_promedio
   FROM productos
   GROUP BY categoria
   HAVING AVG(precio) > 100;  -- Solo categorías con precio promedio > $100
   ```

2. **Agrupar por múltiples columnas**:  
   ```sql
   SELECT categoria, precio, COUNT(*)
   FROM productos
   GROUP BY categoria, precio;  -- Agrupa por categoría Y precio
   ```

### **Errores Comunes**
- **Error**: `SELECT nombre, COUNT(*) FROM productos GROUP BY categoria;`  
  ❌ **Solución**: Incluir `nombre` en `GROUP BY` o usar una función agregada (`MIN(nombre)`, `MAX(nombre)`).

---

### **3. Unir Tablas (JOIN)**
La cláusula `JOIN` combina filas de dos o más tablas basándose en una relación entre ellas. Es esencial cuando los datos están distribuidos en tablas relacionadas (ej: productos y proveedores).

---

### **Sintaxis Básica**
```sql
SELECT columnas_combinadas
FROM tabla1 alias1
[INNER|LEFT|RIGHT|FULL] JOIN tabla2 alias2
ON alias1.columna_común = alias2.columna_común;
```

---

### **Explicación Detallada**
```sql
SELECT p.nombre, pr.proveedor 
FROM productos p
INNER JOIN proveedores pr ON p.id = pr.producto_id;
```

| Componente          | Descripción                                                                 |
|---------------------|----------------------------------------------------------------------------|
| `SELECT p.nombre, pr.proveedor` | Selecciona columnas de ambas tablas (`nombre` de `productos`, `proveedor` de `proveedores`). |
| `FROM productos p`  | Especifica la tabla principal (`productos`) con un alias corto (`p`).        |
| `INNER JOIN proveedores pr` | Une la tabla `proveedores` (alias `pr`) con `productos`.                  |
| `ON p.id = pr.producto_id` | Define la condición de unión: filas donde `id` de `productos` coincide con `producto_id` de `proveedores`. |


### **Ejemplo Práctico**
Supongamos estas tablas:

**Tabla `productos`**:
| id | nombre       | precio |
|----|--------------|--------|
| 1  | Laptop       | 1200   |
| 2  | Mouse        | 25     |

**Tabla `proveedores`**:
| producto_id | proveedor   |
|-------------|-------------|
| 1           | TechCorp    |
| 2           | Electronics |

#### **Consulta:**
```sql
SELECT p.nombre, pr.proveedor 
FROM productos p
INNER JOIN proveedores pr ON p.id = pr.producto_id;
```

#### **Resultado:**
| nombre   | proveedor   |
|----------|-------------|
| Laptop   | TechCorp    |
| Mouse    | Electronics |

---

###  **Tipos de JOIN**
| Tipo          | Descripción                                                                 |
|---------------|----------------------------------------------------------------------------|
| `INNER JOIN`  | Solo devuelve filas con coincidencias en AMBAS tablas.                      |
| `LEFT JOIN`   | Devuelve todas las filas de la tabla izquierda, incluso sin coincidencias.   |
| `RIGHT JOIN`   | Devuelve todas las filas de la tabla derecha, incluso sin coincidencias.     |
| `FULL JOIN`    | Devuelve todas las filas de ambas tablas, llenando con `NULL` donde falten. |

---

###  **Ejemplo en Python**
```python
import sqlite3

# ========================================
# 1. Conectar a la base de datos
# ========================================
conexion = sqlite3.connect('tienda.db')
cursor = conexion.cursor()

# ========================================
# 2. Crear tablas (si no existen)
# ========================================
# Tabla de productos
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL CHECK(precio > 0)
)
''')

# Tabla de proveedores
cursor.execute('''
CREATE TABLE IF NOT EXISTS proveedores (
    producto_id INTEGER,
    proveedor TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
''')

# ========================================
# 3. Insertar datos de ejemplo
# ========================================
# Insertar productos
productos = [
    ('Laptop', 1200.00),
    ('Mouse', 25.50),
    ('Teclado', 45.99)
]
cursor.executemany('INSERT INTO productos (nombre, precio) VALUES (?, ?)', productos)

# Insertar proveedores
proveedores = [
    (1, 'TechCorp'),   # ID 1 corresponde a Laptop
    (2, 'Electronics'), # ID 2 corresponde a Mouse
    (3, 'AccesoriosInc') # ID 3 corresponde a Teclado
]
cursor.executemany('INSERT INTO proveedores (producto_id, proveedor) VALUES (?, ?)', proveedores)

conexion.commit()  # Guardar cambios

# ========================================
# 4. Consulta con INNER JOIN
# ========================================
cursor.execute('''
SELECT p.nombre, pr.proveedor 
FROM productos p
INNER JOIN proveedores pr ON p.id = pr.producto_id
''')

# ========================================
# 5. Mostrar resultados
# ========================================
print("Productos y sus proveedores:")
for fila in cursor.fetchall():
    print(f"Producto: {fila[0]}, Proveedor: {fila[1]}")

conexion.close()
```

#### **Salida Esperada:**
```
Productos y sus proveedores:
Producto: Laptop, Proveedor: TechCorp
Producto: Mouse, Proveedor: Electronics
```


### **Casos de Uso Comunes**
1. **Relaciones 1:N**: Un producto tiene un solo proveedor.  
2. **Relaciones N:M**: Usar tablas intermedias (ej: `pedidos` vinculando `clientes` y `productos`).  
3. **Datos complementarios**: Combinar información de facturación con detalles de clientes.

---

### **Errores Comunes**
- **No especificar `ON`**: Genera un `CROSS JOIN` (todas las combinaciones posibles), lo cual es ineficiente.  
- **Usar columnas incorrectas**: Asegúrate de que las columnas de unión tengan el mismo tipo de dato.

---

### 4. **Actualizar y Eliminar**
Las sentencias `UPDATE` y `DELETE` son fundamentales para modificar o eliminar registros existentes en una tabla.

### **Sintaxis Básica**
| Sentencia | Descripción                          | Ejemplo                                                                 |
|-----------|--------------------------------------|-------------------------------------------------------------------------|
| `UPDATE`  | Modifica datos existentes            | `UPDATE productos SET precio = 1150.00 WHERE nombre = 'Laptop';`      |
| `DELETE`  | Borra registros que cumplen una condición | `DELETE FROM productos WHERE precio < 100;`                             |

---

### **Explicación Detallada**
#### **1. Actualizar datos (`UPDATE`)**
```sql
UPDATE productos SET precio = 1150.00 WHERE nombre = 'Laptop';
```

| Componente       | Descripción                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `UPDATE productos` | Indica la tabla objetivo (`productos`).                                     |
| `SET precio = 1150.00` | Define el cambio: actualizar el campo `precio` a `1150.00`.                |
| `WHERE nombre = 'Laptop'` | Condición: solo afecta al producto llamado `'Laptop'`. |

#### **2. Eliminar datos (`DELETE`)**
```sql
DELETE FROM productos WHERE precio < 100;
```

| Componente       | Descripción                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `DELETE FROM productos` | Indica que se borrarán registros de la tabla `productos`.               |
| `WHERE precio < 100` | Condición: borra solo productos con precio inferior a `$100`.              |


### **Ejemplo Práctico**
Supongamos esta tabla inicial:

| id | nombre       | precio |
|----|--------------|--------|
| 1  | Laptop       | 1200   |
| 2  | Mouse        | 25     |
| 3  | Teclado      | 45     |

#### **Después de ejecutar:**
```sql
UPDATE productos SET precio = 1150.00 WHERE nombre = 'Laptop';
```

| id | nombre       | precio |
|----|--------------|--------|
| 1  | Laptop       | 1150   | ← **Precio actualizado**

#### **Después de ejecutar:**
```sql
DELETE FROM productos WHERE precio < 100;
```

| id | nombre       | precio |
|----|--------------|--------|
| 1  | Laptop       | 1150   | ← **Solo queda este registro**

---

### **Ejemplo en Python**
```python
import sqlite3

# Conectar a la base de datos
conexion = sqlite3.connect('tienda.db')
cursor = conexion.cursor()

# 1. Actualizar precio de una laptop
cursor.execute('''
UPDATE productos SET precio = 1150.00 
WHERE nombre = 'Laptop'
''')

# 2. Eliminar productos baratos
cursor.execute('''
DELETE FROM productos 
WHERE precio < 100
''')

# 3. Verificar cambios
cursor.execute('SELECT * FROM productos')
print("Productos restantes:")
for fila in cursor.fetchall():
    print(f"id: {fila[0]}, nombre: {fila[1]}, precio: {fila[2]}")

conexion.commit()
conexion.close()
```

---

### **Advertencias Clave**
1. **Siempre usa `WHERE` en `UPDATE`/`DELETE`**:  
   Si olvidas la condición, afectará **TODOS los registros de la tabla.

2. **Backup de datos**:  
   Antes de eliminar datos, haz una copia de seguridad:
   ```sql
   CREATE TABLE backup_productos AS SELECT * FROM productos;
   ```

3. **Transacciones (`BEGIN TRANSACTION`)**:  
   Envuelve operaciones críticas para revertir cambios si algo falla:
   ```sql
   BEGIN TRANSACTION;
   UPDATE productos SET precio = 1150.00 WHERE nombre = 'Laptop';
   DELETE FROM productos WHERE precio < 100;
   COMMIT;  -- Confirma cambios
   ```

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
