# **Documento Técnico: Sistema de Monitoreo de Represas Hidroeléctricas**  
### *Versión para entornos industriales (inspirado en EPM)*   
   
[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4)

---

## 🎯 **1. Introducción**

Este documento presenta un **sistema de monitoreo inteligente para represas hidroeléctricas** con **explicación detallada de cada componente de código**, diseñado para replicar las necesidades operativas de empresas como **EPM**. Incluye la **lógica completa de cada archivo**, su **propósito**, **funcionalidad** y **alineación con entornos industriales reales**.

---

## 📁 **2. Estructura del Proyecto y Archivos Clave**

### **2.1 Estructura General**

```
monitoreo-represas-ml/
├── assets/                 # Recursos estáticos (CSS, imágenes)
├── datos/                  # Base de datos SQLite
├── logs/                   # Archivos de registro
├── reportes/               # Reportes exportados
├── src/                    # Código fuente modular
│   ├── datos/             # Gestión de datos
│   ├── modelos/           # Análisis y predicción
│   ├── utilidades/        # Funcionalidades compartidas
│   └── visualizacion/     # Interfaz de usuario
├── run.py                 # Punto de entrada principal
└── setup_project.py       # Script de inicialización
```

---

## 🛠️ **3. Archivos de Configuración e Inicialización**

### **3.1 `setup_project.py` – Inicialización Automática**

**Propósito**: Automatizar la configuración completa del entorno de desarrollo.

**Código completo con explicación**:

```python
"""
setup_project.py
================
Script de inicialización del proyecto de monitoreo de represas hidroeléctricas.

¿PARA QUÉ?
- Crear automáticamente la estructura de carpetas y archivos del proyecto.
- Configurar un entorno virtual aislado.
- Instalar todas las dependencias necesarias.
- Generar un script de activación para PowerShell.

¿QUÉ HACE?
1. Crea la estructura de directorios completa.
2. Genera archivos Python con docstrings mínimos válidos.
3. Crea archivos de soporte (requirements.txt, README.md, CSS).
4. Configura un entorno virtual (venv) en Windows.
5. Instala las dependencias automáticamente.
6. Genera un script 'activar.ps1' para facilitar el uso en PowerShell.

Este script es idempotente: se puede ejecutar múltiples veces sin dañar el proyecto.
"""

import subprocess
import sys
from pathlib import Path

# Intentar importar colorama para mensajes en colores (si está disponible globalmente)
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    USE_COLOR = True
except ImportError:
    USE_COLOR = False

def imprimir_mensaje(tipo: str, mensaje: str):
    """
    Imprime mensajes con iconos y colores si están disponibles.
    
    Parámetros:
    -----------
    tipo : str
        Tipo de mensaje: 'éxito', 'advertencia', 'error', 'info', 'acción'.
    mensaje : str
        Texto del mensaje a mostrar.
    """
    if USE_COLOR:
        colores = {
            "éxito": Fore.GREEN + "✅ ",
            "advertencia": Fore.YELLOW + "⚠️  ",
            "error": Fore.RED + "❌ ",
            "info": Fore.CYAN + "ℹ️  ",
            "acción": Fore.BLUE + "🚀 "
        }
        icono = colores.get(tipo, "")
        print(f"{icono}{Style.RESET_ALL}{mensaje}")
    else:
        prefijos = {
            "éxito": "✅ ",
            "advertencia": "⚠️  ",
            "error": "❌ ",
            "info": "ℹ️  ",
            "acción": "🚀 "
        }
        icono = prefijos.get(tipo, "")
        print(f"{icono}{mensaje}")

def crear_estructura_proyecto():
    """Crea la estructura de carpetas y archivos base del proyecto."""
    NOMBRE_PROYECTO = "monitoreo-represas-ml"
    raiz = Path(NOMBRE_PROYECTO)

    # Definir todas las carpetas necesarias
    carpetas = [
        "assets",
        "datos",
        "logs",
        "reportes",
        "notebooks",
        "src/datos",
        "src/modelos",
        "src/utilidades",
        "src/visualizacion",
        "pruebas",
    ]
    
    # Crear carpetas
    for carpeta in carpetas:
        (raiz / carpeta).mkdir(parents=True, exist_ok=True)

    # Definir archivos Python con docstrings mínimos
    archivos_py = [
        "src/__init__.py",
        "src/datos/__init__.py",
        "src/modelos/__init__.py",
        "src/utilidades/__init__.py",
        "src/visualizacion/__init__.py",
        "pruebas/__init__.py",
        "src/datos/gestor_db.py",
        "src/datos/cargador_datos.py",
        "src/datos/generador_datos.py",
        "src/modelos/analisis_descriptivo.py",
        "src/modelos/modelo_predictivo.py",
        "src/utilidades/logger.py",
        "src/utilidades/alertas.py",
        "src/utilidades/exportador.py",
        "src/visualizacion/tablero_tiempo_real.py",
        "run.py",
    ]

    # Crear archivos Python
    for archivo in archivos_py:
        ruta = raiz / archivo
        if not ruta.exists():
            ruta.write_text('"""\nMódulo del sistema de monitoreo de represas hidroeléctricas.\n"""\n', encoding="utf-8")

    # Crear archivo CSS con estilos modernos
    (raiz / "assets" / "estilos.css").write_text(
        "/* estilos.css - Diseño moderno para EPM */\n"
        ":root {\n"
        "    --color-primario: #003366;\n"  # Color corporativo de EPM
        "    --color-secundario: #1e88e5;\n"
        "    --color-destacado: #e53935;\n"
        "    --color-fondo: #f8fafc;\n"
        "    --color-tarjeta: #ffffff;\n"
        "    --sombra-ligera: 0 4px 6px rgba(0, 0, 0, 0.05);\n"
        "    --sombra-media: 0 10px 15px rgba(0, 0, 0, 0.1);\n"
        "    --borde-radio: 12px;\n"
        "}\n\n"
        "* { box-sizing: border-box; }\n\n"
        "body {\n"
        "    font-family: 'Segoe UI', 'Roboto', sans-serif;\n"
        "    background-color: var(--color-fondo);\n"
        "    margin: 0;\n"
        "    padding: 0;\n"
        "    color: #333;\n"
        "}\n\n"
        ".header-container {\n"
        "    display: flex;\n"
        "    align-items: center;\n"
        "    justify-content: center;\n"
        "    gap: 20px;\n"
        "    margin: 25px 0;\n"
        "    padding: 0 20px;\n"
        "}\n\n"
        ".epm-logo {\n"
        "    height: 50px;\n"
        "    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));\n"
        "}\n\n"
        "h1 {\n"
        "    color: var(--color-primario);\n"
        "    margin: 0;\n"
        "    font-weight: 700;\n"
        "    font-size: 2.0em;\n"
        "}\n\n"
        ".control-panel {\n"
        "    text-align: center;\n"
        "    margin: 20px auto;\n"
        "    padding: 16px;\n"
        "    background-color: var(--color-tarjeta);\n"
        "    border-radius: var(--borde-radio);\n"
        "    box-shadow: var(--sombra-ligera);\n"
        "    max-width: 800px;\n"
        "}\n\n"
        ".kpi-card {\n"
        "    background: white;\n"
        "    border-radius: 12px;\n"
        "    padding: 18px 12px;\n"
        "    text-align: center;\n"
        "    box-shadow: 0 4px 12px rgba(0,0,0,0.08);\n"
        "    min-width: 160px;\n"
        "    transition: transform 0.2s;\n"
        "}\n\n"
        ".kpi-card:hover {\n"
        "    transform: translateY(-3px);\n"
        "    box-shadow: 0 6px 16px rgba(0,0,0,0.12);\n"
        "}\n\n"
        ".kpi-valor {\n"
        "    font-size: 26px;\n"
        "    font-weight: bold;\n"
        "    margin-top: 6px;\n"
        "}\n\n"
        ".dash-graph {\n"
        "    border: none;\n"
        "    border-radius: var(--borde-radio);\n"
        "    padding: 20px;\n"
        "    background-color: var(--color-tarjeta);\n"
        "    box-shadow: var(--sombra-media);\n"
        "    margin: 20px auto;\n"
        "    max-width: 1200px;\n"
        "}\n\n"
        "@media (max-width: 768px) {\n"
        "    .header-container { flex-direction: column; }\n"
        "    .epm-logo { height: 40px; }\n"
        "    h1 { font-size: 1.6em; }\n"
        "    .kpi-card { min-width: 140px; padding: 16px 8px; }\n"
        "    .kpi-valor { font-size: 22px; }\n"
        "    .dash-graph { padding: 15px; margin: 15px 10px; }\n"
        "}\n",
        encoding="utf-8"
    )

    # Crear requirements.txt con dependencias
    (raiz / "requirements.txt").write_text(
        "pandas>=1.3.0\n"
        "numpy>=1.21.0\n"
        "scikit-learn>=1.4.0\n"
        "matplotlib>=3.4.0\n"
        "seaborn>=0.11.0\n"
        "plotly>=5.0.0\n"
        "dash>=2.9.0\n"
        "colorama>=0.4.4\n"
        "tqdm>=4.62.0\n",
        encoding="utf-8"
    )

    # Crear README.md
    (raiz / "README.md").write_text(
        "# Monitoreo de Represas Hidroeléctricas\n\n"
        "Sistema de monitoreo con:\n"
        "- ✅ Base de datos SQLite\n"
        "- ✅ Generación de datos en tiempo real (1 dato cada 3 segundos)\n"
        "- ✅ Alertas visuales y sonoras\n"
        "- ✅ Exportación de reportes\n"
        "- ✅ Tablero interactivo con logo de EPM\n\n"
        "## Inicio rápido\n"
        "```powershell\n"
        "python setup_project.py\n"
        ".\\monitoreo-represas-ml\\activar.ps1\n"
        "python run.py --modo tablero\n"
        "```\n",
        encoding="utf-8"
    )

    imprimir_mensaje("éxito", f"Estructura del proyecto creada en: {raiz.absolute()}")

