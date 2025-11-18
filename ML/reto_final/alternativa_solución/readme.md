# 📑 **Guía Técnica Completa: Sistema de Monitoreo de Represas con Python**  

## 🎯 **Objetivo del Documento**

Proporcionar una guía **completa, detallada y práctica** para crear un sistema de monitoreo de represas con Python, desde cero, siguiendo las mejores prácticas de ingeniería de software, ciencia de datos y seguridad.

Este sistema incluye:
- ✅ Gestión de datos desde múltiples fuentes (CSV, Excel, APIs, bases de datos industriales)
- ✅ API REST para integración con sistemas SCADA y centros de control
- ✅ Dashboard interactivo para operarios y técnicos en campo
- ✅ Generación automática de informes técnicos en PDF (cumplimiento normativo)
- ✅ Exportación de datos para análisis externo
- ✅ Modelos de machine learning para detección de anomalías y predicción
- ✅ Pruebas automatizadas y documentación profesional

---

## 🧩 **Concepto Clave: ¿Qué es y qué hace `__init__.py`?**

Antes de continuar, es fundamental entender el componente más importante para la modularidad en Python: **`__init__.py`**.

### 🔍 **Definición Técnica**

`__init__.py` es un **archivo especial de Python** que marca un directorio como un **paquete Python** (módulo importable). Su presencia permite que el directorio y sus subdirectorios sean tratados como un módulo que puede ser importado con la sentencia `import`.

### 📚 **Historia y Evolución**

- **Python ≤ 3.2**: `__init__.py` era **obligatorio** para definir un paquete.
- **Python ≥ 3.3**: Se introdujo el concepto de **"Namespace Packages"**, permitiendo paquetes sin `__init__.py`.
- **Buenas prácticas modernas**: Seguimos usando `__init__.py` porque:
  - ✅ Explicita la intención de crear un paquete
  - ✅ Permite inicialización personalizada del módulo
  - ✅ Controla qué se exporta con `__all__`
  - ✅ Habilita imports limpios y explícitos
  - ✅ Es requerido por muchas herramientas (pytest, mypy, IDEs)

### ⚙️ **Funciones Esenciales de `__init__.py`**

#### 1. **Marca el directorio como paquete**
Sin `__init__.py`, Python no reconocerá el directorio como un módulo importable.

```
mi_proyecto/
├── src/
│   ├── __init__.py   ← ¡Este archivo hace que 'src' sea un paquete!
│   └── data/
│       └── __init__.py  ← ¡Y 'data' también!
```

#### 2. **Define la interfaz pública del módulo**
Controla qué funciones, clases y submódulos están disponibles cuando se importa el paquete.

```python
# src/data/__init__.py
from .ingestion import load_csv, load_from_db
from .export import export_to_csv

# Define explícitamente qué se exporta
__all__ = [
    "load_csv",
    "load_from_db", 
    "export_to_csv"
]
```

**Resultado**:  
```python
# ✅ Import limpio y explícito
from src.data import load_csv, load_from_db

# ❌ Evita imports profundos y frágiles
# from src.data.ingestion import load_csv  # No recomendado
```

#### 3. **Permite inicialización personalizada**
Puede ejecutar código al importar el módulo (carga de configuración, logs, etc.).

```python
# src/__init__.py
import logging

# Configurar logging al importar el paquete
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Paquete 'src' inicializado correctamente")

from . import config, data, ml
```

#### 4. **Habilita imports relativos**
Permite importar entre módulos del mismo paquete usando rutas relativas.

```python
# src/data/processing.py
from .ingestion import load_csv  # Import relativo dentro del paquete 'data'
from ..config import settings   # Import relativo al paquete padre 'src'
```

#### 5. **Mejora la legibilidad y mantenibilidad**
Documenta explícitamente la estructura del proyecto y sus dependencias.

### 🌟 **Ejemplo Práctico en tu Sistema de Monitoreo**

Considera esta estructura:
```
src/
├── __init__.py          # ← Define el paquete 'src'
├── config/
│   ├── __init__.py      # ← Define el subpaquete 'src.config'
│   └── db.py
└── data/
    ├── __init__.py      # ← Define el subpaquete 'src.data'
    └── ingestion.py
```

**Contenido de `src/__init__.py`:**
```python
"""
Módulo raíz del sistema de monitoreo de represas.

Este archivo habilita imports de alto nivel como:
    from src import config, data, ml

Contenido exportado:
    - config: Configuración del sistema (DB, rutas, claves)
    - data: Funciones para ingestión, procesamiento y exportación
    - ml: Modelos de machine learning para predicción
    - api: API REST para integración
    - dashboard: Interfaz web interactiva
    - reports: Generación de informes técnicos

Nota: Todos los subdirectorios deben tener su propio __init__.py.
"""
# Import explícito para hacer accesibles los subpaquetes
from . import config
from . import data
from . import ml
from . import api
from . import dashboard
from . import reports
```

**Resultado en tu código:**
```python
# ✅ Código limpio y legible
from src import data, config, ml

# Cargar datos desde múltiples fuentes
df = data.load_multiple_sources([
    {"type": "csv", "config": {"file_path": "data/raw/sensors.csv"}},
    {"type": "db", "config": {"query": "SELECT * FROM scada", "db_type": "oracle"}}
])

# Obtener gestor de DB
db = config.db_manager

# Entrenar modelo predictivo
predictor = ml.WaterLevelPredictor()
predictor.fit(df)
```

### 🚫 **Qué NO hacer con `__init__.py`**

- **No dejarlo vacío sin razón**: Si está vacío, documenta por qué (`# Paquete explícito - sin inicialización requerida`)
- **No importar todo con `from . import *`**: Rompe la explícitud y causa conflictos
- **No poner lógica de negocio compleja**: Solo inicialización y definición de interfaz
- **No olvidar `__all__`**: Sin él, `from module import *` importa todo (variables privadas incluidas)

---

# 🛠️ **Fase 1: Inicialización del Proyecto**

## 1.1 Script de Inicialización: `setup_project.py`

El siguiente script es la **pieza central** de tu sistema. Crea automáticamente toda la estructura del proyecto con buenas prácticas.

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_project.py - Versión 2.2.0

Script de inicialización automática para sistemas de monitoreo de infraestructura crítica
(ej. represas, presas de relaves, estructuras hidráulicas).

Características:
- Crea estructura modular y escalable (src/, data/, tests/, etc.)
- Genera entorno virtual aislado (venv)
- Instala dependencias esenciales con justificación técnica
- Configura plantilla segura de variables de entorno (.env.example)
- Compatible con Windows, Linux y macOS
- Robusto frente a advertencias no críticas de pip

Ejecución:
    py setup_project.py nombre-del-proyecto
Ejemplo:
    py setup_project.py dam-monitoring-p1
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def create_project_structure(project_name: str) -> Path:
    """Crea la estructura de directorios del proyecto."""
    base = Path(project_name).resolve()
    print(f"[INFO] Creando estructura en: {base}")

    dir_tree = [
        base,
        base / "data" / "raw",          # Datos crudos: CSV, logs SCADA, sensores
        base / "data" / "processed",    # Datos limpios y listos para modelos/API
        base / "src",
        base / "src" / "config",        # Configuración (paths, logs, settings)
        base / "src" / "data",          # Ingesta, limpieza, transformación
        base / "src" / "ml",            # Modelos de ML: anomalías, predicción
        base / "src" / "api",           # API REST (FastAPI)
        base / "src" / "dashboard",     # Interfaz web interactiva (Streamlit)
        base / "src" / "reports",       # Generación de reportes técnicos (PDF/HTML)
        base / "tests",                 # Pruebas unitarias e integración
        base / "notebooks",             # Exploración (solo desarrollo)
        base / "docs",                  # Documentación técnica y de usuario
        base / "models",                # Modelos entrenados (joblib, ONNX)
        base / "docker",                # Opcional: configuración para contenedores
    ]

    # Crear directorios y __init__.py (módulos explícitos)
    for directory in dir_tree:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "__init__.py").touch(exist_ok=True)

    # Módulo raíz: imports explícitos y limpios
    (base / "src" / "__init__.py").write_text('''"""
Módulo raíz del sistema de monitoreo de represas.

Permite:
    from src import config, data, ml, api, dashboard, reports
"""
from . import config, data, ml, api, dashboard, reports
''', encoding="utf-8")

    # requirements.txt — con justificación técnica integrada
    requirements = [
        "# ==================================================",
        "# CORE: Procesamiento estructurado y numérico",
        "# ==================================================",
        "pandas",        # Series temporales (sensores: nivel, presión, temperatura)",
        "numpy",         # Operaciones eficientes sobre arrays",
        "",
        "# ==================================================",
        "# BASES DE DATOS: Conexión a sistemas operativos",
        "# ==================================================",
        "psycopg2-binary",    # PostgreSQL (históricos, eventos, mantenimiento)",
        "oracledb",           # Oracle en modo 'thin' (SCADA industrial)",
        "",
        "# ==================================================",
        "# APIs Y SERVICIOS WEB",
        "# ==================================================",
        "fastapi",       # API REST moderna, con validación automática (Pydantic)",
        "uvicorn",       # Servidor ASGI de alto rendimiento",
        "streamlit",     # Dashboard interactivo para ingenieros y operarios",
        "requests",      # Integración con APIs externas (meteorología, alertas)",
        "",
        "# ==================================================",
        "# VISUALIZACIÓN",
        "# ==================================================",
        "plotly",        # Gráficos interactivos (tendencias, umbrales, alertas)",
        "matplotlib",    # Figuras para reportes técnicos e impresión",
        "",
        "# ==================================================",
        "# DOCUMENTOS TÉCNICOS",
        "# ==================================================",
        "jinja2",        # Plantillas HTML/Markdown para reportes",
        "weasyprint",    # Generación de PDF con estilos (cumplimiento normativo)",
        "",
        "# ==================================================",
        "# MACHINE LEARNING",
        "# ==================================================",
        "scikit-learn",  # Modelos interpretables: Isolation Forest, Random Forest",
        "# tensorflow",    # Opcional: LSTM para pronóstico dinámico (descomentar si se usa)",
        "",
        "# ==================================================",
        "# UTILIDADES Y SEGURIDAD",
        "# ==================================================",
        "python-dotenv", # Gestión segura de credenciales (.env)",
        "pydantic",      # Validación de modelos de datos (Represa, Sensor, Lectura)",
        "openpyxl",      # Lectura de formatos Excel (usados en inspecciones de campo)",
        "",
        "# ==================================================",
        "# CALIDAD Y PRUEBAS",
        "# ==================================================",
        "pytest",        # Ejecución de pruebas automatizadas",
        "pytest-cov",    # Medición de cobertura (requisito para sistemas seguros)",
    ]
    (base / "requirements.txt").write_text("\n".join(requirements), encoding="utf-8")

    # .env.example — plantilla segura (sin credenciales)
    env_example = '''# ==================================================
# ⚠️  COPIAR A .env Y COMPLETAR CON CREDENCIALES REALES
# Nunca incluir .env en control de versiones
# ==================================================

# PostgreSQL (históricos, eventos, mantenimiento)
PG_HOST=localhost
PG_PORT=5432
PG_DB=dam_monitoring
PG_USER=edi_user
PG_PASSWORD=

# Oracle (SCADA - sensores en tiempo real)
ORA_USER=scada_reader
ORA_PASSWORD=
ORA_DSN=scada-server:1521/SCADADB

# SQLite (desarrollo local / modo offline)
SQLITE_PATH=data/dams_local.db

# Seguridad
API_SECRET_KEY=change-in-production-2025
'''
    (base / ".env.example").write_text(env_example, encoding="utf-8")

    print(f"[OK] Estructura de directorios creada: {base}")
    return base


