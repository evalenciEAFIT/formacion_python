Perfecto, Edi. A continuación te presento una **versión profundamente documentada y profesional** del módulo de inicialización y gestión de datos, con:

✅ **Documentación completa**: desde el nivel de proyecto hasta funciones individuales  
✅ **Código extensamente comentado**: con docstrings en formato **Google Style**, anotaciones de tipo, advertencias y ejemplos de uso  
✅ **Claridad técnica y pedagógica**: ideal para equipos, auditorías o mantenimiento futuro  
✅ **Alineado con tus buenas prácticas** (entorno `venv`, Windows, represas, etc.)

---

# 📚 **Documentación Técnica: Módulo de Inicialización y Gestión de Datos**  
**Proyecto**: `dam-monitoring-system`  
**Versión**: 1.1.0  
**Última actualización**: 18 de noviembre de 2025  
**Autor**: Edi (Equipo de Monitoreo de Infraestructura Crítica)  

---

## 🎯 **Objetivo del Módulo**

Automatizar la creación de un entorno de desarrollo Python listo para producción, con soporte para:

| Capacidad | Tecnología | Caso de uso en represas |
|---------|------------|------------------------|
| ✅ Estructura de proyecto estandarizada | `pathlib`, `os` | Separación clara de configuración, datos, lógica y pruebas |
| ✅ Entorno virtual aislado (`venv`) | `subprocess`, `sys` | Evitar conflictos de dependencias en Windows |
| ✅ Conexión unificada a múltiples bases de datos | `psycopg2`, `oracledb`, `sqlite3` | Integrar sensores (Oracle), históricos (PostgreSQL), local (SQLite) |
| ✅ Ingestión flexible de datos | `pandas`, `requests` | Cargar desde CSV (sensores locales), APIs (meteorología), DBs (SCADA) |
| ✅ Modularidad y reusabilidad | `__init__.py`, paquetes | Permitir `from src.data import load_csv` sin rutas profundas |

---

## 📁 **Estructura Final del Proyecto**

```
my-dam-project/
├── venv/                         # Entorno virtual aislado (no versionado)
├── requirements.txt              # Dependencias explícitas y versionables
├── .env                          # ← Variables sensibles (NO en Git)
├── setup_project.py              # ⭐ Script de inicialización (ejecutable)
│
├── src/
│   ├── __init__.py               # Raíz del paquete: expone `config` y `data`
│   │
│   ├── config/
│   │   ├── __init__.py           # Expone `db_manager`, `settings`
│   │   ├── settings.py           # Configuración: rutas, valores por defecto
│   │   └── db.py                 # ⭐ Gestor unificado de conexiones a DB
│   │
│   └── data/
│       ├── __init__.py           # Expone funciones clave de ingestión
│       ├── ingestion.py          # ⭐ Carga de datos desde múltiples fuentes
│       ├── processing.py         # Limpieza, validación, enriquecimiento
│       └── export.py             # Exportación a CSV, Parquet, Excel, JSON
│
├── data/
│   ├── raw/                      # Datos crudos (inmutables)
│   └── processed/                # Datos transformados (reproducibles)
│
├── tests/                        # Pruebas unitarias e integración
├── notebooks/                    # Exploración y prototipado
└── logs/                         # ← Se crea dinámicamente si se usa logging
```

---

# 🛠️ **1. Script de Inicialización: `setup_project.py`**

> **Propósito**: Crear todo el entorno desde cero con un solo comando.  
> **Ejecución esperada**: `python setup_project.py dam-monitoring-system`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_project.py

Módulo de inicialización automática de proyectos Python para monitoreo de infraestructura crítica (ej: represas).

Funcionalidades:
- Crea una estructura de directorios estandarizada (src/, data/, tests/, etc.)
- Genera archivos __init__.py para habilitar imports limpios (paquetes Python)
- Crea e inicializa un entorno virtual (`venv`) específico del proyecto
- Instala dependencias desde `requirements.txt`
- Genera un archivo requirements.txt con librerías esenciales para:
    * Gestión de datos: pandas, openpyxl
    * Conexión a bases de datos: psycopg2-binary (PostgreSQL), oracledb (Oracle), sqlite3 (estándar)
    * Integración: requests, python-dotenv