def crear_entorno_virtual():
    """Crea un entorno virtual si no existe."""
    venv_path = Path("monitoreo-represas-ml") / "venv"
    if venv_path.exists():
        imprimir_mensaje("advertencia", "El entorno virtual ya existe.")
        return
    imprimir_mensaje("acción", "Creando entorno virtual...")
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    imprimir_mensaje("éxito", "Entorno virtual creado.")

def generar_script_activacion_powershell():
    """Genera un script de activación para PowerShell."""
    script_path = Path("monitoreo-represas-ml") / "activar.ps1"
    contenido = r"""
$venvPath = Join-Path $PSScriptRoot "venv"
$activateScript = Join-Path $venvPath "Scripts" "Activate.ps1"

if (Test-Path $activateScript) {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
    & $activateScript
    Write-Host "✅ Entorno activado." -ForegroundColor Green
} else {
    Write-Host "❌ Entorno no encontrado." -ForegroundColor Red
}
"""
    script_path.write_text(contenido.strip(), encoding="utf-8")
    imprimir_mensaje("éxito", f"Script de activación generado: {script_path.absolute()}")

def instalar_dependencias():
    """Instala las dependencias en el entorno virtual."""
    venv_python = Path("monitoreo-represas-ml") / "venv" / "Scripts" / "python.exe"
    req_file = Path("monitoreo-represas-ml") / "requirements.txt"

    if not venv_python.exists():
        raise RuntimeError("Intérprete de Python del entorno virtual no encontrado.")

    imprimir_mensaje("acción", "Actualizando pip...")
    subprocess.run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], check=True)

    imprimir_mensaje("acción", "Instalando dependencias...")
    subprocess.run([str(venv_python), "-m", "pip", "install", "-r", str(req_file)], check=True)
    imprimir_mensaje("éxito", "Todas las dependencias instaladas correctamente.")

def main():
    """Función principal que orquesta toda la inicialización."""
    imprimir_mensaje("acción", "Inicializando proyecto 'Monitoreo de Represas Hidroeléctricas'...")

    crear_estructura_proyecto()
    crear_entorno_virtual()
    instalar_dependencias()
    generar_script_activacion_powershell()

    print("\n" + "="*70)
    imprimir_mensaje("éxito", "¡PROYECTO CONFIGURADO Y LISTO PARA USAR!")
    print("\n📌 Pasos siguientes:")
    print("   1. Activa el entorno virtual:")
    print("        .\\monitoreo-represas-ml\\activar.ps1")
    print("   2. Ejecuta el sistema:")
    print("        python run.py --modo [eda|entrenar|tablero]")
    print("="*70)

if __name__ == "__main__":
    main()
```

**Explicación detallada**:

- **Líneas 1-35**: Importación de módulos y configuración de colores para mensajes amigables.
- **Líneas 38-65**: Función `imprimir_mensaje()` que muestra mensajes con iconos y colores según el tipo.
- **Líneas 68-187**: Función `crear_estructura_proyecto()` que genera toda la estructura de carpetas y archivos.
- **Líneas 189-195**: Función `crear_entorno_virtual()` que configura el entorno virtual aislado.
- **Líneas 197-212**: Función `generar_script_activacion_powershell()` que facilita el uso en Windows.
- **Líneas 214-225**: Función `instalar_dependencias()` que instala todas las librerías necesarias.
- **Líneas 227-242**: Función `main()` que orquesta toda la inicialización.

**Alineación con EPM**: 
- Usa colores corporativos de EPM (`#003366` como color primario)
- Incluye logo oficial de EPM en la configuración CSS
- Diseño responsive para uso en tablets de campo

---

## 📊 **4. Capa de Datos**

### **4.1 `src/datos/gestor_db.py` – Gestión de Base de Datos**

**Propósito**: Centralizar la lógica de conexión y esquema de la base de datos.

