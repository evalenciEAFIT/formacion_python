# 📘 Guía Avanzada: **Módulos, Paquetes y `__init__.py` en Python**  
## *Con enfoque práctico para APIs profesionales (FastAPI, Flask, etc.)*  
> 🎯 Ideal para tu entorno: **Windows + `venv` + proyecto de monitoreo de represas con ML y base de datos**

---

## 🔍 ¿Qué es un **módulo**? ¿Y un **paquete**?

### ✅ Módulo  
Un archivo `.py` que contiene código reutilizable: funciones, clases, variables.  
Ejemplo:
```python
# tools/math_utils.py
def safe_divide(a, b):
    return a / b if b != 0 else 0.0
```
→ Es un **módulo** llamado `math_utils`.

### ✅ Paquete  
Una **carpeta** que contiene módulos y, crucialmente, un archivo **`__init__.py`**.  
Permite agrupar funcionalidad relacionada (como `db/`, `api/`, `ml/`).

Ejemplo:
```
ml/
├── __init__.py   ← ¡Esto hace a `ml/` un paquete!
├── inference.py
└── preprocessing/
    ├── __init__.py
    └── scaler.py
```
→ Puedes importar como: `from ml.inference import predict_maintenance_risk`

---

## 🧩 El rol de `__init__.py`: **El "contrato público" de tu paquete**

El archivo `__init__.py` tiene **tres funciones principales**, y no siempre deben estar todas juntas — depende del nivel de control que quieras.

| Función | ¿Qué hace? | ¿Es obligatorio? | Ejemplo de uso |
|--------|-------------|------------------|----------------|
| 1️⃣ **Marca la carpeta como paquete** | Sin él, Python no reconoce la carpeta como importable. | ✅ Sí (en Python < 3.3 *absolutamente*; en ≥3.3 funciona sin él, pero **no lo recomiendes** → rompe compatibilidad y buenas prácticas). | `import ml` → falla si `ml/__init__.py` no existe (en algunos entornos). |
| 2️⃣ **Define la interfaz pública** | Decides qué se expone cuando alguien hace `from ml import X`. | ⚠️ Opcional, pero **altamente recomendado** para APIs profesionales. | `from ml import predict_maintenance_risk` (sin saber que está en `inference.py`). |
| 3️⃣ **Ejecuta código de inicialización** | Carga modelos, configura logs, conecta a recursos externos. | ⚠️ Úsalo con cuidado → ¡evita efectos secundarios pesados! | Cargar modelo ML una sola vez al iniciar el paquete. |

---

## 📁 Ejemplo práctico: `ml/__init__.py` bien hecho

Veamos un caso realista para tu sistema de predicción de mantenimiento:

### 📄 `ml/__init__.py`
```python
"""
Módulo `ml`: Gestión de modelos predictivos para mantenimiento de represas.

Este archivo:
- Expone una interfaz limpia y estable.
- Carga el modelo una sola vez (al primer import).
- Evita que el usuario final sepa los detalles internos (encapsulamiento).

✅ Uso recomendado:
   from ml import predict_maintenance_risk

❌ Evitar:
   from ml.inference import _internal_predict_raw
"""

# 1. Importar funciones clave (las que queremos exponer públicamente)
from .inference import predict_maintenance_risk

# 2. Definir __all__ (opcional pero muy recomendado)
# Esto controla qué se importa con `from ml import *` (aunque no se debe usar `*` en producción)
__all__ = [
    "predict_maintenance_risk",
]

# 3. Inicialización ligera (¡nada de conexiones pesadas aquí!)
# Nota: El modelo se carga DENTRO de `predict_maintenance_risk` con "carga diferida",
# o mejor aún, en una variable de módulo en `inference.py` (ver más abajo).

# ✅ Buen patrón: carga perezosa + caché
# (Implementado en `inference.py`, no aquí → evita bloqueo al importar)
```

---

### 🔍 ¿Por qué no cargar el modelo directamente en `__init__.py`?

❌ **Malo** (bloquea y expone detalles):
```python
# ml/__init__.py — ❌ EVITAR
import joblib
model = joblib.load("models/maintenance_v2.joblib")  # ← Se ejecuta AL IMPORTAR ml/
def predict(data): return model.predict(data)
```
→ Problemas:
- Si el archivo no existe, **todo el sistema falla al iniciar**, incluso si no usas ML.
- Dificulta testing (mockear `model` es más complejo).
- Ralentiza el arranque del servidor.