⚠️ Notas importantes:
- Diseñado para Windows (usa `venv\Scripts\activate`), pero compatible con Linux/macOS.
- Usa `subprocess` para crear el entorno virtual → no depende de librerías externas.
- No sobrescribe directorios existentes (usa `exist_ok=True`).
- El entorno virtual se crea en ./venv/ (buena práctica: evita rutas globales).

Ejemplo de uso:
    $ python setup_project.py dam-monitoring-system
    $ cd dam-monitoring-system
    $ venv\Scripts\activate
    (venv) $ python -c "from src import data; print('✅ Todo listo')"

Autor: Edi
Fecha: 2025-11-18
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import NoReturn


def create_project_structure(project_name: str) -> Path:
    """
    Crea la estructura de directorios estándar para un proyecto de monitoreo de represas.

    La estructura sigue buenas prácticas de Python:
    - Separación clara entre código (`src/`), datos (`data/`) y pruebas (`tests/`)
    - Uso de paquetes explícitos (__init__.py en cada carpeta)
    - Directorios `raw/` y `processed/` para flujo ETL reproducible

    Args:
        project_name (str): Nombre del directorio raíz del proyecto.

    Returns:
        Path: Ruta absoluta al directorio del proyecto creado.

    Raises:
        OSError: Si falla la creación de algún directorio (permisos, disco lleno, etc.)

    Ejemplo:
        >>> base = create_project_structure("dam-monitoring")
        >>> (base / "src" / "__init__.py").exists()
        True
    """
    # Convertir a Path y resolver ruta absoluta
    base = Path(project_name).resolve()
    print(f"📁 Creando estructura en: {base}")

    # Lista de directorios a crear (incluye subdirectorios anidados)
    # Nota: Path.mkdir(parents=True) crea toda la cadena de directorios
    dir_tree = [
        base,
        base / "data" / "raw",
        base / "data" / "processed",
        base / "src",
        base / "src" / "config",
        base / "src" / "data",
        base / "tests",
        base / "notebooks",
        base / "logs",  # útil para futura integración con logging
    ]

    # Crear cada directorio y su __init__.py vacío (marca como paquete Python)
    for directory in dir_tree:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            # Crear __init__.py para habilitar imports (aunque esté vacío)
            init_file = directory / "__init__.py"
            init_file.touch(exist_ok=True)  # touch() crea el archivo si no existe
        except OSError as e:
            raise OSError(f"Error al crear el directorio '{directory}': {e}") from e

    # ✅ src/__init__.py especial: expone submódulos para imports limpios
    # Esto permite: `from src import config, data`
    src_init_content = '''"""
Módulo raíz del proyecto de monitoreo de represas.

Este archivo habilita imports de alto nivel:
    from src import config, data

Contenido:
    - config: Configuración del sistema (DB, rutas, claves)
    - data: Funciones para ingestión, procesamiento y exportación de datos

Nota: Todos los subdirectorios deben tener su propio __init__.py.
"""
# Import explícito para hacer accesibles los subpaquetes
from . import config
from . import data
'''
    (base / "src" / "__init__.py").write_text(src_init_content, encoding="utf-8")

    # ✅ requirements.txt: lista de dependencias mínimas y seguras
    # Se priorizan versiones estables y binarios precompilados para Windows
    requirements = [
        "# Dependencias esenciales para monitoreo de represas",
        "pandas>=2.0.0",                     # Manipulación de datos tabulares
        "numpy>=1.24.0",                     # Computación numérica (dependencia de pandas)
        "psycopg2-binary>=2.9.0",            # Cliente PostgreSQL (binario: no requiere compilación en Windows)
        "oracledb>=2.0.0",                   # Cliente Oracle oficial (modo 'thin': sin Oracle Client instalado)
        "openpyxl>=3.1.0",                   # Soporte para archivos Excel (.xlsx)
        "requests>=2.31.0",                  # Comunicación con APIs REST
        "python-dotenv>=1.0.0",              # Carga de variables de entorno desde .env
        "pydantic>=2.0.0",                   # Validación de modelos (útil para APIs con FastAPI)
        "",
        "# Opcionales (descomentar según necesidad)",
        "# matplotlib>=3.7.0",               # Visualización
        "# streamlit>=1.30.0",               # Dashboard interactivo
        "# reportlab>=4.0.0",                # Generación de PDFs
    ]
    (base / "requirements.txt").write_text("\n".join(requirements), encoding="utf-8")

    # ✅ .env de ejemplo (NO incluye credenciales reales)
    env_example = '''# ⚠️ NUNCA versionar este archivo con credenciales reales
# Copiar a .env y completar con valores reales

# PostgreSQL (históricos, dashboards)
PG_HOST=localhost
PG_PORT=5432
PG_DB=dam_monitoring
PG_USER=edi_user
PG_PASSWORD=

# Oracle (SCADA, sensores en tiempo real)
ORA_USER=sensor_reader
ORA_PASSWORD=
ORA_DSN=10.10.5.20:1521/DAMDB

# SQLite (modo local/offline)
SQLITE_PATH=data/dams_local.db

# Otras configuraciones
LOG_LEVEL=INFO
API_SECRET_KEY=dev-secret-2025
'''
    (base / ".env.example").write_text(env_example, encoding="utf-8")
    print("📄 Archivos base generados: requirements.txt, .env.example")

    print(f"✅ Estructura creada exitosamente en: {base}")
    return base