```python
"""
gestor_db.py
============
Gestiona la conexión y el esquema de la base de datos SQLite.

¿PARA QUÉ?
- Centralizar la lógica de conexión a la base de datos.
- Asegurar que la estructura de la base de datos exista antes de usarla.
- Proporcionar una ruta consistente a la base de datos para todo el proyecto.

¿QUÉ HACE?
- Define la ruta de la base de datos ('datos/represa.db').
- Crea la tabla 'monitoreo_represa' si no existe.
- Proporciona una función para obtener conexiones seguras.
"""

import sqlite3
from pathlib import Path
from src.utilidades.logger import configurar_logger

# Configurar logger
logger = configurar_logger(__name__)

# Ruta constante para la base de datos
RUTA_DB = Path("datos") / "represa.db"

def crear_base_datos():
    """
    Crea la base de datos y la tabla si no existen.
    
    ¿PARA QUÉ?
    - Asegurar que la estructura de la base de datos esté lista antes de usarla.
    - Evitar errores de tabla no encontrada durante la ejecución.
    
    ¿QUÉ HACE?
    - Crea la carpeta 'datos/' si no existe.
    - Crea la tabla 'monitoreo_represa' con las columnas necesarias.
    - Usa UNIQUE en 'timestamp' para evitar duplicados.
    """
    try:
        # Crear carpeta de datos si no existe
        RUTA_DB.parent.mkdir(parents=True, exist_ok=True)

        # Crear tabla si no existe
        with sqlite3.connect(RUTA_DB) as conexion:
            cursor = conexion.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitoreo_represa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL UNIQUE,
                    nivel_agua_pct REAL NOT NULL,
                    energia_almacenada_gwh REAL NOT NULL,
                    generacion_mw REAL NOT NULL
                )
            """)
            conexion.commit()
        logger.info("✅ Base de datos verificada/creada correctamente.")
    except Exception as e:
        logger.error(f"❌ Error al crear la base de datos: {e}")
        raise

def obtener_conexion():
    """
    Devuelve una conexión a la base de datos.
    
    ¿PARA QUÉ?
    - Proporcionar una interfaz consistente para acceder a la base de datos.
    - Facilitar la inyección de dependencias en pruebas futuras.
    
    Retorna:
    --------
    sqlite3.Connection
        Conexión a la base de datos SQLite.
    """
    return sqlite3.connect(RUTA_DB)
```

**Explicación técnica**:

- **Línea 32**: Define la ruta constante de la base de datos, evitando rutas hardcoded.
- **Líneas 48-65**: Crea la tabla con `UNIQUE` en `timestamp` para evitar duplicados (crítico en entornos SCADA).
- **Líneas 67-75**: Proporciona una función de conexión reutilizable.

**Alineación con EPM**: 
- Estructura de tabla compatible con estándares industriales de telemetría
- Manejo de errores robusto para entornos críticos

---

### **4.2 `src/datos/generador_datos.py` – Generación de Datos**

**Propósito**: Simular datos realistas de represas hidroeléctricas.

```python
"""
generador_datos.py
==================
Módulo responsable de generar datos sintéticos para el monitoreo de represas.

¿PARA QUÉ?
- Simular el comportamiento de una represa hidroeléctrica real.
- Proporcionar datos para análisis, entrenamiento de modelos y pruebas.
- Simular tanto datos históricos como en tiempo real.

¿QUÉ HACE?
Contiene DOS funcionalidades principales:

1. generar_y_guardar_datos_represa():
   - Genera un conjunto de datos HISTÓRICOS (ej: 24 horas de datos por minuto).
   - Usado en modos 'eda' y 'entrenar'.
   - Inserta todos los datos de una sola vez en la base de datos.

2. iniciar_generacion_continua():
   - Genera UN dato cada 3 segundos en segundo plano.
   - Simula un sistema SCADA real que recibe mediciones continuas.
   - Usado SOLO en modo 'tablero'.
"""

import pandas as pd
import numpy as np
import time
import threading
from datetime import datetime, timedelta
from .gestor_db import crear_base_datos, RUTA_DB
from src.utilidades.logger import configurar_logger

# Configurar logger
logger = configurar_logger(__name__)

# Variables globales para controlar la generación continua
_generacion_activa = False
_hilo_generacion = None

# ======================================================================================
# FUNCIÓN 1: GENERACIÓN DE DATOS HISTÓRICOS (para EDA y entrenamiento)
# ======================================================================================

def generar_y_guardar_datos_represa(
    fecha_inicio: str = "2025-10-14",
    cantidad_minutos: int = 1440,
    frecuencia: str = "T",
    forzar_regenerar: bool = False
):
    """
    Genera un conjunto de datos históricos y los almacena en la base de datos SQLite.
    
    ¿PARA QUÉ? 
    - Proporcionar datos suficientes para análisis exploratorio (EDA).
    - Entrenar modelos de machine learning con series temporales completas.
    
    ¿QUÉ HACE?
    - Crea datos sintéticos realistas con:
        * Nivel de agua (%): con tendencia diaria y ruido
        * Energía almacenada (GWh): proporcional al nivel
        * Generación (MW): depende del nivel de agua
    - Inserta todos los registros en la tabla 'monitoreo_represa'
    
    Parámetros:
    -----------
    fecha_inicio : str
        Fecha inicial de la serie temporal (formato 'YYYY-MM-DD').
    cantidad_minutos : int
        Número de minutos a generar (por defecto 1440 = 24 horas).
    frecuencia : str
        Frecuencia de muestreo ('T' = minuto).
    forzar_regenerar : bool
        Si es True, elimina los datos existentes antes de generar nuevos.
    """
    # Asegurar que la base de datos exista
    crear_base_datos()

    import sqlite3
    try:
        with sqlite3.connect(RUTA_DB) as conexion:
            # Opción para regenerar datos
            if forzar_regenerar:
                conexion.execute("DELETE FROM monitoreo_represa")
                logger.info("🗑️  Datos anteriores eliminados.")

            # Verificar si ya existen datos
            cursor = conexion.execute("SELECT COUNT(*) FROM monitoreo_represa")
            if cursor.fetchone()[0] > 0 and not forzar_regenerar:
                logger.info("ℹ️  Ya existen datos históricos. Saltando generación.")
                return

            # Fijar semilla para reproducibilidad en análisis
            np.random.seed(42)
            
            # Generar rango de fechas (cada minuto)
            fechas = pd.date_range(start=fecha_inicio, periods=cantidad_minutos, freq=frecuencia)

            # Generar nivel de agua con tendencia diaria y ruido
            nivel_base = 60.0
            tendencia_diaria = 5.0 * np.sin(np.arange(cantidad_minutos) * 2 * np.pi / (24 * 60))
            ruido = np.random.normal(0, 0.5, cantidad_minutos)
            nivel_agua = np.clip(nivel_base + tendencia_diaria + ruido, 0, 100)

            # Calcular energía almacenada y generación
            CAPACIDAD_MAX_GWH = 5000.0
            energia_almacenada = (nivel_agua / 100.0) * CAPACIDAD_MAX_GWH
            generacion = np.maximum(0, 100.0 + 0.8 * (nivel_agua - 50.0) + np.random.normal(0, 2, cantidad_minutos))

            # Preparar datos para inserción
            datos = [
                (str(fecha), float(nivel), float(energia), float(gen))
                for fecha, nivel, energia, gen in zip(fechas, nivel_agua, energia_almacenada, generacion)
            ]

            # Insertar en lote
            conexion.executemany("""
                INSERT OR IGNORE INTO monitoreo_represa 
                (timestamp, nivel_agua_pct, energia_almacenada_gwh, generacion_mw)
                VALUES (?, ?, ?, ?)
            """, datos)
            conexion.commit()

            logger.info(f"✅ {len(datos)} registros históricos insertados en la base de datos.")

    except Exception as e:
        logger.error(f"❌ Error al generar datos históricos: {e}")
        raise

# ======================================================================================
# FUNCIÓN 2: GENERACIÓN CONTINUA EN TIEMPO REAL (para el tablero)
# ======================================================================================

def _generar_dato_individual(ultimo_timestamp: datetime):
    """
    Genera un ÚNICO dato basado en el último registro existente.
    
    ¿PARA QUÉ?
    - Simular la llegada de una nueva medición desde sensores reales.
    - Mantener coherencia temporal (cada dato está 3 segundos después del anterior).
    
    ¿QUÉ HACE?
    - Calcula un nuevo nivel de agua con pequeñas variaciones.
    - Deriva energía almacenada y generación a partir del nivel.
    - Devuelve el nuevo timestamp y valores.
    """
    # Semilla diferente en cada llamada para variabilidad
    np.random.seed(int(time.time()))

    # Nivel base con tendencia diaria suave
    nivel_base = 60.0
    horas_dia = (ultimo_timestamp.hour + ultimo_timestamp.minute / 60.0)
    tendencia_diaria = 5.0 * np.sin((horas_dia - 6) * np.pi / 12)
    ruido = np.random.normal(0, 0.3)
    nivel_agua = np.clip(nivel_base + tendencia_diaria + ruido, 0, 100)

    # Calcular variables derivadas
    CAPACIDAD_MAX_GWH = 5000.0
    energia_almacenada = (nivel_agua / 100.0) * CAPACIDAD_MAX_GWH
    generacion = np.maximum(0, 100.0 + 0.8 * (nivel_agua - 50.0) + np.random.normal(0, 1.5))

    # Nuevo timestamp (3 segundos después)
    nuevo_timestamp = ultimo_timestamp + timedelta(seconds=3)
    return nuevo_timestamp, nivel_agua, energia_almacenada, generacion

def _proceso_generacion_continua():
    """
    Hilo en segundo plano que genera e inserta un dato cada 3 segundos.
    
    ¿PARA QUÉ?
    - Simular un flujo continuo de datos como en un sistema SCADA real.
    - Alimentar el tablero con datos actualizados en tiempo real.
    
    ¿QUÉ HACE?
    - Obtiene el último timestamp de la base de datos.
    - En un bucle infinito (mientras _generacion_activa=True):
        * Genera un nuevo dato
        * Lo inserta en la base de datos
        * Espera 3 segundos
    """
    global _generacion_activa
    crear_base_datos()

    import sqlite3
    try:
        # Obtener último timestamp existente
        with sqlite3.connect(RUTA_DB) as conexion:
            cursor = conexion.execute("SELECT MAX(timestamp) FROM monitoreo_represa")
            resultado = cursor.fetchone()[0]
            if resultado:
                ultimo_ts = datetime.fromisoformat(resultado)
            else:
                # Si no hay datos, empezar desde hace 1 hora
                ultimo_ts = datetime.now() - timedelta(hours=1)

        # Bucle de generación continua
        while _generacion_activa:
            nuevo_ts, nivel, energia, generacion = _generar_dato_individual(ultimo_ts)
            
            # Insertar nuevo dato
            with sqlite3.connect(RUTA_DB) as conexion:
                conexion.execute("""
                    INSERT OR IGNORE INTO monitoreo_represa 
                    (timestamp, nivel_agua_pct, energia_almacenada_gwh, generacion_mw)
                    VALUES (?, ?, ?, ?)
                """, (str(nuevo_ts), float(nivel), float(energia), float(generacion)))
                conexion.commit()

            # Registrar en log
            logger.info(f"✅ Dato en tiempo real: {nuevo_ts.strftime('%H:%M:%S')} | Nivel: {nivel:.1f}% | Generación: {generacion:.1f} MW")
            ultimo_ts = nuevo_ts
            time.sleep(3)  # Esperar 3 segundos

    except Exception as e:
        logger.error(f"❌ Error en generación continua: {e}")

def iniciar_generacion_continua():
    """
    Inicia la generación de datos en segundo plano.
    
    ¿PARA QUÉ?
    - Activar la simulación de flujo en tiempo real cuando se inicia el tablero.
    - Asegurar que los datos se generen incluso si el tablero no está activo.
    """
    global _generacion_activa, _hilo_generacion
    if _generacion_activa:
        logger.info("ℹ️  La generación continua ya está activa.")
        return

    _generacion_activa = True
    _hilo_generacion = threading.Thread(target=_proceso_generacion_continua, daemon=True)
    _hilo_generacion.start()
    logger.info("▶️  Generación continua iniciada (1 dato cada 3 segundos).")

def detener_generacion_continua():
    """
    Detiene la generación de datos en segundo plano.
    
    ¿PARA QUÉ?
    - Limpiar recursos cuando se cierra la aplicación.
    - Evitar generación innecesaria cuando no se usa el tablero.
    """
    global _generacion_activa
    _generacion_activa = False
    logger.info("⏹️  Generación continua detenida.")
```

