## Guía Completa: Proyecto de Visualización y Predicción

Este documento contiene la implementación técnica completa, paso a paso, para el proyecto de ejemplo de las hidroeléctricas.

[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4) | 
[Nivel 5: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel5) | 
[Nivel 6: Guía: Proyecto de Visualización y Prediccióno](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel6)

---

### Sección 0: Configuración del Entorno de Desarrollo

Antes de escribir código, es crucial crear un entorno aislado para tu proyecto. Esto asegura que las librerías que instales no entren en conflicto con otros proyectos.

#### 1\. Crear un Entorno Virtual (`venv`)

Un entorno virtual es una carpeta que contiene una instalación de Python y las librerías específicas para tu proyecto.

1.  Abre tu terminal o línea de comandos.

2.  Navega a la carpeta donde vivirá tu proyecto (ej. `C:\Proyectos\` o `~/Proyectos/`).

3.  Crea una carpeta para el proyecto y entra en ella:

    ```bash
    mkdir proyecto_hidro_epm
    cd proyecto_hidro_epm
    ```

4.  Crea el entorno virtual. Es una convención llamarlo `venv`:

    ```bash
    python -m venv venv
    ```

#### 2\. Activar el Entorno Virtual

Deberás activar el entorno cada vez que trabajes en el proyecto.

  * **En Windows (PowerShell):**

    ```powershell
    .\venv\Scripts\Activate
    ```

  * **En Windows (CMD):**

    ```bat
    .\venv\Scripts\activate.bat
    ```
    (Tu terminal debería ahora mostrar `(venv)` al inicio de la línea).


#### 3\. Instalación de Paquetes y `requirements.txt`

El archivo `requirements.txt` es una lista de todas las librerías que tu proyecto necesita.

1.  Con tu entorno `venv` activado, instala las librerías una por una. Usaremos:

      * `pandas` y `numpy`: Para manipulación de datos.
      * `scikit-learn` y `joblib`: Para crear y guardar el modelo de ML.
      * `dash` y `plotly`: Para el dashboard web interactivo.
      * `openpyxl`: Para que pandas pueda escribir en Excel.
      * `SQLAlchemy`: Para que pandas pueda escribir en bases de datos SQL (usaremos SQLite).
      * `WeasyPrint` y `kaleido`: Para generar el reporte PDF y exportar gráficos de Plotly a imágenes.
      * `dash-leaflet`: Para generar los mapas https://leafletjs.com
      * `xhtml2pdf` : Alternativa a WeasyPrint

    <!-- end list -->

    ```bash
    pip install pandas numpy scikit-learn joblib dash plotly openpyxl SQLAlchemy WeasyPrint kaleido dash-leaflet xhtml2pdf
    ```

2.  Una vez instaladas, genera el archivo `requirements.txt` automáticamente. Este comando "congela" la lista de paquetes instalados en el entorno y la guarda en un archivo:

    ```bash
    pip freeze > requirements.txt
    ```

Ahora, cualquier otra persona puede replicar tu entorno exacto simplemente corriendo `pip install -r requirements.txt`.

-----

### Sección 1: Creación de la Estructura de Archivos

Una buena estructura de carpetas es fundamental. Aquí tienes un script para crearla automáticamente.


**Para Windows (guarda esto como `setup.ps1` y ejecuta en PowerShell):**

```powershell
Write-Host "Creando estructura de carpetas para el proyecto..."

# Crear directorios
New-Item -ItemType Directory -Path "data"
New-Item -ItemType Directory -Path "dashboard\assets"
New-Item -ItemType Directory -Path "notebooks"
New-Item -ItemType Directory -Path "src"
New-Item -ItemType Directory -Path "models"
New-Item -ItemType Directory -Path "tests"

Write-Host "Creando archivos iniciales..."

# Archivos __init__.py
New-Item -ItemType File -Path "src\__init__.py"
New-Item -ItemType File -Path "tests\__init__.py"

# Archivos de código principales
New-Item -ItemType File -Path "src\data_ingestion.py"
New-Item -ItemType File -Path "src\feature_engineering.py"
New-Item -ItemType File -Path "src\model_training.py"
New-Item -ItemType File -Path "src\model_prediction.py"
New-Item -ItemType File -Path "src\report_generator.py"
New-Item -ItemType File -Path "dashboard\app.py"

# Marcadores de posición
New-Item -ItemType File -Path "data\.gitkeep"
New-Item -ItemType File -Path "models\.gitkeep"

# Archivos de exploración
New-Item -ItemType File -Path "notebooks\01_exploracion_datos.ipynb"
New-Item -ItemType File -Path "notebooks\02_prototipo_modelo_ml.ipynb"

# Archivos de proyecto
New-Item -ItemType File -Path "README.md"
New-Item -ItemType File -Path ".gitignore"

Write-Host "Estructura creada exitosamente."
```

-----

### Sección 2: Código de Ingesta y Generación de Datos

Este script creará los datos simulados y los guardará en CSV, Excel y una base de datos SQLite.

**Copia este código en `src/data_ingestion.py`:**

```python
"""
Módulo de Ingesta y Simulación de Datos.

Este script es responsable de:
1. Simular datos históricos y operativos de las centrales hidroeléctricas.
   La simulación genera 3 años de datos que terminan en la fecha actual.
2. Guardar estos datos en múltiples formatos (CSV, Excel, SQLite DB).
3. Configurar la base de datos inicial, creando tablas para 'Centrales' y 'Mediciones'.
"""

import pandas as pd
import numpy as np
import datetime
import sqlite3
from sqlalchemy import create_engine
import os

# --- 1. Configuración de la Simulación ---

# Define las centrales y sus atributos (coordenadas, capacidad, etc.)
# Estos datos son estáticos y definen las entidades que estamos midiendo.
CENTRALES = {
    'Guatape': {'lat': 6.32, 'lon': -75.16, 'capacidad_MWh': 560, 'nivel_max_msnm': 1900},
    'Ituango': {'lat': 7.15, 'lon': -75.63, 'capacidad_MWh': 2400, 'nivel_max_msnm': 401},
    'Playas': {'lat': 6.45, 'lon': -74.88, 'capacidad_MWh': 201, 'nivel_max_msnm': 780},
    'SanCarlos': {'lat': 6.19, 'lon': -74.98, 'capacidad_MWh': 1240, 'nivel_max_msnm': 805}
}

# --- MEJORA: Configuración de Fecha Dinámica ---
# Esto es crucial para que el modelo de predicción funcione.
# El modelo necesita datos de "hoy" para predecir "mañana".
# Al generar datos hasta hoy, nos aseguramos de que no falten datos recientes.

# Obtenemos la fecha actual y la limpiamos (sin hora, minuto, etc.)
FECHA_HOY = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

# Calculamos la fecha de inicio para tener 3 años de historial.
FECHA_INICIO = FECHA_HOY - datetime.timedelta(days=(3 * 365)) # 3 años de historia

# Calculamos el número total de días a simular, incluyendo hoy.
N_DIAS_HISTORICOS = (FECHA_HOY - FECHA_INICIO).days + 1
# --- Fin de la Mejora ---


# --- 2. Rutas de Archivos de Salida ---

# Definimos una carpeta 'data' para mantener el proyecto organizado.
RUTA_DATA = 'data'
RUTA_CSV = os.path.join(RUTA_DATA, 'mediciones_hidro.csv')
RUTA_EXCEL = os.path.join(RUTA_DATA, 'mediciones_hidro.xlsx')
# Usamos SQLite para una base de datos simple basada en archivos.
# 'sqlite:///' es el prefijo que SQLAlchemy usa para archivos locales.
RUTA_DB_ENGINE = f'sqlite:///{os.path.join(RUTA_DATA, "hidro.db")}'
RUTA_DB_FILE = os.path.join(RUTA_DATA, "hidro.db") # Ruta para conexión directa

# Asegurarse de que la carpeta 'data' exista
os.makedirs(RUTA_DATA, exist_ok=True)


def simular_datos():
    """
    Crea un DataFrame de pandas con datos simulados de mediciones.
    
    Simula nivel, caudal y generación con estacionalidad y ruido
    para cada central definida en CENTRALES.
    
    Retorna:
        pd.DataFrame: Un DataFrame con todos los datos históricos simulados.
    """
    print(f"Iniciando simulación de datos desde {FECHA_INICIO.date()} hasta {FECHA_HOY.date()}...")
    datos_simulados = []
    
    # Iteramos por cada central definida en el diccionario
    for central, info in CENTRALES.items():
        
        # Iteramos por cada día en nuestro rango de simulación
        for i in range(N_DIAS_HISTORICOS):
            fecha = FECHA_INICIO + datetime.timedelta(days=i)
            
            # --- Simulación de Variables ---
            # 1. Estacionalidad: Creamos un ciclo anual (senoide) para simular
            #    temporadas de lluvia (valores altos) y sequía (valores bajos).
            #    (i / 365.25) * 2 * np.pi -> convierte el día en una posición del círculo (radianes)
            estacionalidad = np.sin((i / 365.25) * 2 * np.pi - np.pi / 2) # Senoide anual
            
            # 2. Nivel (msnm): Es la variable clave.
            nivel_base = info['nivel_max_msnm'] * 0.75 # Asumimos un nivel promedio del 75%
            ruido = np.random.rand() * 0.1 - 0.05 # Pequeña variación aleatoria diaria
            # El nivel final es el promedio + estacionalidad + ruido
            nivel_actual = nivel_base * (1 + 0.2 * estacionalidad + ruido)
            
            # 3. Caudal (m3/s): Relacionado con la estacionalidad (lluvia).
            caudal_entrada = 150 + 100 * estacionalidad + np.random.uniform(-20, 20)
            
            # 4. Generación (MW): Depende de la capacidad de la central y del nivel del agua.
            #    Un nivel más alto significa más presión/potencial de generación.
            factor_gen = (nivel_actual / info['nivel_max_msnm']) * np.random.uniform(0.7, 1.0)
            generacion_mw = info['capacidad_MWh'] * factor_gen
            
            # Agregamos los datos de este día a nuestra lista
            datos_simulados.append({
                'id_central': central,
                'fecha_hora': fecha,
                'nivel_msnm': round(nivel_actual, 2),
                'caudal_entrada_m3s': round(max(0, caudal_entrada), 2), # Asegurar que no sea negativo
                'generacion_mw': round(max(0, generacion_mw), 2), # Asegurar que no sea negativo
            })

    # Convertimos la lista de diccionarios en un DataFrame de Pandas
    df = pd.DataFrame(datos_simulados)
    print(f"Simulación completada. Generados {len(df)} registros.")
    return df

def guardar_datos(df_mediciones):
    """
    Guarda el DataFrame de mediciones en CSV, Excel y SQLite.
    También crea una tabla 'Centrales' en la BD.
    
    Args:
        df_mediciones (pd.DataFrame): DataFrame con las mediciones simuladas.
    """
    print(f"Guardando datos en {RUTA_CSV}, {RUTA_EXCEL}, y {RUTA_DB_FILE}...")
    
    # 1. Guardar en CSV
    df_mediciones.to_csv(RUTA_CSV, index=False)
    
    # 2. Guardar en Excel (Opcional, puede ser lento para muchos datos)
    df_mediciones.to_excel(RUTA_EXCEL, index=False) 

    # 3. Guardar en Base de Datos SQLite
    # SQLAlchemy provee una forma estándar de interactuar con bases de datos SQL.
    engine = create_engine(RUTA_DB_ENGINE)
    
    # --- Crear y guardar la tabla de Centrales ---
    # Convertimos el diccionario CENTRALES en un DataFrame
    df_centrales = pd.DataFrame.from_dict(CENTRALES, orient='index')
    # El índice (nombre de la central) se convierte en la columna 'id_central'
    df_centrales.index.name = 'id_central'
    # Guardamos este DataFrame en la BD en la tabla 'Centrales'.
    # if_exists='replace' borra la tabla si ya existe y la crea de nuevo.
    df_centrales.to_sql('Centrales', engine, if_exists='replace')
    
    # --- Guardar la tabla de Mediciones ---
    # Guardamos las mediciones simuladas en la tabla 'Mediciones'.
    # 'index_label' define el nombre de la columna de clave primaria en la BD.
    df_mediciones.to_sql('Mediciones', engine, if_exists='replace', index_label='id_medicion')
    
    print("Datos guardados exitosamente en la base de datos.")
    
    # --- Verificación (Opcional pero recomendado) ---
    # Nos conectamos directamente para hacer una consulta SQL y verificar.
    try:
        conn = sqlite3.connect(RUTA_DB_FILE)
        print("\n--- Verificación de Base de Datos ---")
        print("Tabla 'Centrales' (primeras 3 filas):")
        print(pd.read_sql("SELECT * FROM Centrales LIMIT 3", conn))
        print("\nTabla 'Mediciones' (últimas 3 filas):")
        # Mostramos las últimas filas para confirmar que los datos llegan hasta hoy
        print(pd.read_sql(f"SELECT * FROM Mediciones ORDER BY fecha_hora DESC LIMIT 3", conn))
        conn.close()
    except Exception as e:
        print(f"Error durante la verificación de la BD: {e}")


# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    """
    Este bloque se ejecuta solo cuando corres el script directamente
    (ejecutando: `python src/data_ingestion.py`)
    No se ejecutará si otro script importa este archivo (ej. `import data_ingestion`).
    """
    # Paso 1: Generar los datos en memoria
    datos_simulados = simular_datos()
    
    # Paso 2: Guardar los datos en los archivos de salida
    guardar_datos(datos_simulados)
```

**Para ejecutar este script:**
(Asegúrate de tener tu `venv` activado)

```bash
python src/data_ingestion.py
```

Verás archivos nuevos en tu carpeta `data/`.

-----

### Sección 3: Código de Machine Learning (Entrenamiento)

Este script cargará los datos, creará características (features) y entrenará un modelo para predecir el `nivel_msnm`.

**Copia este código en `src/model_training.py`:**

```python
"""
Módulo de Entrenamiento del Modelo de ML.

Este script es responsable de:
1. Cargar los datos históricos desde la base de datos (o CSV).
2. Realizar la ingeniería de características (feature engineering).
3. Entrenar un modelo de Regresión (ej. RandomForest).
4. Guardar el modelo entrenado en la carpeta /models.
"""

import pandas as pd
import sqlite3
import joblib # Para guardar el modelo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# --- Configuración ---
RUTA_DB = 'data/hidro.db'
RUTA_MODELO = 'models/modelo_prediccion_nivel.pkl'
TARGET_VARIABLE = 'nivel_msnm' # Lo que queremos predecir

def cargar_datos():
    """
    Carga los datos de mediciones desde la base de datos SQLite.
    
    Retorna:
        pd.DataFrame: DataFrame con todas las mediciones.
    """
    print("Cargando datos desde la BD...")
    try:
        conn = sqlite3.connect(RUTA_DB)
        # Cargamos datos de todas las centrales
        query = "SELECT * FROM Mediciones"
        df = pd.read_sql(query, conn, parse_dates=['fecha_hora'])
        conn.close()
        return df
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return pd.DataFrame()

def ingenieria_de_caracteristicas(df):
    """
    Crea nuevas características (features) para el modelo.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos crudos.
        
    Retorna:
        pd.DataFrame: DataFrame con las nuevas features añadidas.
    """
    print("Iniciando ingeniería de características...")
    # Aseguramos el orden por fecha
    df = df.sort_values(by=['id_central', 'fecha_hora']).copy()
    
    # Creamos 'lags' (valores de días anteriores)
    # Agrupamos por central para que los lags no se "crucen" entre centrales
    df['nivel_lag_1'] = df.groupby('id_central')[TARGET_VARIABLE].shift(1)
    df['nivel_lag_7'] = df.groupby('id_central')[TARGET_VARIABLE].shift(7)
    df['caudal_lag_1'] = df.groupby('id_central')['caudal_entrada_m3s'].shift(1)
    
    # Características basadas en la fecha
    df['dia_del_ano'] = df['fecha_hora'].dt.dayofyear
    df['mes'] = df['fecha_hora'].dt.month
    
    # Variable categórica para la central
    # Convertimos 'id_central' en dummies (One-Hot Encoding)
    df_dummies = pd.get_dummies(df['id_central'], prefix='central')
    df = pd.concat([df, df_dummies], axis=1)
    
    # Eliminamos filas con NaN (creadas por los lags)
    df = df.dropna()
    
    print("Features creadas:", df.columns.tolist())
    return df

def entrenar_modelo(df):
    """
    Entrena un modelo RandomForestRegressor y lo guarda.
    
    Args:
        df (pd.DataFrame): DataFrame con todas las features y el target.
    """
    print("Iniciando entrenamiento del modelo...")
    
    # 1. Definir features (X) y target (y)
    # Seleccionamos todas las columnas excepto el target y columnas no numéricas
    features = [
        'nivel_lag_1', 'nivel_lag_7', 'caudal_lag_1', 'dia_del_ano', 'mes',
        'central_Guatape', 'central_Ituango', 'central_Playas', 'central_SanCarlos'
    ]
    X = df[features]
    y = df[TARGET_VARIABLE]
    
    # 2. Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Inicializar y entrenar el modelo
    # RandomForest es bueno porque maneja bien diferentes escalas de features
    # n_estimators=50 y max_depth=10 para que sea rápido (en un caso real, usaríamos más)
    modelo = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    modelo.fit(X_train, y_train)
    
    # 4. Evaluar el modelo
    y_pred = modelo.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"\nEntrenamiento completado.")
    print(f"RMSE (Error cuadrático medio) en datos de prueba: {rmse:.2f} msnm")
    
    # 5. Guardar el modelo entrenado
    print(f"Guardando modelo en {RUTA_MODELO}...")
    joblib.dump(modelo, RUTA_MODELO)
    print("Modelo guardado.")

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    df_datos = cargar_datos()
    if not df_datos.empty:
        df_features = ingenieria_de_caracteristicas(df_datos)
        entrenar_modelo(df_features)
```

**Para ejecutar este script:**

```bash
python src/model_training.py
```

Verás un archivo `modelo_prediccion_nivel.pkl` en tu carpeta `models/`.   
Más información en: https://github.com/evalenciEAFIT/formacion_python/blob/main/ML/nivel6/pkl.md

-----

### Sección 4: Código de Machine Learning (Predicción)

Este script carga el modelo entrenado y genera las predicciones futuras (7, 15, 30 días).

**Copia este código en `src/model_prediction.py`:**

```python
"""
Módulo de Generación de Predicciones.

Este script es responsable de:
1. Cargar el modelo entrenado desde /models.
2. Cargar los últimos datos reales desde la BD.
3. Generar las features futuras (simuladas, ya que no tenemos pronóstico de clima).
4. Generar predicciones a 7, 15 y 30 días.
5. Guardar estas predicciones en la BD (o un CSV).
"""

import pandas as pd
import numpy as np
import joblib
import sqlite3
import datetime
from sqlalchemy import create_engine
import os

# --- Configuración ---
RUTA_DATA = 'data'
RUTA_DB = os.path.join(RUTA_DATA, 'hidro.db')
RUTA_MODELO = os.path.join('models', 'modelo_prediccion_nivel.pkl')
DIAS_A_PREDECIR = [7, 15, 30] # Días en el futuro
CENTRALES = ['Guatape', 'Ituango', 'Playas', 'SanCarlos']

def cargar_ultimos_datos_y_modelo():
    """
    Carga el modelo entrenado y los últimos datos necesarios 
    para inicializar las predicciones (los últimos 7 días).
    
    Retorna:
        (modelo, df_ultimos_datos)
    """
    print("Cargando modelo y datos recientes...")
    modelo = joblib.load(RUTA_MODELO)
    
    conn = sqlite3.connect(RUTA_DB)
    # Necesitamos al menos 7 días de datos para el 'nivel_lag_7'
    # Cargamos 10 por seguridad.
    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    query = f"SELECT * FROM Mediciones WHERE fecha_hora >= '{fecha_limite}'"
    df_ultimos = pd.read_sql(query, conn, parse_dates=['fecha_hora'])
    conn.close()
    
    return modelo, df_ultimos

def generar_predicciones(modelo, df_historico):
    """
    Genera predicciones futuras para todas las centrales.
    
    IMPORTANTE: En un proyecto real, aquí se consumiría la API
    del pronóstico del clima (IDEAM) para los próximos 30 días.
    Como no tenemos eso, vamos a simular un caudal promedio.
    
    Args:
        modelo: El modelo de ML cargado.
        df_historico (pd.DataFrame): Datos históricos recientes.
        
    Retorna:
        pd.DataFrame: Un DataFrame con las predicciones futuras.
    """
    print("Generando predicciones futuras...")
    predicciones_futuras = []
    hoy = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Definimos las features que el modelo espera
    features_modelo = [
        'nivel_lag_1', 'nivel_lag_7', 'caudal_lag_1', 'dia_del_ano', 'mes',
        'central_Guatape', 'central_Ituango', 'central_Playas', 'central_SanCarlos'
    ]
    
    for central in CENTRALES:
        # 1. Obtenemos el historial de esta central
        df_central = df_historico[df_historico['id_central'] == central].copy()
        df_central = df_central.sort_values(by='fecha_hora')
        
        # 2. Simulamos el caudal futuro (aquí iría el pronóstico real)
        caudal_simulado_futuro = df_central['caudal_entrada_m3s'].mean() # Simulación simple
        
        # 3. Iteramos para predecir día a día (predicción autoregresiva)
        # Usamos un 'lookback_data' para ir actualizando con las predicciones
        lookback_data = df_central.set_index('fecha_hora').to_dict('index')

        # Convertimos las fechas del índice a objetos datetime.date puros para la búsqueda
        # Esto fue clave para arreglar el KeyError anterior
        lookback_dates = {k.date(): v for k, v in lookback_data.items()}

        for i in range(1, max(DIAS_A_PREDECIR) + 1):
            fecha_futura = hoy + datetime.timedelta(days=i)
            
            # --- Crear features para la fecha_futura ---
            fecha_lag_1 = (fecha_futura - datetime.timedelta(days=1)).date()
            fecha_lag_7 = (fecha_futura - datetime.timedelta(days=7)).date()

            # Obtenemos los valores de lag (del historial o de predicciones previas)
            nivel_lag_1 = lookback_dates[fecha_lag_1]['nivel_msnm']
            nivel_lag_7 = lookback_dates[fecha_lag_7]['nivel_msnm']
            caudal_lag_1 = lookback_dates[fecha_lag_1].get('caudal_entrada_m3s', caudal_simulado_futuro)
            
            # --- ### INICIO DE LA CORRECCIÓN ### ---
            # Features de fecha
            # Los objetos datetime.datetime no tienen .dayofyear
            # Se debe usar .timetuple().tm_yday
            dia_del_ano = fecha_futura.timetuple().tm_yday
            mes = fecha_futura.month
            # --- ### FIN DE LA CORRECCIÓN ### ---
            
            # Features de la central (One-Hot)
            central_Guatape = 1 if central == 'Guatape' else 0
            central_Ituango = 1 if central == 'Ituango' else 0
            central_Playas = 1 if central == 'Playas' else 0
            central_SanCarlos = 1 if central == 'SanCarlos' else 0

            # 4. Crear el vector de features para el modelo
            features_input = pd.DataFrame([[
                nivel_lag_1, nivel_lag_7, caudal_lag_1, dia_del_ano, mes,
                central_Guatape, central_Ituango, central_Playas, central_SanCarlos
            ]], columns=features_modelo)
            
            # 5. Predecir
            prediccion = modelo.predict(features_input)[0]
            
            # 6. Guardar la predicción para usarla en el siguiente 'lag'
            lookback_dates[fecha_futura.date()] = {
                'nivel_msnm': prediccion,
                'caudal_entrada_m3s': caudal_simulado_futuro # Caudal simulado
            }
            
            # 7. Almacenar solo los días que nos interesan (7, 15, 30)
            if i in DIAS_A_PREDECIR:
                predicciones_futuras.append({
                    'id_central': central,
                    'fecha_prediccion': fecha_futura,
                    'dias_futuro': i,
                    'nivel_predicho_msnm': round(prediccion, 2)
                })
                
    return pd.DataFrame(predicciones_futuras)

def guardar_predicciones(df_predicciones):
    """
    Guarda las predicciones generadas en la base de datos.
    """
    print("Guardando predicciones en la base de datos...")
    # Aseguramos que la ruta de la BD sea correcta
    db_path = os.path.join(RUTA_DATA, 'hidro.db')
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Sobrescribimos la tabla de predicciones cada vez que corre
    df_predicciones.to_sql('Predicciones', engine, if_exists='replace', index=False)
    
    print("Predicciones guardadas.")
    # Verificación
    with engine.connect() as conn:
        print("\nVerificación de BD (Tabla Predicciones):")
        print(pd.read_sql("SELECT * FROM Predicciones LIMIT 5", conn))

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    modelo_cargado, df_hist = cargar_ultimos_datos_y_modelo()
    df_preds = generar_predicciones(modelo_cargado, df_hist)
    guardar_predicciones(df_preds)
```

**Para ejecutar este script:**

```bash
python src/model_prediction.py
```

Esto creará o actualizará la tabla `Predicciones` en tu archivo `data/hidro.db`.

-----

### Sección 5: Dashboard Interactivo

Este script utiliza `Dash` y `Plotly` para crear la visualización web.

**Copia este código en `dashboard/app.py`:**

```python
"""
Dashboard Interactivo con Dash y Leaflet.

Este script es el punto central de la aplicación web. Se encarga de:
1. Cargar los datos (reales y predichos) desde la base de datos.
2. Definir la estructura visual (Layout) del dashboard usando componentes Dash.
3. Crear un mapa interactivo con Dash-Leaflet.
4. Definir la interactividad (Callbacks) para que al hacer clic en el mapa,
   el gráfico de series de tiempo se actualice.
"""

# --- 1. IMPORTACIÓN DE LIBRERÍAS ---

import dash
# Componentes principales de Dash: dcc (componentes de control como gráficos, sliders)
# y html (componentes HTML como Div, H1, etc.)
from dash import dcc, html
# Dependencias para los Callbacks (Input, Output) y el patrón 'ALL'
from dash.dependencies import Input, Output, ALL
import plotly.graph_objects as go # Para crear las figuras (gráficos de líneas)
import pandas as pd # Para la manipulación y análisis de datos (DataFrames)
import sqlite3 # Para conectarnos a la base de datos SQLite
import datetime # Para manejar objetos de fecha y hora
import numpy as np # Para crear arrays (usado en una versión anterior, pero se mantiene por si acaso)
import os # Para construir rutas de archivos (ej. os.path.join) que funcionen en cualquier S.O.
import json # Para procesar la información del callback de Leaflet

# Importamos la biblioteca Dash-Leaflet para el mapa
import dash_leaflet as dl 


# --- 2. CONFIGURACIÓN Y CARGA DE DATOS ---

# Definimos la ruta a la carpeta de datos
RUTA_DATA = 'data'
# Construimos la ruta al archivo de la base de datos de forma segura
RUTA_DB = os.path.join(RUTA_DATA, 'hidro.db')

def cargar_datos_dashboard():
    """
    Carga todos los datos necesarios para el dashboard desde la BD.
    
    PARA QUÉ: Centralizar toda la lógica de lectura de datos en una sola función.
    POR QUÉ: Mantiene el código limpio y permite recargar datos fácilmente si fuera necesario.
    """
    
    # Nos conectamos a la BD en modo 'read-only' (ro).
    # POR QUÉ: Es una buena práctica de seguridad para un dashboard,
    # asegura que esta aplicación no pueda modificar los datos.
    conn = sqlite3.connect(f'file:{RUTA_DB}?mode=ro', uri=True) 
    
    # Leemos la tabla de centrales (info estática: lat, lon, capacidad)
    df_centrales = pd.read_sql("SELECT * FROM Centrales", conn)
    
    # Calculamos la fecha de hoy menos 90 días para limitar la carga de datos
    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    # Preparamos la consulta SQL para obtener solo el historial reciente
    query_hist = f"SELECT * FROM Mediciones WHERE fecha_hora >= '{fecha_limite}'"
    # Leemos los datos históricos, convirtiendo 'fecha_hora' a objeto datetime
    df_historico = pd.read_sql(query_hist, conn, parse_dates=['fecha_hora'])
    
    # Leemos la tabla de predicciones
    df_predicciones = pd.read_sql("SELECT * FROM Predicciones", conn, parse_dates=['fecha_prediccion'])
    
    # Cerramos la conexión a la BD
    conn.close()
    
    # --- Procesamiento de Datos ---
    
    # Unimos (merge) los datos históricos con los de las centrales.
    # PARA QUÉ: Para tener el 'nivel_max_msnm' en el mismo DataFrame que el 'nivel_msnm'.
    # POR QUÉ: Necesitamos ambos valores para calcular el porcentaje.
    df_historico = pd.merge(df_historico, df_centrales[['id_central', 'nivel_max_msnm']], on='id_central')
    
    # Calculamos el nivel como porcentaje.
    # POR QUÉ: Es una métrica normalizada (0-100) fácil de visualizar y colorear en el mapa.
    df_historico['nivel_pct'] = (df_historico['nivel_msnm'] / df_historico['nivel_max_msnm']) * 100

    # Creamos el DataFrame para el mapa (df_mapa)
    if not df_historico.empty:
        # Obtenemos el registro más reciente de CADA central.
        # .groupby('id_central')['fecha_hora'].idxmax() encuentra el índice del valor máximo (fecha más reciente) para cada grupo.
        # .loc[] usa esos índices para seleccionar las filas completas.
        df_mapa = df_historico.loc[df_historico.groupby('id_central')['fecha_hora'].idxmax()]
        
        # Le añadimos la latitud y longitud a estos últimos registros.
        df_mapa = pd.merge(df_mapa, df_centrales[['id_central', 'lat', 'lon']], on='id_central')
    else:
        # Si no hay datos históricos, creamos un DataFrame vacío con las columnas esperadas.
        # POR QUÉ: Para evitar que la aplicación falle si la BD está vacía.
        df_mapa = pd.DataFrame(columns=['lat', 'lon', 'nivel_pct', 'id_central', 'nivel_msnm'])

    return df_centrales, df_historico, df_predicciones, df_mapa

# --- 3. PREPARACIÓN INICIAL DE DATOS Y MAPA ---

# Ejecutamos la función de carga UNA VEZ cuando la aplicación se inicia.
df_centrales, df_historico, df_predicciones, df_mapa = cargar_datos_dashboard()

# --- Funciones auxiliares para el mapa Leaflet ---

def get_color_para_mapa(pct):
    """
    Retorna un color (string) basado en el porcentaje de nivel.
    PARA QUÉ: Para asignar un color de estado (rojo, naranja, verde) a cada marcador.
    """
    if pct > 80:
        return "green"
    if pct > 50:
        return "orange"
    return "red"

def crear_marcadores_mapa(df_mapa):
    """
    Crea una lista de componentes dl.CircleMarker a partir del DataFrame df_mapa.
    PARA QUÉ: Para generar los puntos que se mostrarán en el mapa.
    """
    marcadores = []
    # Iteramos sobre cada fila del DataFrame que contiene el último estado de cada central
    for _, row in df_mapa.iterrows():
        color = get_color_para_mapa(row['nivel_pct'])
        
        # Creamos un Marcador Circular
        marker = dl.CircleMarker(
            center=[row['lat'], row['lon']], # Posición [latitud, longitud]
            color=color, # Color del borde
            fill=True, # Rellenar el círculo
            fillOpacity=0.8, # Opacidad del relleno
            radius=10, # Tamaño del círculo
            
            # --- ID de Diccionario (CLAVE PARA EL CALLBACK) ---
            # PARA QUÉ: Asignar un ID único y estructurado a cada marcador.
            # POR QUÉ: Esto permite que nuestro callback use un "patrón"
            # (type='map-marker') para "escuchar" los clics de TODOS los marcadores,
            # y luego usar el 'name' para saber CUÁL fue clickeado.
            id={
                'type': 'map-marker', # Tipo de componente
                'name': row['id_central'] # ID único (nombre de la central)
            },
            children=[
                # Tooltip: Texto que aparece al pasar el mouse por encima
                dl.Tooltip(f"{row['id_central']}: {row['nivel_pct']:.1f}%")
            ]
        )
        marcadores.append(marker)
    return marcadores

# Creamos la lista de marcadores al iniciar la app.
marcadores_leaflet = crear_marcadores_mapa(df_mapa)

# --- 4. CONFIGURACIÓN DE CAPAS DE MAPA ---

# URLs de los "Tiles" (las "baldosas" o imágenes que componen el mapa)
# POR QUÉ: Usamos proveedores gratuitos (CARTO, OpenStreetMap, Esri)
# que no requieren un Token/llave de API, solucionando el problema del mapa en blanco.
url_claro = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
url_oscuro = "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
url_callejero = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
url_satelite = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"

# Textos de atribución (requeridos por los proveedores de mapas)
attr_carto = '&copy; <a href="https://carto.com/attributions">CARTO</a>'
attr_osm = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
attr_esri = 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye...'


# --- 5. INICIALIZACIÓN Y LAYOUT DE LA APP DASH ---

# Creamos la instancia de la aplicación Dash
app = dash.Dash(__name__)
app.title = "Dashboard Hidroeléctricas EPM" # Título en la pestaña del navegador

# --- Layout (Estructura Visual) ---
# Define la apariencia de la página usando componentes HTML y Dash
app.layout = html.Div(
    # 'style' aplica CSS. Aquí definimos la fuente y un padding general.
    style={'fontFamily': 'Arial, sans-serif', 'padding': '10px'}, 
    children=[ # 'children' contiene los componentes "hijos" de este Div
    
        # Título principal
        html.H1(children='Dashboard de Monitoreo Hidroeléctricas'),
        # Línea horizontal
        html.Hr(),
        
        # Contenedor de Fila (para las dos columnas)
        html.Div(
            className='row', # Un nombre de clase (para CSS opcional)
            # Usamos 'display: flex' para crear un layout de columnas flexibles
            style={'display': 'flex'}, 
            children=[
                
                # --- Columna Izquierda: Mapa ---
                html.Div(
                    style={'width': '40%', 'padding': '10px'}, # Esta columna ocupa el 40%
                    children=[
                        html.H3('Mapa de Centrales'),
                        
                        # --- El Mapa Leaflet ---
                        dl.Map(
                            center=[6.5, -75], # Centro inicial del mapa (Colombia)
                            zoom=6, # Nivel de zoom inicial
                            style={'height': '500px'}, # Altura fija (IMPORTANTE para que se vea)
                            children=[
                                # --- Controlador de Capas ---
                                # PARA QUÉ: Muestra un icono en la esquina que
                                # permite al usuario cambiar el mapa base.
                                dl.LayersControl(
                                    [
                                        # Capa Base 1: Claro
                                        dl.BaseLayer( # Define una opción en el controlador
                                            # El mapa en sí
                                            dl.TileLayer(url=url_claro, attribution=attr_carto),
                                            name="Claro", # Nombre en el menú
                                            checked=True # Esta es la capa por defecto
                                        ),
                                        # Capa Base 2: Oscuro
                                        dl.BaseLayer(
                                            dl.TileLayer(url=url_oscuro, attribution=attr_carto),
                                            name="Oscuro",
                                            checked=False
                                        ),
                                        # Capa Base 3: Callejero
                                        dl.BaseLayer(
                                            dl.TileLayer(url=url_callejero, attribution=attr_osm),
                                            name="Callejero",
                                            checked=False
                                        ),
                                        # Capa Base 4: Satélite
                                        dl.BaseLayer(
                                            dl.TileLayer(url=url_satelite, attribution=attr_esri),
                                            name="Satélite",
                                            checked=False
                                        ),
                                    ]
                                ),
                                # --- Capa de Marcadores ---
                                # Esta capa "flota" encima del mapa base
                                dl.LayerGroup(children=marcadores_leaflet)
                            ]
                        )
                    ]
                ),
                
                # --- Columna Derecha: Gráfico ---
                html.Div(
                    style={'width': '60%', 'padding': '10px'}, # Esta columna ocupa el 60%
                    children=[
                        # Título dinámico (se actualiza por el callback)
                        html.H3(id='titulo-grafico-detalle', children='Detalle de Central'),
                        
                        # El Gráfico (inicialmente vacío)
                        dcc.Graph(
                            id='grafico-detalle', # ID para que el callback lo controle
                            style={'height': '500px'} # Altura fija
                        )
                    ]
                )
            ]
        )
    ]
)


# --- 6. CALLBACKS (Interactividad) ---

# El "decorador" @app.callback conecta Inputs y Outputs con una función.
@app.callback(
    # Salidas (Outputs): Qué componentes vamos a actualizar
    [
        # Actualiza la propiedad 'figure' (el gráfico) del componente 'grafico-detalle'
        Output('grafico-detalle', 'figure'),
        # Actualiza la propiedad 'children' (el texto) del componente 'titulo-grafico-detalle'
        Output('titulo-grafico-detalle', 'children')
    ],
    # Entradas (Inputs): Qué componentes van a disparar esta función
    [
        # --- Patrón "Pattern-Matching Callback" ---
        # Input: Escucha la propiedad 'n_clicks' (número de clics) de...
        # ...TODOS los componentes cuyo ID coincida con el diccionario
        # {'type': 'map-marker', 'name': ALL}
        # 'ALL' es un comodín que captura todos los nombres.
        Input({'type': 'map-marker', 'name': ALL}, 'n_clicks')
    ]
)
def actualizar_grafico_detalle(marker_n_clicks):
    """
    Esta función se ejecuta CADA VEZ que un Input cambia (o sea, se hace clic en un marcador).
    
    PARA QUÉ: Para actualizar el gráfico de líneas y el título.
    POR QUÉ: Es el "cerebro" de la interactividad del dashboard.
    """
    
    # 'dash.callback_context' nos da información sobre qué disparó el callback
    ctx = dash.callback_context

    # --- Determinar qué central seleccionar ---
    
    if not ctx.triggered:
        # 'ctx.triggered' está vacío en la carga inicial (antes de cualquier clic)
        # Seleccionamos la primera central de la lista como valor por defecto.
        if not df_centrales.empty:
            central_seleccionada = df_centrales['id_central'].iloc[0]
        else:
            central_seleccionada = "Ninguna Central"
    else:
        # Si 'ctx.triggered' NO está vacío, significa que un usuario hizo clic.
        
        # 1. Obtenemos el ID del componente que disparó el callback.
        #    Viene como un string JSON: '{"name":"Guatape","type":"map-marker"}.n_clicks'
        button_id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # 2. Convertimos ese string JSON a un diccionario Python
        #    Ej: {'name': 'Guatape', 'type': 'map-marker'}
        button_id_dict = json.loads(button_id_str)
        
        # 3. Extraemos el nombre de la central de ese diccionario
        central_seleccionada = button_id_dict['name']
    
    # --- Generación del Gráfico ---
        
    # Actualizamos el título
    titulo = f"Detalle y Predicción: {central_seleccionada}"
    
    # Creamos una figura vacía de Plotly
    fig = go.Figure()
    
    # Filtramos los DataFrames para obtener solo los datos de la central seleccionada
    df_hist_filtrado = df_historico[df_historico['id_central'] == central_seleccionada]
    df_pred_filtrado = df_predicciones[df_predicciones['id_central'] == central_seleccionada]
    
    # Solo dibujamos si encontramos datos históricos
    if not df_hist_filtrado.empty:
        # Obtenemos los niveles máximo y crítico para esta central
        nivel_max = df_centrales[df_centrales['id_central'] == central_seleccionada]['nivel_max_msnm'].iloc[0]
        nivel_critico = nivel_max * 0.4 # Asumimos 40% como crítico
        
        # Trazo 1: Línea de datos históricos
        fig.add_trace(go.Scatter(
            x=df_hist_filtrado['fecha_hora'],
            y=df_hist_filtrado['nivel_msnm'],
            mode='lines',
            name='Nivel Histórico (Real)',
            line=dict(color='blue')
        ))
        
        # Trazo 2: Puntos de predicción
        fig.add_trace(go.Scatter(
            x=df_pred_filtrado['fecha_prediccion'],
            y=df_pred_filtrado['nivel_predicho_msnm'],
            mode='markers', # 'markers' = solo puntos
            name='Predicción ML',
            marker=dict(color='red', size=10, symbol='x') # Marcador 'x' rojo
        ))
        
        # Trazo 3: Línea de umbral (Nivel Máximo)
        fig.add_hline(y=nivel_max, line_dash="dot", line_color="green",
                      annotation_text="Nivel Máximo", annotation_position="bottom right")
        # Trazo 4: Línea de umbral (Nivel Crítico)
        fig.add_hline(y=nivel_critico, line_dash="dot", line_color="red",
                      annotation_text="Nivel Crítico", annotation_position="bottom right")
    else:
        # Si no hay datos, muestra un mensaje en el gráfico
        fig.update_layout(
            annotations=[dict(text="No hay datos disponibles para esta central", 
                              xref="paper", yref="paper",
                              showarrow=False, font=dict(size=16))]
        )
    
    # Configuraciones de layout del gráfico (títulos de ejes, leyenda)
    fig.update_layout(
        title=f"Nivel del Embalse (msnm)",
        xaxis_title="Fecha",
        yaxis_title="Nivel (msnm)",
        legend_title="Leyenda",
        hovermode="x unified" # Muestra info de todas las trazas al pasar el mouse
    )
    
    # Retornamos los nuevos valores para los 'Outputs'
    return fig, titulo


# --- 7. PUNTO DE ENTRADA PRINCIPAL ---

# `if __name__ == '__main__':`
# Este bloque solo se ejecuta cuando corres el script directamente
# (ej. `python dashboard/app.py`)
# No se ejecuta si este archivo es importado por otro.
if __name__ == '__main__':
    
    # Definimos las rutas a los scripts de datos
    script_ingestion = os.path.join("src", "data_ingestion.py")
    script_training = os.path.join("src", "model_training.py")
    script_prediction = os.path.join("src", "model_prediction.py")
    
    print("Asegurando que los datos y modelos están actualizados...")
    
    # --- Ejecución de scripts de datos ---
    # PARA QUÉ: Asegurar que los datos (simulados) y el modelo (entrenado)
    # estén frescos CADA VEZ que se inicia el dashboard.
    # POR QUÉ: Esto es útil para desarrollo. En producción, estos scripts
    # correrían por separado (ej. una vez al día) y el dashboard solo leería.
    
    print(f"Ejecutando {script_ingestion}...")
    os.system(f'python {script_ingestion}')
    
    print(f"Ejecutando {script_training}...")
    os.system(f'python {script_training}')
    
    print(f"Ejecutando {script_prediction}...")
    os.system(f'python {script_prediction}')
    
    # --- Iniciar el servidor web ---
    print("\nLanzando el servidor del Dashboard en http://127.0.0.1:8050/")
    # 'debug=True' activa el modo de depuración:
    # 1. El servidor se reinicia automáticamente cuando guardas cambios en el código.
    # 2. Muestra errores detallados en el navegador.
    app.run(debug=True)
```

**Para ejecutar este script:**
(El script ejecutará automáticamente la ingesta y predicción antes de iniciar)

```bash
python dashboard/app.py
```

Abre tu navegador en `http://127.0.0.1:8050/`.

-----

### Sección 6: Generación de Reportes PDF

Este script genera los gráficos estáticos y los ensambla en un PDF.

**Copia este código en `src/report_generator.py`:**

```python
"""
Módulo de Generación de Reportes (HTML y PDF).

--- VERSIÓN CON ACTUALIZACIÓN DE DATOS ---
- Se añaden los comandos 'os.system' para refrescar los datos
  (data_ingestion, model_training, model_prediction)
  antes de que el reporte se genere.
"""

import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.io as pio
import datetime
import os
import traceback # Para imprimir errores detallados

try:
    from xhtml2pdf import pisa
    XHTML2PDF_DISPONIBLE = True
except ImportError:
    print("************************************************************")
    print("ALERTA: No se pudo importar 'xhtml2pdf'.")
    print("Por favor, instálala con: pip install xhtml2pdf")
    print("La generación de PDF estará deshabilitada.")
    print("************************************************************")
    XHTML2PDF_DISPONIBLE = False

# --- Configuración (Sin cambios) ---
RUTA_DB = os.path.join('data', 'hidro.db')
RUTA_REPORTES = 'reportes'
RUTA_IMAGENES = os.path.join(RUTA_REPORTES, 'img')
FECHA_HOY = datetime.datetime.now().strftime('%Y-%m-%d')
NOMBRE_REPORTE_HTML = f'Reporte_Hidro_EPM_{FECHA_HOY}.html'
NOMBRE_REPORTE_PDF = f'Reporte_Hidro_EPM_{FECHA_HOY}.pdf'

os.makedirs(RUTA_REPORTES, exist_ok=True)
os.makedirs(RUTA_IMAGENES, exist_ok=True)


def cargar_datos_reporte():
    """Carga los datos de la BD (igual que el dashboard)."""
    print("Cargando datos frescos de la Base de Datos...")
    db_path = os.path.join('data', 'hidro.db')
    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
    df_centrales = pd.read_sql("SELECT * FROM Centrales", conn)
    
    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    query_hist = f"SELECT * FROM Mediciones WHERE date(fecha_hora) >= '{fecha_limite}'"
    df_historico = pd.read_sql(query_hist, conn, parse_dates=['fecha_hora'])
    
    df_predicciones = pd.read_sql("SELECT * FROM Predicciones", conn, parse_dates=['fecha_prediccion'])
    conn.close()
    
    print(f"Cargados {len(df_historico)} registros históricos.")
    
    df_historico = pd.merge(df_historico, df_centrales, on='id_central')
    df_historico['nivel_pct'] = (df_historico['nivel_msnm'] / df_historico['nivel_max_msnm']) * 100
    
    df_estado_actual = pd.DataFrame()
    if not df_historico.empty:
        df_estado_actual = df_historico.loc[df_historico.groupby('id_central')['fecha_hora'].idxmax()]
    
    return df_centrales, df_historico, df_predicciones, df_estado_actual

def generar_grafico_estatico(central, df_hist, df_pred, df_centrales):
    """Genera un gráfico PNG estático."""
    print(f"Generando gráfico para {central}...")
    df_h = df_hist[df_hist['id_central'] == central]
    df_p = df_pred[df_pred['id_central'] == central]
    
    if df_centrales[df_centrales['id_central'] == central].empty:
        return None
        
    info = df_centrales[df_centrales['id_central'] == central].iloc[0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_h['fecha_hora'], y=df_h['nivel_msnm'], mode='lines', name='Histórico'))
    fig.add_trace(go.Scatter(x=df_p['fecha_prediccion'], y=df_p['nivel_predicho_msnm'], mode='markers', name='Predicción', marker=dict(color='red', size=8)))
    fig.add_hline(y=info['nivel_max_msnm'], line_dash="dot", line_color="green")
    fig.add_hline(y=info['nivel_max_msnm'] * 0.4, line_dash="dot", line_color="red")
    fig.update_layout(title=f"Evolución Nivel: {central}", xaxis_title="Fecha", yaxis_title="Nivel (msnm)")
    
    ruta_img = os.path.join(RUTA_IMAGENES, f"grafico_{central}.png")
    
    pio.write_image(fig, ruta_img, scale=2) 
    
    return ruta_img

def crear_html_reporte(df_estado_actual, rutas_graficos):
    """Crea el string HTML con rutas relativas."""
    print("Generando plantilla HTML...")
    
    html_str = f"""
    <html>
    <head>
        <style>
            @page {{ size: a4 portrait; @frame content_frame {{ left: 50pt; right: 50pt; top: 50pt; bottom: 50pt; }} }}
            body {{ font-family: Arial, sans-serif; margin: 0; }}
            h1 {{ color: #004a99; font-size: 24pt; }}
            h2 {{ color: #333; border-bottom: 2px solid #004a99; padding-bottom: 5px; font-size: 18pt; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; font-size: 10pt; }}
            th {{ background-color: #f2f2f2; }}
            .container {{ padding: 10px; }}
            .grafico-container {{ margin-top: 20px; text-align: center; }}
            img {{ max-width: 90%; height: auto; }}
        </style>
    </head>
    <body>
    <div class="container">
        <h1>Reporte de Estado y Proyección de Centrales Hidroeléctricas</h1>
        <p>Fecha del reporte: {FECHA_HOY}</p>
        
        <h2>Resumen de Estado Actual</h2>
        <table>
            <tr>
                <th>Central</th>
                <th>Nivel Actual (msnm)</th>
                <th>Nivel Máximo (msnm)</th>
                <th>Capacidad (%)</th>
            </tr>
    """
    
    if df_estado_actual.empty:
         # Esta fila se añadirá si los datos históricos están vacíos
         html_str += '<tr><td colspan="4">No hay datos actuales disponibles.</td></tr>'
    else:
        # Si df_estado_actual SÍ tiene datos, se llenará la tabla
        for _, row in df_estado_actual.iterrows():
            color_pct = "green" if row['nivel_pct'] > 70 else ("orange" if row['nivel_pct'] > 40 else "red")
            html_str += f"""
                <tr>
                    <td>{row['id_central']}</td>
                    <td>{row['nivel_msnm']:.2f}</td>
                    <td>{row['nivel_max_msnm']}</td>
                    <td style="color: {color_pct}; font-weight: bold;">{row['nivel_pct']:.1f}%</td>
                </tr>
            """
    
    html_str += "</table>"
    html_str += "<h2>Detalle y Proyección por Central</h2>"
    
    for central, ruta_img in rutas_graficos.items():
        if ruta_img:
            ruta_img_rel = os.path.relpath(ruta_img, RUTA_REPORTES)
            ruta_img_rel = ruta_img_rel.replace(os.path.sep, '/')
            html_str += f"""
            <div class="grafico-container">
                <img src="{ruta_img_rel}" alt="Gráfico de {central}">
            </div>
            """
    
    html_str += "</div></body></html>"
    return html_str

def convertir_html_a_pdf(source_html, output_filename, base_dir='.'):
    """Convierte el HTML a PDF usando xhtml2pdf."""
    with open(output_filename, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(
            source_html,
            dest=result_file,
            path=base_dir
        )
    return pisa_status.err


# --- Punto de Entrada Principal (MODIFICADO) ---
if __name__ == "__main__":

    # --- ### INICIO DE LA CORRECCIÓN ### ---
    #
    # Añadimos los mismos comandos de actualización de datos
    # que tiene el script 'dashboard/app.py'.
    # Esto asegura que la base de datos esté FRESCA cada vez
    # que se genera el reporte.
    #
    script_ingestion = os.path.join("src", "data_ingestion.py")
    script_training = os.path.join("src", "model_training.py")
    script_prediction = os.path.join("src", "model_prediction.py")
    
    print("Asegurando que los datos y modelos están actualizados...")
    
    print(f"Ejecutando {script_ingestion}...")
    os.system(f'python {script_ingestion}')
    
    print(f"Ejecutando {script_training}...")
    os.system(f'python {script_training}')
    
    print(f"Ejecutando {script_prediction}...")
    os.system(f'python {script_prediction}')
    #
    # --- ### FIN DE LA CORRECCIÓN ### ---

    print(f"\nIniciando generación de reportes...")
    
    # --- PASO 1: Cargar datos (AHORA FRESCOS) ---
    df_c, df_h, df_p, df_actual = cargar_datos_reporte()
    
    # --- PASO 2: Generar gráficos (Archivos .png) ---
    rutas_graficos = {}
    if not df_c.empty:
        for central in df_c['id_central']:
            rutas_graficos[central] = generar_grafico_estatico(central, df_h, df_p, df_c)
    
    # --- PASO 3: Generar el string HTML ---
    # (Ahora df_actual no estará vacío, y la tabla tendrá datos)
    html_content = crear_html_reporte(df_actual, rutas_graficos)
    
    # --- PASO 4: Guardar el archivo HTML ---
    ruta_html = os.path.join(RUTA_REPORTES, NOMBRE_REPORTE_HTML)
    try:
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\nReporte HTML generado exitosamente en: {ruta_html}")
    except Exception as e:
        print(f"Error al guardar el archivo HTML: {e}")

    # --- PASO 5: Generar el archivo PDF ---
    if XHTML2PDF_DISPONIBLE:
        print("Iniciando generación de PDF con xhtml2pdf...")
        ruta_pdf = os.path.join(RUTA_REPORTES, NOMBRE_REPORTE_PDF)
        
        try:
            base_dir_abs = os.path.abspath(RUTA_REPORTES)
            pisa_error = convertir_html_a_pdf(html_content, ruta_pdf, base_dir=base_dir_abs)
            
            if not pisa_error:
                print(f"Reporte PDF generado exitosamente en: {ruta_pdf}")
            else:
                # Ya no deberías ver '<table> is empty'
                print(f"ERROR: Falló la generación de PDF con xhtml2pdf: {pisa_error}")
        except Exception as e:
            print(f"ERROR FATAL durante la generación de PDF: {e}")
            traceback.print_exc()
    else:
        print("\nGeneración de PDF omitida (xhtml2pdf no está disponible).")
```

**Para ejecutar este script:**

```bash
python src/report_generator.py
```

Busca el archivo `Reporte_Hidro_EPM_YYYY-MM-DD.pdf` en la nueva carpeta `reportes/`.

-----


## Cómo Ejecutar el Proyecto

### 1. Configuración del Entorno

Asegúrate de tener Python 3.8 o superior.

```bash
# 1. Clona este repositorio (si está en Git)
# git clone ...
# cd proyecto_hidro_epm

# 2. Crea y activa el entorno virtual
python -m venv venv
source venv/bin/activate  # En macOS/Linux
# .\venv\Scripts\Activate   # En Windows PowerShell

# 3. Instala las dependencias
pip install -r requirements.txt
````

### 2\. Ejecutar el Dashboard Interactivo

El dashboard es el punto de entrada principal. Ejecutará automáticamente los scripts de datos y predicción antes de iniciar.

```bash
python dashboard/app.py
```

Abre tu navegador en `http://127.0.0.1:8050/`.

### 3\. Generar un Reporte PDF Manualmente

Si solo deseas generar el reporte PDF estático:

```bash
python src/report_generator.py
```

El archivo se guardará en la carpeta `/reportes`.

