# Sistema de Analytics para Granjas Solares

## 📋 Índice de Contenidos

1. [Introducción y Arquitectura](#introduccion)
2. [Programación Modular con `__init__.py`](#modulos)
3. [Estructura de Carpetas y Generación en Windows](#estructura)
4. [Configuración del Entorno](#configuracion)
5. [Componente de Gestión de Datos](#datamanager)
6. [Componente de Predicción](#predictor)
7. [API REST](#api)
8. [Dashboard Interactivo](#dashboard)
9. [Ejecución y Despliegue](#ejecucion)
10. [Mejores Prácticas Aplicadas](#practicas)

---

## 1. Introducción y Arquitectura <a name="introduccion"></a>

### Propósito del Sistema
Esta aplicación resuelve el problema real de **monitoreo y predicción de generación energética** en granjas solares. Permite a operadores:
- Visualizar métricas en tiempo real de paneles fotovoltaicos
- Predecir generación basada en condiciones meteorológicas
- Tomar decisiones data-driven sobre mantenimiento y optimización

### Principios de Diseño

**Separación de Responsabilidades**: Cada componente tiene una única razón de cambiar (SRP - Single Responsibility Principle).

```python
# app/core/data_manager.py → Solo gestiona datos
# app/core/predictor.py → Solo maneja ML
# app/api/routes.py → Solo expone endpoints
# app/dashboard/app.py → Solo visualización
```

---

## 2. Programación Modular con `__init__.py` <a name="modulos"></a>

### ¿Qué es `__init__.py` y por qué es crucial?

El archivo `__init__.py` es el **pilar de la programación modular en Python**. Convierte un directorio en un **paquete Python importable**, permitiendo organizar código en módulos lógicos y reutilizables.

### Funciones Clave de `__init__.py`:

#### 1. **Marcador de Paquete**
Hace que Python trate el directorio como paquete:
```python
# Sin __init__.py
import app.api.routes  # Error: ModuleNotFoundError

# Con __init__.py
import app.api.routes  # ✅ Funciona
```

#### 2. **Control de Imports**
Define la API pública del paquete:
```python
# app/core/__init__.py
from .data_manager import DataManager
from .predictor import Predictor

__all__ = ['DataManager', 'Predictor']  # Opcional: explícito
```

Ahora puedes importar así:
```python
from app.core import DataManager  # En lugar de app.core.data_manager.DataManager
```

#### 3. **Inicialización de Paquete**
Ejecuta código al importar:
```python
# app/__init__.py
import logging
logging.basicConfig(level=logging.INFO)
print("📦 Paquete app inicializado")
```

#### 4. **Patrón Factory**
Centraliza creación de objetos:
```python
# app/__init__.py
def create_app(config_name='development'):
    """Factory que crea instancia Flask configurada"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    return app
```

### Ventajas en Nuestro Proyecto:

```python
# app/__init__.py
"""
Fábrica de Aplicación y Paquete Principal

Este archivo hace que `app` sea un paquete Python y provee
la función factory para crear instancias configuradas de Flask.

Beneficios:
-  Desacoplamiento: app no depende de cómo se inicia
-  Testabilidad: tests pueden crear app con config='testing'
-  Configuración centralizada: una sola función para todos los entornos
"""

from flask import Flask
from app.api.routes import api_bp
import logging
from app.config import config_by_name

def create_app(config_name='development'):
    """
    Factory function para crear instancia de Flask.
    
    Args:
        config_name: Nombre del entorno ('development', 'production', 'testing')
        
    Returns:
        Instancia de Flask configurada
        
    ¿Por qué factory?
    - Evita variables globales
    - Permite múltiples instancias (útil en tests)
    - Facilita inyección de configuración
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Registrar blueprints
    app.register_blueprint(api_bp)
    
    # Ruta principal
    @app.route('/')
    def index():
        return {
            "mensaje": "Analytics API v1.0 - Granja Solar",
            "endpoints": {
                "api": "/api/v1",
                "dashboard": "/dashboard/",
                "swagger": "/api/v1/salud"
            }
        }
    
    return app
```

### Importancia en el Proyecto:

```python
# Sin modularidad (❌ MAL)
# app.py (monolítico)
from flask import Flask
import pandas as pd
import joblib

app = Flask(__name__)
df = pd.read_csv('data.csv')
model = joblib.load('model.pkl')

@app.route('/')
def index():
    return "Hola"

# Problemas:
# - Difícil de probar
# - Código acoplado
# - No se puede reutilizar componentes

# Con modularidad (✅ BIEN)
# app/__init__.py
from flask import Flask
from app.core.data_manager import DataManager
from app.core.predictor import Predictor

def create_app():
    app = Flask(__name__)
    data_manager = DataManager()  # Inyectado
    predictor = Predictor()       # Inyectado
    return app

# Ventajas:
# - Cada componente es testable individualmente
# - Fácil de mantener y extender
# - Reutilizable en otros proyectos
```

---

## 3. Estructura de Carpetas y Generación en Windows <a name="estructura"></a>

### Estructura Completa del Proyecto

```
granja-solar/
├── app/                          # Paquete principal de la aplicación
│   ├── __init__.py              # Fábrica de aplicación + inicialización
│   ├── config.py                # Configuración por entorno
│   ├── api/                     # Capa de presentación (API)
│   │   ├── __init__.py          # Hace api un subpaquete
│   │   └── routes.py            # Endpoints REST
│   ├── core/                    # Lógica de negocio (patrón Repository)
│   │   ├── __init__.py          # Exporta DataManager y Predictor
│   │   ├── data_manager.py      # Gestión de datos de paneles
│   │   └── predictor.py         # Modelo ML de predicción
│   └── dashboard/               # Capa de visualización
│       ├── __init__.py          # Hace dashboard un subpaquete
│       └── app.py               # Aplicación Dash
├── tests/                       # Suite de pruebas
│   ├── __init__.py              # Hace tests un paquete
│   ├── test_api.py              # Tests de endpoints
│   └── test_core.py             # Tests de lógica de negocio
├── data/                        # Almacén de datos (no versionar)
│   └── paneles_solar.csv        # Dataset de generación solar
├── models/                      # Modelos entrenados (no versionar)
│   └── modelo_energia.pkl       # RandomForestRegressor serializado
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno (no versionar)
├── .gitignore                   # Reglas de Git
├── README.md                    # Documentación del proyecto
└── run.py                       # Punto de entrada
```

### Generación de Estructura en Windows

#### Método 1: Comandos CMD (Command Prompt)

```batch
@echo off
echo Creando estructura de proyecto para Granja Solar...

mkdir granja-solar
cd granja-solar

mkdir app\api\core\dashboard
mkdir tests
mkdir data
mkdir models

rem Crear archivos __init__.py
type nul > app\__init__.py
type nul > app\api\__init__.py
type nul > app\core\__init__.py
type nul > app\dashboard\__init__.py
type nul > tests\__init__.py

rem Crear archivos principales
type nul > app\config.py
type nul > app\api\routes.py
type nul > app\core\data_manager.py
type nul > app\core\predictor.py
type nul > app\dashboard\app.py
type nul > requirements.txt
type nul > .env
type nul > .gitignore
type nul > README.md
type nul > run.py

echo ✅ Estructura creada exitosamente en granja-solar\
```

#### Método 2: Comandos PowerShell

```powershell
# Crear estructura de directorios
$dirs = @(
    "granja-solar",
    "granja-solar\app\api",
    "granja-solar\app\core",
    "granja-solar\app\dashboard",
    "granja-solar\tests",
    "granja-solar\data",
    "granja-solar\models"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir
}

# Crear archivos __init__.py
$initFiles = @(
    "granja-solar\app\__init__.py",
    "granja-solar\app\api\__init__.py",
    "granja-solar\app\core\__init__.py",
    "granja-solar\app\dashboard\__init__.py",
    "granja-solar\tests\__init__.py"
)

foreach ($file in $initFiles) {
    New-Item -ItemType File -Force -Path $file
}

# Crear archivos principales
$mainFiles = @(
    "granja-solar\app\config.py",
    "granja-solar\app\api\routes.py",
    "granja-solar\app\core\data_manager.py",
    "granja-solar\app\core\predictor.py",
    "granja-solar\app\dashboard\app.py",
    "granja-solar\requirements.txt",
    "granja-solar\.env",
    "granja-solar\.gitignore",
    "granja-solar\README.md",
    "granja-solar\run.py"
)

foreach ($file in $mainFiles) {
    New-Item -ItemType File -Force -Path $file
}

Write-Host "✅ Estructura creada exitosamente en granja-solar\" -ForegroundColor Green
```

#### Método 3: Script Python Cross-Platform

```python
"""
create_structure.py - Script universal para crear estructura del proyecto
Compatible con Windows, Linux y macOS
"""

import os
from pathlib import Path

def crear_estructura(base_path="granja-solar"):
    """Crea estructura completa de directorios y archivos"""
    
    # Definir estructura de directorios
    directorios = [
        "app/api",
        "app/core",
        "app/dashboard",
        "tests",
        "data",
        "models"
    ]
    
    # Crear directorios
    for dir_path in directorios:
        Path(f"{base_path}/{dir_path}").mkdir(parents=True, exist_ok=True)
        print(f"📁 Creado: {base_path}/{dir_path}")
    
    # Archivos __init__.py
    init_files = [
        "app/__init__.py",
        "app/api/__init__.py",
        "app/core/__init__.py",
        "app/dashboard/__init__.py",
        "tests/__init__.py"
    ]
    
    # Archivos principales
    archivos_principales = [
        "app/config.py",
        "app/api/routes.py",
        "app/core/data_manager.py",
        "app/core/predictor.py",
        "app/dashboard/app.py",
        "requirements.txt",
        ".env",
        ".gitignore",
        "README.md",
        "run.py"
    ]
    
    todos_los_archivos = init_files + archivos_principales
    
    for archivo in todos_los_archivos:
        ruta_completa = Path(f"{base_path}/{archivo}")
        ruta_completa.touch(exist_ok=True)
        print(f"📄 Creado: {base_path}/{archivo}")
    
    print(f"✅ Estructura completa creada en '{base_path}'")

if __name__ == "__main__":
    crear_estructura()
```

**Ejecutar en Windows:**
```cmd
python create_structure.py
```

### Contenido de archivos `__init__.py`

```python
# app/api/__init__.py
"""
Subpaquete API

Exporta blueprints y configuración de rutas REST.
"""

from .routes import api_bp

__all__ = ['api_bp']
```

```python
# app/core/__init__.py
"""
Subpaquete Core (Lógica de Negocio)

Exporta clases principales de dominio.
"""

from .data_manager import DataManager
from .predictor import Predictor

__all__ = ['DataManager', 'Predictor']
```

```python
# app/dashboard/__init__.py
"""
Subpaquete Dashboard

Inicialización de la aplicación Dash.
"""
# Dash app se inicializa en app.py
```

```python
# tests/__init__.py
"""
Paquete de Tests

Contiene todas las pruebas unitarias y de integración.
"""
# pytest descubre tests automáticamente
```

---

## 4. Configuración del Entorno <a name="configuracion"></a>

### `requirements.txt`

```txt
# Framework web para API REST
flask==3.0.0
# Habilita CORS para llamadas desde el frontend
flask-cors==4.0.0

# Análisis de datos y manipulación
pandas==2.1.4
numpy==1.26.2

# Machine Learning
scikit-learn==1.3.2

# Visualización interactiva
plotly==5.18.0
dash==2.14.2
dash-bootstrap-components==1.5.0

# Gestión de configuración
python-dotenv==1.0.0

# Servidor WSGI para producción
gunicorn==21.2.0

# Testing
pytest==7.4.3
pytest-flask==1.3.0
```

### `.env`

```bash
# Entorno de ejecución: development o production
FLASK_ENV=development

# Archivo de entrada de la aplicación
FLASK_APP=run.py

# Clave secreta para sesiones (cambiar en producción)
SECRET_KEY=dev-clave-secreta-granja-solar-2024

# Puerto para API Flask
PORT=5000

# Puerto para Dashboard Dash
DASH_PORT=8050

# Rutas de archivos (permite cambiar sin modificar código)
DATA_PATH=data/paneles_solar.csv
MODEL_PATH=models/modelo_energia.pkl
```

### `app/config.py`

```python
"""
Módulo de configuración basado en dataclasses.
Implementa el patrón Strategy para diferentes entornos.
"""

import os
from dataclasses import dataclass
from typing import Dict, Type

@dataclass
class Config:
    """
    Configuración base común a todos los entornos.
    
    Atributos:
        SECRET_KEY: Clave para sesiones Flask
        FLASK_ENV: Entorno actual (development/production)
        DATA_PATH: Ruta al dataset de paneles solares
        MODEL_PATH: Ruta al modelo ML serializado
        DEBUG: Flag de modo depuración
    """
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-key-cambiar-en-prod')
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'production')
    DATA_PATH: str = os.getenv('DATA_PATH', 'data/paneles_solar.csv')
    MODEL_PATH: str = os.getenv('MODEL_PATH', 'models/modelo_energia.pkl')
    
    # Propiedad calculada: DEBUG solo en desarrollo
    @property
    def DEBUG(self) -> bool:
        """Activar modo debug solo en desarrollo para seguridad"""
        return self.FLASK_ENV == 'development'


class DevelopmentConfig(Config):
    """Configuración específica para desarrollo"""
    DEBUG: bool = True


class ProductionConfig(Config):
    """Configuración específica para producción"""
    DEBUG: bool = False


# Factory registry: Mapea nombres a clases de configuración
config_by_name: Dict[str, Type[Config]] = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
```

---

## 5. Componente de Gestión de Datos <a name="datamanager"></a>

### `app/core/data_manager.py`

```python
"""
Gestor de Datos para Granjas Solares

Este módulo encapsula toda la lógica de acceso y manipulación de datos
relacionados con paneles fotovoltaicos. Implementa el patrón Repository,
abstractando el almacenamiento subyacente (CSV, pero fácilmente extensible a DB).

¿Por qué esta abstracción?
- Desacopla la capa de datos de la lógica de negocio
- Facilita el testing (puedes mock DataManager)
- Permite cambiar a PostgreSQL/MySQL sin modificar API ni Dashboard
"""

import pandas as pd
from typing import Optional, Dict, Any, List
import logging

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


class DataManager:
    """
    Clase reponsable de cargar, filtrar, agregar y persistir datos
    de rendimiento de paneles solares.
    """
    
    def __init__(self, data_path: str):
        """
        Inicializa el gestor con la ruta al dataset.
        
        Args:
            data_path: Ruta al archivo CSV con datos de paneles
            
        ¿Por qué no cargar datos en __init__?
        - Lazy loading: Solo carga cuando se necesita (ahorra memoria)
        - Evita errores en import si el archivo no existe
        - Mejora tiempo de startup de la app
        """
        self.data_path = data_path
        self._df: Optional[pd.DataFrame] = None  # Variable privada con cache
    
    @property
    def dataframe(self) -> pd.DataFrame:
        """
        Propiedad que devuelve el DataFrame cargado.
        Implementa carga perezosa (lazy loading) con cacheo.
        
        Returns:
            DataFrame de pandas con datos de paneles solares
            
        ¿Por qué @property?
        - Oculta la lógica de carga al consumidor
        - Sintaxis más limpia: data_manager.dataframe vs data_manager.load_data()
        - Garantiza que los datos siempre estén cargados antes de usar
        """
        if self._df is None:
            logger.info("Primer acceso a datos, iniciando carga...")
            self.load_data()
        return self._df
    
    def load_data(self) -> None:
        """
        Carga datos desde CSV y realiza validaciones iniciales.
        
        ¿Por qué validar aquí?
        - Falla rápido (fail-fast) si hay problemas con datos
        - Evita propagar DataFrames corruptos por todo el sistema
        - Centraliza la lógica de limpieza inicial
        """
        try:
            self._df = pd.read_csv(self.data_path)
            
            # Validaciones específicas del dominio solar
            self._validar_datos_solar()
            
            logger.info(f"✅ Datos cargados exitosamente: {self._df.shape}")
            
        except FileNotFoundError:
            logger.error(f"❌ Archivo no encontrado: {self.data_path}")
            raise RuntimeError(f"No se encontró el dataset en {self.data_path}")
            
        except pd.errors.EmptyDataError:
            logger.error("❌ El archivo CSV está vacío")
            raise RuntimeError("Dataset vacío, revise la fuente de datos")
            
        except Exception as e:
            logger.error(f"❌ Error inesperado cargando datos: {e}")
            raise
    
    def _validar_datos_solar(self) -> None:
        """
        Valida que los datos contengan columnas esenciales para análisis solar.
        
        Columnas requeridas:
        - timestamp: Fecha y hora de la medición
        - potencia_generada_kw: Output actual del panel
        - irradiancia_w_m2: Radiación solar incidente
        - temperatura_celsius: Temp ambiente o del panel
        
        ¿Por qué validación privada?
        - Es un detalle de implementación, no parte de la API pública
        - No debe ser llamado desde fuera de la clase
        """
        required_cols = ['timestamp', 'potencia_generada_kw', 'irradiancia_w_m2', 'temperatura_celsius']
        missing = [col for col in required_cols if col not in self._df.columns]
        
        if missing:
            raise ValueError(f"Columnas requeridas faltantes: {missing}")
        
        # Validar tipos de datos
        if not pd.api.types.is_datetime64_any_dtype(self._df['timestamp']):
            self._df['timestamp'] = pd.to_datetime(self._df['timestamp'])
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Genera resumen estadístico del rendimiento de paneles.
        
        Returns:
            Diccionario con métricas clave:
            - shape: Dimensiones del dataset
            - columns: Lista de variables disponibles
            - efficiencia_promedio: % de eficiencia energética
            - correlacion_irradiancia_potencia: Relación causa-efecto
        
        ¿Por qué calcular métricas derivadas?
        - Proporciona insights inmediatos sin procesamiento adicional
        - Valida la calidad de los datos (correlación alta esperada)
        """
        df = self.dataframe
        
        # Calcular eficiencia relativa (potencia / irradiancia)
        # Evita división por cero con .replace(0, np.nan)
        df['eficiencia'] = df['potencia_generada_kw'] / df['irradiancia_w_m2'].replace(0, float('nan'))
        
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing": df.isnull().sum().to_dict(),
            "summary_stats": df.describe().to_dict(),
            "eficiencia_promedio": df['eficiencia'].mean(),
            "correlacion_irradiancia_potencia": df['irradiancia_w_m2'].corr(df['potencia_generada_kw'])
        }
    
    def filtrar_por_fecha(self, fecha_inicio: str, fecha_fin: str) -> pd.DataFrame:
        """
        Filtra el dataset por rango de fechas.
        
        Args:
            fecha_inicio: Fecha inicial en formato ISO (YYYY-MM-DD)
            fecha_fin: Fecha final en formato ISO
            
        Returns:
            DataFrame filtrado
            
        ¿Por qué método específico en vez de genérico?
        - Fecha es el filtro más común en series temporales
        - Permite optimización (indexación) en el futuro
        - API más clara para el consumidor
        """
        df = self.dataframe.copy()
        mask = (df['timestamp'] >= fecha_inicio) & (df['timestamp'] <= fecha_fin)
        return df[mask]
    
    def filtrar_por_condiciones(self, condiciones: Dict[str, Any]) -> pd.DataFrame:
        """
        Filtra dinámicamente basado en múltiples condiciones.
        
        Args:
            condiciones: Dict {columna: valor} para filtrar
            
        Returns:
            DataFrame filtrado
            
        Ejemplo:
            condiciones = {'temperatura_celsius': 25, 'panel_id': 'P001'}
            
        ¿Por qué Dict en vez de múltiples parámetros?
        - Flexible: permite filtros arbitrarios sin cambiar firma del método
        - Extensible: fácil añadir nuevos filtros desde API
        - Admite programación dinámica
        """
        df = self.dataframe.copy()
        
        for columna, valor in condiciones.items():
            if columna in df.columns:
                df = df[df[columna] == valor]
            else:
                logger.warning(f"Columna de filtro no existe: {columna}")
        
        return df
    
    def agregar_medicion(self, medicion: Dict[str, Any]) -> bool:
        """
        Agrega una nueva medición de rendimiento de panel.
        
        Args:
            medicion: Diccionario con valores de la nueva medida
                     Debe incluir: timestamp, potencia_generada_kw,
                     irradiancia_w_m2, temperatura_celsius
            
        Returns:
            True si se agregó correctamente, False si hubo error
            
        ¿Por qué bool en vez de excepción?
        - API más robusta: permite al llamador decidir si propagar error
        - Útil para batch operations (continuar si una falla)
        - Logging interno ya registra el problema
        """
        try:
            # Validar que la medición tenga las columnas esenciales
            required = ['timestamp', 'potencia_generada_kw', 'irradiancia_w_m2', 'temperatura_celsius']
            if not all(key in medicion for key in required):
                logger.error(f"Medición incompleta. Requerido: {required}")
                return False
            
            # Crear nueva fila y concatenar
            nueva_fila = pd.DataFrame([medicion])
            self._df = pd.concat([self.dataframe, nueva_fila], ignore_index=True)
            
            # Persistir cambios
            self.guardar_datos()
            logger.info(f"✅ Medición agregada: {medicion['timestamp']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error agregando medición: {e}")
            return False
    
    def guardar_datos(self) -> None:
        """
        Persiste el DataFrame actual en disco.
        
        ¿Por qué guardar automáticamente en cada operación?
        - Evita pérdida de datos en caso de fallo del sistema
        - Simplifica la API (no necesitas llamar guardar() explícitamente)
        
        Nota: En producción con alta frecuencia de escrituras,
        considerar batch saves o base de datos.
        """
        try:
            self.dataframe.to_csv(self.data_path, index=False)
            logger.info(f"💾 Datos guardados en {self.data_path}")
        except Exception as e:
            logger.error(f"❌ Error guardando datos: {e}")
            raise RuntimeError("No se pudo persistir los datos")
```

---

## 6. Componente de Predicción <a name="predictor"></a>

### `app/core/predictor.py`

```python
"""
Motor de Predicción de Generación Solar

Este módulo encapsula el modelo de Machine Learning para predecir
la potencia generada basada en condiciones meteorológicas.
Usa RandomForestRegressor por su robustez y capacidad de capturar
relaciones no lineales entre irradiancia, temperatura y potencia.

Patrones aplicados:
- Singleton (carga lazy del modelo)
- Strategy (fácil cambiar RandomForest por XGBoost)
- Repository (abstrae el almacenamiento del modelo)
"""

import joblib  # Serialización eficiente de modelos sklearn
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class Predictor:
    """
    Clase responsable de entrenar, guardar, cargar y hacer predicciones
    de generación de energía solar.
    """
    
    def __init__(self, model_path: str):
        """
        Inicializa el predictor con ruta al modelo.
        
        Args:
            model_path: Ruta donde se guardará/cargará el modelo .pkl
            
        ¿Por qué __init__ no carga el modelo?
        - Speed up del startup: Modelos grandes pueden tardar segundos
        - Si la API no usa ML, no consume memoria innecesaria
        - Mejora la robustez: App puede arrancar sin modelo
        """
        self.model_path = model_path
        self._model: Optional[RandomForestRegressor] = None
        self._feature_names: Optional[List[str]] = None
    
    @property
    def model(self) -> RandomForestRegressor:
        """
        Propiedad que carga el modelo bajo demanda (lazy loading).
        
        Returns:
            Modelo RandomForest entrenado
            
        Raises:
            RuntimeError: Si no hay modelo entrenado
            
        ¿Por qué @property con raise en vez de Optional?
        - Fuerza al llamador a manejar el error explícitamente
        - Evita errores silenciosos (None.predict())
        - API más clara: si hay modelo, funciona; si no, falla rápido
        """
        if self._model is None:
            logger.info("Modelo no está en memoria, intentando cargar...")
            self.cargar_modelo()
        
        if self._model is None:
            raise RuntimeError("Modelo no entrenado. Llame a entrenar_modelo() primero")
        
        return self._model
    
    def cargar_modelo(self) -> None:
        """
        Carga el modelo desde disco usando joblib.
        
        joblib es mejor que pickle para modelos sklearn porque:
        - Más eficiente con arrays numpy (backbone de sklearn)
        - Maneja mejor objetos grandes
        - Compatible entre versiones de sklearn
        """
        try:
            self._model = joblib.load(self.model_path)
            
            # Extraer nombres de características si están disponibles
            if hasattr(self._model, 'feature_names_in_'):
                self._feature_names = self._model.feature_names_in_.tolist()
            
            logger.info(f"✅ Modelo cargado desde {self.model_path}")
            
        except FileNotFoundError:
            logger.warning(f"⚠️ Modelo no encontrado en {self.model_path}")
            logger.info("Debe entrenar un nuevo modelo usando /api/v1/modelo/entrenar")
            self._model = None
            
        except Exception as e:
            logger.error(f"❌ Error al cargar modelo: {e}")
            self._model = None
    
    def preparar_datos(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """
        Prepara el dataset para entrenamiento.
        
        Args:
            df: DataFrame con columnas timestamp, irradiancia_w_m2,
                temperatura_celsius, potencia_generada_kw
                
        Returns:
            Tupla (X, y) donde X son características e y es el target
            
        Lógica de preparación:
        1. Remover timestamp (no es una feature cuantitativa útil para RF)
        2. Usar irradiancia y temperatura como predictores (X)
        3. Usar potencia generada como target (y)
        
        ¿Por qué no usar timestamp como feature?
        - RandomForest no entiende secuencia temporal sin ingeniería
        - Podría sobreajustar a patrones específicos de fechas
        - Para series temporales usaríamos LSTM/Prophet
        """
        # Definir columnas
        feature_cols = ['irradiancia_w_m2', 'temperatura_celsius']
        target_col = 'potencia_generada_kw'
        
        # Validar que existan
        missing_features = [col for col in feature_cols if col not in df.columns]
        if missing_features:
            raise ValueError(f"Faltan columnas requeridas: {missing_features}")
        
        if target_col not in df.columns:
            raise ValueError(f"Falta columna target: {target_col}")
        
        X = df[feature_cols]
        y = df[target_col]
        
        # Guardar nombres de features para predicción
        self._feature_names = feature_cols
        
        return X, y
    
    def entrenar_modelo(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Entrena un RandomForestRegressor con los datos proporcionados.
        
        Args:
            df: DataFrame con datos históricos de paneles
            
        Returns:
            Diccionario con métricas de rendimiento
            
        Proceso de entrenamiento:
        1. Preparar datos (X, y)
        2. Split train/test (80/20) con random_state fijo para reproducibilidad
        3. Entrenar RandomForest con 100 árboles (balance precisión/velocidad)
        4. Calcular métricas (R², RMSE)
        5. Guardar modelo automáticamente
        
        ¿Por qué RandomForestRegressor?
        - No requiere escalado de features (robusto a magnitudes)
        - Captura interacciones no lineales (irrad + temp → potencia)
        - Resistente a overfitting con n_estimators alto
        - Interpretable (feature_importance)
        
        ¿Por qué 100 árboles?
        - Más árboles = mejor generalización pero más lento
        - 100 es un buen default para datasets pequeños/medios
        - En producción, podría ajustarse con GridSearchCV
        """
        try:
            # Preparar datos
            X, y = self.preparar_datos(df)
            
            # Split estratificado para series temporales (no shuffle aquí)
            # Nota: Para datos temporales reales, usar TimeSeriesSplit
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=True
            )
            
            # Inicializar y entrenar modelo
            self._model = RandomForestRegressor(
                n_estimators=100,      # Número de árboles en el bosque
                max_depth=10,          # Limitar profundidad para evitar overfit
                min_samples_split=5,   # Nodo debe tener ≥5 muestras para dividir
                random_state=42,       # Reproducibilidad
                n_jobs=-1              # Usar todos los cores disponibles
            )
            
            self._model.fit(X_train, y_train)
            
            # Calcular métricas
            y_pred = self._model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            
            logger.info(f"✅ Modelo entrenado. R²={r2:.3f}, RMSE={rmse:.3f}")
            
            # Persistir modelo
            self.guardar_modelo()
            
            return {
                "r2_score": round(r2, 4),
                "rmse": round(rmse, 4),
                "modelo_path": self.model_path,
                "muestras_entrenamiento": len(X_train),
                "muestras_test": len(X_test)
            }
            
        except Exception as e:
            logger.error(f"❌ Error en entrenamiento: {e}")
            raise RuntimeError(f"Falló el entrenamiento del modelo: {e}")
    
    def guardar_modelo(self) -> None:
        """
        Serializa el modelo entrenado a disco.
        
        ¿Qué información se guarda?
        - El estimador entrenado (RandomForest)
        - Los árboles y splits aprendidos
        - Feature names (si están disponibles)
        
        Nota: joblib no guarda el DataFrame de entrenamiento,
        solo el modelo. Para reproducir, guarda también X_train, y_train
        o usa MLflow.
        """
        if self._model is None:
            logger.warning("No hay modelo para guardar")
            return
        
        try:
            joblib.dump(self._model, self.model_path)
            logger.info(f"💾 Modelo guardado en {self.model_path}")
        except Exception as e:
            logger.error(f"❌ Error guardando modelo: {e}")
            raise RuntimeError("No se pudo persistir el modelo")
    
    def predecir(self, datos_meteorologicos: Dict[str, float]) -> Optional[float]:
        """
        Predice la potencia generada dadas condiciones meteorológicas.
        
        Args:
            datos_meteorologicos: Dict con irradiancia_w_m2 y temperatura_celsius
            
        Returns:
            Potencia generada en kW (float) o None si error
            
        Ejemplo:
            predictor.predecir({
                'irradiancia_w_m2': 800,
                'temperatura_celsius': 28.5
            })
            # Returns: 154.3 (kW generados por un panel)
        
        ¿Por qué Optional[float]?
        - Null object pattern: None indica error de predicción
        - El llamador decide cómo manejar (reintentar, default, etc.)
        - Evita excepciones en request de API (devuelve 500 con mensaje)
        """
        try:
            # Validar que el modelo existe
            modelo = self.model  # Esto carga si es necesario
            
            # Crear DataFrame con datos de entrada
            # Nota: El orden de columnas debe coincidir con el entrenamiento
            df_input = pd.DataFrame([datos_meteorologicos])
            
            # Asegurar orden de columnas (importante para sklearn)
            if self._feature_names:
                df_input = df_input[self._feature_names]
            
            # Realizar predicción
            prediccion = modelo.predict(df_input)[0]
            
            logger.info(f"🔮 Predicción realizada: {prediccion:.2f} kW")
            
            return float(prediccion)
            
        except KeyError as e:
            logger.error(f"❌ Columna faltante en datos de entrada: {e}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error en predicción: {e}")
            return None
    
    def get_importancia_caracteristicas(self) -> Optional[Dict[str, float]]:
        """
        Retorna la importancia de cada feature en el modelo.
        
        Returns:
            Dict {nombre_feature: importancia_normalizada} ordenado de mayor a menor
            
        ¿Por qué es útil?
        - Interpretabilidad: Qué factor afecta más la generación?
        - Validación: Irradiancia debería ser más importante que temperatura
        - Debugging: Si importancias no tienen sentido, puede haber data leakage
        
        Ejemplo esperado:
        {
            'irradiancia_w_m2': 0.85,
            'temperatura_celsius': 0.15
        }
        """
        try:
            modelo = self.model
            
            # Verificar que el modelo tiene atributo de importancia
            if not hasattr(modelo, 'feature_importances_'):
                logger.warning("Modelo no soporta importancia de features")
                return None
            
            # Extraer nombres de features
            features = self._feature_names or []
            if not features:
                logger.warning("Nombres de features no disponibles")
                return None
            
            # Combinar feature → importancia
            importancias = dict(zip(features, modelo.feature_importances_))
            
            # Ordenar de mayor a menor importancia
            importancias_ordenadas = dict(
                sorted(importancias.items(), key=lambda x: x[1], reverse=True)
            )
            
            return importancias_ordenadas
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo importancia: {e}")
            return None
```

---

## 7. API REST <a name="api"></a>

### `app/api/routes.py`

```python
"""
API REST para Granja Solar

Endpoints:
- /salud: Health check
- /datos: CRUD de mediciones
- /modelo: Entrenamiento y predicción

Arquitectura:
- Blueprints de Flask para modularidad
- Versionado en URL (/v1/) para backward compatibility
- Manejo centralizado de errores
- Logging de peticiones y respuestas

Seguridad:
- Input validation en cada endpoint
- No expone excepciones internas al cliente (evita info leak)
- Usa HTTP status codes semánticos
"""

from flask import Blueprint, jsonify, request
from http import HTTPStatus  # Constantes semánticas (200, 404, etc.)
from app.core.data_manager import DataManager
from app.core.predictor import Predictor
from app.config import Config

# Crear blueprint con prefijo de versión
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Inicializar dependencias (singletons por módulo)
# Nota: En producción, usar Flask-Injector o similar
data_manager = DataManager(Config.DATA_PATH)
predictor = Predictor(Config.MODEL_PATH)


@api_bp.route('/salud', methods=['GET'])
def health_check():
    """
    Health check del servicio.
    
    Returns:
        200 OK si el servicio está disponible
        
    ¿Para qué sirve?
    - Kubernetes readiness/liveness probes
    - Monitoreo uptime (Pingdom, Datadog)
    - Load balancers health checks
    """
    return jsonify({
        "status": "saludable",
        "servicio": "granja-solar-api",
        "version": "1.0.0"
    }), HTTPStatus.OK


@api_bp.route('/datos/resumen', methods=['GET'])
def resumen_datos():
    """
    Retorna métricas agregadas de rendimiento.
    
    Returns:
        200: JSON con shape, columnas, eficiencia promedio, correlación
        
    ¿Por qué GET sin parámetros?
    - Operation idempotente: llamadas repetidas dan mismo resultado
    - Cacheable: se puede almacenar en CDN/redis por 5 min
    - Seguro: no modifica estado del servidor
    """
    try:
        summary = data_manager.get_summary()
        return jsonify(summary), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error en resumen: {e}")
        # No exponer detalles internos al cliente
        return jsonify({"error": "Error interno obteniendo resumen"}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/datos', methods=['GET'])
def obtener_datos():
    """
    Retorna mediciones crudas con paginación.
    
    Query params:
        limite (int, default=100): Número máximo de registros
        offset (int, default=0): Número de registros a saltar
        
    Returns:
        200: Lista de objetos JSON con mediciones
        
    ¿Por qué paginación?
    - Previene OOM (Out of Memory) si dataset es grande
- Reduce tiempo de respuesta
- Mejora UX en frontend (carga incremental)
    """
    try:
        # Extraer parámetros de query con defaults
        limite = request.args.get('limite', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        # Validar rangos
        if limite > 1000:
            return jsonify({"error": "Limite máximo es 1000"}), HTTPStatus.BAD_REQUEST
        
        if offset < 0 or limite < 0:
            return jsonify({"error": "Offset y limite deben ser positivos"}), HTTPStatus.BAD_REQUEST
        
        df = data_manager.dataframe.iloc[offset:offset+limite]
        
        # Convertir a JSON
        # orient='records' crea lista de objetos (más RESTful)
        return jsonify(df.to_dict(orient='records')), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error obteniendo datos: {e}")
        return jsonify({"error": "Error obteniendo datos"}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/datos/filtrar', methods=['POST'])
def filtrar_datos():
    """
    Filtra datos basado en condiciones dinámicas.
    
    Body JSON:
        {
            "temperatura_celsius": 25,
            "panel_id": "P001"
        }
        
    Returns:
        200: Lista de registros que cumplen condiciones
        
    ¿Por qué POST en vez de GET?
    - GET con body es malo (no está en espec HTTP y algunos clientes lo ignoran)
    - Condiciones complejas no caben en URL (límite de 2048 caracteres)
    - Más seguro: datos no quedan en logs de servidor/proxy
    """
    try:
        # Validar que el body es JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), HTTPStatus.BAD_REQUEST
        
        condiciones = request.get_json()
        
        # Validar que no está vacío
        if not condiciones:
            return jsonify({"error": "Body JSON no puede estar vacío"}), HTTPStatus.BAD_REQUEST
        
        # Filtrar usando DataManager
        df_filtrado = data_manager.filtrar_por_condiciones(condiciones)
        
        return jsonify(df_filtrado.to_dict(orient='records')), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error filtrando datos: {e}")
        return jsonify({"error": "Error filtrando datos"}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/datos', methods=['POST'])
def agregar_medicion():
    """
    Agrega una nueva medición de panel solar.
    
    Body JSON:
        {
            "timestamp": "2024-01-15T12:00:00",
            "potencia_generada_kw": 150.5,
            "irradiancia_w_m2": 850,
            "temperatura_celsius": 32.1,
            "panel_id": "P001",
            "inversor_id": "INV01"
        }
        
    Returns:
        201: Created si se agregó correctamente
        
    ¿Por qué 201 Created?
    - RFC 7231: POST que crea recurso debe retornar 201
    - Location header podría incluir URL al nuevo recurso
    - Distingue de 200 OK (éxito sin creación)
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), HTTPStatus.BAD_REQUEST
        
        medicion = request.get_json()
        
        # Validar campos esenciales
        required = ['timestamp', 'potencia_generada_kw', 'irradiancia_w_m2', 'temperatura_celsius']
        missing = [field for field in required if field not in medicion]
        
        if missing:
            return jsonify({"error": f"Campos requeridos faltantes: {missing}"}), HTTPStatus.BAD_REQUEST
        
        # Intentar agregar
        success = data_manager.agregar_medicion(medicion)
        
        if success:
            return jsonify({"mensaje": "Medición agregada", "timestamp": medicion['timestamp']}), HTTPStatus.CREATED
        
        return jsonify({"error": "No se pudo agregar medición"}), HTTPStatus.BAD_REQUEST
        
    except Exception as e:
        logger.error(f"Error agregando medición: {e}")
        return jsonify({"error": "Error interno"}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/modelo/entrenar', methods=['POST'])
def entrenar_modelo():
    """
    Entrena el modelo predictivo con datos históricos.
    
    Returns:
        200: Métricas de rendimiento (R², RMSE)
        
    ¿Por qué POST si es idempotente?
    - No es idempotente: cada llamada entrena un modelo diferente (random_state podría cambiar)
    - Crea/modifica recurso (el archivo .pkl)
    - Operación costosa (puede tardar segundos/minutos)
    """
    try:
        df = data_manager.dataframe
        
        # Verificar que hay suficientes datos
        if len(df) < 50:
            return jsonify({"error": "Se requieren al menos 50 muestras"}), HTTPStatus.BAD_REQUEST
        
        # Entrenar usando Predictor
        resultado = predictor.entrenar_modelo(df)
        
        return jsonify(resultado), HTTPStatus.OK
        
    except Exception as e:
        logger.error(f"Error entrenando modelo: {e}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/modelo/predecir', methods=['POST'])
def predecir_generacion():
    """
    Predice generación basada en condiciones meteorológicas.
    
    Body JSON:
        {
            "irradiancia_w_m2": 800,
            "temperatura_celsius": 28.5
        }
        
    Returns:
        200: {"prediccion": 156.7}
        
    ¿Por qué valores en JSON y no query params?
    - Valores son flotantes con decimales (problemas de encoding en URL)
    - Más de 2 features haría URL muy larga
    - Consistencia con otros endpoints POST
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), HTTPStatus.BAD_REQUEST
        
        datos = request.get_json()
        
        # Validar datos de entrada
        if 'irradiancia_w_m2' not in datos or 'temperatura_celsius' not in datos:
            return jsonify({"error": "Debe incluir irradiancia_w_m2 y temperatura_celsius"}), HTTPStatus.BAD_REQUEST
        
        # Realizar predicción
        prediccion = predictor.predecir(datos)
        
        if prediccion is not None:
            return jsonify({"prediccion": prediccion}), HTTPStatus.OK
        
        return jsonify({"error": "Predicción fallida"}), HTTPStatus.BAD_REQUEST
        
    except RuntimeError as e:
        # Modelo no entrenado
        return jsonify({"error": str(e)}), HTTPStatus.PRECONDITION_FAILED
        
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        return jsonify({"error": "Error interno en predicción"}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/modelo/importancia', methods=['GET'])
def importancia_caracteristicas():
    """
    Retorna importancia de variables en el modelo entrenado.
    
    Returns:
        200: {"irradiancia_w_m2": 0.85, "temperatura_celsius": 0.15}
        
    ¿Por qué GET?
    - Operación idempotente (no modifica estado)
    - Cacheable (importancia no cambia hasta nuevo entrenamiento)
    - Representa un recurso (la importancia es propiedad del modelo)
    """
    try:
        importancia = predictor.get_importancia_caracteristicas()
        
        if importancia:
            return jsonify(importancia), HTTPStatus.OK
        
        return jsonify({"error": "Modelo no entrenado o no soporta importancia"}), HTTPStatus.PRECONDITION_FAILED
        
    except Exception as e:
        logger.error(f"Error obteniendo importancia: {e}")
        return jsonify({"error": "Error interno"}), HTTPStatus.INTERNAL_SERVER_ERROR
```

---

## 8. Dashboard Interactivo <a name="dashboard"></a>

### `app/dashboard/app.py`

```python
"""
Dashboard Interactivo para Operadores de Granja Solar

Construido con Dash (framework Plotly para Python).
Permite visualizar en tiempo real:
- Tendencias de generación
- Distribuciones de eficiencia
- Predicción interactiva
- Importancia de variables

Arquitectura:
- App Dash ejecutada en thread separado (no bloquea Flask)
- Comunicación mediante archivos CSV (en producción usar Redis/DB)
- Callbacks reactivos: cambios en inputs actualizan gráficos
"""

import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

from app.core.data_manager import DataManager
from app.core.predictor import Predictor
from app.config import Config

# Inicializar app Dash
# external_stylesheets: CSS de Bootstrap para diseño responsivo
# url_base_pathname: Monta dashboard en /dashboard/
app = dash.Dash(
    __name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
    url_base_pathname='/dashboard/'
)

# Título de la pestaña del navegador
app.title = "Dashboard Granja Solar"

# Inicializar managers (mismos que usa la API)
data_manager = DataManager(Config.DATA_PATH)
predictor = Predictor(Config.MODEL_PATH)


# Layout principal
app.layout = html.Div([
    # Cabecera
    html.Div([
        html.H1('🌞 Dashboard de Granja Solar', style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.P('Monitoreo y predicción de rendimiento de paneles fotovoltaicos', 
               style={'textAlign': 'center', 'fontSize': '18px'})
    ], className='row'),
    
    # KPIs en cards
    html.Div([
        html.Div([
            html.H3('⚡ Potencia Actual'),
            html.H2(id='kpi-potencia', style={'color': '#f39c12'})
        ], className='three columns', style={'backgroundColor': '#f7f7f7', 'padding': '20px', 'borderRadius': '10px'}),
        
        html.Div([
            html.H3('🌡️ Temp Promedio'),
            html.H2(id='kpi-temperatura', style={'color': '#e74c3c'})
        ], className='three columns', style={'backgroundColor': '#f7f7f7', 'padding': '20px', 'borderRadius': '10px'}),
        
        html.Div([
            html.H3('☀️ Irradiancia'),
            html.H2(id='kpi-irradiancia', style={'color': '#3498db'})
        ], className='three columns', style={'backgroundColor': '#f7f7f7', 'padding': '20px', 'borderRadius': '10px'}),
        
        html.Div([
            html.H3('📊 Eficiencia'),
            html.H2(id='kpi-eficiencia', style={'color': '#27ae60'})
        ], className='three columns', style={'backgroundColor': '#f7f7f7', 'padding': '20px', 'borderRadius': '10px'})
    ], className='row', style={'marginBottom': '30px'}),
    
    # Filtros
    html.Div([
        html.Div([
            html.Label('Rango de Fechas:'),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=datetime.now() - timedelta(days=7),
                end_date=datetime.now(),
                display_format='YYYY-MM-DD'
            )
        ], className='six columns'),
        
        html.Div([
            html.Label('Panel ID:'),
            dcc.Dropdown(
                id='panel-selector',
                placeholder="Todos los paneles",
                multi=True
            )
        ], className='six columns')
    ], className='row', style={'marginBottom': '30px'}),
    
    # Gráficos principales
    html.Div([
        html.Div([
            html.H3('📈 Serie Temporal de Generación'),
            dcc.Graph(id='time-series-chart')
        ], className='twelve columns')
    ], className='row', style={'marginBottom': '30px'}),
    
    html.Div([
        html.Div([
            html.H3('📊 Distribución de Eficiencia'),
            dcc.Graph(id='efficiency-histogram')
        ], className='six columns'),
        
        html.Div([
            html.H3('☢️ Correlación Irradiancia vs Potencia'),
            dcc.Graph(id='scatter-correlacion')
        ], className='six columns')
    ], className='row', style={'marginBottom': '30px'}),
    
    # Predicción interactiva
    html.Div([
        html.H3('🔮 Predicción Interactiva'),
        html.P('Ajuste las condiciones meteorológicas para predecir generación:'),
        
        html.Div([
            html.Div([
                html.Label('Irradiancia (W/m²):'),
                dcc.Slider(
                    id='slider-irradiancia',
                    min=0, max=1200, step=50, value=800,
                    marks={i: str(i) for i in range(0, 1201, 200)}
                )
            ], className='six columns'),
            
            html.Div([
                html.Label('Temperatura (°C):'),
                dcc.Slider(
                    id='slider-temperatura',
                    min=0, max=50, step=1, value=25,
                    marks={i: str(i) for i in range(0, 51, 10)}
                )
            ], className='six columns')
        ], className='row', style={'marginBottom': '20px'}),
        
        html.Div(id='prediction-output', style={
            'fontSize': '24px',
            'textAlign': 'center',
            'padding': '20px',
            'backgroundColor': '#e8f4fd',
            'borderRadius': '10px'
        })
    ], className='row', style={'marginBottom': '30px'}),
    
    # Importancia de variables
    html.Div([
        html.H3('🎯 Importancia de Variables en el Modelo'),
        dcc.Graph(id='feature-importance-chart')
    ], className='row')
])


# Callbacks

@app.callback(
    [Output('kpi-potencia', 'children'),
     Output('kpi-temperatura', 'children'),
     Output('kpi-irradiancia', 'children'),
     Output('kpi-eficiencia', 'children'),
     Output('panel-selector', 'options')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_kpis(start_date, end_date):
    """
    Actualiza los KPIs basados en rango de fechas.
    
    ¿Por qué en un solo callback?
    - Eficiencia: Una lectura de datos para múltiples outputs
    - Consistencia: Todos los KPIs provienen del mismo subset
    - Menor overhead: Menos llamadas al DataManager
    """
    df = data_manager.dataframe
    
    # Filtrar por fecha si se especificó
    if start_date and end_date:
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    
    # Calcular métricas
    potencia_promedio = df['potencia_generada_kw'].mean()
    temp_promedio = df['temperatura_celsius'].mean()
    irradiancia_promedio = df['irradiancia_w_m2'].mean()
    
    # Calcular eficiencia (evitando división por cero)
    eficiencia = (df['potencia_generada_kw'] / df['irradiancia_w_m2'].replace(0, float('nan'))).mean() * 1000
    
    # Opciones para dropdown de paneles
    if 'panel_id' in df.columns:
        panel_options = [{'label': pid, 'value': pid} for pid in df['panel_id'].unique()]
    else:
        panel_options = []
    
    return (
        f"{potencia_promedio:.1f} kW",
        f"{temp_promedio:.1f} °C",
        f"{irradiancia_promedio:.0f} W/m²",
        f"{eficiencia:.2f} kW/W",
        panel_options
    )


@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('panel-selector', 'value')]
)
def update_time_series(start_date, end_date, selected_panels):
    """
    Actualiza la serie temporal de generación.
    
    ¿Por qué Plotly en vez de Matplotlib?
    - Interactivo: zoom, hover, tooltip
    - Responsive: se adapta a tamaño de pantalla
    - Exportable: PNG/SVG desde el UI
    - No requiere backend de rendering (como Matplotlib)
    """
    df = data_manager.dataframe
    
    # Aplicar filtros
    if start_date and end_date:
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    
    if selected_panels:
        df = df[df['panel_id'].isin(selected_panels)]
    
    # Crear línea de tendencia
    fig = px.line(
        df, 
        x='timestamp', 
        y='potencia_generada_kw',
        title='Generación de Potencia a lo Largo del Tiempo',
        labels={
            'timestamp': 'Fecha/Hora',
            'potencia_generada_kw': 'Potencia Generada (kW)'
        }
    )
    
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig


@app.callback(
    Output('efficiency-histogram', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_efficiency_hist(start_date, end_date):
    """
    Histograma de eficiencia de paneles.
    """
    df = data_manager.dataframe
    
    if start_date and end_date:
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    
    # Calcular eficiencia
    df['eficiencia'] = df['potencia_generada_kw'] / df['irradiancia_w_m2'].replace(0, float('nan'))
    
    fig = px.histogram(
        df,
        x='eficiencia',
        nbins=30,
        title='Distribución de Eficiencia de Paneles',
        labels={'eficiencia': 'Eficiencia (kW/W)'},
        color_discrete_sequence=['#2ecc71']
    )
    
    fig.update_layout(template='plotly_whأمتe')
    
    return fig


@app.callback(
    Output('scatter-correlacion', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_scatter(start_date, end_date):
    """
    Scatter plot irradiancia vs potencia (valida correlación esperada).
    """
    df = data_manager.dataframe
    
    if start_date and end_date:
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
    
    fig = px.scatter(
        df,
        x='irradiancia_w_m2',
        y='potencia_generada_kw',
        title='Irradiancia vs Potencia',
        labels={
            'irradiancia_w_m2': 'Irradiancia (W/m²)',
            'potencia_generada_kw': 'Potencia (kW)'
        },
        trendline='ols',  # Línea de tendencia (ordinary least squares)
        color_discrete_sequence=['#3498db']
    )
    
    fig.update_layout(template='plotly_white')
    
    return fig


@app.callback(
    Output('prediction-output', 'children'),
    [Input('slider-irradiancia', 'value'),
     Input('slider-temperatura', 'value')],
    prevent_initial_call=True
)
def actualizar_prediccion(irradiancia, temperatura):
    """
    Realiza predicción en tiempo real al mover sliders.
    
    prevent_initial_call=True evita que se ejecute al cargar la página,
    mejorando la experiencia inicial (no hay predicción vacía).
    """
    try:
        prediccion = predictor.predecir({
            'irradiancia_w_m2': irradiancia,
            'temperatura_celsius': temperatura
        })
        
        if prediccion is not None:
            return html.Div([
                html.H4(f'🔮 Potencia Predicha: {prediccion:.2f} kW', style={'color': '#2980b9'}),
                html.P(f'Condiciones: {irradiancia} W/m², {temperatura}°C')
            ])
        
        return html.Div([
            html.H4('❌ No se pudo realizar predicción', style={'color': 'red'}),
            html.P('Verifica que el modelo esté entrenado')
        ])
        
    except RuntimeError as e:
        return html.Div([
            html.H4('⚠️ Modelo no entrenado', style={'color': 'orange'}),
            html.P(str(e))
        ])


@app.callback(
    Output('feature-importance-chart', 'figure'),
    [Input('feature-importance-chart', 'id')]
)
def update_importance_chart(_):
    """
    Muestra importancia de variables del modelo.
    """
    importancia = predictor.get_importancia_caracteristicas()
    
    if importancia:
        fig = px.bar(
            x=list(importancia.values()),
            y=list(importancia.keys()),
            orientation='h',
            title='Importancia de Variables en el Modelo',
            labels={
                'x': 'Importancia Relativa',
                'y': 'Variable'
            },
            color=list(importancia.values()),
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(template='plotly_white')
        
        return fig
    
    # Mensaje si no hay modelo
    fig = go.Figure()
    fig.add_annotation(
        text="Modelo no entrenado.<br>Usa /api/v1/modelo/entrenar",
        xref="paper", yref="paper",
        x=0.5, y=0.5, xanchor='center', yanchor='middle',
        showarrow=False, font=dict(size=16)
    )
    
    return fig


# Inicialización de servidor (solo para desarrollo)
if __name__ == '__main__':
    app.run_server(debug=True)
```

---

## 9. Ejecución y Despliegue <a name="ejecucion"></a>

### `run.py` - Punto de Entrada

```python
"""
Script principal para iniciar la aplicación completa.

Inicia dos servicios en threads separados:
1. Flask API (puerto 5000): Endpoint REST
2. Dash Dashboard (puerto 8050): Visualización

¿Por qué threads en vez de procesos separados?
- Simplicidad: Un solo archivo para iniciar todo
- Recursos compartidos: Ambos usan mismo DataManager (caché de datos)
- Desarrollo: Fácil debugging con un solo comando

Para producción, considera:
- Gunicorn con múltiples workers para API
- Supervisor/Poetry para Dash
- Orquestador (Kubernetes) gestionando dos pods
"""

import os
from app import create_app
from threading import Thread
from app.dashboard.app import app as dash_app

def run_dashboard():
    """
    Función de ejecución para el thread del dashboard.
    
    Configuración:
    - debug=False: Modo producción (no reload automático)
    - use_reloader=False: Evita conflictos con threads
    """
    dash_app.run_server(
        host='0.0.0.0',
        port=int(os.getenv('DASH_PORT', 8050)),
        debug=False,
        use_reloader=False  # Crítico: evita que Flask reinicie al detectar cambios
    )


if __name__ == '__main__':
    # Crear app Flask con configuración según entorno
    flask_app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    # Iniciar Dashboard en thread daemon (termina con main thread)
    dashboard_thread = Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()
    logger.info(f"🚀 Dashboard iniciado en thread {dashboard_thread.ident}")
    
    # Iniciar Flask en main thread
    flask_port = int(os.getenv('PORT', 5000))
    logger.info(f"🚀 Flask API iniciando en puerto {flask_port}")
    
    flask_app.run(
        host='0.0.0.0',
        port=flask_port,
        debug=flask_app.config['DEBUG']
    )
```

### Primeros Pasos (Windows)

**1. Instalar dependencias**:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**2. Crear dataset de ejemplo**:
```python
# data_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Simular una granja solar de 10 paneles durante 30 días
np.random.seed(42)

fechas = pd.date_range(
    start=datetime.now() - timedelta(days=30),
    end=datetime.now(),
    freq='15min'  # Datos cada 15 minutos
)

data = []
for fecha in fechas:
    # Patrón diario: más irradiancia al medio día
    hora = fecha.hour + fecha.minute/60
    irradiancia_base = max(0, -((hora-12)**2) + 100) * 9  # Parábola
    
    for panel_id in range(1, 11):
        # Añadir ruido realista
        irradiancia = np.random.normal(irradiancia_base, 20)
        irradiancia = max(0, min(1200, irradiancia))
        
        temp = np.random.normal(25 + irradiancia/50, 3)
        temp = max(0, min(50, temp))
        
        # Potencia con correlación positiva a irradiancia y negativa a temp
        potencia = irradiancia * 0.18 - temp * 0.5 + np.random.normal(0, 5)
        potencia = max(0, potencia)
        
        data.append({
            'timestamp': fecha,
            'panel_id': f'P{panel_id:03d}',
            'potencia_generada_kw': potencia,
            'irradiancia_w_m2': irradiancia,
            'temperatura_celsius': temp
        })

df = pd.DataFrame(data)
df.to_csv('data/paneles_solar.csv', index=False)
print(f"✅ Dataset creado: {len(df)} registros")
```

Ejecutar en CMD:
```cmd
python data_generator.py
```

**3. Iniciar aplicación**:
```cmd
python run.py
```

**4. Verificar servicios**:

CMD (nueva terminal):
```cmd
# API
curl http://localhost:5000/api/v1/salud

# Entrenar modelo
curl -X POST http://localhost:5000/api/v1/modelo/entrenar

# Hacer predicción
curl -X POST http://localhost:5000/api/v1/modelo/predecir ^
  -H "Content-Type: application/json" ^
  -d "{\"irradiancia_w_m2\": 800, \"temperatura_celsius\": 28.5}"

# Dashboard
# Abrir navegador en http://localhost:8050
```


## 10. Mejores Prácticas Aplicadas <a name="practicas"></a>

| Práctica | Implementación | Beneficio |
|----------|----------------|-----------|
| **SRP** | Cada clase tiene una única responsabilidad | Facilita mantenimiento y testing |
| **Dependency Injection** | DataManager recibe `data_path` | Desacoplamiento y testabilidad |
| **Factory Pattern** | `create_app()` | Configuración flexible por entorno |
| **Lazy Loading** | `@property` en managers | Mejora startup time y uso de memoria |
| **Type Hints** |`: Optional[Dict[str, Any]]` | Autocomplete, linting, documentación |
| **Error Handling** | Try/except con logging | Debugging y monitoreo en producción |
| **HTTP Semántico** | Status codes correctos | Clientes REST pueden manejar errores |
| **Data Validation** | `_validar_datos_solar()` | Garantía de calidad de datos |
| **Versionado API** | `/api/v1/` | Backward compatibility |
| **Environment Variables** | `.env` + `python-dotenv` | Seguridad y configuración externa |
| **Threading** | Dash en thread daemon | Ambos servicios sin bloqueo |
| **Logging** | `logger = logging.getLogger(__name__)` | Diferentes niveles por módulo |
| **Docstrings** | Todos los métodos documentados | Sphinx, IDE hints, onboarding |
| **Test Structure** | Directorio `tests/` | `pytest` descubre automáticamente |
| **.gitignore** | `data/, models/, .env` | No versionar datos sensibles o generados |
| **Modularidad** | `__init__.py` en cada paquete | Organización clara y reusabilidad |

---
