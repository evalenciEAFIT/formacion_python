# Nivel 1: Manejo Avanzado de Datos

[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4) | 
[Nivel 5: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel5) | 
[Nivel 6: Guía: Proyecto de Visualización y Prediccióno](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel6)

---
Este nivel cubre técnicas para trabajar con datos utilizando **SQL (SQLite)**, **Excel**, **archivos planos** y **Pandas**..

## Temas Incluidos
1. **SQL con SQLite**:  
   - Conexión a bases de datos, creación de tablas, inserción/consulta de datos.  
   - Consultas complejas (JOIN, GROUP BY, subconsultas).
  
2. **ETL con Pandas y SQL**:  
   - Estructuras de datos (Series, DataFrames).  
   - Limpieza, transformación y análisis estadístico.  



## Requisitos
- Haber completado el [Nivel 0](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0).  
- Instalar dependencias: `pip install pandas openpyxl sqlite3`.


## Ejemplos de Código
-----------------
# 1. SQL con SQLite

## Comandos Básicos (Explicados Simply)

###  **Crear una Base de Datos**
```sql
-- Crea un archivo de base de datos (.db)
sqlite3 mi_base_de_datos.db
```
**Explicación:** Esto genera un archivo llamado `mi_base_de_datos.db` donde se guardarán tus tablas y datos.


### **Crear Tablas**

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
# RESUMEN CRUD

| Operación | Descripción                          | SQL Command                          | Ejemplo en Python (sqlite3)                          |
|-----------|--------------------------------------|--------------------------------------|--------------------------------------------------|
| **C** (Create) | Insertar nuevos datos               | `INSERT INTO tabla (campos) VALUES (?)` | `cursor.execute("INSERT INTO...", params)`        |
| **R** (Read)   | Consultar datos existentes          | `SELECT * FROM tabla WHERE ...`       | `cursor.execute("SELECT...", params).fetchall()`   |
| **U** (Update)| Modificar datos existentes          | `UPDATE tabla SET campo=? WHERE ...`  | `cursor.execute("UPDATE...", params)`             |
| **D** (Delete)| Eliminar datos                      | `DELETE FROM tabla WHERE ...`         | `cursor.execute("DELETE...", params)`             |

---

### **Ejemplos Prácticos**
#### 1. **Crear (Insertar Datos)**
```sql
-- SQL
INSERT INTO productos (nombre, precio) VALUES ('Laptop', 1200.00);

-- Python
cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", ('Laptop', 1200.00))
conexion.commit()  # ¡Importante!
```

#### 2. **Leer (Consultar Datos)**
```sql
-- SQL
SELECT * FROM productos WHERE precio > 500;

-- Python
cursor.execute("SELECT * FROM productos WHERE precio > ?", (500,))
results = cursor.fetchall()
for row in results:
    print(row)
```

#### 3. **Actualizar (Modificar Datos)**
```sql
-- SQL
UPDATE productos SET precio = 1150.00 WHERE nombre = 'Laptop';

-- Python
cursor.execute("UPDATE productos SET precio=? WHERE nombre=?", (1150.00, 'Laptop'))
conexion.commit()
```

#### 4. **Eliminar (Borrar Datos)**
```sql
-- SQL
DELETE FROM productos WHERE precio < 100;

-- Python
cursor.execute("DELETE FROM productos WHERE precio < ?", (100,))
conexion.commit()
```

---

### **Notas Críticas**
1. **Commit Transacciones**:  
   Siempre usa `conexion.commit()` después de `INSERT`, `UPDATE` o `DELETE`.

2. **Parámetros Parametrizados**:  
   Usa `?` en lugar de concatenar strings para **prevenir inyección SQL**:
   ```python
   # MAL (vulnerable a inyección):
   cursor.execute(f"SELECT * FROM productos WHERE nombre='{user_input}'")
   
   # BIEN (seguro):
   cursor.execute("SELECT * FROM productos WHERE nombre=?", (user_input,))
   ```