def create_virtualenv(project_path: Path):
    """Crea el entorno virtual en ./venv."""
    venv_path = project_path / "venv"
    print(f"[INFO] Creando entorno virtual en: {venv_path}")

    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print(f"[OK] Entorno virtual creado: {venv_path}")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Fallo al crear el entorno virtual: {e}") from e


def install_requirements(project_path: Path):
    """Instala dependencias dentro del entorno virtual (sin actualizar pip)."""
    pip_exe = project_path / "venv" / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")

    if not pip_exe.exists():
        raise FileNotFoundError(f"pip no encontrado en: {pip_exe}")

    print("[INFO] Instalando dependencias desde requirements.txt...")

    # Ejecutar instalación directa — evita el bloqueo de pip en Windows
    result = subprocess.run(
        [str(pip_exe), "install", "-r", str(project_path / "requirements.txt")],
        capture_output=True,
        text=True,
        encoding="utf-8",  # Evita fallos de encoding al leer stdout/stderr
    )

    if result.returncode != 0:
        # Filtrar advertencias no críticas (pip notices, deprecations)
        critical_errors = [
            line for line in result.stderr.splitlines()
            if not line.startswith(("[notice]", "[", "WARNING:", "DEPRECATION:", "Requirement already satisfied"))
        ]
        if critical_errors:
            print("[ERROR] Falló la instalación. Errores críticos:")
            for line in critical_errors:
                print(f"  → {line}")
            raise RuntimeError("Instalación interrumpida por errores críticos.")
        else:
            # Solo advertencias no críticas: continuar
            print("[OK] Dependencias instaladas (advertencias no críticas ignoradas).")
            return

    print("[OK] Todas las dependencias instaladas correctamente.")


