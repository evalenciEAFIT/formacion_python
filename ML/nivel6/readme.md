## Guía Completa: Proyecto de Visualización y Predicción

Este documento contiene la implementación técnica completa, paso a paso, para el proyecto de ejemplo de las hidroeléctricas.

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

   * **En macOS / Linux:**

    ```bash
    source venv/bin/activate
    ```


#### 3\. Instalación de Paquetes y `requirements.txt`

El archivo `requirements.txt` es una lista de todas las librerías que tu proyecto necesita.

1.  Con tu entorno `venv` activado, instala las librerías una por una. Usaremos:

      * `pandas` y `numpy`: Para manipulación de datos.
      * `scikit-learn` y `joblib`: Para crear y guardar el modelo de ML.
      * `dash` y `plotly`: Para el dashboard web interactivo.
      * `openpyxl`: Para que pandas pueda escribir en Excel.
      * `SQLAlchemy`: Para que pandas pueda escribir en bases de datos SQL (usaremos SQLite).
      * `WeasyPrint` y `kaleido`: Para generar el reporte PDF y exportar gráficos de Plotly a imágenes.

    <!-- end list -->

    ```bash
    pip install pandas numpy scikit-learn joblib dash plotly openpyxl SQLAlchemy WeasyPrint kaleido
    ```

2.  Una vez instaladas, genera el archivo `requirements.txt` automáticamente. Este comando "congela" la lista de paquetes instalados en el entorno y la guarda en un archivo:

    ```bash
    pip freeze > requirements.txt
    ```

Ahora, cualquier otra persona puede replicar tu entorno exacto simplemente corriendo `pip install -r requirements.txt`.

-----

### Sección 1: Creación de la Estructura de Archivos

Una buena estructura de carpetas es fundamental. Aquí tienes un script para crearla automáticamente.

**Para macOS / Linux (guarda esto como `setup.sh` y ejecuta `bash setup.sh`):**