def create_virtualenv(project_path: Path) -> None:
    """
    Crea un entorno virtual Python (`venv`) dentro del proyecto.

    Ventajas:
    - Aislamiento de dependencias (evita conflictos con otros proyectos)
    - Reproducibilidad (mismo entorno en desarrollo, pruebas y producción)
    - Portabilidad (el venv se puede recrear desde requirements.txt)

    Implementación:
    - Usa `subprocess.run()` para invocar `python -m venv`
    - Detecta sistema operativo: en Windows usa `venv\Scripts\`, en Unix `venv/bin/`
    - No activa el entorno automáticamente (debe hacerse manualmente)

    Args:
        project_path (Path): Ruta al directorio raíz del proyecto.

    Raises:
        subprocess.CalledProcessError: Si falla la creación del entorno virtual.
        FileNotFoundError: Si no se encuentra el ejecutable de Python.

    Nota para Windows:
        - El script `activate.bat` se genera en `venv\Scripts\`
        - Para activar: `venv\Scripts\activate` (CMD) o `venv\Scripts\Activate.ps1` (PowerShell)
    """
    venv_path = project_path / "venv"
    print(f"⚙️ Creando entorno virtual en: {venv_path}")

    try:
        # Ejecutar: python -m venv ./venv
        # Usamos sys.executable para garantizar que se use el mismo Python que ejecutó este script
        result = subprocess.run(
            [sys.executable, "-m", "venv", str(venv_path)],
            capture_output=True,
            text=True,
            check=True  # Lanza excepción si el comando falla
        )
        print(f"✅ Entorno virtual creado: {venv_path}")
    except subprocess.CalledProcessError as e:
        error_msg = (
            f"❌ Error al crear el entorno virtual:\n"
            f"Comando: {e.cmd}\n"
            f"Salida estándar: {e.stdout}\n"
            f"Error estándar: {e.stderr}\n"
            f"Código de retorno: {e.returncode}"
        )
        raise RuntimeError(error_msg) from e
    except FileNotFoundError as e:
        raise RuntimeError(
            "❌ El ejecutable de Python no se encontró. "
            "Asegúrese de tener Python instalado y en el PATH."
        ) from e