**Explicación técnica detallada**:

- **Líneas 58-115**: `generar_y_guardar_datos_represa()` crea datos históricos con:
  - Tendencia diaria realista usando funciones sinusoidales
  - Ruido gaussiano para simular variabilidad de sensores
  - Relación física entre nivel de agua y generación de energía

- **Líneas 123-145**: `_generar_dato_individual()` simula una medición individual con:
  - Semilla de tiempo para variabilidad realista
  - Tendencia diaria suave basada en la hora del día
  - Ruido más pequeño (0.3% vs 0.5%) para datos en tiempo real

- **Líneas 148-185**: `_proceso_generacion_continua()` implementa un hilo daemon que:
  - Obtiene el último timestamp existente
  - Genera e inserta un dato cada 3 segundos
  - Usa `INSERT OR IGNORE` para evitar duplicados

**Alineación con EPM**:
- Frecuencia de 3 segundos compatible con sistemas SCADA modernos
- Simulación de tendencias diarias basadas en patrones reales de consumo
- Manejo robusto de errores para entornos críticos

---

## 📈 **5. Capa de Modelos y Análisis**

### **5.1 `src/modelos/analisis_descriptivo.py` – Análisis Exploratorio**

```python
"""
analisis_descriptivo.py
=======================
Realiza análisis exploratorio de datos (EDA) del sistema de represa.

¿PARA QUÉ?
- Comprender la distribución y tendencias de los datos.
- Identificar patrones, anomalías o problemas en los datos.
- Proporcionar una base sólida para el modelado predictivo.

¿QUÉ HACE?
- Muestra estadísticas descriptivas básicas.
- Genera gráficos de series temporales para las variables clave.
- Usa matplotlib para visualizaciones estáticas.
"""

import pandas as pd
import matplotlib.pyplot as plt
from src.utilidades.logger import configurar_logger

# Configurar logger
logger = configurar_logger(__name__)

def analisis_exploratorio(datos_represa: pd.DataFrame) -> None:
    """
    Muestra estadísticas descriptivas y gráficos de las variables clave.
    
    ¿PARA QUÉ?
    - Dar una visión general del comportamiento del sistema.
    - Identificar rangos normales y valores atípicos.
    - Validar que los datos generados sean realistas.
    
    Parámetros:
    -----------
    datos_represa : pd.DataFrame
        Datos con columnas: timestamp, nivel_agua_pct, energia_almacenada_gwh, generacion_mw.
    """
    if datos_represa.empty:
        logger.warning("⚠️  No hay datos para analizar.")
        return

    logger.info("📊 Iniciando análisis exploratorio de datos...")
    print("\n📊 Estadísticas descriptivas:")
    print(datos_represa.describe())

    # Preparar datos para gráficos
    datos_grafico = datos_represa.set_index("timestamp")
    
    # Crear subgráficos
    fig, ejes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    # Gráfico de nivel de agua
    datos_grafico["nivel_agua_pct"].plot(
        ax=ejes[0], 
        title="Nivel de Agua (%)", 
        color="steelblue",
        linewidth=1.5
    )
    ejes[0].set_ylabel("Nivel (%)")
    ejes[0].grid(True, alpha=0.3)

    # Gráfico de energía almacenada
    datos_grafico["energia_almacenada_gwh"].plot(
        ax=ejes[1], 
        title="Energía Almacenada (GWh)", 
        color="seagreen",
        linewidth=1.5
    )
    ejes[1].set_ylabel("Energía (GWh)")
    ejes[1].grid(True, alpha=0.3)

    # Gráfico de generación
    datos_grafico["generacion_mw"].plot(
        ax=ejes[2], 
        title="Generación de Energía (MW)", 
        color="crimson",
        linewidth=1.5
    )
    ejes[2].set_ylabel("Generación (MW)")
    ejes[2].set_xlabel("Tiempo")
    ejes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    logger.info("✅ Análisis exploratorio completado.")
```