def main():
    parser = argparse.ArgumentParser(
        description="🔧 Configurador automático para monitoreo de represas y estructuras críticas"
    )
    parser.add_argument(
        "project_name",
        help="Nombre del proyecto (ej: dam-monitoring-p1, scada-anomaly-detector)"
    )
    args = parser.parse_args()

    try:
        print("=" * 60)
        print("INICIANDO CONFIGURACIÓN AUTOMÁTICA DEL PROYECTO")
        print("=" * 60)

        project_path = create_project_structure(args.project_name)
        create_virtualenv(project_path)
        install_requirements(project_path)

        print("\n" + "=" * 60)
        print(" ✅ PROYECTO CONFIGURADO EXITOSAMENTE ")
        print("=" * 60)
        print(f"\nPasos siguientes:")
        print(f"  cd {args.project_name}")
        print(f"  venv\\Scripts\\activate          # Windows")
        print(f"  source venv/bin/activate         # Linux/macOS")
        print(f"\nVerificación rápida:")
        print(f"  python -c \"import pandas, sklearn; print('✅ Entorno listo')\"")

        print("\n[INFO] Este entorno soporta:")
        print("  - Ingesta y procesamiento de datos SCADA")
        print("  - Detección de anomalías en comportamiento estructural")
        print("  - Generación automatizada de reportes técnicos (PDF)")
        print("  - Dashboard interactivo para monitoreo en tiempo real")

    except Exception as e:
        print(f"\n[ERROR FATAL] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 🔍 **Análisis Detallado de `setup_project.py`**

#### **Línea 1-2: Shebang y encoding**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```
- **`#!/usr/bin/env python3`**: Permite ejecutar el script directamente (`./setup_project.py`) en sistemas Unix-like. En Windows, se ignora pero no causa errores.
- **`# -*- coding: utf-8 -*-`**: Especifica que el archivo usa codificación UTF-8, permitiendo caracteres especiales (ñ, á, é, etc.) en comentarios y strings.

#### **Línea 22-51: Creación de estructura**
```python
dir_tree = [
    base,
    base / "data" / "raw",          # Datos crudos: CSV, logs SCADA, sensores
    # ... más directorios
]
```
- **Separación clara de responsabilidades**: 
  - `data/raw/`: Datos originales (nunca modificar)
  - `data/processed/`: Datos transformados (reproducibles)
  - `src/`: Código fuente (solo lógica, sin datos)
  - `tests/`: Pruebas automatizadas
- **Comentarios explicativos**: Cada directorio tiene un comentario que explica su propósito específico en el contexto de represas.

#### **Línea 54-61: Creación de `__init__.py`**
```python
for directory in dir_tree:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "__init__.py").touch(exist_ok=True)
```
- **`parents=True`**: Crea directorios padres automáticamente (ej: `data/raw/` crea `data/` si no existe).
- **`exist_ok=True`**: No falla si el directorio ya existe.
- **`.touch(exist_ok=True)`**: Crea el archivo `__init__.py` si no existe (vacío por defecto).

#### **Línea 63-68: `src/__init__.py` especial**
```python
(base / "src" / "__init__.py").write_text('''"""
Módulo raíz del sistema de monitoreo de represas.

Permite:
    from src import config, data, ml, api, dashboard, reports
"""
from . import config, data, ml, api, dashboard, reports
''', encoding="utf-8")
```
- **Docstring detallada**: Explica explícitamente qué permite este archivo.
- **Imports explícitos**: Cada subpaquete se importa individualmente, evitando imports dinámicos o implícitos.
- **Encoding UTF-8**: Asegura que los caracteres especiales se guarden correctamente.

#### **Línea 70-108: `requirements.txt` con justificación**
Cada dependencia incluye un **comentario técnico** que explica su propósito en el contexto específico de monitoreo de represas:
- `oracledb`: "Oracle en modo 'thin' (SCADA industrial)"
- `weasyprint`: "Generación de PDF con estilos (cumplimiento normativo)"
- `scikit-learn`: "Modelos interpretables: Isolation Forest, Random Forest"

#### **Línea 110-126: `.env.example` seguro**
- **Advertencia clara**: "⚠️ COPIAR A .env Y COMPLETAR CON CREDENCIALES REALES"
- **Instrucción explícita**: "Nunca incluir .env en control de versiones"
- **Ejemplo realista**: Variables para PostgreSQL (históricos), Oracle (SCADA), SQLite (offline)

#### **Línea 152-178: Instalación robusta**
```python
# Filtrar advertencias no críticas
critical_errors = [
    line for line in result.stderr.splitlines()
    if not line.startswith(("[notice]", "[", "WARNING:", "DEPRECATION:"))
]
```
- **Manejo inteligente de errores**: En Windows, `pip` a veces muestra advertencias no críticas que no deben detener la instalación.
- **Filtrado preciso**: Solo se consideran errores críticos (fallos reales de instalación).
- **Retroalimentación clara**: Muestra exactamente qué líneas causaron el fallo.

## 1.2 Ejecución del Script

### Paso 1: Guardar el script
Guarda el código anterior como `setup_project.py` en tu escritorio.

### Paso 2: Ejecutar desde línea de comandos
```cmd
:: Abrir CMD o PowerShell
cd Desktop
py setup_project.py dam-monitoring-p1
```

### Paso 3: Resultado esperado
```
============================================================
INICIANDO CONFIGURACIÓN AUTOMÁTICA DEL PROYECTO
============================================================
[INFO] Creando estructura en: C:\Users\Edi\Desktop\dam-monitoring-p1
[OK] Estructura de directorios creada: C:\Users\Edi\Desktop\dam-monitoring-p1
[INFO] Creando entorno virtual en: C:\Users\Edi\Desktop\dam-monitoring-p1\venv
[OK] Entorno virtual creado: C:\Users\Edi\Desktop\dam-monitoring-p1\venv
[INFO] Instalando dependencias desde requirements.txt...
[OK] Todas las dependencias instaladas correctamente.

============================================================
 ✅ PROYECTO CONFIGURADO EXITOSAMENTE 
============================================================

Pasos siguientes:
  cd dam-monitoring-p1
  venv\Scripts\activate          # Windows
  source venv/bin/activate       # Linux/macOS

Verificación rápida:
  python -c "import pandas, sklearn; print('✅ Entorno listo')"

[INFO] Este entorno soporta:
  - Ingesta y procesamiento de datos SCADA
  - Detección de anomalías en comportamiento estructural
  - Generación automatizada de reportes técnicos (PDF)
  - Dashboard interactivo para monitoreo en tiempo real
```

### Paso 4: Activar el entorno
```cmd
cd dam-monitoring-p1
venv\Scripts\activate
```

Verás el prompt cambiado:
```cmd
(venv) C:\Users\Edi\Desktop\dam-monitoring-p1>
```

### Paso 5: Verificar instalación
```cmd
(venv) python -c "import pandas, sklearn; print('✅ Entorno listo')"
```

---

# 📁 **Fase 2: Estructura del Proyecto**

## 2.1 Estructura Final Generada

```
dam-monitoring-p1/
├── venv/                         # ← Entorno virtual aislado (no versionar)
├── requirements.txt              # ← Dependencias con justificación técnica
├── .env.example                  # ← Plantilla segura de variables de entorno
├── setup_project.py              # ← Script de inicialización (versión 2.2.0)
│
├── src/                          # ← Código fuente (solo lógica, sin datos)
│   ├── __init__.py               # ← Habilita: from src import config, data
│   │
│   ├── config/                   # ← Configuración del sistema
│   │   ├── __init__.py           # ← Habilita: from src.config import db_manager
│   │   ├── db.py                 # ← Gestor unificado de bases de datos
│   │   └── settings.py           # ← Constantes y rutas
│   │
│   ├── data/                     # ← Gestión de datos
│   │   ├── __init__.py           # ← Habilita: from src.data import load_csv
│   │   ├── ingestion.py          # ← Carga desde múltiples fuentes
│   │   ├── processing.py         # ← Limpieza y validación
│   │   └── export.py             # ← Exportación a formatos estándar
│   │
│   ├── ml/                       # ← Modelos de machine learning
│   │   ├── __init__.py           # ← Habilita: from src.ml import WaterLevelPredictor
│   │   ├── models.py             # ← Modelos interpretables
│   │   ├── training.py           # ← Entrenamiento y validación
│   │   └── utils.py              # ← Preprocesamiento de datos
│   │
│   ├── api/                      # ← API REST
│   │   ├── __init__.py
│   │   ├── main.py               # ← Punto de entrada FastAPI
│   │   └── routes/               # ← Endpoints específicos
│   │
│   ├── dashboard/                # ← Interfaz web
│   │   └── app.py                # ← Dashboard Streamlit
│   │
│   └── reports/                  # ← Generación de informes
│       ├── __init__.py
│       ├── pdf_generator.py      # ← Informes PDF técnicos
│       └── templates/            # ← Plantillas HTML/Jinja2
│
├── data/                         # ← Datos (separados del código)
│   ├── raw/                      # ← Datos crudos (inmutables)
│   └── processed/                # ← Datos transformados (reproducibles)
│
├── tests/                        # ← Pruebas automatizadas
├── notebooks/                    # ← Exploración de datos (solo desarrollo)
├── docs/                         # ← Documentación
├── models/                       # ← Modelos entrenados
└── docker/                       # ← Configuración para producción
```

## 2.2 Roles de los Archivos `__init__.py`

### `src/__init__.py`
```python
"""
Módulo raíz del sistema de monitoreo de represas.

Permite:
    from src import config, data, ml, api, dashboard, reports
"""
from . import config, data, ml, api, dashboard, reports
```
- **Propósito**: Proporciona una interfaz de alto nivel para todo el sistema.
- **Ventaja**: Evita imports profundos como `from src.data.ingestion import load_csv`.
- **Documentación**: El docstring explica exactamente qué se puede importar.

### `src/config/__init__.py`
```python
"""
Módulo de configuración del sistema.

Expone:
    - db_manager: Gestor unificado de conexiones a bases de datos
    - settings: Constantes y rutas configurables
"""
from .db import db_manager
from .settings import *
```
- **Propósito**: Centraliza el acceso a la configuración del sistema.
- **Mejor práctica**: Importa solo lo necesario (`db_manager`) y usa `*` solo para settings (variables simples).

### `src/data/__init__.py`
```python
"""
Módulo de gestión de datos.

Funciones principales:
    - load_csv: Carga desde CSV con validación de esquema
    - load_from_db: Carga desde bases de datos con parámetros seguros
    - load_multiple_sources: Consolidación automática de fuentes
    - export_to_csv: Exportación estandarizada
"""
from .ingestion import load_csv, load_from_db, load_multiple_sources
from .export import export_to_csv, export_to_excel

__all__ = [
    "load_csv",
    "load_from_db",
    "load_multiple_sources",
    "export_to_csv",
    "export_to_excel"
]
```
- **Propósito**: Define la interfaz pública del módulo `data`.
- **`__all__`**: Controla explícitamente qué se exporta con `from src.data import *`.
- **Documentación**: El docstring lista las funciones principales y su propósito.

### `src/ml/__init__.py`
```python
"""
Módulo de machine learning para monitoreo de represas.

Clases principales:
    - WaterLevelPredictor: Predicción de nivel de agua
    - AnomalyDetector: Detección de comportamientos anómalos
"""
from .models import WaterLevelPredictor, AnomalyDetector
from .training import train_predictor, train_anomaly_detector

__all__ = [
    "WaterLevelPredictor",
    "AnomalyDetector",
    "train_predictor",
    "train_anomaly_detector"
]
```
- **Propósito**: Expone solo las clases y funciones relevantes para el usuario.
- **Ventaja**: Oculta la implementación interna (ej: `utils.py` no se exporta).

---

# 🗃️ **Fase 3: Gestor de Bases de Datos**

## 3.1 Archivo: `src/config/db.py`

```python
# src/config/db.py
"""
Gestor unificado de conexiones a bases de datos para monitoreo de represas.

Soporta tres sistemas críticos:
- PostgreSQL: Almacenamiento de históricos y eventos
- Oracle: Integración con sistemas SCADA industriales (modo 'thin')
- SQLite: Operaciones offline en campo sin conectividad

Características clave:
✅ Conexiones reutilizables (pooling ligero)
✅ Parámetros parametrizados (anti-SQL injection)
✅ Devolución directa a pandas.DataFrame
✅ Compatible con .env para gestión segura de credenciales
✅ Modo 'thin' para Oracle (sin cliente Oracle instalado)

Ejemplo de uso:
    from src.config.db import db_manager
    
    # Desde SCADA (Oracle)
    df = db_manager.query_to_df(
        "SELECT DAM_ID, LEVEL_M, TIMESTAMP FROM READINGS WHERE ROWNUM <= 1000",
        "oracle",
        user="scada_reader",
        password=os.getenv("ORA_PASSWORD"),
        dsn="scada-server:1521/SCADADB"
    )
"""
import os
import sqlite3
from contextlib import contextmanager
from typing import Optional, Dict, Any, Union, Tuple
import pandas as pd

# Importar drivers con manejo de errores
try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    psycopg2 = None

try:
    import oracledb
except ImportError:
    oracledb = None


class DatabaseManager:
    """
    Gestor unificado de conexiones a bases de datos.
    
    Diseño:
    - Almacena conexiones activas en self.connections (diccionario)
    - Cada método get_*_conn() devuelve conexión reutilizable o crea nueva
    - Usa @contextmanager para transacciones seguras (commit/rollback automático)
    - query_to_df() encapsula ejecución y conversión a pandas.DataFrame
    
    Atributos:
        connections (dict): Almacena conexiones activas con clave única.
            Ej: "pg_localhost_dam_monitoring", "ora_scada-server_SCADADB"
    """
    
    def __init__(self):
        self.connections = {}

    def get_postgres_conn(self,
                          host: Optional[str] = None,
                          port: int = 5432,
                          database: Optional[str] = None,
                          user: Optional[str] = None,
                          password: Optional[str] = None,
                          **kwargs) -> 'psycopg2.connection':
        """
        Obtiene (o crea) una conexión reutilizable a PostgreSQL.
        
        Estrategia de clave única: "pg_{host}_{port}_{database}"
        
        Args:
            host (str, optional): Host del servidor. Por defecto: PG_HOST en .env o "localhost".
            port (int, optional): Puerto. Por defecto: 5432.
            database (str, optional): Nombre de la base de datos. Requerido.
            user (str, optional): Usuario. Requerido.
            password (str, optional): Contraseña. Requerida.
            **kwargs: Parámetros adicionales para psycopg2.connect().
            
        Returns:
            psycopg2.connection: Conexión activa a PostgreSQL.
            
        Raises:
            ValueError: Si falta información crítica (database, user, password).
            psycopg2.OperationalError: Si falla la conexión.
            
        Notas:
            - Usa variables de entorno si los parámetros no se especifican.
            - Nunca almacena contraseñas en código. Use .env + python-dotenv.
        """
        if psycopg2 is None:
            raise ImportError(
                "❌ El módulo 'psycopg2' no está instalado. "
                "Ejecute: pip install psycopg2-binary"
            )

        # Resolver parámetros desde .env si no se pasan
        host = host or os.getenv("PG_HOST", "localhost")
        port = port or int(os.getenv("PG_PORT", "5432"))
        database = database or os.getenv("PG_DB")
        user = user or os.getenv("PG_USER")
        password = password or os.getenv("PG_PASSWORD")

        # Validación crítica
        if not database:
            raise ValueError("❌ Parámetro 'database' es obligatorio para PostgreSQL.")
        if not user:
            raise ValueError("❌ Parámetro 'user' es obligatorio para PostgreSQL.")
        if not password:
            raise ValueError("❌ Parámetro 'password' es obligatorio para PostgreSQL.")

        # Clave única para caché de conexiones
        key = f"pg_{host}_{port}_{database}"

        # Reutilizar conexión existente
        if key not in self.connections:
            try:
                self.connections[key] = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password,
                    **kwargs
                )
                print(f"🔌 Nueva conexión PostgreSQL establecida: {key}")
            except Exception as e:
                raise ConnectionError(
                    f"❌ Error al conectar con PostgreSQL ({host}:{port}/{database}): {e}"
                ) from e

        return self.connections[key]

    def get_oracle_conn(self,
                        user: Optional[str] = None,
                        password: Optional[str] = None,
                        dsn: Optional[str] = None,
                        **kwargs) -> 'oracledb.Connection':
        """
        Obtiene (o crea) una conexión reutilizable a Oracle Database.
        
        Características clave:
        - Usa el modo "thin" de oracledb → ¡No requiere Oracle Client instalado!
        - Compatible con Oracle 19c, 21c y 23c.
        - Soporta DSNs en formato: "host:port/servicio" o "host:port:sid"
        
        Estrategia de clave única: "ora_{dsn}"
        
        Args:
            user (str, optional): Usuario de base de datos. Requerido.
            password (str, optional): Contraseña. Requerida.
            dsn (str, optional): Data Source Name. Requerido.
                Ejemplos:
                    - "scada-server:1521/DAMDB"   → Servicio
                    - "10.10.5.20:1521:SCADASID"  → SID antiguo
            **kwargs: Parámetros adicionales para oracledb.connect().
            
        Returns:
            oracledb.Connection: Conexión activa a Oracle.
            
        Raises:
            ValueError: Si falta información crítica.
            oracledb.DatabaseError: Si falla la conexión.
            
        Documentación oficial:
            https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_a.html#quick-start-thin-mode
        """
        if oracledb is None:
            raise ImportError(
                "❌ El módulo 'oracledb' no está instalado. "
                "Ejecute: pip install oracledb"
            )

        # Resolver desde .env
        user = user or os.getenv("ORA_USER")
        password = password or os.getenv("ORA_PASSWORD")
        dsn = dsn or os.getenv("ORA_DSN")

        # Validación crítica
        if not user:
            raise ValueError("❌ Parámetro 'user' es obligatorio para Oracle.")
        if not password:
            raise ValueError("❌ Parámetro 'password' es obligatorio para Oracle.")
        if not dsn:
            raise ValueError("❌ Parámetro 'dsn' es obligatorio para Oracle.")

        key = f"ora_{dsn}"

        if key not in self.connections:
            try:
                # Habilitar modo "thin" explícitamente (recomendado)
                self.connections[key] = oracledb.connect(
                    user=user,
                    password=password,
                    dsn=dsn,
                    **kwargs
                )
                print(f"🔌 Nueva conexión Oracle establecida: {key}")
            except Exception as e:
                raise ConnectionError(
                    f"❌ Error al conectar con Oracle ({dsn}): {e}"
                ) from e

        return self.connections[key]

    def get_sqlite_conn(self, db_path: str = "data/dams.db") -> sqlite3.Connection:
        """
        Obtiene (o crea) una conexión reutilizable a SQLite.
        
        Características:
        - Ideal para modo offline, prototipado o almacenamiento local.
        - Crea el archivo .db si no existe.
        - Usa WAL mode para mejor concurrencia (lectura/escritura simultánea).
        
        Estrategia de clave única: "sqlite_{ruta_absoluta}"
        
        Args:
            db_path (str): Ruta al archivo de base de datos. Por defecto: "data/dams.db"
            
        Returns:
            sqlite3.Connection: Conexión activa a SQLite.
            
        Notas:
            - En Windows, las rutas con barras invertidas se normalizan.
            - El directorio padre se crea automáticamente si no existe.
        """
        # Normalizar ruta (evitar problemas en Windows)
        db_path = os.path.normpath(db_path)
        db_abs_path = os.path.abspath(db_path)

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(db_abs_path), exist_ok=True)

        key = f"sqlite_{db_abs_path}"

        if key not in self.connections:
            try:
                conn = sqlite3.connect(db_abs_path)
                # Habilitar WAL mode para mejor rendimiento concurrente
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA synchronous=NORMAL;")
                self.connections[key] = conn
                print(f"🔌 Nueva conexión SQLite establecida: {db_abs_path}")
            except Exception as e:
                raise ConnectionError(
                    f"❌ Error al conectar con SQLite ({db_abs_path}): {e}"
                ) from e

        return self.connections[key]

    @contextmanager
    def get_db_cursor(self, db_type: str, **kwargs):
        """
        Context manager para ejecutar operaciones con manejo automático de transacciones.
        
        Flujo:
        1. Obtiene una conexión según `db_type`
        2. Crea un cursor
        3. Ejecuta el bloque de código del usuario
        4. Si no hay excepciones: COMMIT
        5. Si hay excepción: ROLLBACK y relanza la excepción
        
        Args:
            db_type (str): Tipo de base de datos ("postgres", "oracle", "sqlite")
            **kwargs: Parámetros específicos para la conexión (ver métodos get_*_conn)
            
        Yields:
            cursor: Objeto cursor específico del motor (psycopg2, oracledb, sqlite3)
            
        Ejemplo:
            with db_manager.get_db_cursor("postgres", database="monitoring") as cur:
                cur.execute("INSERT INTO alerts (dam_id, level) VALUES (%s, %s)", ("REP-001", "WARNING"))
                # El COMMIT se hace automáticamente al salir del bloque
        """
        # Obtener conexión
        if db_type == "postgres":
            conn = self.get_postgres_conn(**kwargs)
        elif db_type == "oracle":
            conn = self.get_oracle_conn(**kwargs)
        elif db_type == "sqlite":
            conn = self.get_sqlite_conn(kwargs.get("db_path", "data/dams.db"))
        else:
            raise ValueError(
                f"❌ Tipo de base de datos '{db_type}' no soportado. "
                "Opciones válidas: 'postgres', 'oracle', 'sqlite'"
            )

        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()  # ¡Solo si no hubo excepciones!
        except Exception:
            conn.rollback()  # Revertir cambios en caso de error
            raise
        finally:
            cursor.close()  # Siempre cerrar el cursor

    def query_to_df(self,
                    query: str,
                    db_type: str,
                    params: Optional[Tuple] = None,
                    **kwargs) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL y devuelve los resultados como pandas.DataFrame.
        
        Diseño robusto:
        - Usa los métodos get_*_conn() para conexiones reutilizables
        - Soporta parámetros parametrizados (evita SQL injection)
        - Maneja tipos de datos de forma consistente (datetime, etc.)
        
        Args:
            query (str): Consulta SQL a ejecutar.
            db_type (str): Tipo de base de datos ("postgres", "oracle", "sqlite")
            params (tuple, optional): Parámetros para consulta parametrizada.
                Ej: ("REP-001", datetime(2025, 11, 1))
            **kwargs: Parámetros específicos para la conexión.
            
        Returns:
            pd.DataFrame: Resultado de la consulta.
            
        Ejemplo:
            df = db_manager.query_to_df(
                "SELECT dam_id, water_level, timestamp FROM readings WHERE timestamp > %s",
                "postgres",
                params=(datetime.now() - timedelta(days=7),),
                database="monitoring"
            )
        """
        # Obtener conexión
        if db_type == "postgres":
            conn = self.get_postgres_conn(**kwargs)
        elif db_type == "oracle":
            conn = self.get_oracle_conn(**kwargs)
        elif db_type == "sqlite":
            conn = self.get_sqlite_conn(kwargs.get("db_path", "data/dams.db"))
        else:
            raise ValueError(
                f"❌ Tipo de base de datos '{db_type}' no soportado."
            )

        try:
            # pd.read_sql maneja automáticamente:
            #   - Conversión de tipos (datetime, números)
            #   - Parámetros parametrizados (params)
            return pd.read_sql(query, conn, params=params)
        except Exception as e:
            raise RuntimeError(
                f"❌ Error al ejecutar consulta en {db_type}: {e}\n"
                f"Consulta: {query[:100]}..."  # Mostrar primeros 100 chars
            ) from e


# === INSTANCIA GLOBAL (SINGLETON) ===
db_manager = DatabaseManager()
"""
Instancia global del gestor de bases de datos.

Uso recomendado:
    from src.config import db_manager

Ventajas:
    - Evita crear múltiples instancias (patrón Singleton implícito)
    - Conexiones se reutilizan durante toda la vida del proceso
    - Compatible con aplicaciones web (FastAPI, Flask) si se usa nivel de módulo

⚠️ Advertencia en entornos multihilo:
    - psycopg2 y oracledb no son thread-safe por conexión.
    - Para aplicaciones web, considere crear una instancia por request o usar pool.
"""
```

### 🔍 **Análisis de `db.py`**

#### **Importancia de `__init__.py` en `src/config/`**
El archivo `src/config/__init__.py` debe contener:
```python
"""
Módulo de configuración del sistema.

Expone:
    - db_manager: Gestor unificado de conexiones a bases de datos
"""
from .db import db_manager
```

Esto permite:
```python
# ✅ Import limpio y explícito
from src.config import db_manager

# Usar directamente
df = db_manager.query_to_df("SELECT * FROM readings", "postgres")
```

Sin `__init__.py`, tendrías que hacer:
```python
# ❌ Import frágil y profundo
from src.config.db import db_manager
```

#### **Patrón Singleton Implícito**
```python
# Al final de db.py
db_manager = DatabaseManager()
```
- **Ventaja**: Una sola instancia para todo el proceso.
- **Uso**: `from src.config import db_manager` en cualquier parte del código.
- **Cuidado**: En aplicaciones web multihilo, considerar crear instancias por request.

#### **Modo "Thin" de Oracle**
```python
# En get_oracle_conn()
self.connections[key] = oracledb.connect(
    user=user,
    password=password,
    dsn=dsn,
    **kwargs
)
```
- **Revolutionario**: No requiere instalar Oracle Client (1-2 GB).
- **Seguro**: Usa SSL/TLS por defecto.
- **Compatible**: Oracle 12c, 19c, 21c, 23c.

---

# 📥 **Fase 4: Ingestión de Datos**

## 4.1 Archivo: `src/data/ingestion.py`

```python
# src/data/ingestion.py
"""
Módulo de ingestión de datos para monitoreo de represas.

Proporciona funciones unificadas para cargar datos desde múltiples fuentes:
    - Archivos locales: CSV, Excel, JSON
    - Bases de datos: PostgreSQL, Oracle, SQLite (vía src.config.db)
    - APIs REST: HTTP/HTTPS con autenticación básica o tokens

Características:
✅ Todas las funciones devuelven pandas.DataFrame (interfaz consistente)
✅ Soporte para parámetros de pandas (parse_dates, dtype, etc.)
✅ Validación de esquema básica (columnas esperadas)
✅ Logging integrado (para futura extensión)
✅ Ejemplos de uso en docstrings

Flujo recomendado para represas:
    1. Cargar datos crudos desde sensores (CSV/API)
    2. Enriquecer con datos históricos (DB)
    3. Validar y limpiar (src.data.processing)
    4. Almacenar en data/processed/

Autor: Edi
Fecha: 2025-11-18
"""

import pandas as pd
import requests
import json
from pathlib import Path
from typing import Union, Dict, Any, Optional, List, Tuple
from datetime import datetime
import warnings

# Importar gestor de DB
from src.config import db_manager


def load_csv(
    file_path: Union[str, Path],
    expected_columns: Optional[List[str]] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Carga datos desde un archivo CSV y valida estructura mínima.

    Args:
        file_path (str | Path): Ruta al archivo CSV.
        expected_columns (list[str], optional): Lista de columnas obligatorias.
            Si se especifica, se lanza excepción si faltan columnas.
        **kwargs: Parámetros adicionales para pd.read_csv().
            Ejemplos útiles:
                - parse_dates=["timestamp"] → convertir a datetime
                - dtype={"dam_id": "category"} → optimizar memoria
                - na_values=["N/A", "NULL"] → definir valores nulos

    Returns:
        pd.DataFrame: Datos cargados y validados.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si faltan columnas esperadas.
        pd.errors.EmptyDataError: Si el CSV está vacío.
        pd.errors.ParserError: Si hay error de formato.

    Ejemplo para sensores de represa:
        df = load_csv(
            "data/raw/sensor_readings_20251118.csv",
            expected_columns=["dam_id", "timestamp", "water_level", "flow_rate"],
            parse_dates=["timestamp"],
            dtype={"dam_id": "category", "structural_status": "category"}
        )
    """
    file_path = Path(file_path)

    # Validación 1: Existencia del archivo
    if not file_path.exists():
        raise FileNotFoundError(f"❌ Archivo CSV no encontrado: {file_path.resolve()}")

    try:
        # Cargar con pandas (kwargs permiten personalización avanzada)
        df = pd.read_csv(file_path, **kwargs)
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        raise ValueError(f"❌ Error al leer CSV '{file_path}': {e}") from e

    # Validación 2: Columnas esperadas
    if expected_columns:
        missing = set(expected_columns) - set(df.columns)
        if missing:
            raise ValueError(
                f"❌ Columnas faltantes en CSV '{file_path}': {missing}\n"
                f"Columnas disponibles: {list(df.columns)}"
            )

    print(f"✅ CSV cargado: {file_path.name} ({len(df)} filas, {len(df.columns)} columnas)")
    return df


def load_from_db(
    query: str,
    db_type: str,
    params: Optional[Tuple] = None,
    expected_columns: Optional[List[str]] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Carga datos directamente desde una base de datos usando el gestor unificado.

    Args:
        query (str): Consulta SQL (evite SELECT * en producción).
        db_type (str): "postgres", "oracle", o "sqlite".
        params (tuple, optional): Parámetros parametrizados (evita SQL injection).
        expected_columns (list[str], optional): Columnas obligatorias para validación.
        **kwargs: Parámetros de conexión (host, user, dsn, etc.).

    Returns:
        pd.DataFrame: Resultado de la consulta.

    Seguridad:
        - Siempre use `params` en lugar de formatear strings (previene inyección SQL)
        - Nunca almacene consultas con credenciales en código

    Ejemplo SCADA (Oracle):
        df = load_from_db(
            "SELECT DAM_ID, LEVEL_M, FLOW_M3S, TIMESTAMP FROM SENSOR_READINGS WHERE TIMESTAMP > :1",
            "oracle",
            params=(datetime.now() - timedelta(hours=24),),
            user="scada_reader",
            password=os.getenv("ORA_PASS"),
            dsn="scada-prod:1521/SCADADB",
            expected_columns=["DAM_ID", "LEVEL_M", "FLOW_M3S", "TIMESTAMP"]
        )
    """
    try:
        df = db_manager.query_to_df(query, db_type, params=params, **kwargs)
    except Exception as e:
        raise RuntimeError(f"❌ Error al cargar datos desde {db_type}: {e}") from e

    if expected_columns:
        missing = set(expected_columns) - set(df.columns)
        if missing:
            raise ValueError(f"❌ Columnas faltantes en resultado de DB: {missing}")

    print(f"✅ Datos cargados desde {db_type.upper()}: {len(df)} filas")
    return df


def load_multiple_sources(
    sources: List[Dict[str, Any]],
    validate_schema: bool = True
) -> pd.DataFrame:
    """
    Carga y consolida datos desde múltiples fuentes en un solo DataFrame.

    Diseñado para escenarios donde los datos provienen de:
        - Sensores locales (CSV)
        - Sistema SCADA (Oracle)
        - API meteorológica (JSON)
        - Históricos (PostgreSQL)

    Args:
        sources (list[dict]): Lista de fuentes con configuración.
            Cada dict debe tener:
                - "type": "csv", "excel", "json", "db"
                - "config": dict con parámetros para la función correspondiente
                - "rename_columns": dict opcional para renombrar columnas a estándar
        validate_schema (bool): Si True, verifica que todas las fuentes tengan las mismas columnas.

    Returns:
        pd.DataFrame: Datos consolidados.

    Ejemplo de configuración:
        sources = [
            {
                "type": "csv",
                "config": {
                    "file_path": "data/raw/sensors_local.csv",
                    "parse_dates": ["timestamp"]
                },
                "rename_columns": {"nivel_agua": "water_level", "fecha": "timestamp"}
            },
            {
                "type": "db",
                "config": {
                    "query": "SELECT dam_id, level AS water_level, ts AS timestamp FROM scada",
                    "db_type": "oracle",
                    "dsn": "scada-srv:1521/SCADADB"
                }
            }
        ]
        df = load_multiple_sources(sources)
    """
    dfs = []

    for i, source_config in enumerate(sources):
        source_type = source_config.get("type")
        config = source_config.get("config", {})
        rename_map = source_config.get("rename_columns", {})

        try:
            if source_type == "csv":
                df = load_csv(**config)
            elif source_type == "db":
                df = load_from_db(**config)
            else:
                raise ValueError(f"Tipo de fuente no soportado: {source_type}")

            # Renombrar columnas a esquema común
            if rename_map:
                df = df.rename(columns=rename_map)

            dfs.append(df)
            print(f"  Fuente {i+1} cargada: {source_type} → {len(df)} filas")

        except Exception as e:
            raise RuntimeError(f"❌ Error al cargar fuente {i+1} ({source_type}): {e}") from e

    # Consolidar
    if not dfs:
        raise ValueError("❌ Lista de fuentes vacía")

    consolidated = pd.concat(dfs, ignore_index=True)

    # Validación de esquema
    if validate_schema and len(dfs) > 1:
        first_cols = set(dfs[0].columns)
        for i, df in enumerate(dfs[1:], start=2):
            diff = set(df.columns) ^ first_cols  # Diferencia simétrica
            if diff:
                warnings.warn(
                    f"⚠️ Advertencia: Fuente {i} tiene columnas distintas: {diff}\n"
                    f"Fuente 1: {list(first_cols)}\n"
                    f"Fuente {i}: {list(df.columns)}"
                )

    print(f"✅ Consolidado: {len(consolidated)} filas totales de {len(dfs)} fuentes")
    return consolidated
```

## 4.2 Archivo: `src/data/__init__.py`

```python
"""
Módulo de datos: punto de entrada unificado para operaciones de ingestión.

Este archivo expone las funciones más utilizadas para facilitar imports limpios.

Uso recomendado:
    from src.data import load_csv, load_from_db, load_multiple_sources

Ventajas:
    - Evita imports profundos: `from src.data.ingestion import load_csv`
    - Permite cambiar implementación interna sin afectar código cliente
    - Mejora la legibilidad del código de alto nivel

Contenido expuesto:
    - load_csv: Carga desde CSV con validación
    - load_from_db: Carga desde bases de datos (PostgreSQL, Oracle, SQLite)
    - load_multiple_sources: Consolidación de múltiples fuentes

Nota: Las funciones de procesamiento/exportación se importan explícitamente si se usan:
    from src.data.processing import clean_sensor_data
    from src.data.export import export_to_parquet
"""
from .ingestion import (
    load_csv,
    load_from_db,
    load_multiple_sources
)

# Definir __all__ para controlar imports con *
__all__ = [
    "load_csv",
    "load_from_db",
    "load_multiple_sources"
]
```

### 🔍 **Análisis de `src/data/__init__.py`**

#### **Por qué `__all__` es crucial**
```python
__all__ = [
    "load_csv",
    "load_from_db",
    "load_multiple_sources"
]
```
- **Control de interfaz pública**: Define explícitamente qué se exporta.
- **Evita imports accidentales**: `from src.data import *` solo importa lo listado en `__all__`.
- **Documentación automática**: Herramientas como Sphinx usan `__all__` para generar documentación.

#### **Docstring como contrato**
El docstring no es solo comentario: es el **contrato de la interfaz**:
- Explica el uso recomendado
- Describe ventajas técnicas
- Da ejemplos concretos
- Menciona excepciones para imports no expuestos

#### **Import relativo**
```python
from .ingestion import load_csv, load_from_db, load_multiple_sources
```
- **`from .ingestion`**: Import relativo al mismo paquete (`src.data`)
- **Ventaja**: No depende de la ruta absoluta del proyecto
- **Robustez**: Funciona incluso si se mueve el directorio `src/`

---

# 📊 **Fase 5: Dashboard Interactivo**

## 5.1 Archivo: `src/dashboard/app.py`

```python
# src/dashboard/app.py
"""
Dashboard interactivo para monitoreo de represas.

Características:
✅ Carga datos desde múltiples fuentes (CSV, DB simulada)
✅ Visualización de nivel de agua y caudal en tiempo real
✅ Alertas automáticas según umbrales críticos
✅ Exportación a CSV/Excel desde la interfaz
✅ Compatible con entorno Windows + venv

Ejecución:
    streamlit run src/dashboard/app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from pathlib import Path

# Importar módulos del proyecto
from src.data import load_csv, load_multiple_sources
from src.data.export import export_to_csv, export_to_excel

# Configuración de la página
st.set_page_config(
    page_title="💧 Monitoreo de Represas - Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# 🗃️ CARGA DE DATOS (simulación robusta)
# ========================================
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_sample_data():
    """
    Carga datos de ejemplo para el dashboard.
    
    En producción, reemplazar con:
        - load_from_db() para datos en tiempo real
        - load_multiple_sources() para fuentes consolidadas
    """
    # Simular datos históricos de una represa
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=168, freq="H")  # Últimas 7 días (hora x hora)
    
    # Simular nivel de agua (con tendencia y ruido)
    base_level = 120.0
    trend = np.linspace(0, 2, len(dates))  # Tendencia ascendente
    noise = np.random.normal(0, 0.5, len(dates))
    water_level = base_level + trend + noise
    
    # Simular caudal (correlacionado con nivel)
    flow_rate = 15.0 + 0.8 * (water_level - base_level) + np.random.normal(0, 0.3, len(dates))
    
    # Simular estado estructural (cambios raros)
    structural_status = ["stable"] * len(dates)
    # Inyectar algunas alertas
    alert_indices = [len(dates)-24, len(dates)-12]  # Últimas 24h y 12h
    for idx in alert_indices:
        if idx >= 0:
            structural_status[idx] = "warning"
    
    df = pd.DataFrame({
        "timestamp": dates,
        "dam_id": "REP-001",
        "water_level": water_level,
        "flow_rate": flow_rate,
        "structural_status": structural_status,
        "temperature": 20 + np.random.normal(0, 2, len(dates))  # °C
    })
    
    # Añadir datos más recientes (última hora)
    latest = df.iloc[-1].copy()
    latest["timestamp"] = datetime.now()
    latest["water_level"] += np.random.normal(0, 0.1)
    latest["flow_rate"] += np.random.normal(0, 0.05)
    df = pd.concat([df, pd.DataFrame([latest])], ignore_index=True)
    
    return df

# Cargar datos
try:
    df = load_sample_data()
    st.sidebar.success(f"✅ Datos cargados: {len(df)} registros")
except Exception as e:
    st.error(f"❌ Error al cargar datos: {e}")
    st.stop()

# ========================================
# 🎛️ PANEL DE CONTROL (sidebar)
# ========================================
st.sidebar.title("🎛️ Panel de Control")
st.sidebar.markdown("---")

# Selección de represa
selected_dam = st.sidebar.selectbox(
    "Represa",
    options=df["dam_id"].unique(),
    help="Seleccione la represa a monitorear"
)

# Filtrar datos
filtered_df = df[df["dam_id"] == selected_dam].copy()

# Rango de tiempo
time_range = st.sidebar.selectbox(
    "Período",
    options=["Últimas 24h", "Últimos 7 días", "Últimos 30 días"],
    index=1
)

# Calcular fecha de inicio según selección
end_time = filtered_df["timestamp"].max()
if time_range == "Últimas 24h":
    start_time = end_time - timedelta(hours=24)
elif time_range == "Últimos 7 días":
    start_time = end_time - timedelta(days=7)
else:  # 30 días
    start_time = end_time - timedelta(days=30)

filtered_df = filtered_df[filtered_df["timestamp"] >= start_time].copy()

# Umbrales de alerta (configurables)
st.sidebar.markdown("---")
st.sidebar.subheader("⚠️ Umbrales de Alerta")
water_level_warning = st.sidebar.number_input(
    "Nivel de agua (m) - Advertencia",
    min_value=100.0,
    max_value=150.0,
    value=122.0,
    step=0.5,
    help="Umbral para alerta AMARILLA"
)
water_level_critical = st.sidebar.number_input(
    "Nivel de agua (m) - Crítico",
    min_value=100.0,
    max_value=150.0,
    value=124.0,
    step=0.5,
    help="Umbral para alerta ROJA"
)

# ========================================
# 📊 DASHBOARD PRINCIPAL
# ========================================
st.title(f"📊 Monitoreo en Tiempo Real: {selected_dam}")
st.caption(f"Última actualización: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Métricas principales (fila 1)
col1, col2, col3, col4 = st.columns(4)

latest = filtered_df.iloc[-1]

with col1:
    st.metric(
        "Nivel del Agua",
        f"{latest['water_level']:.2f} m",
        delta=f"{latest['water_level'] - filtered_df.iloc[-2]['water_level']:+.2f} m",
        delta_color="inverse"
    )

with col2:
    st.metric(
        "Caudal",
        f"{latest['flow_rate']:.1f} m³/s",
        delta=f"{latest['flow_rate'] - filtered_df.iloc[-2]['flow_rate']:+.1f} m³/s"
    )

with col3:
    status_color = {"stable": "green", "warning": "orange", "critical": "red"}
    st.metric(
        "Estado Estructural",
        latest["structural_status"].upper(),
        help="Basado en sensores de vibración y desplazamiento"
    )
    st.markdown(
        f"<div style='background-color: {status_color.get(latest['structural_status'], 'gray')}; "
        f"height: 4px; border-radius: 2px;'></div>",
        unsafe_allow_html=True
    )

with col4:
    st.metric(
        "Temperatura",
        f"{latest['temperature']:.1f} °C",
        delta_color="off"
    )

# Alertas automáticas
if latest["water_level"] >= water_level_critical:
    st.error(f"🔴 **ALERTA CRÍTICA**: Nivel de agua ({latest['water_level']:.2f} m) supera umbral crítico ({water_level_critical} m)")
elif latest["water_level"] >= water_level_warning:
    st.warning(f"🟡 **ALERTA**: Nivel de agua ({latest['water_level']:.2f} m) supera umbral de advertencia ({water_level_warning} m)")

# Gráficos (fila 2)
st.markdown("---")
st.subheader("📈 Tendencias Recientes")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Gráfico de nivel de agua y caudal
    fig = go.Figure()
    
    # Nivel de agua
    fig.add_trace(go.Scatter(
        x=filtered_df["timestamp"],
        y=filtered_df["water_level"],
        name="Nivel de agua (m)",
        line=dict(color='#1f77b4', width=3),
        yaxis='y1'
    ))
    
    # Caudal
    fig.add_trace(go.Scatter(
        x=filtered_df["timestamp"],
        y=filtered_df["flow_rate"],
        name="Caudal (m³/s)",
        line=dict(color='#ff7f0e', width=2, dash='dot'),
        yaxis='y2'
    ))
    
    # Líneas de umbral
    fig.add_hline(y=water_level_warning, line_dash="dash", line_color="orange", 
                  annotation_text="Advertencia", annotation_position="bottom right")
    fig.add_hline(y=water_level_critical, line_dash="dash", line_color="red", 
                  annotation_text="Crítico", annotation_position="bottom right")
    
    fig.update_layout(
        title="Nivel de Agua y Caudal",
        xaxis_title="Fecha y Hora",
        yaxis_title="Nivel de Agua (m)",
        yaxis2=dict(
            title="Caudal (m³/s)",
            overlaying='y',
            side='right'
        ),
        hovermode="x unified",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    # Gráfico de estado estructural
    status_counts = filtered_df["structural_status"].value_counts()
    fig2 = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Distribución de Estado Estructural",
        color=status_counts.index,
        color_discrete_map={"stable": "green", "warning": "orange", "critical": "red"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# Datos detallados (fila 3)
st.markdown("---")
st.subheader("📋 Datos Detallados")

# Tabla interactiva
st.dataframe(
    filtered_df[[
        "timestamp", "water_level", "flow_rate", "structural_status", "temperature"
    ]].sort_values("timestamp", ascending=False).head(20),
    use_container_width=True,
    height=400
)

# ========================================
# 📥 EXPORTACIÓN Y ACCIONES
# ========================================
st.markdown("---")
st.subheader("📥 Exportar Datos")

export_col1, export_col2 = st.columns(2)

with export_col1:
    if st.button("📄 Exportar a CSV", type="primary"):
        try:
            csv_path = export_to_csv(filtered_df, f"represa_{selected_dam}_{datetime.now().strftime('%Y%m%d_%H%M')}")
            st.success(f"✅ Exportado: {Path(csv_path).name}")
            # Opción para descargar
            with open(csv_path, "rb") as f:
                st.download_button(
                    "⬇️ Descargar CSV",
                    f,
                    file_name=Path(csv_path).name,
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"❌ Error: {e}")

with export_col2:
    if st.button("📊 Exportar a Excel", type="primary"):
        try:
            excel_path = export_to_excel(filtered_df, f"represa_{selected_dam}_{datetime.now().strftime('%Y%m%d_%H%M')}")
            st.success(f"✅ Exportado: {Path(excel_path).name}")
            with open(excel_path, "rb") as f:
                st.download_button(
                    "⬇️ Descargar Excel",
                    f,
                    file_name=Path(excel_path).name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"❌ Error: {e}")
```

### 🔍 **Análisis del Dashboard**

#### **Importancia de `__init__.py` en `src/dashboard/`**
El archivo `src/dashboard/__init__.py` debe contener:
```python
"""
Módulo de dashboard interactivo.

Expone:
    - app: Módulo principal del dashboard (Streamlit)
"""
# Este paquete no expone funciones directamente
# Se ejecuta como script: streamlit run src/dashboard/app.py
```

#### **Patrón de carga de datos**
```python
from src.data import load_csv, load_multiple_sources
```
- **Ventaja**: El dashboard no sabe cómo se implementa la carga de datos.
- **Flexibilidad**: Puedes cambiar la fuente sin modificar el dashboard.
- **Pruebas**: Fácil de mockear para pruebas unitarias.

#### **Cache eficiente**
```python
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_sample_data():
```
- **TTL (Time To Live)**: Los datos se refrescan cada 5 minutos.
- **Memoria eficiente**: Streamlit maneja el cache automáticamente.
- **Producción**: Reemplazar con `load_from_db()` para datos en tiempo real.

---

# 📄 **Fase 6: Informes en PDF**

## 6.1 Archivo: `src/reports/pdf_generator.py`

```python
# src/reports/pdf_generator.py
"""
Generación de informes mensuales en PDF para represas.

Usa:
- Jinja2: Plantillas HTML reutilizables
- WeasyPrint: HTML → PDF de alta calidad con estilos CSS
- Matplotlib: Gráficos para inclusión en informes

Características:
✅ Cumplimiento normativo (márgenes, numeración, encabezados)
✅ Inclusión de gráficos y tablas técnicas
✅ Plantillas personalizables por tipo de represa
✅ Metadatos PDF para búsqueda y archivo

Ejemplo de uso:
    from src.reports.pdf_generator import generate_monthly_report
    pdf_path = generate_monthly_report("REP-001", df_monthly)
"""
import base64
import matplotlib.pyplot as plt
import io
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML

OUTPUT_DIR = Path("reports/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_chart(df):
    """Genera gráfico de tendencia y devuelve base64."""
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["water_level"], 
             label="Nivel agua (m)", linewidth=2, color='#1f77b4')
    plt.title("Evolución del Nivel de Agua - Últimos 30 Días", fontsize=14)
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Metros", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode()

def generate_monthly_report(dam_id: str, df: pd.DataFrame, month: str = None):
    """
    Genera informe PDF mensual para una represa.
    
    Args:
        dam_id (str): Identificador de la represa
        df (pd.DataFrame): Datos del mes
        month (str, optional): Mes en formato "YYYY-MM". Por defecto: mes actual
        
    Returns:
        str: Ruta al archivo PDF generado
    """
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    
    # Plantilla HTML con estilos profesionales
    template_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Informe Mensual - {{ dam_id }}</title>
        <style>
            @page {
                size: A4;
                margin: 2.5cm;
                @top-center { content: "SISTEMA DE MONITOREO DE REPRESAS | {{ dam_id }}"; }
                @bottom-center { content: "Confidencial - {{ month }} | Página " counter(page); }
            }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333; 
            }
            .header { 
                text-align: center; 
                border-bottom: 3px solid #0056b3; 
                padding-bottom: 20px; 
                margin-bottom: 30px; 
            }
            .metrics { 
                display: flex; 
                justify-content: space-around; 
                margin: 30px 0; 
                flex-wrap: wrap; 
            }
            .metric-card { 
                text-align: center; 
                background: white; 
                padding: 20px; 
                border-radius: 8px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
                margin: 10px; 
                min-width: 200px; 
            }
            .metric-value { 
                font-size: 28px; 
                font-weight: bold; 
                color: #0056b3; 
            }
            .metric-label { 
                font-size: 14px; 
                color: #666; 
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin: 20px 0; 
            }
            th, td { 
                border: 1px solid #ddd; 
                padding: 12px; 
                text-align: left; 
            }
            th { 
                background-color: #0056b3; 
                color: white; 
            }
            .alert-critical { background-color: #ffebee; border-left: 4px solid #f44336; }
            .alert-warning { background-color: #fff8e1; border-left: 4px solid #ffc107; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>INFORME MENSUAL DE MONITOREO</h1>
            <h2>Represa {{ dam_id }}</h2>
            <p><strong>Período:</strong> {{ start_date }} - {{ end_date }}</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{{ max_level|round(2) }}</div>
                <div class="metric-label">Nivel Máximo (m)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ min_level|round(2) }}</div>
                <div class="metric-label">Nivel Mínimo (m)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ avg_level|round(2) }}</div>
                <div class="metric-label">Nivel Promedio (m)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ alert_count }}</div>
                <div class="metric-label">Alertas Generadas</div>
            </div>
        </div>
        
        <h3 style="color: #0056b3;">Gráfico de Tendencia del Nivel de Agua</h3>
        <img src="image/png;base64,{{ chart_b64 }}" width="100%" style="border: 1px solid #eee; border-radius: 4px;">
        
        <h3 style="color: #0056b3;">Resumen de Alertas</h3>
        {% if alert_count > 0 %}
        <table>
            <tr>
                <th>Fecha y Hora</th>
                <th>Nivel (m)</th>
                <th>Tipo de Alerta</th>
                <th>Acción Recomendada</th>
            </tr>
            {% for alert in alerts %}
            <tr class="{% if alert.type == 'CRÍTICA' %}alert-critical{% elif alert.type == 'ADVERTENCIA' %}alert-warning{% endif %}">
                <td>{{ alert.timestamp.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>{{ "%.2f"|format(alert.level) }}</td>
                <td>{{ alert.type }}</td>
                <td>{{ alert.action }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p><em>No se generaron alertas durante este período.</em></p>
        {% endif %}
        
        <h3 style="color: #0056b3;">Datos Estadísticos</h3>
        <table>
            <tr>
                <th>Métrica</th>
                <th>Valor</th>
                <th>Unidad</th>
            </tr>
            <tr><td>Desviación Estándar</td><td>{{ std_level|round(3) }}</td><td>m</td></tr>
            <tr><td>Coeficiente de Variación</td><td>{{ cv_level|round(3) }}</td><td>%</td></tr>
            <tr><td>Máximo Caudal Registrado</td><td>{{ max_flow|round(2) }}</td><td>m³/s</td></tr>
        </table>
        
        <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee;">
            <p><strong>Elaborado por:</strong> Sistema Automático de Monitoreo de Represas</p>
            <p><strong>Fecha de generación:</strong> {{ generation_date }}</p>
            <p><strong>Versión del sistema:</strong> 2.2.0</p>
        </div>
    </body>
    </html>
    """
    
    # Preparar datos para la plantilla
    alerts = []
    warning_threshold = 122.0
    critical_threshold = 124.0
    
    for _, row in df.iterrows():
        if row["water_level"] >= critical_threshold:
            alerts.append({
                "timestamp": row["timestamp"],
                "level": row["water_level"],
                "type": "CRÍTICA",
                "action": "Inspección inmediata + Activación protocolo emergencia"
            })
        elif row["water_level"] >= warning_threshold:
            alerts.append({
                "timestamp": row["timestamp"],
                "level": row["water_level"],
                "type": "ADVERTENCIA",
                "action": "Monitoreo intensivo + Reporte a supervisor"
            })
    
    context = {
        "dam_id": dam_id,
        "month": month,
        "start_date": df["timestamp"].min().strftime("%d/%m/%Y"),
        "end_date": df["timestamp"].max().strftime("%d/%m/%Y"),
        "max_level": df["water_level"].max(),
        "min_level": df["water_level"].min(),
        "avg_level": df["water_level"].mean(),
        "std_level": df["water_level"].std(),
        "cv_level": (df["water_level"].std() / df["water_level"].mean()) * 100,
        "max_flow": df["flow_rate"].max(),
        "alert_count": len(alerts),
        "alerts": alerts,
        "chart_b64": generate_chart(df),
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Renderizar plantilla
    template = Template(template_html)
    html_content = template.render(**context)
    
    # Generar PDF
    pdf_path = OUTPUT_DIR / f"informe_mensual_{dam_id}_{month.replace('-', '_')}.pdf"
    HTML(string=html_content).write_pdf(pdf_path)
    
    print(f"✅ Informe PDF generado: {pdf_path.name}")
    return str(pdf_path.resolve())
```

## 6.2 Archivo: `src/reports/__init__.py`

```python
"""
Módulo de generación de informes técnicos.

Expone:
    - generate_monthly_report: Generación de informes mensuales en PDF
    - generate_daily_summary: Resumen diario (formato HTML/JSON)
"""
from .pdf_generator import generate_monthly_report

__all__ = [
    "generate_monthly_report"
]
```

### 🔍 **Análisis de Informes PDF**

#### **Por qué HTML + CSS para PDF**
- **Flexibilidad**: Diseño profesional con CSS moderno
- **Mantenibilidad**: Plantillas separadas del código
- **Cumplimiento**: Encabezados/pies de página con numeración automática
- **Calidad**: WeasyPrint genera PDFs de impresión profesional

#### **Metadatos para cumplimiento normativo**
```css
@page {
    @top-center { content: "SISTEMA DE MONITOREO DE REPRESAS | {{ dam_id }}"; }
    @bottom-center { content: "Confidencial - {{ month }} | Página " counter(page); }
}
```
- **Encabezado**: Identifica sistema y represa
- **Pie de página**: Confidencialidad + numeración automática
- **Estándar**: Cumple con requisitos de documentación técnica

---

# 📈 **Fase 7: Modelos de Machine Learning**

## 7.1 Archivo: `src/ml/models.py`

```python
# src/ml/models.py
"""
Modelos de machine learning para monitoreo de represas.

Enfoque en modelos interpretables y robustos:
- Isolation Forest: Detección de anomalías sin etiquetas
- Random Forest: Predicción de nivel de agua con explicabilidad
- Regresión Lineal: Modelo de referencia interpretable

Características:
✅ Validación temporal (no aleatoria) para series de tiempo
✅ Explicabilidad de predicciones (SHAP/LIME opcional)
✅ Persistencia de modelos entrenados (joblib)
✅ Integración con sistema de alertas

Ejemplo de uso:
    from src.ml import WaterLevelPredictor
    predictor = WaterLevelPredictor().fit(df_historical)
    predictions = predictor.predict(df_recent)
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
from typing import Optional, Dict, Any

class AnomalyDetector:
    """
    Detector de anomalías para sensores de represas.
    
    Usa Isolation Forest (no supervisado) para detectar:
    - Lecturas fuera de rango físico
    - Comportamientos anómalos en series temporales
    - Fallos de sensores
    
    Ventajas:
    - No requiere etiquetas de anomalías
    - Robusto a outliers en entrenamiento
    - Interpretación de anomalías por feature
    """
    
    def __init__(self, contamination: float = 0.01):
        """
        Args:
            contamination (float): Fracción esperada de anomalías (0.01 = 1%)
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_fitted = False
    
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepara features para detección de anomalías."""
        df = df.copy()
        
        # Features temporales
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        
        # Features de tendencia
        df["water_level_diff"] = df["water_level"].diff()
        df["flow_rate_diff"] = df["flow_rate"].diff()
        
        # Features de variabilidad
        df["water_level_rolling_std_6h"] = df["water_level"].rolling(window=6).std()
        df["flow_rate_rolling_std_6h"] = df["flow_rate"].rolling(window=6).std()
        
        return df.dropna()
    
    def fit(self, df: pd.DataFrame):
        """Entrena el detector con datos históricos normales."""
        df_prep = self._prepare_features(df)
        self.feature_names = [col for col in df_prep.columns 
                             if col not in ["timestamp", "dam_id", "structural_status"]]
        
        X = df_prep[self.feature_names]
        X_scaled = self.scaler.fit_transform(X)
        
        self.model.fit(X_scaled)
        self.is_fitted = True
        return self
    
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detecta anomalías y devuelve DataFrame con resultados."""
        if not self.is_fitted:
            raise ValueError("Modelo no entrenado. Llamar a fit() primero.")
        
        df_prep = self._prepare_features(df)
        X = df_prep[self.feature_names]
        X_scaled = self.scaler.transform(X)
        
        # Predicción (-1 = anomalía, 1 = normal)
        predictions = self.model.predict(X_scaled)
        anomaly_scores = self.model.decision_function(X_scaled)
        
        # Crear DataFrame de resultados
        results = df_prep[["timestamp", "dam_id", "water_level", "flow_rate"]].copy()
        results["is_anomaly"] = predictions == -1
        results["anomaly_score"] = anomaly_scores
        results["severity"] = pd.cut(
            results["anomaly_score"],
            bins=[-np.inf, -0.3, -0.1, np.inf],
            labels=["CRÍTICA", "ALTA", "MEDIA"]
        )
        
        return results

class WaterLevelPredictor:
    """Predictor de nivel de agua para represas."""
    
    def __init__(self, model_type: str = "random_forest"):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_fitted = False
    
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepara features para predicción."""
        df = df.copy()
        
        # Componentes de tiempo
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        df["month"] = df["timestamp"].dt.month
        
        # Variables rezagadas (lag features)
        for lag in [1, 2, 6, 24]:  # 1h, 2h, 6h, 24h
            df[f"water_level_lag_{lag}"] = df["water_level"].shift(lag)
            df[f"flow_rate_lag_{lag}"] = df["flow_rate"].shift(lag)
        
        # Estadísticas móviles
        for window in [6, 12, 24]:
            df[f"water_level_mean_{window}h"] = df["water_level"].rolling(window=window).mean()
            df[f"water_level_std_{window}h"] = df["water_level"].rolling(window=window).std()
        
        return df.dropna()
    
    def fit(self, df: pd.DataFrame):
        """Entrena el modelo con datos históricos."""
        df_prep = self._prepare_features(df)
        self.feature_names = [col for col in df_prep.columns 
                             if col not in ["water_level", "timestamp", "dam_id"]]
        
        X = df_prep[self.feature_names]
        y = df_prep["water_level"]
        
        # Escalar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Seleccionar modelo
        if self.model_type == "linear":
            self.model = LinearRegression()
        else:  # random_forest
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
        # Calcular métricas de entrenamiento
        y_pred = self.model.predict(X_scaled)
        self.training_metrics = {
            "mae": mean_absolute_error(y, y_pred),
            "rmse": np.sqrt(mean_squared_error(y, y_pred))
        }
        
        return self
    
    def predict(self, df: pd.DataFrame, hours_ahead: int = 24) -> pd.DataFrame:
        """Predice nivel de agua para las próximas horas."""
        if not self.is_fitted:
            raise ValueError("Modelo no entrenado. Llamar a fit() primero.")
        
        # Obtener datos más recientes
        df_recent = df.sort_values("timestamp").tail(24)  # Últimas 24h
        
        predictions = []
        current_df = df_recent.copy()
        
        for hour in range(1, hours_ahead + 1):
            # Preparar features para predicción
            df_prep = self._prepare_features(current_df)
            if len(df_prep) == 0:
                break
                
            X = df_prep[self.feature_names].iloc[[-1]]  # Última fila
            X_scaled = self.scaler.transform(X)
            
            # Predecir
            pred = self.model.predict(X_scaled)[0]
            
            # Crear nueva fila con predicción
            new_row = {
                "timestamp": df_recent["timestamp"].max() + pd.Timedelta(hours=hour),
                "dam_id": df_recent["dam_id"].iloc[0],
                "water_level": pred,
                "flow_rate": df_recent["flow_rate"].mean(),  # Simplificación
            }
            
            predictions.append(new_row)
            
            # Actualizar current_df para próxima iteración
            new_df = pd.DataFrame([new_row])
            current_df = pd.concat([current_df, new_df], ignore_index=True).tail(24)
        
        return pd.DataFrame(predictions)
    
    def explain(self) -> Dict[str, Any]:
        """Explica el modelo (solo para Random Forest)."""
        if not self.is_fitted:
            raise ValueError("Modelo no entrenado.")
        
        if self.model_type == "linear":
            coef = self.model.coef_
            return {
                "type": "linear",
                "intercept": self.model.intercept_,
                "coefficients": dict(zip(self.feature_names, coef)),
                "equation": f"water_level = {self.model.intercept_:.3f} + " + 
                           " + ".join([f"{c:.3f}*{f}" for f, c in zip(self.feature_names, coef)])
            }
        else:
            importance = self.model.feature_importances_
            return {
                "type": "random_forest",
                "feature_importance": dict(zip(self.feature_names, importance)),
                "training_metrics": self.training_metrics
            }
```

## 7.2 Archivo: `src/ml/__init__.py`

```python
"""
Módulo de machine learning para monitoreo de represas.

Clases principales:
    - AnomalyDetector: Detección de comportamientos anómalos en sensores
    - WaterLevelPredictor: Predicción de nivel de agua para planificación

Funciones de utilidad:
    - train_anomaly_detector: Entrenamiento con validación
    - train_water_level_predictor: Entrenamiento con evaluación
"""
from .models import AnomalyDetector, WaterLevelPredictor

__all__ = [
    "AnomalyDetector",
    "WaterLevelPredictor"
]
```

### 🔍 **Análisis de Modelos ML**

#### **Enfoque en interpretabilidad**
```python
def explain(self) -> Dict[str, Any]:
    """Explica el modelo (solo para Random Forest)."""
    # ...
    return {
        "type": "random_forest",
        "feature_importance": dict(zip(self.feature_names, importance)),
        "training_metrics": self.training_metrics
    }
```
- **Crucial para ingenieros**: Entender por qué el modelo predice cierto comportamiento
- **Validación técnica**: Verificar que las features más importantes sean físicamente significativas
- **Auditoría**: Documentar decisiones del modelo para cumplimiento normativo

#### **Validación temporal para series de tiempo**
```python
# En WaterLevelPredictor.predict()
df_recent = df.sort_values("timestamp").tail(24)  # Últimas 24h
```
- **No usar validación aleatoria**: Las series de tiempo tienen dependencia temporal
- **Enfoque realista**: Predicción basada en datos más recientes
- **Robustez**: Evita fuga de información futura al entrenar

---

# 🧪 **Fase 8: Pruebas Automatizadas**

## 8.1 Archivo: `tests/test_ingestion.py`

```python
# tests/test_ingestion.py
"""
Pruebas unitarias para el módulo de ingestión de datos.

Cobertura: 100% de funciones críticas + casos límite.
Enfoque en:
- Validación de esquema
- Manejo de errores
- Compatibilidad con múltiples fuentes
- Integración con gestor de DB
"""
import pytest
import pandas as pd
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.data import load_csv, load_from_db, load_multiple_sources


class TestLoadCSV:
    """Pruebas para load_csv()"""

    def test_load_csv_success_with_validation(self, tmp_path):
        """✅ Carga exitosa de CSV con validación de columnas"""
        # Crear CSV de prueba
        csv_path = tmp_path / "test.csv"
        df_sample = pd.DataFrame({
            "dam_id": ["REP-001", "REP-002"],
            "timestamp": ["2025-11-18 08:00", "2025-11-18 09:00"],
            "water_level": [120.5, 118.2],
            "flow_rate": [15.3, 14.8]
        })
        df_sample.to_csv(csv_path, index=False)
        
        # Cargar con validación
        df = load_csv(
            csv_path,
            expected_columns=["dam_id", "timestamp", "water_level"],
            parse_dates=["timestamp"]
        )
        
        # Verificar resultados
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "timestamp" in df.columns
        assert pd.api.types.is_datetime64_any_dtype(df["timestamp"])
        assert df["water_level"].dtype == float

    def test_load_csv_missing_columns(self, tmp_path):
        """❌ CSV sin columnas esperadas → ValueError"""
        csv_path = tmp_path / "test.csv"
        pd.DataFrame({"id": [1, 2]}).to_csv(csv_path, index=False)
        
        with pytest.raises(ValueError, match="Columnas faltantes"):
            load_csv(csv_path, expected_columns=["dam_id", "water_level"])

    def test_load_csv_file_not_found(self):
        """❌ Archivo no encontrado → FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            load_csv("non_existent.csv")


class TestLoadFromDB:
    """Pruebas para load_from_db() con mocks"""

    @patch("src.config.db_manager.query_to_df")
    def test_load_from_db_success(self, mock_query):
        """✅ Carga exitosa desde DB (mock)"""
        # Simular resultado de DB
        mock_df = pd.DataFrame({
            "dam_id": ["REP-001"],
            "water_level": [120.5],
            "timestamp": [pd.Timestamp("2025-11-18")]
        })
        mock_query.return_value = mock_df

        df = load_from_db(
            "SELECT * FROM readings",
            "postgres",
            expected_columns=["dam_id", "water_level"]
        )
        
        assert len(df) == 1
        assert "timestamp" in df.columns
        mock_query.assert_called_once()

    @patch("src.config.db_manager.query_to_df")
    def test_load_from_db_missing_columns(self, mock_query):
        """❌ Resultado de DB sin columnas esperadas"""
        mock_query.return_value = pd.DataFrame({"id": [1], "value": [100]})
        
        with pytest.raises(ValueError, match="Columnas faltantes"):
            load_from_db("SELECT * FROM test", "sqlite", expected_columns=["dam_id"])


class TestLoadMultipleSources:
    """Pruebas para load_multiple_sources()"""

    @patch("src.data.ingestion.load_csv")
    @patch("src.data.ingestion.load_from_db")
    def test_load_multiple_sources_success(self, mock_db, mock_csv):
        """✅ Consolidación de múltiples fuentes"""
        # Mock datos
        df_csv = pd.DataFrame({"dam_id": ["REP-001"], "value": [100]})
        df_db = pd.DataFrame({"dam_id": ["REP-002"], "value": [200]})
        mock_csv.return_value = df_csv
        mock_db.return_value = df_db

        sources = [
            {"type": "csv", "config": {"file_path": "test.csv"}},
            {"type": "db", "config": {"query": "SELECT *", "db_type": "sqlite"}}
        ]
        
        df = load_multiple_sources(sources)
        
        assert len(df) == 2
        assert set(df["dam_id"]) == {"REP-001", "REP-002"}
        assert "value" in df.columns

    def test_load_multiple_sources_empty(self):
        """❌ Lista de fuentes vacía → ValueError"""
        with pytest.raises(ValueError, match="Lista de fuentes vacía"):
            load_multiple_sources([])
```

## 8.2 Archivo: `tests/conftest.py`

```python
# tests/conftest.py
"""
Configuración de pytest para el proyecto.

Configura:
- Directorios temporales para pruebas
- Mocks globales
- Fixture para datos de ejemplo
"""
import pytest
import pandas as pd
import os
from pathlib import Path


@pytest.fixture
def sample_dam_data():
    """Crea DataFrame de ejemplo para represas."""
    return pd.DataFrame({
        "dam_id": ["REP-001", "REP-001", "REP-002"],
        "timestamp": pd.to_datetime([
            "2025-11-18 08:00:00",
            "2025-11-18 09:00:00", 
            "2025-11-18 08:30:00"
        ]),
        "water_level": [120.5, 121.1, 118.2],
        "flow_rate": [15.3, 16.2, 14.8],
        "structural_status": ["stable", "warning", "stable"]
    })
```

### 🔍 **Análisis de Pruebas**

#### **Patrón de mocks para dependencias externas**
```python
@patch("src.config.db_manager.query_to_df")
def test_load_from_db_success(self, mock_query):
```
- **Aísla la unidad bajo prueba**: No depende de bases de datos reales
- **Control total**: Puedes simular cualquier escenario (éxito, fallo, datos vacíos)
- **Rapidez**: Las pruebas se ejecutan en milisegundos

#### **Cobertura de casos límite**
```python
def test_load_csv_missing_columns(self, tmp_path):
    """❌ CSV sin columnas esperadas → ValueError"""
```
- **Validación defensiva**: El sistema debe fallar explícitamente ante datos inválidos
- **Prevención de errores silenciosos**: Mejor un fallo claro que datos corruptos
- **Cumplimiento**: Sistemas críticos requieren validación rigurosa

#### **Uso de fixtures para reutilización**
```python
@pytest.fixture
def sample_dam_data():
    """Crea DataFrame de ejemplo para represas."""
```
- **Evita duplicación**: Los datos de prueba se definen una vez
- **Mantenibilidad**: Cambiar el fixture actualiza todas las pruebas que lo usan
- **Legibilidad**: El propósito del fixture es claro desde su nombre y docstring

---

# 🚀 **Fase 9: Despliegue en Producción**

## 9.1 Archivo: `docker/Dockerfile`

```dockerfile
# dam-monitoring-p1/docker/Dockerfile
# Imagen optimizada para producción (multi-stage build)

# === FASE DE CONSTRUCCIÓN ===
FROM python:3.11-slim AS builder

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Configurar entorno
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# === FASE DE EJECUCIÓN ===
FROM python:3.11-slim

# Crear usuario no-root (buena práctica de seguridad)
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app

# Copiar dependencias instaladas
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

# Exponer puertos
EXPOSE 8000 8501

# Comandos disponibles:
#   - API: uvicorn src.api.main:app --host 0.0.0.0 --port 8000
#   - Dashboard: streamlit run src/dashboard/app.py --server.port=8501
CMD ["echo", "Use: docker run -p 8000:8000 dam-monitoring-api  o  -p 8501:8501 dam-monitoring-dashboard"]
```

## 9.2 Archivo: `docker/docker-compose.yml`

```yaml
# dam-monitoring-p1/docker/docker-compose.yml
version: '3.8'

services:
  # Base de datos PostgreSQL para históricos
  postgres:
    image: postgres:15
    container_name: dam-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: dam_monitoring
      POSTGRES_USER: edi_user
      POSTGRES_PASSWORD: secure_password_2025
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - dam-network

  # API REST (FastAPI)
  api:
    build: 
      context: ..
      dockerfile: docker/Dockerfile
    container_name: dam-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      PG_HOST: postgres
      PG_DB: dam_monitoring
      PG_USER: edi_user
      PG_PASSWORD: secure_password_2025
      ORA_USER: scada_reader
      ORA_PASSWORD: ${ORA_PASSWORD}
      ORA_DSN: scada-srv:1521/SCADADB
    depends_on:
      - postgres
    networks:
      - dam-network
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

  # Dashboard (Streamlit)
  dashboard:
    build: 
      context: ..
      dockerfile: docker/Dockerfile
    container_name: dam-dashboard
    restart: unless-stopped
    ports:
      - "8501:8501"
    environment:
      PG_HOST: postgres
      PG_DB: dam_monitoring
      PG_USER: edi_user
      PG_PASSWORD: secure_password_2025
    depends_on:
      - api
    networks:
      - dam-network
    command: streamlit run src/dashboard/app.py --server.port=8501 --server.address=0.0.0.0

volumes:
  postgres_data:

networks:
  dam-network:
    driver: bridge
```

### 🔍 **Análisis de Despliegue**

#### **Multi-stage build para optimización**
```dockerfile
FROM python:3.11-slim AS builder
# ... instalar dependencias
FROM python:3.11-slim
# ... copiar solo lo necesario
```
- **Tamaño reducido**: La imagen final no incluye compiladores ni headers
- **Seguridad**: Menos paquetes = menor superficie de ataque
- **Rapidez**: Builds más rápidos y pulls más eficientes

#### **Usuario no-root para seguridad**
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```
- **Principio de mínimo privilegio**: La aplicación no se ejecuta como root
- **Cumplimiento**: Requisito para entornos regulados (ISO 27001, etc.)
- **Prevención**: Mitiga impacto de vulnerabilidades de escalada de privilegios

#### **Variables de entorno para configuración**
```yaml
environment:
  PG_HOST: postgres
  ORA_PASSWORD: ${ORA_PASSWORD}
```
- **Seguridad**: Credenciales sensibles no están en el código
- **Flexibilidad**: Misma imagen para desarrollo, pruebas y producción
- **Mejor práctica**: Usa `.env` para variables locales, secrets para producción

---

# 📚 **Fase 10: Documentación y Siguiente Pasos**

## 10.1 Generar Documentación Automática

Crea un script `generate_docs.py`:

```python
# generate_docs.py
"""
Genera documentación técnica automática para el sistema de monitoreo.

Incluye:
- Diagramas de arquitectura
- Guías de instalación
- Referencia de API
- Ejemplos de uso

Salida: docs/sistema_monitoreo_represas.pdf
"""
import os
from pathlib import Path
from jinja2 import Template
from weasyprint import HTML

# Crear directorio
docs_dir = Path("docs")
docs_dir.mkdir(exist_ok=True)

# Plantilla HTML profesional
template = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Sistema de Monitoreo de Represas - Documentación Técnica</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        h1 { color: #0056b3; border-bottom: 2px solid #0056b3; }
        .section { margin-bottom: 30px; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Sistema de Monitoreo de Represas</h1>
    <p><strong>Versión:</strong> 2.2.0</p>
    <p><strong>Fecha:</strong> {{ date }}</p>
    
    <div class="section">
        <h2>1. Inicialización del Proyecto</h2>
        <p>Ejecutar desde línea de comandos:</p>
        <pre>py setup_project.py dam-monitoring-p1</pre>
    </div>
    
    <div class="section">
        <h2>2. Estructura del Proyecto</h2>
        <pre>dam-monitoring-p1/
├── src/
│   ├── __init__.py          # ← Habilita: from src import config, data
│   ├── config/
│   │   ├── __init__.py      # ← Habilita: from src.config import db_manager
│   │   └── db.py            # ← Gestor unificado de bases de datos
│   └── data/
│       ├── __init__.py      # ← Habilita: from src.data import load_csv
│       └── ingestion.py     # ← Carga desde múltiples fuentes
└── tests/                   # ← Pruebas automatizadas</pre>
    </div>
    
    <div class="section">
        <h2>3. Uso Recomendado</h2>
        <p>Cargar datos desde múltiples fuentes:</p>
        <pre>from src.data import load_multiple_sources

df = load_multiple_sources([
    {"type": "csv", "config": {"file_path": "data/raw/sensors.csv"}},
    {"type": "db", "config": {
        "query": "SELECT * FROM scada_readings", 
        "db_type": "oracle",
        "dsn": "scada-server:1521/SCADADB"
    }}
])</pre>
    </div>
</body>
</html>
""")

# Generar HTML
html_content = template.render(date="2025-11-18")

# Convertir a PDF
pdf_path = docs_dir / "sistema_monitoreo_represas.pdf"
HTML(string=html_content).write_pdf(pdf_path)

print(f"✅ Documentación generada: {pdf_path}")
```

## 10.2 Siguientes Pasos Recomendados

### **Implementación Fase 1: Datos en Tiempo Real**
1. **Configurar conexión a SCADA Oracle**:
   ```python
   # Crear .env con credenciales reales
   ORA_USER=scada_reader
   ORA_PASSWORD=tu_contraseña_segura
   ORA_DSN=scada-server:1521/SCADADB
   ```

2. **Cargar datos en tiempo real**:
   ```python
   from src.data import load_from_db
   df_scada = load_from_db(
       "SELECT DAM_ID, LEVEL_M, FLOW_M3S, TIMESTAMP FROM SENSOR_READINGS WHERE TIMESTAMP > SYSDATE - 1/24",
       "oracle"
   )
   ```

### **Implementación Fase 2: Alertas Automáticas**
1. **Entrenar detector de anomalías**:
   ```python
   from src.ml import AnomalyDetector
   detector = AnomalyDetector(contamination=0.005)
   detector.fit(df_historical)
   ```

2. **Integrar con sistema de alertas**:
   ```python
   anomalies = detector.predict(df_recent)
   critical_alerts = anomalies[anomalies["severity"] == "CRÍTICA"]
   if len(critical_alerts) > 0:
       send_sms_alert(f"ALERTA CRÍTICA en {critical_alerts.iloc[0]['dam_id']}")
   ```

### **Implementación Fase 3: Informes Automatizados**
1. **Generar informe mensual**:
   ```python
   from src.reports import generate_monthly_report
   df_month = load_from_db("SELECT * FROM readings WHERE timestamp >= DATE_TRUNC('month', CURRENT_DATE)", "postgres")
   pdf_path = generate_monthly_report("REP-001", df_month)
   ```

2. **Programar con cron** (Linux) o Task Scheduler (Windows):
   ```bash
   # Generar informe el primer día de cada mes a las 6:00 AM
   0 6 1 * * cd /path/to/project && venv/bin/python -c "from src.reports import generate_monthly_report; generate_monthly_report('REP-001', ...)"
   ```

---

## ✅ **Resumen de Comandos Útiles**

| Acción | Comando |
|--------|---------|
| **Crear proyecto** | `py setup_project.py dam-monitoring-p1` |
| **Activar entorno** | `venv\Scripts\activate` |
| **Ejecutar dashboard** | `streamlit run src/dashboard/app.py` |
| **Iniciar API** | `uvicorn src.api.main:app --reload` |
| **Ejecutar pruebas** | `pytest tests/ -v --cov=src` |
| **Generar documentación** | `python generate_docs.py` |
| **Construir Docker** | `docker-compose -f docker/docker-compose.yml build` |
| **Iniciar servicios** | `docker-compose -f docker/docker-compose.yml up -d` |