```bash
#!/bin/bash
echo "Creando estructura de carpetas para el proyecto..."

mkdir -p data
mkdir -p dashboard/assets
mkdir -p notebooks
mkdir -p src
mkdir -p models
mkdir -p tests

echo "Creando archivos iniciales..."

# Archivos __init__.py para que Python reconozca los módulos
touch src/__init__.py
touch tests/__init__.py

# Archivos de código principales (vacíos)
touch src/data_ingestion.py
touch src/feature_engineering.py
touch src/model_training.py
touch src/model_prediction.py
touch src/report_generator.py
touch dashboard/app.py

# Marcadores de posición para carpetas
touch data/.gitkeep
touch models/.gitkeep

# Archivos de exploración (opcional)
touch notebooks/01_exploracion_datos.ipynb
touch notebooks/02_prototipo_modelo_ml.ipynb

# Archivos de proyecto
touch README.md
touch .gitignore

echo "Estructura creada exitosamente."
```

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
2. Guardar estos datos en múltiples formatos (CSV, Excel, SQLite DB).
3. Configurar la base de datos inicial.
"""

import pandas as pd
import numpy as np
import datetime
import sqlite3
from sqlalchemy import create_engine

# --- Configuración de la Simulación ---

# Define las centrales y sus atributos (coordenadas, capacidad, etc.)
CENTRALES = {
    'Guatape': {'lat': 6.32, 'lon': -75.16, 'capacidad_MWh': 560, 'nivel_max_msnm': 1900},
    'Ituango': {'lat': 7.15, 'lon': -75.63, 'capacidad_MWh': 2400, 'nivel_max_msnm': 401},
    'Playas': {'lat': 6.45, 'lon': -74.88, 'capacidad_MWh': 201, 'nivel_max_msnm': 780},
    'SanCarlos': {'lat': 6.19, 'lon': -74.98, 'capacidad_MWh': 1240, 'nivel_max_msnm': 805}
}

N_DIAS_HISTORICOS = 1095 # Simular 3 años de datos
FECHA_INICIO = datetime.datetime(2022, 1, 1)

# --- Rutas de Archivos de Salida ---
RUTA_DATA = 'data'
RUTA_CSV = f'{RUTA_DATA}/mediciones_hidro.csv'
RUTA_EXCEL = f'{RUTA_DATA}/mediciones_hidro.xlsx'
RUTA_DB = f'sqlite:///{RUTA_DATA}/hidro.db' # Ruta para SQLAlchemy


def simular_datos():
    """
    Crea un DataFrame de pandas con datos simulados de mediciones.
    
    Simula nivel, caudal y generación con estacionalidad y ruido
    para cada central definida en CENTRALES.
    
    Retorna:
        pd.DataFrame: Un DataFrame con todos los datos históricos simulados.
    """
    print("Iniciando simulación de datos...")
    datos_simulados = []
    
    for central, info in CENTRALES.items():
        for i in range(N_DIAS_HISTORICOS):
            fecha = FECHA_INICIO + datetime.timedelta(days=i)
            
            # Simular estacionalidad (ej. temporada de lluvias)
            estacionalidad = np.sin((i / 365.25) * 2 * np.pi - np.pi / 2) # Senoide anual
            
            # Simular nivel (msnm)
            nivel_base = info['nivel_max_msnm'] * 0.75 # Nivel promedio
            ruido = np.random.rand() * 0.1 - 0.05 # Ruido aleatorio
            nivel_actual = nivel_base * (1 + 0.2 * estacionalidad + ruido)
            
            # Simular caudal (m3/s)
            caudal_entrada = 150 + 100 * estacionalidad + np.random.uniform(-20, 20)
            
            # Simular generación (MW)
            factor_gen = (nivel_actual / info['nivel_max_msnm']) * np.random.uniform(0.7, 1.0)
            generacion_mw = info['capacidad_MWh'] * factor_gen
            
            datos_simulados.append({
                'id_central': central,
                'fecha_hora': fecha,
                'nivel_msnm': round(nivel_actual, 2),
                'caudal_entrada_m3s': round(caudal_entrada, 2),
                'generacion_mw': round(generacion_mw, 2),
            })

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
    print(f"Guardando datos en {RUTA_CSV}, {RUTA_EXCEL}, y {RUTA_DB}...")
    
    # 1. Guardar en CSV
    df_mediciones.to_csv(RUTA_CSV, index=False)
    
    # 2. Guardar en Excel
    # df_mediciones.to_excel(RUTA_EXCEL, index=False) # Descomentar si se necesita. Es más lento.

    # 3. Guardar en Base de Datos SQLite
    engine = create_engine(RUTA_DB)
    
    # Crear y guardar la tabla de Centrales
    df_centrales = pd.DataFrame.from_dict(CENTRALES, orient='index')
    df_centrales.index.name = 'id_central'
    df_centrales.to_sql('Centrales', engine, if_exists='replace')
    
    # Guardar la tabla de Mediciones
    df_mediciones.to_sql('Mediciones', engine, if_exists='replace', index_label='id_medicion')
    
    print("Datos guardados exitosamente en todos los formatos.")
    
    # Verificación (opcional)
    with engine.connect() as conn:
        print("\nVerificación de BD (Tabla Centrales):")
        print(pd.read_sql("SELECT * FROM Centrales LIMIT 3", conn))
        print("\nVerificación de BD (Tabla Mediciones):")
        print(pd.read_sql("SELECT * FROM Mediciones LIMIT 3", conn))


# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    """
    Este bloque se ejecuta solo cuando corres el script directamente
    (ej. `python src/data_ingestion.py`)
    """
    datos = simular_datos()
    guardar_datos(datos)
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

# --- Configuración ---
RUTA_DB = 'data/hidro.db'
RUTA_MODELO = 'models/modelo_prediccion_nivel.pkl'
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
            
            # Features de fecha
            dia_del_ano = fecha_futura.dayofyear
            mes = fecha_futura.month
            
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
    engine = create_engine(f'sqlite:///{RUTA_DB}')
    
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
Dashboard Interactivo con Dash y Plotly.

Este script lanza una aplicación web local que muestra:
1. Un mapa interactivo de las centrales (GeoDatos).
2. Un gráfico de series de tiempo con datos históricos y predicciones.
3. El gráfico se actualiza al hacer clic en el mapa (Callback).
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import datetime

# --- Carga de Datos ---
RUTA_DB = 'data/hidro.db'

def cargar_datos_dashboard():
    """
    Carga todos los datos necesarios para el dashboard desde la BD.
    (Centrales, Mediciones históricas y Predicciones futuras).
    """
    conn = sqlite3.connect(f'file:{RUTA_DB}?mode=ro', uri=True) # Modo solo lectura
    
    # 1. Cargar Centrales (para el mapa)
    df_centrales = pd.read_sql("SELECT * FROM Centrales", conn)
    
    # 2. Cargar últimos 90 días de mediciones históricas
    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    query_hist = f"SELECT * FROM Mediciones WHERE fecha_hora >= '{fecha_limite}'"
    df_historico = pd.read_sql(query_hist, conn, parse_dates=['fecha_hora'])
    
    # 3. Cargar Predicciones
    df_predicciones = pd.read_sql("SELECT * FROM Predicciones", conn, parse_dates=['fecha_prediccion'])
    
    conn.close()
    
    # 4. Combinar info de centrales (ej. nivel_max) con histórico
    df_historico = pd.merge(df_historico, df_centrales[['id_central', 'nivel_max_msnm']], on='id_central')
    # Calcular el nivel como porcentaje (para el color del mapa)
    df_historico['nivel_pct'] = (df_historico['nivel_msnm'] / df_historico['nivel_max_msnm']) * 100
    
    # Obtener el estado más reciente para el mapa
    df_mapa = df_historico.loc[df_historico.groupby('id_central')['fecha_hora'].idxmax()]
    df_mapa = pd.merge(df_mapa, df_centrales[['id_central', 'lat', 'lon']], on='id_central')

    return df_centrales, df_historico, df_predicciones, df_mapa

# Cargar datos al iniciar la app
df_centrales, df_historico, df_predicciones, df_mapa = cargar_datos_dashboard()

# --- Inicialización de la App Dash ---
app = dash.Dash(__name__)
app.title = "Dashboard Hidroeléctricas EPM"

# --- Figura: Mapa Geográfico (GeoDatos) ---
fig_mapa = px.scatter_geo(
    df_mapa,
    lat='lat',
    lon='lon',
    color='nivel_pct',
    hover_name='id_central',
    hover_data={'nivel_msnm': ':.2f', 'lat': False, 'lon': False, 'nivel_pct': ':.1f%'},
    size=np.ones(len(df_mapa)) * 15, # Tamaño fijo
    color_continuous_scale='RdYlGn', # Rojo-Amarillo-Verde
    range_color=[30, 100], # Rango para la escala de color
    scope='south america',
    title='Estado Actual de Centrales'
)
# Centrar el mapa en Colombia
fig_mapa.update_geos(center=dict(lat=6.5, lon=-75), projection_scale=5.5)
fig_mapa.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# --- Layout de la Aplicación ---
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '10px'})(children=[
    
    html.H1(children='Dashboard de Monitoreo Hidroeléctricas'),
    html.Hr(),
    
    html.Div(className='row', style={'display': 'flex'}, children=[
        # Columna Izquierda: Mapa
        html.Div(style={'width': '40%', 'padding': '10px'}, children=[
            html.H3('Mapa de Centrales'),
            dcc.Graph(
                id='mapa-centrales',
                figure=fig_mapa,
                clickData=None # Importante para el callback
            )
        ]),
        
        # Columna Derecha: Gráfico de Series de Tiempo
        html.Div(style={'width': '60%', 'padding': '10px'}, children=[
            html.H3(id='titulo-grafico-detalle', children='Detalle de Central'),
            dcc.Graph(id='grafico-detalle')
        ])
    ])
])

# --- Callbacks (Interactividad) ---

@app.callback(
    [Output('grafico-detalle', 'figure'),
     Output('titulo-grafico-detalle', 'children')],
    [Input('mapa-centrales', 'clickData')]
)
def actualizar_grafico_detalle(clickData):
    """
    Esta función se activa cuando el usuario hace clic en el mapa.
    Filtra los datos históricos y de predicción para la central seleccionada.
    """
    
    # Determinar la central seleccionada
    if clickData:
        # Extrae el nombre de la central del punto de datos en el que se hizo clic
        central_seleccionada = clickData['points'][0]['hovertext']
    else:
        # Si no hay clic (carga inicial), selecciona la primera central
        central_seleccionada = df_centrales['id_central'].iloc[0]
        
    titulo = f"Detalle y Predicción: {central_seleccionada}"
    
    # 1. Filtrar datos históricos
    df_hist_filtrado = df_historico[df_historico['id_central'] == central_seleccionada]
    
    # 2. Filtrar predicciones
    df_pred_filtrado = df_predicciones[df_predicciones['id_central'] == central_seleccionada]
    
    # 3. Obtener umbrales (Nivel Máximo)
    nivel_max = df_centrales[df_centrales['id_central'] == central_seleccionada]['nivel_max_msnm'].iloc[0]
    nivel_critico = nivel_max * 0.4 # Asumimos un 40% como crítico
    
    # --- Crear la figura de Plotly ---
    fig = go.Figure()
    
    # Trazo 1: Histórico
    fig.add_trace(go.Scatter(
        x=df_hist_filtrado['fecha_hora'],
        y=df_hist_filtrado['nivel_msnm'],
        mode='lines',
        name='Nivel Histórico (Real)',
        line=dict(color='blue')
    ))
    
    # Trazo 2: Predicciones (como puntos)
    fig.add_trace(go.Scatter(
        x=df_pred_filtrado['fecha_prediccion'],
        y=df_pred_filtrado['nivel_predicho_msnm'],
        mode='markers',
        name='Predicción ML',
        marker=dict(color='red', size=10, symbol='x')
    ))
    
    # Trazo 3: Líneas de Umbral
    fig.add_hline(y=nivel_max, line_dash="dot", line_color="green",
                  annotation_text="Nivel Máximo", annotation_position="bottom right")
    fig.add_hline(y=nivel_critico, line_dash="dot", line_color="red",
                  annotation_text="Nivel Crítico", annotation_position="bottom right")
    
    fig.update_layout(
        title=f"Nivel del Embalse (msnm)",
        xaxis_title="Fecha",
        yaxis_title="Nivel (msnm)",
        legend_title="Leyenda",
        hovermode="x unified"
    )
    
    return fig, titulo


# --- Punto de Entrada Principal para correr el servidor ---
if __name__ == '__main__':
    # Ejecutar todos los scripts de datos y modelo antes de lanzar el dashboard
    # En un entorno de producción, esto se manejaría con un orquestador (ej. Airflow)
    print("Asegurando que los datos y modelos están actualizados...")
    import os
    os.system('python src/data_ingestion.py')
    os.system('python src/model_training.py')
    os.system('python src/model_prediction.py')
    
    print("\nLanzando el servidor del Dashboard en http://127.0.0.1:8050/")
    app.run_server(debug=True)
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
Módulo de Generación de Reportes PDF.

Este script es responsable de:
1. Cargar los datos más recientes (históricos y predicciones).
2. Generar gráficos estáticos (imágenes) usando Plotly y Kaleido.
3. Crear un documento HTML con los gráficos y KPIs.
4. Convertir el HTML a PDF usando WeasyPrint.
"""

