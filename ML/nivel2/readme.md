# Guía Paso a Paso para Usar Pandas 
Caso práctico en el Monitoreo de Electricidad, Agua y Gas   
Material de apoyo: [https://www.w3schools.com/python/pandas/default.asp](https://www.w3schools.com/python/pandas/default.asp)

[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4)


---
## Introducción

Pandas es una biblioteca de código abierto que facilita la manipulación y análisis de datos estructurados.

El enfoque temático se centra en el monitoreo de servicios esenciales, donde los datos provienen de sensores o registros históricos. Conceptualemente, Pandas actúa como una "hoja de cálculo programable" que permite cargar datos de diversas fuentes (CSV, Excel, SQLite), realizar operaciones matemáticas para derivar métricas clave (como costos totales o alertas de consumo alto), y respaldar resultados para auditorías.

## Temario (Tabla de Contenidos)

1. [Importar Bibliotecas](#paso-1-importar-bibliotecas)  
2. [Crear un DataFrame de Ejemplo](#paso-2-crear-un-dataframe-de-ejemplo)  
3. [Cargar Datos desde Diferentes Fuentes](#paso-3-cargar-datos-desde-diferentes-fuentes)  
   - [Desde CSV](#desde-csv)  
   - [Desde Excel](#desde-excel)  
   - [Desde SQLite](#desde-sqlite)  
4. [Manipulación de Datos Básica](#paso-4-manipulación-de-datos-básica)  
   - [Inspeccionar el DataFrame](#inspeccionar-el-dataframe)  
   - [Seleccionar y Filtrar](#seleccionar-y-filtrar)  
   - [Agrupar por Servicio](#agrupar-por-servicio)  
5. [Crear Columnas con Operaciones Matemáticas](#paso-5-crear-columnas-con-operaciones-matemáticas)  
6. [Respaldar Datos](#paso-6-respaldar-datos)  
   - [A CSV](#a-csv)  
   - [A Excel](#a-excel)  
   - [A SQLite](#a-sqlite)  
7. [Visualizaciones con Matplotlib](#paso-7-visualizaciones-con-matplotlib)  
   - [Gráfico de Barras (Consumo por Servicio)](#gráfico-de-barras-consumo-por-servicio)  
   - [Gráfico de Líneas (Costo Total por Fecha)](#gráfico-de-líneas-costo-total-por-fecha)  
   - [Gráfico de Dispersión (Consumo vs Costo)](#gráfico-de-dispersión-consumo-vs-costo)  
8. [Consejos Específicos para Monitoreo de Servicios](#consejos-específicos-para-monitoreo-de-servicios)  

## Paso 1: Importar Bibliotecas

Comienza importando las bibliotecas necesarias para manipular datos y crear visualizaciones.  
Pandas se usa para el manejo de datos tabulares, sqlite3 para bases de datos locales, y Matplotlib para gráficos.

Intenta creando buenas practivas :)

```python
import pandas as pd  # Biblioteca principal para manipulación de datos en DataFrames
import sqlite3  # Para conectar y trabajar con bases de datos SQLite
import matplotlib.pyplot as plt  # Para generar visualizaciones gráficas
```

## Paso 2: Crear un DataFrame de Ejemplo

Para empezar, creamos un DataFrame con datos simulados de consumo de servicios.  
Esto simula lecturas de medidores, permitiendo probar el código sin archivos externos.

```python
# Crear un diccionario con datos simulados de monitoreo
data = {
    'Medidor_ID': ['M001', 'M002', 'M003', 'M004', 'M005'],  # Identificadores únicos de medidores
    'Servicio': ['Electricidad', 'Agua', 'Gas', 'Electricidad', 'Agua'],  # Tipo de servicio monitoreado
    'Consumo': [150, 10, 25, 200, 12],  # Unidades consumidas (kWh, m³, etc.)
    'Costo_Unitario': [0.12, 1.5, 0.8, 0.12, 1.5],  # Costo por unidad ($/unidad)
    'Fecha': ['2025-09-01', '2025-09-01', '2025-09-01', '2025-09-02', '2025-09-02']  # Fecha de la lectura
}

# Convertir el diccionario a un DataFrame de Pandas
df = pd.DataFrame(data)

# Mostrar el DataFrame para verificar los datos
print(df)
```

**Salida esperada:**
```
  Medidor_ID     Servicio  Consumo  Costo_Unitario       Fecha
0      M001  Electricidad      150           0.12  2025-09-01
1      M002          Agua       10           1.50  2025-09-01
2      M003           Gas       25           0.80  2025-09-01
3      M004  Electricidad      200           0.12  2025-09-02
4      M005          Agua       12           1.50  2025-09-02
```

## Paso 3: Cargar Datos desde Diferentes Fuentes

En el monitoreo, los datos pueden provenir de archivos CSV (exportados de sensores), Excel (reportes manuales) o bases de datos SQLite (almacenamiento local).  
Aquí te mostramos cómo cargarlos, logrando flexibilidad en la integración de fuentes.

### Desde CSV
Suponiendo que los datos están en `consumo_servicios.csv`.  
Esto carga datos delimitados por comas, común en logs de medidores.

```python
# Cargar datos desde un archivo CSV
df_csv = pd.read_csv('consumo_servicios.csv')  # Lee el archivo y crea un DataFrame
print(df_csv.head())  # Muestra las primeras filas para inspección inicial
```

### Desde Excel
Suponiendo un archivo `consumo_servicios.xlsx`.  
Útil para reportes con múltiples hojas.

```python
# Cargar datos desde un archivo Excel, especificando la hoja
df_excel = pd.read_excel('consumo_servicios.xlsx', sheet_name='Consumo')  # Lee la hoja indicada
print(df_excel.head())  # Muestra las primeras filas
```

### Desde SQLite
Primero, crea una base de datos y carga los datos.  
Esto simula un almacenamiento persistente para históricos de monitoreo.

```python
# Crear una conexión a la base de datos SQLite (crea el archivo si no existe)
conn = sqlite3.connect('monitoreo.db')  # Establece la conexión

# Cargar datos desde la base de datos usando una consulta SQL
query = "SELECT * FROM consumo"  # Consulta para seleccionar todos los registros
df_sql = pd.read_sql_query(query, conn)  # Ejecuta la consulta y crea un DataFrame
print(df_sql.head())  # Muestra las primeras filas

# Cerrar la conexión para liberar recursos
conn.close()
```

## Codigo Resumen
Se considera la estructura: Data, App, ...

```python
import pandas as pd  # Biblioteca principal para manipulación de datos en DataFrames
import sqlite3  # Para conectar y trabajar con bases de datos SQLite
import matplotlib.pyplot as plt  # Para generar visualizaciones gráficas

#Variables
global variable 
global archivoCSV
global BaseDatos 
global conn 
global Query 

variable = None
archivoCSV = None
BaseDatos = "data/monitoreo.db"
conn = None
Query = "SELECT * FROM consumo"

def CrearVariable():
    global variable
    # Crear un diccionario con datos simulados de monitoreo
    variable = {
        'Medidor_ID': ['M001', 'M002', 'M003', 'M004', 'M005'],  # Identificadores únicos de medidores
        'Servicio': ['Electricidad', 'Agua', 'Gas', 'Electricidad', 'Agua'],  # Tipo de servicio monitoreado
        'Consumo': [150, 10, 25, 200, 12],  # Unidades consumidas (kWh, m³, etc.)
        'Costo_Unitario': [0.12, 1.5, 0.8, 0.12, 1.5],  # Costo por unidad ($/unidad)
        'Fecha': ['2025-09-01', '2025-09-01', '2025-09-01', '2025-09-02', '2025-09-02']  # Fecha de la lectura
    }

def CrearArchivoCSV():
    global archivoCSV
    archivoCSV = "data/consumo_servicios.csv"

def ConexionBD():
    global conn
    conn = sqlite3.connect(BaseDatos)

def DesconectarBD():
    global conn
    # Cerrar la conexión para liberar recursos
    conn.close()

def verResultado(titulo, df):
    print(f"--- [{titulo}] --------")
    print(df)
    print("\n")

if __name__ == '__main__':
    CrearVariable()
    CrearArchivoCSV()
    ConexionBD()

    df_variable = pd.DataFrame(variable)
    df_CSV = pd.read_csv(archivoCSV)
    df_SQL = pd.read_sql_query(Query, conn)

    verResultado("Varible",df_variable)
    verResultado("CSV",df_CSV)
    verResultado("SQL",df_SQL)

    DesconectarBD()

```

## Codigo Resumen 2
```python
import pandas as pd  # Biblioteca principal para manipulación de datos en DataFrames
import sqlite3  # Para conectar y trabajar con bases de datos SQLite
import matplotlib.pyplot as plt  # Para generar visualizaciones gráficas


global variable
global ruta_csv
global rutaBD
global rutaExcel
global conn

def Inicializar():
    global variable
    global ruta_csv
    global rutaBD
    global ruta_excel
    global conn

    ruta_csv = "Data/consumo_servicios.csv"
    rutaBD = "Data/monitoreo.db"
    ruta_excel = "Data/Libro1.xlsx"

    # Crear un diccionario con datos simulados de monitoreo
    variable = {
        'Medidor_ID': ['M001', 'M002', 'M003', 'M004', 'M005'],  # Identificadores únicos de medidores
        'Servicio': ['Electricidad', 'Agua', 'Gas', 'Electricidad', 'Agua'],  # Tipo de servicio monitoreado
        'Consumo': [150, 10, 25, 200, 12],  # Unidades consumidas (kWh, m³, etc.)
        'Costo_Unitario': [0.12, 1.5, 0.8, 0.12, 1.5],  # Costo por unidad ($/unidad)
        'Fecha': ['2025-09-01', '2025-09-01', '2025-09-01', '2025-09-02', '2025-09-02']  # Fecha de la lectura
    }

def cargarVarible():
    global variable
    df = pd.DataFrame(variable)
    return df

def cargarCSV():
    global ruta_csv
    df = pd.read_csv(ruta_csv)
    return df

def cargarExcel(pestaña):
    global ruta_excel
    df = pd.read_excel(ruta_excel, sheet_name=pestaña)
    return df

def cargarSQL(comando):
    global conn
    global rutaBD
    conn = sqlite3.connect(rutaBD)
    df = pd.read_sql_query(comando, conn)
    return df

def desconectarBD():
    global conn
    conn.close()

def verDF(titulo, df):
    print(f"--- [{titulo}] ------------")
    print(df)
    print("\n")

#Funcion principal o programa
if __name__ == '__main__':
    Inicializar()
    d_variable = cargarVarible()
    verDF("VARIABLE", d_variable)

    d_csv = cargarCSV()
    verDF("CSV", d_csv)

    d_SQL = cargarSQL("SELECT * FROM consumo")
    verDF("SQL", d_SQL)
    desconectarBD()
```

## Paso 4: Manipulación de Datos Básica

Una vez cargados, inspecciona, selecciona y filtra los datos para analizar el consumo.  
Esto permite detectar anomalías o resumir métricas, logrando un análisis preliminar eficiente.

### Inspeccionar el DataFrame
```python
# Mostrar las primeras filas del DataFrame
print(df.head())  # Útil para una vista rápida de los datos

# Generar estadísticas descriptivas (media, min, max, etc.)
print(df.describe())  # Resume columnas numéricas

# Mostrar información sobre tipos de datos y valores nulos
print(df.info())  # Ayuda a identificar problemas de datos

# Mostrar la forma (número de filas y columnas)
print(df.shape)  # Proporciona dimensiones del DataFrame
```

### Seleccionar y Filtrar
```python
# Seleccionar columnas específicas para enfocarse en datos relevantes
consumo = df[['Medidor_ID', 'Servicio', 'Consumo']]  # Crea un sub-DataFrame
print(consumo)  # Muestra el subconjunto

# Filtrar por un servicio específico (ej. Electricidad)
electricidad = df[df['Servicio'] == 'Electricidad']  # Aplica condición booleana
print(electricidad)  # Muestra filas filtradas

# Filtrar consumos altos (> 100 unidades) para alertas
altos = df[df['Consumo'] > 100]  # Condición numérica
print(altos)  # Muestra resultados
```

### Agrupar por Servicio
```python
# Agrupar por 'Servicio' y sumar el 'Consumo' para totales
consumo_por_servicio = df.groupby('Servicio')['Consumo'].sum()  # Operación de agregación
print(consumo_por_servicio)  # Muestra suma por grupo
```

**Salida ejemplo:**
```
Servicio
Agua            22
Electricidad   350
Gas             25
Name: Consumo, dtype: int64
```

## Paso 5: Crear Columnas con Operaciones Matemáticas

Calcula costos, alertas o extracciones basadas en los datos de monitoreo.  
Esto deriva nuevas métricas, logrando insights como costos operativos o detección de picos.

```python
# Calcular el costo total multiplicando Consumo por Costo_Unitario
df['Costo_Total'] = df['Consumo'] * df['Costo_Unitario']  # Operación vectorizada eficiente
print(df)  # Muestra DataFrame actualizado

# Crear una columna de alerta usando una función lambda para clasificar consumos
df['Alerta_Consumo_Alto'] = df['Consumo'].apply(lambda x: 'Alto' if x > 100 else 'Normal')  # Aplicación por fila
print(df)  # Muestra con la nueva columna

# Convertir la columna 'Fecha' a formato datetime para operaciones temporales
df['Fecha'] = pd.to_datetime(df['Fecha'])  # Convierte strings a objetos datetime

# Extraer el día de la fecha para análisis granular
df['Dia'] = df['Fecha'].dt.day  # Accede al componente 'día'
print(df)  # Muestra DataFrame final
```

**Salida después de agregar columnas:**
```
  Medidor_ID     Servicio  Consumo  Costo_Unitario      Fecha  Costo_Total Alerta_Consumo_Alto  Dia
0      M001  Electricidad      150           0.12 2025-09-01       18.00               Alto    1
1      M002          Agua       10           1.50 2025-09-01       15.00             Normal    1
2      M003           Gas       25           0.80 2025-09-01       20.00             Normal    1
3      M004  Electricidad      200           0.12 2025-09-02       24.00               Alto    2
4      M005          Agua       12           1.50 2025-09-02       18.00             Normal    2
```

## Paso 6: Respaldar Datos

Guarda los datos procesados para reportes o backups.  
Esto asegura persistencia, logrando trazabilidad en sistemas de monitoreo.

### A CSV
```python
# Guardar el DataFrame en un archivo CSV sin índice
df.to_csv('consumo_respaldo.csv', index=False)  # Formato simple y portátil
```

### A Excel
Se requiere la libreria openpyxl
```python
# Guardar en Excel, especificando nombre de hoja
df.to_excel('consumo_respaldo.xlsx', index=False, sheet_name='Monitoreo')  # Formato con soporte para hojas múltiples
```


### A SQLite
```python
# Conectar a una nueva base de datos para respaldo
conn = sqlite3.connect('respaldo_monitoreo.db')  # Crea o conecta

# Guardar en una tabla SQL
df.to_sql('consumo_respaldo', conn, if_exists='replace', index=False)  # Reemplaza si existe

# Cerrar conexión
conn.close()  # Libera recursos
```

## Paso 7: Visualizaciones con Matplotlib

Crea gráficos para visualizar tendencias en el consumo.  
Esto facilita la interpretación visual, logrando reportes intuitivos para stakeholders.

### Gráfico de Barras (Consumo por Servicio)
```python
# Agrupar y sumar consumo por servicio
consumo_por_servicio = df.groupby('Servicio')['Consumo'].sum()

# Generar gráfico de barras
consumo_por_servicio.plot(kind='bar', title='Consumo Total por Servicio')  # Tipo de gráfico
plt.xlabel('Servicio')  # Etiqueta eje X
plt.ylabel('Consumo (unidades)')  # Etiqueta eje Y
plt.show()  # Muestra el gráfico
```

### Gráfico de Líneas (Costo Total por Fecha)
```python
# Agrupar y sumar costos por fecha
costo_por_fecha = df.groupby('Fecha')['Costo_Total'].sum()

# Generar gráfico de líneas con marcadores
costo_por_fecha.plot(kind='line', marker='o', title='Costo Total por Fecha')  # Tipo de gráfico
plt.xlabel('Fecha')  # Etiqueta eje X
plt.ylabel('Costo Total ($)')  # Etiqueta eje Y
plt.show()  # Muestra el gráfico
```

### Gráfico de Dispersión (Consumo vs Costo)
```python
# Generar gráfico de dispersión
df.plot(kind='scatter', x='Consumo', y='Costo_Total', color='blue', title='Consumo vs Costo Total')  # Tipo de gráfico
plt.xlabel('Consumo (unidades)')  # Etiqueta eje X
plt.ylabel('Costo Total ($)')  # Etiqueta eje Y
plt.show()  # Muestra el gráfico
```

## Consejos Específicos para Monitoreo de Servicios

- **Datos Faltantes**: Usa `df.fillna(0)` para rellenar valores nulos o `df.interpolate()` para estimaciones lineales, común en lecturas de sensores fallidas.  
- **Umbrales de Alerta**: Crea columnas para detectar anomalías (ej. consumo > media + 2*desviación estándar) usando `df['Consumo'].mean()` y `df['Consumo'].std()`.  
- **Automatización**: Integra con bibliotecas como `schedule` para ejecutar monitoreos periódicos, logrando alertas en tiempo real.  
- **Avanzado**: Explora `seaborn` para visualizaciones más complejas o `merge()` para unir datasets de múltiples medidores.  
- **Documentación**: Consulta [pandas.pydata.org](https://pandas.pydata.org) para más detalles.