✅ **Correcto** (carga una vez, con control):
```python
# ml/inference.py
import joblib
from pathlib import Path
from typing import Dict, Optional

# Cache del modelo: se carga SOLO la primera vez que se llama a `predict_maintenance_risk`
_model: Optional = None
_MODEL_PATH = Path(__file__).parent / "models" / "maintenance_risk_v2.joblib"

def _load_model():
    global _model
    if _model is None:
        _model = joblib.load(_MODEL_PATH)
    return _model

def predict_maintenance_risk(features: Dict[str, float]) -> float:
    model = _load_model()  # ← Carga diferida y única
    X = [[features["pressure"], features["vibration"], features["temp"]]]
    return float(model.predict_proba(X)[0][1])
```

→ Así, `import ml` es rápido, y el modelo solo se carga cuando realmente se necesita.

---

## 🧱 Ejemplo completo: `db/__init__.py` (con SQLAlchemy)

### 📄 `db/__init__.py`
```python
"""
Paquete `db`: Gestión de persistencia (lectura/escritura en base de datos).

Expone solo lo esencial para que otros módulos usen la DB sin conocer detalles internos.
"""

# 1. Re-exportar lo que otros paquetes necesitarán
from .session import get_db_session, engine, Base
from .models import Dam, SensorReading
from .repositories import DamRepository

# 2. Definir interfaz pública clara
__all__ = [
    "get_db_session",
    "engine",
    "Base",
    "Dam",
    "SensorReading",
    "DamRepository",
]

# 3. ¡Nada de crear tablas aquí! (eso va en scripts/migrations)
# Crear tablas en __init__.py es un antipatrón:
#   - Rompe testing (crea tablas en DB de prueba sin querer)
#   - Dificulta migraciones con Alembic
```

✅ Ahora, en `app/services/dam_service.py`, puedes escribir:
```python
from db import DamRepository, get_db_session  # ← Limpio y claro
```

En lugar de:
```python
from db.repositories.dam_repository import DamRepository  # ← largo y expone estructura interna
from db.session import get_db_session
```

---

## 🔄 Imports: Absolutos vs Relativos — ¿Cuál usar?

| Tipo | Sintaxis | Cuándo usar | Ejemplo |
|------|----------|-------------|---------|
| **Absoluto** | `from config.settings import settings` | ✅ **Recomendado en la mayoría de casos**.<br>→ Claridad total, no depende de ubicación del archivo.<br>→ Funciona igual en tests y scripts. | `from app.services.dam_service import get_dam_health_report` |
| **Relativo** | `from . import inference`<br>`from ..db import get_db_session` | ⚠️ Solo dentro de un paquete, para imports internos.<br>→ Útil en `__init__.py` para re-exportar.<br>→ Evita nombres largos, pero puede confundir. | En `ml/__init__.py`: `from .inference import predict_maintenance_risk` |

### ❌ Antipatrón común: imports circulares
```python
# app/services/dam_service.py
from db.models.dam import Dam

# db/models/dam.py
from app.services.dam_service import validate_dam_data  # ← ¡Ciclo!
```
→ **Solución**: mueve `validate_dam_data` a `app/utils/validators.py` (capa neutra).

---

## 🛠️ Checklist: Buenas prácticas con `__init__.py`

| ✅ Hacer | ❌ Evitar |
|---------|-----------|
| Usar `__all__` para definir la API pública | Dejar `__init__.py` vacío (oculta tu diseño intencional) |
| Solo importar y re-exportar (no lógica de negocio) | Ejecutar lógica pesada (cargar modelos, conectar a DB) |
| Mantener imports absolutos en capas superiores (`api/`, `app/`) | Usar imports relativos profundos (`from ....x import y`) |
| Documentar brevemente qué expone el paquete (docstring de `__init__.py`) | No documentar: "¿qué puedo importar de `ml/`?" → frustración en equipo |
| Usar `if __name__ == "__main__":` para scripts de prueba pequeños | Ejecutar código de producción en `__init__.py` |

---

## 🧪 Ejemplo de testing con `__init__.py` bien diseñado