import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.io as pio
from weasyprint import HTML
import datetime
import os

# Configuración
RUTA_DB = 'data/hidro.db'
RUTA_REPORTES = 'reportes'
RUTA_IMAGENES = 'reportes/img'
FECHA_HOY = datetime.datetime.now().strftime('%Y-%m-%d')
NOMBRE_REPORTE = f'Reporte_Hidro_EPM_{FECHA_HOY}.pdf'

# Asegurarse que las carpetas de reportes existen
os.makedirs(RUTA_REPORTES, exist_ok=True)
os.makedirs(RUTA_IMAGENES, exist_ok=True)

def cargar_datos_reporte():
    """Carga todos los datos necesarios para el reporte."""
    conn = sqlite3.connect(f'file:{RUTA_DB}?mode=ro', uri=True)
    df_centrales = pd.read_sql("SELECT * FROM Centrales", conn)
    
    # Histórico de los últimos 30 días
    fecha_limite = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    query_hist = f"SELECT * FROM Mediciones WHERE fecha_hora >= '{fecha_limite}'"
    df_historico = pd.read_sql(query_hist, conn, parse_dates=['fecha_hora'])
    
    df_predicciones = pd.read_sql("SELECT * FROM Predicciones", conn, parse_dates=['fecha_prediccion'])
    conn.close()
    
    # Combinar datos
    df_historico = pd.merge(df_historico, df_centrales, on='id_central')
    df_historico['nivel_pct'] = (df_historico['nivel_msnm'] / df_historico['nivel_max_msnm']) * 100
    
    # Estado más reciente
    df_estado_actual = df_historico.loc[df_historico.groupby('id_central')['fecha_hora'].idxmax()]
    
    return df_centrales, df_historico, df_predicciones, df_estado_actual