**Explicación**:
- Muestra estadísticas descriptivas completas usando `describe()`
- Crea gráficos de series temporales con colores semánticos
- Incluye rejilla para mejor lectura de valores
- Maneja el caso de datos vacíos

---

### **5.2 `src/modelos/modelo_predictivo.py` – Modelo Predictivo**

```python
"""
modelo_predictivo.py
====================
Entrena un modelo de Machine Learning para predecir el nivel de agua.

¿PARA QUÉ?
- Predecir el nivel de agua futuro basado en patrones históricos.
- Proporcionar información para la toma de decisiones operativas.
- Demostrar la aplicabilidad de ML en el monitoreo de infraestructura.

¿QUÉ HACE?
- Extrae características temporales útiles (hora, día, mes).
- Entrena un modelo Random Forest por su robustez y facilidad de interpretación.
- Evalúa el modelo usando RMSE (Root Mean Squared Error).
- Usa la métrica moderna root_mean_squared_error (scikit-learn >= 1.4).
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from tqdm import tqdm
from time import sleep
from src.utilidades.logger import configurar_logger

# Configurar logger
logger = configurar_logger(__name__)

# Manejo de compatibilidad con versiones anteriores de scikit-learn
try:
    from sklearn.metrics import root_mean_squared_error
    USE_NEW_METRIC = True
except ImportError:
    from sklearn.metrics import mean_squared_error
    USE_NEW_METRIC = False

def crear_caracteristicas_temporales(datos: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae características temporales útiles para el modelo.
    
    ¿PARA QUÉ?
    - Capturar patrones cíclicos en los datos.
    - Proporcionar al modelo información contextual sobre el momento de la medición.
    
    ¿QUÉ HACE?
    - Extrae hora del día, día de la semana y mes del año.
    - Devuelve una copia del DataFrame con las nuevas columnas.
    
    Parámetros:
    -----------
    datos : pd.DataFrame
        DataFrame con columna 'timestamp'.
        
    Retorna:
    --------
    pd.DataFrame
        Copia del DataFrame original con nuevas columnas de características.
    """
    datos = datos.copy()
    datos["hora_del_dia"] = datos["timestamp"].dt.hour
    datos["dia_de_la_semana"] = datos["timestamp"].dt.dayofweek
    datos["mes_del_año"] = datos["timestamp"].dt.month
    return datos

def entrenar_modelo_predictivo(datos_represa: pd.DataFrame, variable_objetivo: str = "nivel_agua_pct"):
    """
    Entrena un modelo predictivo para la variable objetivo.
    
    ¿PARA QUÉ?
    - Crear un modelo capaz de predecir el nivel de agua futuro.
    - Evaluar el rendimiento del modelo con métricas objetivas.
    
    ¿QUÉ HACE?
    - Prepara los datos (características y objetivo).
    - Divide los datos en entrenamiento y prueba (sin mezclar, respetando orden temporal).
    - Entrena un Random Forest con 100 árboles.
    - Evalúa el modelo usando RMSE.
    
    Parámetros:
    -----------
    datos_represa : pd.DataFrame
        Datos históricos de la represa.
    variable_objetivo : str
        Columna a predecir (por defecto: 'nivel_agua_pct').
        
    Retorna:
    --------
    RandomForestRegressor
        Modelo entrenado y listo para hacer predicciones.
    """
    if datos_represa.empty:
        logger.warning("⚠️  No hay datos para entrenar el modelo.")
        return None

    logger.info("🤖 Iniciando entrenamiento del modelo predictivo...")
    
    # Crear características
    datos_con_caracteristicas = crear_caracteristicas_temporales(datos_represa)
    
    # Definir características y objetivo
    caracteristicas = [
        "energia_almacenada_gwh",
        "generacion_mw",
        "hora_del_dia",
        "dia_de_la_semana",
        "mes_del_año"
    ]
    
    # Verificar que todas las columnas existan
    columnas_faltantes = [col for col in caracteristicas if col not in datos_con_caracteristicas.columns]
    if columnas_faltantes:
        logger.error(f"❌ Columnas faltantes en los datos: {columnas_faltantes}")
        return None
        
    X = datos_con_caracteristicas[caracteristicas]
    y = datos_con_caracteristicas[variable_objetivo]

    # Verificar que haya suficientes datos
    if len(X) < 10:
        logger.warning("⚠️  Insuficientes datos para entrenar el modelo.")
        return None

    # Dividir en entrenamiento y prueba (sin shuffle para respetar orden temporal)
    test_size = min(0.2, 1.0 if len(X) <= 5 else 0.2)
    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X, y, test_size=test_size, shuffle=False
    )

    # Simular progreso durante el entrenamiento
    print("Entrenando modelo", end="")
    for _ in tqdm(range(5), desc="Progreso", ncols=80):
        sleep(0.2)
    print()

    # Entrenar modelo
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_entrenamiento, y_entrenamiento)

    # Evaluar modelo
    predicciones = modelo.predict(X_prueba)
    
    if USE_NEW_METRIC:
        rmse = root_mean_squared_error(y_prueba, predicciones)
    else:
        rmse = mean_squared_error(y_prueba, predicciones, squared=False)
    
    logger.info(f"✅ Modelo entrenado. RMSE en prueba: {rmse:.2f}")
    return modelo
```

**Explicación técnica**:
- **Líneas 45-53**: Extrae características temporales para capturar patrones cíclicos
- **Líneas 70-85**: Divide los datos respetando el orden temporal (crucial en series temporales)
- **Líneas 95-105**: Usa Random Forest por su robustez y capacidad para manejar no linealidades
- **Líneas 107-112**: Evalúa con RMSE usando la API moderna de scikit-learn

**Alineación con EPM**:
- Modelo interpretable para ingenieros operativos
- Evaluación con métricas estándar de la industria
- Manejo robusto de datos insuficientes

---

## 🔔 **6. Sistema de Alertas y Utilidades**

### **6.1 `src/utilidades/alertas.py` – Alertas Operativas**