Supón que quieres probar `dam_service.py`, pero **sin tocar la base de datos real**.

### 📄 `tests/unit/test_dam_service.py`
```python
from unittest.mock import patch
from app.services.dam_service import get_dam_health_report

@patch("app.services.dam_service.predict_maintenance_risk")
@patch("app.services.dam_service.DamRepository")
def test_high_risk_report(mock_repo, mock_predict):
    # Simular datos
    mock_dam = Mock(id=3, name="Represa Norte")
    mock_readings = [Mock(pressure=89, vibration=4.8), Mock(pressure=91, vibration=5.1)]
    
    mock_repo.return_value.get_by_id.return_value = mock_dam
    mock_repo.return_value.get_last_24h_readings.return_value = mock_readings
    mock_predict.return_value = 0.92

    # Llamar → gracias a la separación, no necesitas DB ni modelo real
    report = get_dam_health_report(3, db_session=None)

    assert report["risk_assessment"]["level"] == "high"
    assert "urgente" in report["risk_assessment"]["action"]
```

✅ ¿Por qué funciona?  
Porque `dam_service.py` **no importa directamente** `db.models` ni `ml.inference`, sino que usa:
- `from db import DamRepository`
- `from ml import predict_maintenance_risk`  
→ Y esos son *re-exportados* por los `__init__.py`, así que son fáciles de mockear.

---

## 📦 Bonus: Script para generar estructura base (Windows + venv)

Crea un archivo `setup_project.py` en tu raíz:

```python
# setup_project.py
import os

DIRECTORIES = [
    "config",
    "api",
    "api/routes",
    "app",
    "app/core",
    "app/services",
    "app/utils",
    "db",
    "db/models",
    "db/repositories",
    "ml",
    "ml/models",
    "ml/preprocessing",
    "tests",
    "tests/unit",
    "tests/integration",
    "scripts",
]

INIT_TEMPLATES = {
    "config/__init__.py": '"""Configuración centralizada del sistema."""\n',
    "api/__init__.py": '"""Capa de API: endpoints REST."""\n',
    "app/__init__.py": '"""Lógica de negocio: reglas del dominio (represas, mantenimiento)."""\n',
    "db/__init__.py": '"""Persistencia: acceso a datos (DB, archivos)."""\n',
    "ml/__init__.py": '"""Modelos predictivos para mantenimiento preventivo."""\nfrom .inference import predict_maintenance_risk\n__all__ = ["predict_maintenance_risk"]\n',
    "tests/__init__.py": '"""Tests automatizados."""\n',
}

def create_structure():
    for d in DIRECTORIES:
        os.makedirs(d, exist_ok=True)
        print(f"✓ Carpeta creada: {d}")
    
    for path, content in INIT_TEMPLATES.items():
        full_path = os.path.join(*path.split("/"))
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✓ {path} inicializado")

if __name__ == "__main__":
    create_structure()
    print("\n✅ Estructura base creada. Ahora activa tu venv y ejecuta:")
    print("   pip install -r requirements.txt")
    print("   uvicorn main:app --reload")
```

Ejecútalo con:
```powershell
venv\Scripts\python setup_project.py
```

---

## 🧭 ¿Qué más hay que considerar? (Lista de verificación profesional)

| Tema | Recomendación |
|------|---------------|
| **Versionado de API** | Usa `/api/v1/...` en rutas. En `api/__init__.py`, podrías tener `v1/`, `v2/` como subpaquetes. |
| **Dependencias explícitas** | Documenta en `requirements-dev.txt` y `requirements-prod.txt` (ej: `pytest` solo en dev). |
| **Tipado estático** | Usa `mypy` + anotaciones → detecta errores antes de ejecutar. Ej: `def predict(...) -> float:` |
| **Linting** | `ruff` o `flake8` + `pre-commit` para mantener estilo consistente. |
| **Documentación automática** | FastAPI genera `/docs` (Swagger) y `/redoc`. Añade docstrings en funciones de `api/routes/`. |
| **Entornos** | Usa `config/settings.py` con clases: `DevSettings`, `ProdSettings` que hereden de `BaseSettings`. |
| **Seguridad** | Nunca commits `.env`. Añade `.env` a `.gitignore`. Usa `python-dotenv` solo en desarrollo. |