3. **Manejo de Errores**:  
   Envuelve operaciones críticas en bloques `try-except`:
   ```python
   try:
       cursor.execute(...)
       conexion.commit()
   except sqlite3.Error as e:
       print(f"Error: {e}")
       conexion.rollback()  # Revertir cambios si falla
   ```

---

### **Estructura de Código Completo**
```python
import sqlite3

# Conectar a la DB
conexion = sqlite3.connect('tienda.db')
cursor = conexion.cursor()

# --- OPERACIONES CRUD ---
# CREATE
cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", ('Tablet', 800.00))
conexion.commit()

# READ
cursor.execute("SELECT * FROM productos")
print("Productos:", cursor.fetchall())

# UPDATE
cursor.execute("UPDATE productos SET precio=? WHERE nombre=?", (750.00, 'Tablet'))
conexion.commit()

# DELETE
cursor.execute("DELETE FROM productos WHERE precio < 200")
conexion.commit()

# Cerrar conexión
conexion.close()
```

---
# **ETL: Extracción, Transformación y Carga de Datos**  
Un **ETL (Extract, Transform, Load)** es el proceso para mover datos de una fuente a un destino, aplicando transformaciones necesarias. Es **fundamental para ciencia de datos y ML** porque:
- **Garantiza calidad de datos**: Limpia inconsistencias, valores nulos y errores.
- **Prepara datos para modelos**: Convierte datos crudos en un formato usable para entrenamiento.
- **Centraliza información**: Combina datos de múltiples fuentes en una única base.

## **Parte 1: Crear Datos y Tablas (Fuente de Datos)**
Primero, generamos datos de ejemplo y creamos tablas en SQLite:

```python
import sqlite3
import pandas as pd
from datetime import datetime

# ========================================
# 1. CREAR BASE DE DATOS Y TABLAS
# ========================================
conexion = sqlite3.connect('ventas.db')
cursor = conexion.cursor()

# Crear tabla de ventas
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    producto TEXT,
    cantidad INTEGER CHECK(cantidad > 0),
    fecha_venta DATE,
    total_venta REAL
)
''')

# Insertar datos de ejemplo
ventas_data = [
    ('Cliente_A', 'Laptop', 2, '2023-10-01', 2400.00),
    ('Cliente_B', 'Mouse', 5, '2023-10-02', 127.50),
    ('Cliente_C', 'Teclado', 1, '2023-10-03', 45.99),
    ('Cliente_D', 'Monitor', 3, '2023-10-04', 900.00),
    ('Cliente_E', 'Audífonos', 10, '2023-10-05', 800.00)
]
cursor.executemany('INSERT INTO ventas (cliente, producto, cantidad, fecha_venta, total_venta) VALUES (?, ?, ?, ?, ?)', ventas_data)

conexion.commit()
conexion.close()

print("Base de datos 'ventas.db' creada con datos de ejemplo.")
```

## **Parte 2: ETL Completo (SQLite → Pandas → Excel)**
Realizamos el ETL para transformar los datos y generar un informe en Excel:

```python#  pip uninstall pandas
# pip install pandas openpyxl

import sqlite3
import pandas as pd  # <-- Asegúrate de importar pandas
from datetime import datetime

# ========================================
# 1. CREAR BASE DE DATOS Y TABLAS
# ========================================
conexion = sqlite3.connect('ventas_etl.db')
cursor = conexion.cursor()

# Crear tabla de ventas
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    producto TEXT,
    cantidad INTEGER CHECK(cantidad > 0),
    fecha_venta DATE,
    total_venta REAL
)
''')

# Crear tabla de proveedores
cursor.execute('''
CREATE TABLE IF NOT EXISTS proveedores (
    producto_id INTEGER,
    proveedor TEXT,
    FOREIGN KEY (producto_id) REFERENCES ventas(id)
)
''')

# Insertar datos de ejemplo
ventas_data = [
    ('Cliente_A', 'Laptop', 2, '2023-10-01', 2400.00),
    ('Cliente_B', 'Mouse', 5, '2023-10-02', 127.50),
    ('Cliente_C', 'Teclado', 1, '2023-10-03', 45.99),
    ('Cliente_D', 'Monitor', 3, '2023-10-04', 900.00),
    ('Cliente_E', 'Audífonos', 10, '2023-10-05', 800.00)
]
cursor.executemany('INSERT INTO ventas (cliente, producto, cantidad, fecha_venta, total_venta) VALUES (?, ?, ?, ?, ?)', ventas_data)

# Insertar proveedores
proveedores_data = [
    (1, 'TechCorp'),    # ID 1 = Laptop
    (2, 'Electronics'), # ID 2 = Mouse
    (3, 'AccesoriosInc'), # ID 3 = Teclado
    (4, 'DisplaysLtd'),  # ID 4 = Monitor
    (5, 'AudioMax')     # ID 5 = Audífonos
]
cursor.executemany('INSERT INTO proveedores (producto_id, proveedor) VALUES (?, ?)', proveedores_data)

conexion.commit()
conexion.close()

print("Base de datos 'ventas_etl.db' creada con datos de ejemplo.")

# ========================================
# 2. ETL COMPLETO (SQLite → Manual → Pandas → CSV/Excel)
# ========================================
# ========================================
# 2.1. EXTRACCIÓN MANUAL DESDE SQLITE
# ========================================
conexion = sqlite3.connect('ventas_etl.db')
cursor = conexion.cursor()

# Leer datos de ventas
cursor.execute("SELECT * FROM ventas")
ventas_filas = cursor.fetchall()

# Leer datos de proveedores
cursor.execute("SELECT * FROM proveedores")
proveedores_filas = cursor.fetchall()

conexion.close()

# ========================================
# 2.2. TRANSFORMACIÓN DE DATOS (MANUAL + PANDAS)
# ========================================
# Convertir datos a diccionarios para facilidad
columnas_ventas = ['id', 'cliente', 'producto', 'cantidad', 'fecha_venta', 'total_venta']
ventas_dict = [dict(zip(columnas_ventas, fila)) for fila in ventas_filas]

# Convertir a DataFrame de Pandas
df_ventas = pd.DataFrame(ventas_dict)
df_ventas['fecha_venta'] = pd.to_datetime(df_ventas['fecha_venta'])  # Formatear fechas

# Agregar margen de ganancia (25%)
df_ventas['margen_ganancia'] = df_ventas['total_venta'] * 0.25

# Filtrar ventas de octubre 2023
df_octubre = df_ventas[df_ventas['fecha_venta'].dt.month == 10].copy()

# ========================================
# 2.3. CARGA DE DATOS (CSV + EXCEL)
# ========================================
# Generar archivo CSV
df_ventas.to_csv('ventas_transformadas.csv', index=False)
print("Archivo CSV generado: ventas_transformadas.csv")

# Generar archivo Excel
with pd.ExcelWriter('reporte_ventas_etl.xlsx', engine='openpyxl') as writer:
    df_ventas.to_excel(writer, sheet_name='Todas_Ventas', index=False)
    df_octubre.to_excel(writer, sheet_name='Ventas_Octubre_2023', index=False)

print("ETL completado! Archivos generados:")
print("- ventas_transformadas.csv")
print("- reporte_ventas_etl.xlsx")
```

---

## **Resultado del ETL**
Generará un archivo `reporte_ventas_etl.xlsx` con dos hojas:
1. **Todas_Ventas**: Todos los registros originales.
2. **Ventas_Octubre_2023**: Solo ventas del mes de octubre, con margen de ganancia calculado.


## **Importancia del ETL para ML**
- **Calidad de datos**: Elimina errores que podrían sesgar modelos.
- **Consistencia**: Asegura que todos los datos sigan el mismo formato.
- **Eficiencia**: Permite entrenar modelos con datos estructurados y relevantes.


## **Mejoras Potenciales**
- **Incorporar datos externos**: Unir con APIs o archivos CSV.
- **Automatización**: Programar el ETL para ejecutarse diariamente.
- **Monitoreo**: Agregar logs para rastrear errores.