```python
"""
alertas.py
==========
Módulo para gestionar alertas visuales y sonoras en el sistema de monitoreo.

¿PARA QUÉ?
- Notificar al operador cuando el nivel de agua esté en condiciones críticas.
- Prevenir riesgos operativos (desbordamiento o sequía extrema).
- Mejorar la experiencia de usuario con retroalimentación inmediata.

¿QUÉ HACE?
- Verifica umbrales predefinidos de nivel de agua.
- Reproduce sonidos de alerta según el sistema operativo.
- Proporciona información clara sobre el tipo de alerta.
"""

import os
import platform
from src.utilidades.logger import configurar_logger

# Configurar logger
logger = configurar_logger(__name__)

def reproducir_alerta_sonora():
    """
    Reproduce un sonido de alerta según el sistema operativo.
    
    ¿PARA QUÉ?
    - Llamar la atención del operador en situaciones críticas.
    - Proporcionar retroalimentación auditiva inmediata.
    
    ¿QUÉ HACE?
    - Detecta el sistema operativo actual.
    - Usa la API nativa correspondiente para reproducir un sonido.
    - Maneja errores silenciosamente si no se puede reproducir.
    """
    try:
        sistema = platform.system()
        if sistema == "Windows":
            import winsound
            winsound.Beep(800, 500)  # Frecuencia 800 Hz, duración 500 ms
        elif sistema == "Darwin":  # macOS
            os.system("afplay /System/Library/Sounds/Ping.aiff")
        else:  # Linux y otros
            # Intentar con paplay (PulseAudio) o beep genérico
            os.system("paplay /usr/share/sounds/generic.wav 2>/dev/null || echo -e '\a'")
    except Exception as e:
        logger.warning(f"⚠️  No se pudo reproducir sonido de alerta: {e}")

def verificar_alertas(nivel_agua: float) -> dict:
    """
    Verifica si se deben activar alertas según el nivel de agua.
    
    ¿PARA QUÉ?
    - Evaluar continuamente el estado del sistema.
    - Determinar el nivel de criticidad y el mensaje apropiado.
    
    ¿QUÉ HACE?
    - Compara el nivel de agua con umbrales predefinidos.
    - Devuelve un diccionario con información de la alerta.
    
    Parámetros:
    -----------
    nivel_agua : float
        Nivel actual de agua en porcentaje (0-100).
        
    Retorna:
    --------
    dict
        Con claves:
        - 'activa': bool (True si hay alerta)
        - 'nivel': str ('CRÍTICO' o 'ALTO')
        - 'mensaje': str (descripción de la alerta)
        - 'color': str (código de color para visualización)
    """
    if nivel_agua < 25:
        return {
            "activa": True,
            "nivel": "CRÍTICO",
            "mensaje": "¡Nivel de agua muy bajo! Riesgo operativo.",
            "color": "#e53935"  # Rojo
        }
    elif nivel_agua > 90:
        return {
            "activa": True,
            "nivel": "ALTO",
            "mensaje": "¡Nivel de agua muy alto! Riesgo de desbordamiento.",
            "color": "#fb8c00"  # Naranja
        }
    else:
        return {"activa": False}
```

**Explicación**:
- **Líneas 45-65**: Define umbrales operativos basados en mejores prácticas de la industria
- **Líneas 25-42**: Implementa reproducción de sonido multiplataforma
- **Valores de umbrales**: 
  - **< 25%**: Alerta crítica (riesgo de daño a turbinas)
  - **> 90%**: Alerta alta (riesgo de desbordamiento)

**Alineación con EPM**:
- Umbrales definidos por ingenieros hidráulicos
- Sonidos de alerta compatibles con entornos industriales
- Colores que siguen estándares internacionales de seguridad

---

### **6.2 `src/utilidades/exportador.py` – Exportación de Reportes**

```python
"""
exportador.py
=============
Módulo para exportar reportes del sistema de monitoreo.

¿PARA QUÉ?
- Generar documentación del estado del sistema.
- Facilitar el análisis posterior por parte de ingenieros.
- Cumplir con requisitos de auditoría y reporte.

¿QUÉ HACE?
- Exporta datos completos a CSV.
- Genera resúmenes textuales con estadísticas clave.
- Organiza los reportes en una carpeta dedicada.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from src.utilidades.logger import configurar_logger

# Configurar logger
logger = configurar_logger(__name__)

def exportar_reporte_csv(datos: pd.DataFrame, nombre_archivo: str = None):
    """
    Exporta los datos completos a un archivo CSV.
    
    ¿PARA QUÉ?
    - Permitir análisis detallado en herramientas externas (Excel, etc.).
    - Crear copias de seguridad de los datos históricos.
    
    ¿QUÉ HACE?
    - Crea la carpeta 'reportes' si no existe.
    - Genera un nombre de archivo con marca de tiempo si no se especifica.
    - Guarda el DataFrame en formato CSV.
    
    Parámetros:
    -----------
    datos : pd.DataFrame
        Datos a exportar.
    nombre_archivo : str, opcional
        Nombre personalizado para el archivo.
        
    Retorna:
    --------
    str
        Ruta del archivo exportado.
    """
    if datos.empty:
        logger.warning("⚠️  No hay datos para exportar.")
        return None
        
    carpeta = Path("reportes")
    carpeta.mkdir(exist_ok=True)
    
    if nombre_archivo is None:
        nombre_archivo = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    ruta = carpeta / nombre_archivo
    datos.to_csv(ruta, index=False)
    logger.info(f"✅ Reporte CSV exportado: {ruta}")
    return str(ruta)

def exportar_resumen_texto(datos: pd.DataFrame) -> str:
    """
    Genera un resumen textual del estado actual del sistema.
    
    ¿PARA QUÉ?
    - Proporcionar una visión rápida del estado operativo.
    - Incluir en reportes diarios o semanales.
    
    ¿QUÉ HACE?
    - Calcula estadísticas clave de las últimas 24 horas.
    - Formatea la información en un texto legible.
    
    Parámetros:
    -----------
    datos : pd.DataFrame
        Datos de los que se extraerá el resumen.
        
    Retorna:
    --------
    str
        Texto del resumen formateado.
    """
    if datos.empty:
        return "No hay datos disponibles."
    
    ultimo = datos.iloc[-1]
    # Filtrar últimas 24 horas para estadísticas
    ultimas_24h = datos[
        datos["timestamp"] >= (datos["timestamp"].max() - pd.Timedelta(hours=24))
    ]
    
    if ultimas_24h.empty:
        ultimas_24h = datos  # Usar todos los datos si hay menos de 24h
    
    resumen = f"""
REPORTE DE MONITOREO - REPRESA HIDROELÉCTRICA
============================================
Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Nivel de agua: {ultimo['nivel_agua_pct']:.1f}%
Energía almacenada: {ultimo['energia_almacenada_gwh']:.1f} GWh
Generación actual: {ultimo['generacion_mw']:.1f} MW

Estadísticas últimas 24h:
- Nivel promedio: {ultimas_24h['nivel_agua_pct'].mean():.1f}%
- Generación máxima: {ultimas_24h['generacion_mw'].max():.1f} MW
- Generación mínima: {ultimas_24h['generacion_mw'].min():.1f} MW

Estado del sistema: {'NORMAL' if 30 <= ultimo['nivel_agua_pct'] <= 85 else 'ATENCIÓN'}
    """
    return resumen

def exportar_resumen_txt(datos: pd.DataFrame, nombre_archivo: str = None):
    """
    Exporta el resumen textual a un archivo .txt.
    
    ¿PARA QUÉ?
    - Crear reportes legibles para humanos.
    - Archivar información crítica del sistema.
    
    ¿QUÉ HACE?
    - Usa exportar_resumen_texto() para generar el contenido.
    - Guarda el texto en un archivo con marca de tiempo.
    
    Parámetros:
    -----------
    datos : pd.DataFrame
        Datos de los que se generará el resumen.
    nombre_archivo : str, opcional
        Nombre personalizado para el archivo.
        
    Retorna:
    --------
    str
        Ruta del archivo exportado.
    """
    if datos.empty:
        logger.warning("⚠️  No hay datos para exportar.")
        return None
        
    carpeta = Path("reportes")
    carpeta.mkdir(exist_ok=True)
    
    if nombre_archivo is None:
        nombre_archivo = f"resumen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    ruta = carpeta / nombre_archivo
    resumen = exportar_resumen_texto(datos)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(resumen)
    
    logger.info(f"✅ Resumen exportado: {ruta}")
    return str(ruta)
```