def generar_grafico_estatico(central, df_hist, df_pred, df_centrales):
    """
    Genera un gráfico de serie de tiempo para una central y lo guarda como PNG.
    
    Retorna:
        str: La ruta al archivo de imagen generado.
    """
    print(f"Generando gráfico para {central}...")
    df_h = df_hist[df_hist['id_central'] == central]
    df_p = df_pred[df_pred['id_central'] == central]
    info = df_centrales[df_centrales['id_central'] == central].iloc[0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_h['fecha_hora'], y=df_h['nivel_msnm'], mode='lines', name='Histórico'))
    fig.add_trace(go.Scatter(x=df_p['fecha_prediccion'], y=df_p['nivel_predicho_msnm'], mode='markers', name='Predicción', marker=dict(color='red', size=8)))
    
    # Líneas de umbral
    fig.add_hline(y=info['nivel_max_msnm'], line_dash="dot", line_color="green")
    fig.add_hline(y=info['nivel_max_msnm'] * 0.4, line_dash="dot", line_color="red")
    
    fig.update_layout(
        title=f"Evolución Nivel: {central}",
        xaxis_title="Fecha", yaxis_title="Nivel (msnm)",
        legend_title="Leyenda",
    )
    
    # Guardar la imagen
    ruta_img = f"{RUTA_IMAGENES}/grafico_{central}.png"
    pio.write_image(fig, ruta_img, engine='kaleido', scale=2) # scale=2 para mejor resolución
    return ruta_img