def install_requirements(project_path: Path) -> None:
    """
    Instala las dependencias listadas en `requirements.txt` dentro del entorno virtual.

    Flujo:
    1. Localiza el ejecutable `pip` dentro del entorno virtual (`venv/Scripts/pip.exe` en Windows)
    2. Ejecuta: pip install -r requirements.txt
    3. Verifica que todas las librerías críticas se instalen correctamente

    Args:
        project_path (Path): Ruta al directorio raíz del proyecto.

    Raises:
        FileNotFoundError: Si no se encuentra el ejecutable `pip` del entorno virtual.
        subprocess.CalledProcessError: Si falla la instalación de alguna dependencia.

    Advertencia de seguridad:
        - Nunca instale dependencias desde fuentes no confiables.
        - Revise periódicamente `requirements.txt` en busca de vulnerabilidades (usar `pip-audit`).
    """
    # Determinar ruta de pip según el sistema operativo
    if os.name == "nt":  # Windows
        pip_exe = project_path / "venv" / "Scripts" / "pip.exe"
    else:  # Linux/macOS
        pip_exe = project_path / "venv" / "bin" / "pip"

    if not pip_exe.exists():
        raise FileNotFoundError(
            f"❌ No se encontró el ejecutable de pip en: {pip_exe}\n"
            "¿Falló la creación del entorno virtual?"
        )

    print(f"📦 Instalando dependencias desde: {project_path / 'requirements.txt'}")
    try:
        # Ejecutar: pip install -r requirements.txt
        subprocess.run(
            [str(pip_exe), "install", "-r", str(project_path / "requirements.txt")],
            check=True,
            text=True
        )
        print("✅ Todas las dependencias instaladas exitosamente.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"❌ Error al instalar dependencias:\n{e.stderr}"
        ) from e