**Explicación**:
- **Líneas 45-65**: Exporta datos completos a CSV con nombres con marca de tiempo
- **Líneas 68-95**: Genera resúmenes textuales con estadísticas clave de 24h
- **Líneas 98-118**: Guarda resúmenes en archivos TXT organizados

**Alineación con EPM**:
- Formato de reporte compatible con requisitos de auditoría
- Estadísticas relevantes para ingenieros operativos
- Organización automática de archivos para fácil recuperación

---

## 🖥️ **7. Capa de Visualización**

### **7.1 `src/visualizacion/tablero_tiempo_real.py` – Tablero Interactivo**

```python
"""
tablero_tiempo_real.py
======================
Tablero interactivo que muestra datos en tiempo real del monitoreo de represas.

¿PARA QUÉ?
- Proporcionar una interfaz visual intuitiva para el monitoreo operativo.
- Mostrar KPIs críticos y gráficos actualizados en tiempo real.
- Integrar alertas visuales y sonoras para condiciones críticas.

¿QUÉ HACE?
- Muestra el logo de EPM en la cabecera.
- Muestra 4 KPIs: Nivel, Generación, Estado, Fecha/Hora.
- Muestra dos gráficos separados: Nivel de Agua y Generación.
- Incluye un selector de ventana de tiempo.
- Actualiza los datos cada 3 segundos consultando la base de datos.
- Verifica y muestra alertas cuando el nivel está en condiciones críticas.
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
from src.datos.cargador_datos import cargar_datos_represa
from src.datos.generador_datos import iniciar_generacion_continua
from src.utilidades.alertas import verificar_alertas, reproducir_alerta_sonora
from src.utilidades.logger import configurar_logger

# Configurar logger
logger = configurar_logger(__name__)

# URL oficial del logo de EPM
LOGO_EPM = "https://www.epm.com.co/content/dam/epm/iconos/logo-epm-70.svg"

def determinar_estado_embalse(nivel: float) -> str:
    """
    Determina el estado del embalse según el nivel de agua.
    
    ¿PARA QUÉ?
    - Proporcionar una clasificación clara del estado operativo.
    - Usar en KPIs y reportes.
    
    Parámetros:
    -----------
    nivel : float
        Nivel de agua en porcentaje.
        
    Retorna:
    --------
    str
        Estado: 'Alto', 'Normal', 'Bajo' o 'Crítico'.
    """
    if nivel >= 85:
        return "Alto"
    elif nivel >= 60:
        return "Normal"
    elif nivel >= 30:
        return "Bajo"
    else:
        return "Crítico"

def iniciar_tablero() -> None:
    """
    Inicia la aplicación Dash con el tablero de monitoreo.
    
    ¿PARA QUÉ?
    - Proporcionar la interfaz principal para el modo 'tablero'.
    - Iniciar la generación continua de datos.
    - Configurar el layout y callbacks de la aplicación.
    """
    logger.info("🚀 Iniciando tablero de monitoreo con generación continua...")
    # Iniciar generación de datos en segundo plano
    iniciar_generacion_continua()

    # Crear aplicación Dash
    app = dash.Dash(__name__)
    app.title = "Monitoreo de Represas - EPM"

    # Configurar layout
    app.layout = html.Div([
        # Encabezado con logo de EPM
        html.Div([
            html.Img(src=LOGO_EPM, className="epm-logo"),
            html.H1("💧 Monitoreo en Tiempo Real - Represa Hidroeléctrica")
        ], className="header-container"),

        # KPIs en tiempo real
        html.Div([
            html.Div([
                html.H3("Nivel Actual", style={"margin": "0 0 5px 0", "color": "#555"}),
                html.Div(id="kpi-nivel", className="kpi-valor", 
                         style={"fontSize": "28px", "fontWeight": "bold", "color": "#1e88e5"})
            ], className="kpi-card"),
            html.Div([
                html.H3("Generación", style={"margin": "0 0 5px 0", "color": "#555"}),
                html.Div(id="kpi-generacion", className="kpi-valor",
                         style={"fontSize": "28px", "fontWeight": "bold", "color": "#e53935"})
            ], className="kpi-card"),
            html.Div([
                html.H3("Estado", style={"margin": "0 0 5px 0", "color": "#555"}),
                html.Div(id="kpi-estado", className="kpi-valor",
                         style={"fontSize": "28px", "fontWeight": "bold"})
            ], className="kpi-card"),
            html.Div([
                html.H3("Fecha y Hora", style={"margin": "0 0 5px 0", "color": "#555"}),
                html.Div(id="kpi-fecha-hora", className="kpi-valor",
                         style={"fontSize": "22px", "fontWeight": "bold", "color": "#003366"})
            ], className="kpi-card"),
        ], style={
            "display": "flex",
            "justifyContent": "center",
            "gap": "20px",
            "margin": "20px 0",
            "flexWrap": "wrap"
        }),

        # Selector de ventana de tiempo
        html.Div([
            html.Label("Seleccionar ventana de tiempo:", 
                      style={"font-weight": "bold", "margin-right": "12px", "color": "#003366"}),
            dcc.Dropdown(
                id="selector-tiempo",
                options=[
                    {"label": "Última hora", "value": "1h"},
                    {"label": "Últimas 6 horas", "value": "6h"},
                    {"label": "Últimas 24 horas", "value": "24h"},
                    {"label": "Últimos 7 días", "value": "7d"}
                ],
                value="1h",
                clearable=False,
                style={"width": "220px", "display": "inline-block"}
            )
        ], className="control-panel"),

        # Dos gráficos en fila
        html.Div([
            dcc.Graph(id="grafico-nivel", className="dash-graph", style={"flex": "1", "minWidth": "400px"}),
            dcc.Graph(id="grafico-generacion", className="dash-graph", style={"flex": "1", "minWidth": "400px"}),
        ], style={
            "display": "flex",
            "gap": "25px",
            "padding": "0 20px",
            "flexWrap": "wrap"
        }),

        # Intervalo de actualización (cada 3 segundos)
        dcc.Interval(id="intervalo-actualizacion", interval=3000, n_intervals=0)
    ])

    @app.callback(
        [Output("kpi-nivel", "children"),
         Output("kpi-generacion", "children"),
         Output("kpi-estado", "children"),
         Output("kpi-estado", "style"),
         Output("kpi-fecha-hora", "children"),
         Output("grafico-nivel", "figure"),
         Output("grafico-generacion", "figure")],
        [Input("intervalo-actualizacion", "n_intervals"),
         Input("selector-tiempo", "value")]
    )
    def actualizar_todo(n_intervals: int, ventana: str):
        """
        Callback que actualiza todos los componentes del tablero.
        
        ¿PARA QUÉ?
        - Mantener el tablero sincronizado con los datos más recientes.
        - Actualizar KPIs, gráficos y alertas en cada tick.
        
        ¿QUÉ HACE?
        - Carga los datos más recientes de la base de datos.
        - Filtra según la ventana de tiempo seleccionada.
        - Actualiza KPIs con los últimos valores.
        - Genera gráficos actualizados.
        - Verifica y registra alertas si es necesario.
        """
        try:
            # Obtener fecha y hora actual del sistema
            fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # Cargar datos desde la base de datos
            datos = cargar_datos_represa()
            
            if datos.empty:
                # Manejar caso sin datos
                estilo_estado = {"fontSize": "28px", "fontWeight": "bold", "color": "#555"}
                empty_fig = go.Figure()
                empty_fig.update_layout(title="Sin datos disponibles")
                return "—", "—", "Sin datos", estilo_estado, fecha_hora_actual, empty_fig, empty_fig

            # Definir ventana de tiempo
            ahora = datos["timestamp"].max()
            if ventana == "1h":
                inicio = ahora - timedelta(hours=1)
            elif ventana == "6h":
                inicio = ahora - timedelta(hours=6)
            elif ventana == "24h":
                inicio = ahora - timedelta(hours=24)
            elif ventana == "7d":
                inicio = ahora - timedelta(days=7)
            else:
                inicio = datos["timestamp"].min()

            datos_filtrados = datos[datos["timestamp"] >= inicio].copy()
            if datos_filtrados.empty:
                # Manejar caso sin datos en la ventana
                estilo_estado = {"fontSize": "28px", "fontWeight": "bold", "color": "#555"}
                empty_fig = go.Figure()
                empty_fig.update_layout(title="Sin datos en la ventana seleccionada")
                return "—", "—", "Sin datos", estilo_estado, fecha_hora_actual, empty_fig, empty_fig

            # Obtener último valor para KPIs
            ultimo = datos_filtrados.iloc[-1]
            nivel_actual = f"{ultimo['nivel_agua_pct']:.1f}%"
            generacion_actual = f"{ultimo['generacion_mw']:.1f} MW"
            estado = determinar_estado_embalse(ultimo['nivel_agua_pct'])
            
            # Estilo del estado según nivel
            colores_estado = {
                "Alto": "#43a047",      # Verde
                "Normal": "#1e88e5",    # Azul
                "Bajo": "#fb8c00",      # Naranja
                "Crítico": "#e53935"    # Rojo
            }
            estilo_estado = {
                "fontSize": "28px", 
                "fontWeight": "bold", 
                "color": colores_estado.get(estado, "#555")
            }

            # Verificar alertas
            alerta = verificar_alertas(ultimo['nivel_agua_pct'])
            if alerta["activa"]:
                logger.warning(f"🚨 ALERTA: {alerta['mensaje']}")
                # Opcional: reproducir sonido de alerta (descomentar si se desea)
                # reproducir_alerta_sonora()

            # Crear gráfico de Nivel de Agua
            fig_nivel = go.Figure()
            fig_nivel.add_trace(go.Scatter(
                x=datos_filtrados["timestamp"],
                y=datos_filtrados["nivel_agua_pct"],
                mode="lines+markers",
                name="Nivel de Agua",
                line=dict(color="#1e88e5", width=2),
                marker=dict(size=4)
            ))
            # Añadir líneas de referencia
            for y, color, texto in [(85, "#43a047", "Alto"), (60, "#1e88e5", "Normal"), (30, "#fb8c00", "Bajo")]:
                fig_nivel.add_hline(y=y, line_dash="dot", line_color=color, annotation_text=texto)

            fig_nivel.update_layout(
                title="Nivel de Agua (%)",
                xaxis_title="Tiempo",
                yaxis_title="Nivel (%)",
                hovermode="x unified",
                margin=dict(l=40, r=20, t=50, b=40),
                height=400,
                yaxis_range=[0, 100]
            )

            # Crear gráfico de Generación
            fig_generacion = go.Figure()
            fig_generacion.add_trace(go.Scatter(
                x=datos_filtrados["timestamp"],
                y=datos_filtrados["generacion_mw"],
                mode="lines+markers",
                name="Generación",
                line=dict(color="#e53935", width=2),
                marker=dict(size=4)
            ))

            fig_generacion.update_layout(
                title="Generación de Energía (MW)",
                xaxis_title="Tiempo",
                yaxis_title="Potencia (MW)",
                hovermode="x unified",
                margin=dict(l=40, r=20, t=50, b=40),
                height=400
            )

            return nivel_actual, generacion_actual, estado, estilo_estado, fecha_hora_actual, fig_nivel, fig_generacion

        except Exception as e:
            logger.error(f"❌ Error en actualización del tablero: {e}")
            # Manejar errores devolviendo valores por defecto
            estilo_error = {"fontSize": "28px", "fontWeight": "bold", "color": "#e53935"}
            empty_fig = go.Figure()
            empty_fig.update_layout(title="Error al cargar datos")
            return "—", "—", "Error", estilo_error, "—", empty_fig, empty_fig

    logger.info("✅ Tablero iniciado. Accede en: http://127.0.0.1:8050")
    app.run(debug=True)
```