def crear_html_reporte(df_estado_actual, rutas_graficos):
    """
    Crea una cadena de string HTML que sirve como plantilla para el PDF.
    """
    print("Generando plantilla HTML...")
    
    # --- Inicio del HTML ---
    html_str = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #004a99; }} /* Color EPM */
            h2 {{ color: #333; border-bottom: 2px solid #004a99; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .grafico-container {{ 
                page-break-inside: avoid; /* Evita que el gráfico se corte entre páginas */
                margin-top: 20px; 
            }}
            img {{ width: 100%; }}
        </style>
    </head>
    <body>
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
    
    # --- Tabla de Resumen ---
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
    
    # --- Sección de Gráficos ---
    html_str += "<h2>Detalle y Proyección por Central</h2>"
    
    for central, ruta_img in rutas_graficos.items():
        # Usamos la ruta relativa para el HTML
        ruta_img_rel = os.path.relpath(ruta_img, RUTA_REPORTES) 
        html_str += f"""
        <div class="grafico-container">
            <img src="{ruta_img}">
        </div>
        """
    
    html_str += "</body></html>"
    return html_str

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    print(f"Iniciando generación de reporte PDF: {NOMBRE_REPORTE}")
    
    # 1. Cargar datos
    df_c, df_h, df_p, df_actual = cargar_datos_reporte()
    
    # 2. Generar gráficos
    rutas_graficos = {}
    for central in df_c['id_central']:
        rutas_graficos[central] = generar_grafico_estatico(central, df_h, df_p, df_c)
    
    # 3. Crear HTML
    html_content = crear_html_reporte(df_actual, rutas_graficos)
    
    # 4. Convertir HTML a PDF
    ruta_pdf = os.path.join(RUTA_REPORTES, NOMBRE_REPORTE)
    # WeasyPrint necesita una URL base para encontrar las imágenes
    base_url = os.path.dirname(os.path.abspath(__file__))
    HTML(string=html_content, base_url=base_url).write_pdf(ruta_pdf)
    
    print(f"\nReporte PDF generado exitosamente en: {ruta_pdf}")