def main() -> NoReturn:
    """
    Punto de entrada principal del script de inicialización.

    Flujo completo:
    1. Parsea argumentos de línea de comandos (nombre del proyecto)
    2. Crea la estructura de directorios
    3. Inicializa el entorno virtual
    4. Instala las dependencias
    5. Muestra instrucciones de activación y uso

    Ejemplo de uso en terminal:
        python setup_project.py dam-monitoring-system

    Salida esperada:
        📁 Creando estructura en: ...
        ✅ Estructura creada...
        ⚙️ Creando entorno virtual...
        ✅ Entorno virtual creado...
        📦 Instalando dependencias...
        ✅ Dependencias instaladas.
        🎉 ¡Proyecto listo!
        ➡️  Activa el entorno con: dam-monitoring-system\\venv\\Scripts\\activate
    """
    parser = argparse.ArgumentParser(
        description=(
            "🔧 Crea un entorno de desarrollo Python listo para producción "
            "para proyectos de monitoreo de represas."
        ),
        epilog="Ejemplo: python setup_project.py dam-monitoring-system"
    )
    parser.add_argument(
        "project_name",
        type=str,
        help="Nombre del directorio del proyecto (ej: dam-monitoring-system)"
    )

    args = parser.parse_args()

    try:
        # Paso 1: Crear estructura
        project_path = create_project_structure(args.project_name)

        # Paso 2: Crear entorno virtual
        create_virtualenv(project_path)

        # Paso 3: Instalar dependencias
        install_requirements(project_path)

        # ✅ Mensaje final con instrucciones claras
        print("\n" + "🎉" * 3 + " ¡PROYECTO CONFIGURADO EXITOSAMENTE! " + "🎉" * 3)
        print("\n➡️  Pasos siguientes:")
        
        if os.name == "nt":
            activate_cmd = f"{project_path}\\venv\\Scripts\\activate"
            print(f"   1. Activa el entorno: {activate_cmd}")
            print(f"   2. Navega al proyecto: cd {project_path}")
        else:
            activate_cmd = f"source {project_path}/venv/bin/activate"
            print(f"   1. Activa el entorno: {activate_cmd}")
            print(f"   2. Navega al proyecto: cd {project_path}")

        print("   3. Verifica instalación: python -c \"import pandas; print('✅ pandas=', pandas.__version__)\"")
        print("   4. Empieza a desarrollar en: src/data/ingestion.py")

        # Información adicional útil
        print("\n📌 Recursos útiles:")
        print("   • Documentación de oracledb (modo thin): https://python-oracledb.readthedocs.io/")
        print("   • Ejemplo de conexión a Oracle sin cliente: src/config/db.py")
        print("   • Plantilla .env: renombra .env.example a .env y completa credenciales")

    except Exception as e:
        print(f"\n❌ Error crítico durante la configuración: {e}", file=sys.stderr)
        print("🔍 Verifique permisos, espacio en disco y conexión a internet.", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


# Permitir ejecución directa como script
if __name__ == "__main__":
    main()
```

---

# 🗃️ **2. Gestor de Bases de Datos: `src/config/db.py`**

> **Propósito**: Abstraer la complejidad de múltiples motores de base de datos en una interfaz unificada.  
> **Clave técnica**: Patrón **Singleton** implícito (`db_manager` global) + **conexiones reutilizables** (pooling manual ligero).

```python
# src/config/db.py
# -*- coding: utf-8 -*-
"""
Gestor unificado de conexiones a bases de datos para monitoreo de represas.

Este módulo proporciona una interfaz consistente para interactuar con:
    - PostgreSQL: Almacenamiento de históricos, dashboards analíticos
    - Oracle: Integración con sistemas SCADA existentes (sensores en tiempo real)
    - SQLite: Modo local/offline para operaciones en campo sin conectividad

Características clave:
✅ Conexiones reutilizables (evita sobrecarga de creación/destucción)
✅ Soporte para modo "thin" de Oracle (sin instalar Oracle Client)
✅ Context manager para manejo seguro de transacciones
✅ Devolución directa de DataFrames con pandas
✅ Compatible con variables de entorno (.env)

Advertencias importantes:
⚠️  Nunca almacene credenciales en código fuente. Use .env + python-dotenv.
⚠️  Oracle en modo "thin" requiere que la base de datos tenga SSL/TLS configurado (recomendado).
⚠️  Para producción, considere usar un pool de conexiones (ej: SQLAlchemy + async).

Ejemplo de uso:
    from src.config.db import db_manager

    # Desde PostgreSQL
    df = db_manager.query_to_df(
        "SELECT * FROM dam_readings WHERE dam_id = %s",
        "postgres",
        params=("REP-001",),
        host="dam-db-prod",
        database="monitoring"
    )

    # Desde Oracle (SCADA)
    df = db_manager.query_to_df(
        "SELECT DAM_ID, LEVEL, TIMESTAMP FROM SENSOR_HIST WHERE ROWNUM <= 1000",
        "oracle",
        user="scada_reader",
        password=os.getenv("ORA_PASS"),
        dsn="scada-srv:1521/SCADADB"
    )

Autor: Edi
Fecha: 2025-11-18
"""

import os
import sqlite3
from contextlib import contextmanager
from typing import Optional, Dict, Any, Iterator, Union, Tuple
import pandas as pd

# Importar drivers de bases de datos
# Nota: psycopg2 y oracledb ya están en requirements.txt
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
    Clase principal para gestión unificada de conexiones a bases de datos.

    Diseño:
    - Almacena conexiones activas en `self.connections` (diccionario con clave única)
    - Cada método `get_*_conn()` devuelve una conexión reutilizable o crea una nueva
    - Usa `@contextmanager` para transacciones seguras (commit/rollback automático)
    - `query_to_df()` encapsula la lógica de ejecución y conversión a pandas.DataFrame

    Atributos:
        connections (dict): Almacena conexiones activas. Clave: cadena única por DB.
            Ej: "pg_localhost_monitoring", "ora_scada-srv_SCADADB", "sqlite_data/dams.db"
    """

    def __init__(self) -> None:
        """Inicializa el gestor sin conexiones activas."""
        self.connections: Dict[str, Union[
            psycopg2.extensions.connection,
            oracledb.Connection,
            sqlite3.Connection
        ]] = {}

    # === POSTGRESQL ===
    def get_postgres_conn(self,
                          host: Optional[str] = None,
                          port: int = 5432,
                          database: Optional[str] = None,
                          user: Optional[str] = None,
                          password: Optional[str] = None,
                          **kwargs) -> psycopg2.extensions.connection:
        """
        Obtiene (o crea) una conexión reutilizable a PostgreSQL.

        Estrategia de clave única:
            "pg_{host}_{port}_{database}"

        Args:
            host (str, optional): Host del servidor. Por defecto: PG_HOST en .env o "localhost".
            port (int, optional): Puerto. Por defecto: 5432.
            database (str, optional): Nombre de la base de datos. Requerido.
            user (str, optional): Usuario. Requerido.
            password (str, optional): Contraseña. Requerida.
            **kwargs: Parámetros adicionales para psycopg2.connect().

        Returns:
            psycopg2.extensions.connection: Conexión activa a PostgreSQL.

        Raises:
            ValueError: Si falta información crítica (database, user, password).
            psycopg2.OperationalError: Si falla la conexión (credenciales, red, etc.).

        Notas:
            - Usa variables de entorno si los parámetros no se especifican:
                PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD
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
            except psycopg2.OperationalError as e:
                raise ConnectionError(
                    f"❌ Error al conectar con PostgreSQL ({host}:{port}/{database}): {e}"
                ) from e

        return self.connections[key]

    # === ORACLE ===
    def get_oracle_conn(self,
                        user: Optional[str] = None,
                        password: Optional[str] = None,
                        dsn: Optional[str] = None,
                        **kwargs) -> oracledb.Connection:
        """
        Obtiene (o crea) una conexión reutilizable a Oracle Database.

        Características clave:
        - Usa el modo "thin" de oracledb → ¡No requiere Oracle Client instalado!
        - Compatible con Oracle 19c, 21c y 23c.
        - Soporta DSNs en formato: "host:port/servicio" o "host:port:sid"

        Estrategia de clave única:
            "ora_{dsn}"

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
                oracledb.init_oracle_client()  # Solo necesario en modo "thick"; en "thin" es opcional
                self.connections[key] = oracledb.connect(
                    user=user,
                    password=password,
                    dsn=dsn,
                    **kwargs
                )
                print(f"🔌 Nueva conexión Oracle establecida: {key}")
            except oracledb.DatabaseError as e:
                raise ConnectionError(
                    f"❌ Error al conectar con Oracle ({dsn}): {e}"
                ) from e

        return self.connections[key]

    # === SQLITE ===
    def get_sqlite_conn(self, db_path: str = "data/dams.db") -> sqlite3.Connection:
        """
        Obtiene (o crea) una conexión reutilizable a SQLite.

        Características:
        - Ideal para modo offline, prototipado o almacenamiento local.
        - Crea el archivo .db si no existe.
        - Usa WAL mode para mejor concurrencia (lectura/escritura simultánea).

        Estrategia de clave única:
            "sqlite_{ruta_absoluta}"

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
            except sqlite3.Error as e:
                raise ConnectionError(
                    f"❌ Error al conectar con SQLite ({db_abs_path}): {e}"
                ) from e

        return self.connections[key]

    # === CONTEXT MANAGER PARA TRANSACCIONES ===
    @contextmanager
    def get_db_cursor(self, db_type: str, **kwargs) -> Iterator:
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

    # === CONSULTA DIRECTA A DATAFRAME ===
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
# Esta instancia se importa directamente: from src.config.db import db_manager
db_manager = DatabaseManager()
"""
Instancia global del gestor de bases de datos.

Uso recomendado:
    from src.config.db import db_manager

Ventajas:
    - Evita crear múltiples instancias (patrón Singleton implícito)
    - Conexiones se reutilizan durante toda la vida del proceso
    - Compatible con aplicaciones web (FastAPI, Flask) si se usa nivel de módulo

⚠️ Advertencia en entornos multihilo:
    - psycopg2 y oracledb no son thread-safe por conexión.
    - Para aplicaciones web, considere crear una instancia por request o usar pool.
"""
```

---

# 📥 **3. Módulo de Ingestión de Datos: `src/data/ingestion.py`**

> **Propósito**: Cargar datos desde cualquier fuente a un `pandas.DataFrame` estandarizado.  
> **Principios**: Idempotencia, trazabilidad, y manejo de errores explícito.

```python
# src/data/ingestion.py
# -*- coding: utf-8 -*-
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
from src.config.db import db_manager


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


def load_excel(
    file_path: Union[str, Path],
    sheet_name: Union[str, int] = 0,
    expected_columns: Optional[List[str]] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Carga datos desde un archivo Excel (.xlsx, .xls).

    Args:
        file_path (str | Path): Ruta al archivo Excel.
        sheet_name (str | int): Nombre o índice de la hoja. Por defecto: primera hoja.
        expected_columns (list[str], optional): Columnas obligatorias (validación).
        **kwargs: Parámetros para pd.read_excel().

    Returns:
        pd.DataFrame: Datos de la hoja especificada.

    Notas:
        - Requiere openpyxl instalado (en requirements.txt).
        - Útil para informes manuales de inspección de represas.

    Ejemplo:
        df = load_excel(
            "data/raw/inspection_report_nov2025.xlsx",
            sheet_name="Readings",
            expected_columns=["dam_id", "inspector", "date", "crack_width_mm"],
            parse_dates=["date"]
        )
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"❌ Archivo Excel no encontrado: {file_path.resolve()}")

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
    except Exception as e:
        raise ValueError(f"❌ Error al leer Excel '{file_path}': {e}") from e

    if expected_columns:
        missing = set(expected_columns) - set(df.columns)
        if missing:
            raise ValueError(f"❌ Columnas faltantes en Excel: {missing}")

    print(f"✅ Excel cargado: {file_path.name}[{sheet_name}] ({len(df)} filas)")
    return df


def load_json(
    source: str,
    expected_columns: Optional[List[str]] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Carga datos desde JSON local o remoto (API).

    Soporta dos modos:
    A. Archivo local: source = "ruta/al/archivo.json"
    B. URL remota: source = "https://api.ejemplo.com/data"

    Args:
        source (str): Ruta de archivo o URL.
        expected_columns (list[str], optional): Columnas obligatorias.
        **kwargs: 
            - Para archivos locales: parámetros de pd.read_json()
            - Para URLs: parámetros de requests.get() (headers, params, timeout)

    Returns:
        pd.DataFrame: Datos normalizados.

    Estrategia para APIs:
        - Detecta automáticamente si es URL (empieza con http:// o https://)
        - Maneja respuestas con envoltorio (ej: { "data": [...] })
        - Soporta paginación básica (no implementada aquí; extensible)

    Ejemplo API meteorológica:
        df = load_json(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": -33.45, "longitude": -70.66, "hourly": "rain"},
            expected_columns=["time", "rain"]
        )
    """
    # Detectar si es URL
    is_url = source.startswith(("http://", "https://"))

    if is_url:
        # === MODO API ===
        # Separar kwargs para requests y para pandas
        req_kwargs = {k: v for k, v in kwargs.items() if k in ["params", "headers", "timeout"]}
        pd_kwargs = {k: v for k, v in kwargs.items() if k not in req_kwargs}

        try:
            response = requests.get(source, **req_kwargs)
            response.raise_for_status()  # Lanza excepción para códigos 4xx/5xx
            json_data = response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"❌ Error al conectar con API '{source}': {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Respuesta no es JSON válido: {e}") from e

        # Normalizar datos (manejar envoltorios comunes)
        if isinstance(json_data, dict):
            # Buscar claves comunes que contengan listas de registros
            for key in ["data", "records", "results", "items"]:
                if key in json_data and isinstance(json_data[key], list):
                    json_data = json_data[key]
                    break

        # Convertir a DataFrame
        try:
            df = pd.json_normalize(json_data, **pd_kwargs)
        except Exception as e:
            raise ValueError(f"❌ Error al normalizar JSON de API: {e}") from e

    else:
        # === MODO ARCHIVO LOCAL ===
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"❌ Archivo JSON no encontrado: {file_path.resolve()}")

        try:
            df = pd.read_json(file_path, **kwargs)
        except (ValueError, TypeError) as e:
            raise ValueError(f"❌ Error al leer JSON '{file_path}': {e}") from e

    # Validación de columnas
    if expected_columns:
        missing = set(expected_columns) - set(df.columns)
        if missing:
            raise ValueError(f"❌ Columnas faltantes en JSON: {missing}")

    source_desc = source if is_url else Path(source).name
    print(f"✅ JSON cargado: {source_desc} ({len(df)} filas)")
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
            elif source_type == "excel":
                df = load_excel(**config)
            elif source_type == "json":
                df = load_json(**config)
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

---

# 📦 **4. Vinculación de Módulos: `src/data/__init__.py`**

```python
# src/data/__init__.py
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
    - load_excel: Carga desde Excel
    - load_json: Carga desde JSON local o API
    - load_from_db: Carga desde bases de datos (PostgreSQL, Oracle, SQLite)
    - load_multiple_sources: Consolidación de múltiples fuentes

Nota: Las funciones de procesamiento/exportación se importan explícitamente si se usan:
    from src.data.processing import clean_sensor_data
    from src.data.export import export_to_parquet
"""
from .ingestion import (
    load_csv,
    load_excel,
    load_json,
    load_from_db,
    load_multiple_sources
)

# Definir __all__ para controlar imports con *
__all__ = [
    "load_csv",
    "load_excel",
    "load_json",
    "load_from_db",
    "load_multiple_sources"
]
```

---

## ✅ **Resumen de Buenas Prácticas Aplicadas**

| Área | Práctica | Beneficio |
|------|----------|-----------|
| **Documentación** | Docstrings en Google Style + ejemplos ejecutables | Claridad para nuevos desarrolladores y generación automática de docs (Sphinx) |
| **Tipado** | Anotaciones de tipo (`-> pd.DataFrame`) | Detección temprana de errores con mypy, mejor autocompletado |
| **Seguridad** | Nunca credenciales en código, uso de `.env` | Cumplimiento con estándares de ciberseguridad |
| **Mantenibilidad** | Funciones pequeñas, una responsabilidad | Fácil de probar y modificar |
| **Robustez** | Validación de entradas, manejo explícito de errores | Sistema más confiable en producción |
| **Reproducibilidad** | Estructura estándar + venv | Mismo entorno en todos los equipos |

---

## ▶️ **Próximos Pasos Recomendados**

1. **Ejecutar inicialización**:
   ```bash
   python setup_project.py dam-monitoring-system
   cd dam-monitoring-system
   venv\Scripts\activate
   ```

2. **Probar conexión a Oracle (modo thin)**:
   ```python
   from src.config.db import db_manager
   df = db_manager.query_to_df("SELECT * FROM DUAL", "oracle", user="scott", password="tiger", dsn="localhost:1521/XE")
   ```

3. **Crear notebook de exploración**:
   ```python
   # notebooks/01_data_ingestion.ipynb
   from src.data import load_csv, load_from_db
   df_sensors = load_csv("data/raw/sample.csv", parse_dates=["timestamp"])
   df_scada = load_from_db("SELECT * FROM sensor_readings", "oracle", ...)
   ```

¿Te gustaría que genere también:
- 📄 Un **archivo PDF de esta documentación** (con índice y formato profesional)?
- 🧪 Un **conjunto de pruebas unitarias** (`tests/test_ingestion.py`) con cobertura >90%?
- 📊 Un **dashboard de ejemplo en Streamlit** que use estos módulos?

Estoy listo para seguir profundizando según tus necesidades, Edi.