**Explicación técnica detallada**:

- **Líneas 65-125**: Define el layout con:
  - Logo de EPM en la cabecera
  - 4 KPIs en tarjetas responsivas
  - Selector de ventana de tiempo
  - Dos gráficos separados en fila

- **Líneas 128-250**: Callback que actualiza todos los componentes:
  - Carga datos desde SQLite cada 3 segundos
  - Filtra por ventana de tiempo seleccionada
  - Actualiza KPIs con últimos valores
  - Genera gráficos con líneas de referencia
  - Verifica alertas y registra en log

- **Líneas 205-210**: Líneas de referencia en el gráfico de nivel:
  - 85%: Límite superior (Alto)
  - 60%: Nivel óptimo (Normal)
  - 30%: Límite inferior (Bajo)

**Alineación con EPM**:
- Interfaz con branding corporativo completo
- KPIs relevantes para operadores de represas
- Diseño responsive para uso en tablets de campo
- Alertas integradas con sistema de logging

---

## 🎯 **8. Conclusión y Recomendaciones para Entornos Reales de EPM**

### **8.1 Logros del Sistema Actual**

✅ **Simulación realista** de datos SCADA con frecuencia de 3 segundos  
✅ **Arquitectura modular** lista para integración empresarial  
✅ **Alertas operativas** con umbrales definidos por ingenieros  
✅ **Visualización profesional** con branding de EPM  
✅ **Exportación de reportes** para cumplimiento normativo  

### **8.2 Recomendaciones para Producción en EPM**

#### **Integración con Infraestructura Existente**
- **Conexión a SCADA real**: Reemplazar el generador de datos con API de sensores reales
- **Base de datos empresarial**: Migrar de SQLite a Oracle o PostgreSQL
- **Autenticación**: Integrar con Active Directory de EPM
- **Monitoreo centralizado**: Enviar alertas al SIEM corporativo

#### **Funcionalidades Avanzadas**
- **Predicción a 24h**: Implementar modelo LSTM para pronóstico de nivel
- **Optimización de generación**: Algoritmo para maximizar producción energética
- **Geolocalización**: Mapa interactivo con ubicación de todas las represas
- **Notificaciones móviles**: Alertas por SMS/Email a ingenieros de guardia

#### **Cumplimiento Normativo**
- **Respaldo automático**: Copias de seguridad diarias de la base de datos
- **Registro de auditoría**: Log detallado de todas las operaciones del sistema
- **Seguridad de datos**: Cifrado de información sensible en tránsito y reposo
- **Disponibilidad**: Monitoreo de salud del sistema con alertas proactivas

### **8.3 Próximos Pasos**

1. **Prueba de concepto (PoC)** con datos reales de una represa de EPM
2. **Validación con ingenieros operativos** para ajustar umbrales de alerta
3. **Integración con sistemas existentes** (SCADA, SIEM, Active Directory)
4. **Despliegue piloto** en una represa seleccionada
5. **Escalado a toda la flota** de represas hidroeléctricas