```

**Para ejecutar este script:**

```bash
python src/report_generator.py
```

Busca el archivo `Reporte_Hidro_EPM_YYYY-MM-DD.pdf` en la nueva carpeta `reportes/`.

-----

### Sección 7: Archivos de Proyecto (`.gitignore` y `README.md`)

**1. Archivo `.gitignore`:**
Crea un archivo llamado `.gitignore` en la raíz del proyecto para evitar que Git rastree archivos innecesarios.

```text
# Entornos virtuales
venv/
.venv/

# Bases de datos y datos generados
data/
*.db
*.csv
*.xlsx

# Reportes generados
reportes/

# Modelos entrenados
models/
*.pkl

# Caches de Python
__pycache__/
.pytest_cache/
*.pyc

# Caches de IDEs
.vscode/
.idea/
```

**2. Archivo `README.md` (Documentación):**
Crea un archivo `README.md` en la raíz para explicar tu proyecto.

```markdown
# Proyecto: Dashboard y Predicción de Hidroeléctricas

Este proyecto es un prototipo para visualizar el estado actual y futuro (7, 15, 30 días) de las centrales hidroeléctricas de EPM, utilizando un dashboard interactivo, geodatos y modelos de Machine Learning.

## Estructura del Proyecto

```

/proyecto\_hidro\_epm/
|
├── 📁 data/               \# Datos generados (CSV, Excel, SQLite DB)
├── 📁 dashboard/          \# Código de la aplicación Dash
|   └── 📄 app.py
├── 📁 models/             \# Modelos de ML entrenados (.pkl)
├── 📁 notebooks/          \# Jupyter notebooks para exploración
├── 📁 reportes/           \# PDFs e imágenes generadas
├── 📁 src/                \# Código fuente principal
|   ├── 📄 data\_ingestion.py    \# Simula y guarda datos
|   ├── 📄 model\_training.py    \# Entrena el modelo de ML
|   ├── 📄 model\_prediction.py   \# Genera predicciones futuras
|   └── 📄 report\_generator.py   \# Crea el reporte PDF
|
├── 📄 .gitignore          \# Archivos a ignorar por Git
├── 📄 requirements.txt    \# Librerías de Python
└── 📄 README.md           \# Esta documentación

````

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

```
```
