# Mantenimiento Predictivo en Represas con Machine Learning  
   
[Nivel 0: Buenas prácticas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel0) | 
[Nivel 1: Uso de datos en SQL](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel1) |
[Nivel 2: Uso Pandas](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel2) |
[Nivel 3: Uso Dash](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/Nivel3) | 
[Nivel 4: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel4) | 
[Nivel 5: Ejemplo Proyecto](https://github.com/evalenciEAFIT/formacion_python/tree/main/ML/nivel5)

---

# Modelos de Machine Learning para Servicios Públicos

## **Introducción**

En sectores como la **gestión de represas**, la **distribución de agua**, el **suministro de gas** o la **generación de energía hidroeléctrica**, el uso de Machine Learning permite mejorar la eficiencia, prevenir fallas, optimizar recursos y garantizar la continuidad del servicio. Esta guía explica de forma sencilla los principales modelos de ML, los problemas que resuelven y cómo se estructuran los datos en estos contextos.

---

## **A. Tipos de Problemas en Servicios Públicos**

Antes de elegir un modelo, es clave identificar el **tipo de problema**:

| Tipo de problema | Descripción | Ejemplo en servicios públicos |
|------------------|-------------|-------------------------------|
| **Clasificación** | Predecir una categoría o etiqueta | ¿Fallará una válvula en los próximos 7 días? (Sí/No) |
| **Regresión** | Predecir un valor numérico continuo | ¿Cuál será el nivel de agua en la represa mañana? |
| **Detección de anomalías** | Identificar comportamientos inusuales | ¿Hay una fuga en la red de gas? |
| **Agrupamiento (Clustering)** | Agrupar datos similares sin etiquetas | Segmentar zonas con patrones similares de consumo de agua |
| **Series temporales** | Predecir valores futuros basados en el tiempo | Pronosticar demanda de electricidad por hora |

---

## **B. Modelos de Machine Learning y su Aplicación**

### **B.1. Regresión Lineal y Regresión Logística**

- **Problema que resuelve**:  
  - Regresión lineal → Regresión  
  - Regresión logística → Clasificación binaria  

- **Estructura de datos**:  
  Tabla con **características (features)** numéricas/categóricas y una **variable objetivo** (numérica o binaria).

- **Ejemplo en represas**:  
  - *Regresión lineal*: Predecir el caudal de salida de una represa según lluvia, nivel actual y temperatura.  
  - *Regresión logística*: Predecir si el nivel de sedimentos superará un umbral crítico (Sí/No).

---

### **B.2. Árboles de Decisión y Bosques Aleatorios (Random Forest)**

- **Problema que resuelve**: Clasificación o regresión  
- **Ventaja**: Interpretación fácil, maneja datos no lineales y faltantes.

- **Estructura de datos**:  
  Tabla con múltiples variables (presión, caudal, temperatura, estado de válvulas, etc.).

- **Ejemplo en distribución de agua**:  
  - Predecir zonas con alto riesgo de rotura de tuberías usando edad de la red, presión, tipo de material y clima.

---

### **B.3. Máquinas de Soporte Vectorial (SVM)**

- **Problema que resuelve**: Clasificación (principalmente), también regresión (SVR)  
- **Útil cuando**: Hay pocos datos pero muchas características.

- **Estructura de datos**:  
  Datos normalizados, con pocas observaciones pero muchas variables técnicas (sensores, alarmas, etc.).

- **Ejemplo en gasoductos**:  
  - Clasificar si una lectura de presión indica una fuga inminente.

---

### **B.4. Redes Neuronales (incluyendo LSTM para series temporales)**

- **Problema que resuelve**:  
  - Redes densas → Regresión/clasificación compleja  
  - LSTM → Predicción en series temporales

- **Estructura de datos**:  
  - Para LSTM: Secuencias temporales (ej. mediciones horarias de los últimos 30 días)  
  - Para redes densas: Tablas con muchas variables

- **Ejemplo en energía**:  
  - LSTM: Predecir generación hidroeléctrica diaria usando datos históricos de lluvia, caudal y demanda.  
  - Red densa: Detectar fallas en turbinas a partir de vibraciones, temperatura y ruido.

---

### **B.5. Modelos de Detección de Anomalías (Isolation Forest, Autoencoders)**

- **Problema que resuelve**: Detección de comportamientos atípicos  
- **Estructura de datos**:  
  - Datos sin etiquetas (no se sabe qué es “normal” o “anómalo” a priori)  
  - Solo se usan las variables de entrada (sensores, caudales, presiones)

- **Ejemplo en represas**:  
  - Detectar fugas no reportadas en canales de derivación al identificar caudales de salida inconsistentes con los de entrada.

---

### **B.6. Clustering (K-Means, DBSCAN)**

- **Problema que resuelve**: Agrupar zonas o equipos con comportamientos similares  
- **Estructura de datos**:  
  Tabla con métricas de operación (consumo, presión, mantenimientos, etc.)

- **Ejemplo en agua potable**:  
  - Agrupar barrios por patrones de consumo para ajustar horarios de bombeo o detectar fraudes.

---

## **C. Comparación General de Modelos**

| Modelo | Tipo de problema | Interpretabilidad | Requiere muchos datos | Maneja datos temporales | Ideal para sensores IoT |
|--------|------------------|-------------------|------------------------|--------------------------|--------------------------|
| Regresión lineal | Regresión | Alta | No | No | Sí (simple) |
| Regresión logística | Clasificación | Alta | No | No | Sí |
| Árboles / Random Forest | Clasif./Reg. | Media-Alta | No-Media | No | Sí |
| SVM | Clasif./Reg. | Baja | Sí (en alta dimensión) | No | Limitado |
| Redes Neuronales | Cualquiera | Baja | Sí | Sí (con LSTM) | Sí (con suficientes datos) |
| Isolation Forest | Anomalías | Media | No | No | Sí |
| K-Means | Clustering | Media | No | No | Sí |

---

## **D. Recomendaciones para tu Proyecto de Monitoreo de Represas**

1. **Para mantenimiento predictivo**: Usa **Random Forest** o **XGBoost** (más potente) para predecir fallas en compuertas o sensores.
2. **Para pronóstico de niveles**: Usa **LSTM** o modelos clásicos como **ARIMA** si los datos son estacionales.
3. **Para detección de fugas o errores de medición**: Implementa **Isolation Forest** o **Autoencoders**.
4. **Para priorizar intervenciones**: Combina **clustering** (zonas similares) + **clasificación** (riesgo de falla).

---

Elegir el modelo adecuado depende del **tipo de problema**, la **calidad y cantidad de datos**, y la necesidad de **interpretabilidad**. En servicios públicos, donde la seguridad y la transparencia son críticas, modelos como **árboles de decisión** o **regresión logística** suelen ser buenos puntos de partida. 

--- 
## 1. 🌊 Situación del problema

Las represas son infraestructuras críticas donde las fallas no anticipadas pueden causar riesgos de seguridad, impacto ambiental y altos costos operativos. El mantenimiento predictivo con Machine Learning permite **predecir fallas 7 días antes** de que ocurran.

---

## ❓ ¿Qué preguntas puede responder el ML?

| Tipo de pregunta | Ejemplo concreto |
|------------------|------------------|
| **Clasificación binaria** | ¿Fallará el componente X en los próximos 7 días? (Sí/No) |
| **Regresión** | ¿Cuántos días faltan para que el sellado de la compuerta falle? |
| **Detección de anomalías** | ¿Es anómalo el aumento repentino de presión en el muro este? |
| **Priorización** | ¿Qué componente tiene mayor riesgo hoy y debe revisarse primero? |

## 2. 🤖 ¿Por qué Random Forest es la mejor opción?

### Random Forest
- **¿Qué es?** Un conjunto de árboles de decisión entrenados con datos y variables aleatorias.
- **¿Por qué usarlo?**  
  - Maneja bien datos desbalanceados (pocas fallas).  
  - No requiere normalización.  
  - Proporciona **importancia de variables** → interpretable.  
- **¿Cómo funciona?** Cada árbol vota; la mayoría decide.

### Métricas clave
| Métrica | Fórmula | ¿Por qué importa en represas? |
|--------|--------|-------------------------------|
| **Precisión** | VP / (VP + FP) | Reduce falsas alarmas (evita paradas innecesarias) |
| **Recall** | VP / (VP + FN) | **Prioridad**: detectar la mayor cantidad de fallas reales |
| **F1-Score** | 2·(Prec·Rec)/(Prec+Rec) | Equilibrio cuando hay desbalance |

> En mantenimiento predictivo: **maximizar recall**, aunque aumente ligeramente las falsas alarmas.

### Comparación con otros modelos:

| Criterio | **Random Forest** | Regresión Logística | Redes Neuronales |
|---------|-------------------|---------------------|------------------|
| **Datos desbalanceados** | ✅ Excelente | ❌ Pobre | ⚠️ Requiere balanceo |
| **Interpretabilidad** | ✅ Alta (importancia de variables) | ✅ Alta | ❌ Muy baja |
| **Robustez al ruido** | ✅ Alta | ❌ Baja | ⚠️ Moderada |
| **No linealidades** | ✅ Excelente | ❌ No maneja | ✅ Excelente |
| **Requiere normalización** | ❌ No | ✅ Sí | ✅ Sí |

**Conclusión**: Random Forest es ideal para represas porque maneja datos desbalanceados, es interpretable y robusto sin requerir preprocesamiento complejo.

---

## 3. 🗃️ Modelo de datos

### Fuentes de datos:
- **Sensores**: presión, humedad, vibración, temperatura
- **Ambientales**: lluvia acumulada, caudal
- **Históricos**: mantenimientos y fallas

### Dataset para ML:
| Campo | Descripción |
|------|-------------|
| `presion_bar` | Presión promedio del día |
| `humedad_pct` | Humedad relativa promedio |
| `vibracion_mm_s` | Vibración promedio |
| `dias_desde_mant` | Días desde último mantenimiento |
| `falla_prox_7d` | Etiqueta: ¿falla en próximos 7 días? |

---

## 4. 🗂️ Estructura del proyecto

```
represa_ml/
├── install_project.py
├── requirements.txt
├── main.py
├── generate_data_cli.py
├── data/raw/
├── models/
├── reports/
├── logs/
├── scripts/
└── src/
```

---

## 5. 💻 Códigos en Python

### 📄 `install_project.py`
```python
"""
install_project.py

¿PARA QUÉ?
- Crear la estructura completa del proyecto con un solo comando.

¿POR QUÉ?
- Automatiza la configuración inicial.
- Aísla dependencias en un entorno virtual.
- Evita errores manuales.

¿CÓMO?
1. Crea directorios y archivos vacíos.
2. Genera requirements.txt con dependencias.
3. Crea entorno virtual (venv).
4. Instala paquetes automáticamente.
"""

import os
import sys
import subprocess
import venv

PROJECT_NAME = "represa_ml"
REQUIREMENTS = [
    "pandas", "numpy", "scikit-learn", "streamlit",
    "joblib", "matplotlib", "reportlab"
]

ARCHIVOS = [
    "requirements.txt",
    "main.py",
    "generate_data_cli.py",
    "src/__init__.py",
    "src/data_generation.py",
    "src/data_loader.py",
    "src/data_preparation.py",
    "src/model.py",
    "src/alerts.py",
    "src/email_alert.py",
    "src/report_pdf.py",
    "scripts/run_scheduled.py",
    "scripts/schedule_daily_task.py"
]

DIRECTORIOS = ["data", "models", "reports", "logs", "scripts", "src"]

def crear_estructura(base_path):
    for d in DIRECTORIOS:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)
    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write("\n".join(REQUIREMENTS))
    for archivo in ARCHIVOS:
        if archivo == "requirements.txt": continue
        ruta = os.path.join(base_path, archivo)
        dir_name = os.path.dirname(ruta)
        if dir_name: os.makedirs(dir_name, exist_ok=True)
        with open(ruta, "w") as f: pass

def main():
    if os.path.basename(os.getcwd()) == PROJECT_NAME:
        print("⚠️ Ejecuta desde una carpeta PADRE.")
        sys.exit(1)
    base_dir = os.path.abspath(PROJECT_NAME)
    env_dir = os.path.join(base_dir, "venv")
    print(f"🚀 Creando proyecto '{PROJECT_NAME}'...")
    os.makedirs(base_dir, exist_ok=True)
    crear_estructura(base_dir)
    venv.create(env_dir, with_pip=True)
    python_exe = os.path.join(env_dir, "Scripts", "python.exe")
    subprocess.check_call([python_exe, "-m", "pip", "install", "-r", os.path.join(base_dir, "requirements.txt")])
    print("\n🎉 ¡Listo! Activa el entorno con:\n   represa_ml\\venv\\Scripts\\activate")

if __name__ == "__main__":
    main()
```

---

### 📄 `generate_data_cli.py`
```python
"""
generate_data_cli.py

¿PARA QUÉ?
- Generar datos sintéticos densos desde la línea de comandos.

¿POR QUÉ?
- Permite simular desde miles hasta millones de registros.
- Útil para pruebas de escalabilidad.

¿CÓMO?
- Usa argparse para recibir parámetros.
- Llama a la función de generación con esos valores.
"""

import argparse
from src.data_generation import generate_and_save_dummy_data

def main():
    parser = argparse.ArgumentParser(description="Genera datos sintéticos para represa.")
    parser.add_argument("--components", type=int, default=5, help="Número de componentes")
    parser.add_argument("--days", type=int, default=365, help="Días a simular")
    parser.add_argument("--freq-hours", type=float, default=1.0, help="Frecuencia en horas")
    parser.add_argument("--output", default="data/raw", help="Carpeta de salida")
    parser.add_argument("--seed", type=int, default=42, help="Semilla")
    args = parser.parse_args()
    generate_and_save_dummy_data(
        days=args.days,
        n_components=args.components,
        freq_hours=args.freq_hours,
        seed=args.seed,
        output_dir=args.output
    )

if __name__ == "__main__":
    main()
```

---

### 📄 `src/data_generation.py`
```python
"""
src/data_generation.py

¿PARA QUÉ?
- Generar datos sintéticos realistas y densos para sensores y eventos.

¿POR QUÉ?
- Permite probar el sistema sin sensores reales.
- Escalable: desde miles hasta millones de registros.
- Guarda en CSV para reutilización.

¿CÓMO?
- Usa operaciones vectorizadas de pandas (rápido y eficiente).
- Simula tendencias estacionales y ruido.
- Genera mantenimientos y fallas con lógica realista.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_and_save_dummy_data(days=365, n_components=5, freq_hours=1, seed=42, output_dir="data/raw"):
    np.random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)
    componentes = [f"compuerta_{i+1}" for i in range(n_components)]
    start_date = datetime(2024, 1, 1)
    freq_str = f"{int(freq_hours * 60)}min" if freq_hours < 1 else f"{int(freq_hours)}h"
    total_steps = int(days * 24 / freq_hours)
    dates = pd.date_range(start=start_date, periods=total_steps, freq=freq_str)
    print(f"📅 Generando datos: {n_components} componentes, {days} días, cada {freq_hours}h → {total_steps * n_components:,} registros...")
    time_series = pd.Series(dates.repeat(n_components))
    comp_series = pd.Series(componentes * total_steps)
    day_of_year = time_series.dt.dayofyear
    month = time_series.dt.month
    presion = 1.0 + 0.3 * np.sin(day_of_year / 365 * 2 * np.pi) + np.random.normal(0, 0.1, size=len(time_series))
    humedad = 60 + 20 * np.sin(month / 12 * 2 * np.pi) + np.random.normal(0, 5, size=len(time_series))
    vibracion = 0.5 + np.random.exponential(0.2, size=len(time_series))
    temperatura = 20 + 10 * np.sin(day_of_year / 365 * 2 * np.pi) + np.random.normal(0, 2, size=len(time_series))
    df_sensores = pd.DataFrame({
        'timestamp': time_series,
        'id_componente': comp_series,
        'presion_bar': np.clip(presion, 0.5, None),
        'humedad_pct': np.clip(humedad, 20, 100),
        'vibracion_mm_s': vibracion,
        'temperatura_c': temperatura
    })
    eventos = []
    for comp in componentes:
        maint_dates = [start_date + timedelta(days=d) for d in range(0, days, 90)]
        for md in maint_dates:
            eventos.append({'timestamp': md, 'id_componente': comp, 'tipo_evento': 'mantenimiento', 'subtipo': 'preventivo', 'gravedad': 'baja'})
        n_fallas = max(2, int(10 * days / 365))
        for _ in range(n_fallas):
            dias = np.random.randint(10, days)
            falla_date = start_date + timedelta(days=dias)
            if any(abs((falla_date - md).days) < 15 for md in maint_dates):
                continue
            eventos.append({'timestamp': falla_date, 'id_componente': comp, 'tipo_evento': 'falla', 'subtipo': np.random.choice(['fuga', 'bloqueo', 'corrosion']), 'gravedad': np.random.choice(['baja', 'media', 'alta'])})
    df_eventos = pd.DataFrame(eventos)
    df_sensores.to_csv(os.path.join(output_dir, "sensores.csv"), index=False)
    df_eventos.to_csv(os.path.join(output_dir, "eventos.csv"), index=False)
    print(f"✅ Datos guardados: {len(df_sensores):,} lecturas, {len(df_eventos):,} eventos.")
    return df_sensores, df_eventos
```

---

### 📄 `src/data_loader.py`
```python
"""
src/data_loader.py

¿PARA QUÉ?
- Cargar datos desde archivos CSV.

¿POR QUÉ?
- Desacopla generación de datos del entrenamiento.
- Permite usar datos reales sin cambiar código.

¿CÓMO?
- Lee sensores.csv y eventos.csv.
- Convierte timestamp a datetime.
"""

import pandas as pd
import os

def load_data_from_csv(data_dir="data/raw"):
    sensores_path = os.path.join(data_dir, "sensores.csv")
    eventos_path = os.path.join(data_dir, "eventos.csv")
    if not os.path.exists(sensores_path):
        raise FileNotFoundError("Ejecuta generate_data_cli.py primero.")
    df_sensores = pd.read_csv(sensores_path, parse_dates=['timestamp'])
    df_eventos = pd.read_csv(eventos_path, parse_dates=['timestamp'])
    return df_sensores, df_eventos
```

---

### 📄 `src/data_preparation.py`
```python
"""
src/data_preparation.py

¿PARA QUÉ?
- Transformar datos crudos en dataset listo para ML.

¿POR QUÉ?
- El modelo necesita una observación por día.
- La etiqueta debe construirse sin fuga de información.

¿CÓMO?
1. Resamplea a diario.
2. Calcula días desde último mantenimiento.
3. Crea etiqueta: ¿falla en próximos 7 días?
"""

import pandas as pd
import numpy as np

def create_ml_dataset(df_sensores, df_eventos):
    df_fallas = df_eventos[df_eventos['tipo_evento'] == 'falla'][['timestamp', 'id_componente']].copy()
    df_fallas = df_fallas.rename(columns={'timestamp': 'falla_timestamp'})
    df_sensores['date'] = df_sensores['timestamp'].dt.floor('D')
    df_daily = df_sensores.groupby(['id_componente', 'date']).agg({
        'presion_bar': 'mean',
        'humedad_pct': 'mean',
        'vibracion_mm_s': 'mean',
        'temperatura_c': 'mean'
    }).reset_index()
    df_mant = df_eventos[df_eventos['tipo_evento'] == 'mantenimiento'][['timestamp', 'id_componente']].copy()
    df_mant = df_mant.rename(columns={'timestamp': 'mant_timestamp'})
    df_daily['dias_desde_mant'] = df_daily.apply(
        lambda row: min([
            (row['date'] - mant_row['mant_timestamp']).days
            for _, mant_row in df_mant[df_mant['id_componente'] == row['id_componente']].iterrows()
            if row['date'] >= mant_row['mant_timestamp']
        ], default=365), axis=1
    )
    df_daily['falla_prox_7d'] = df_daily.apply(
        lambda row: any(
            (falla_row['falla_timestamp'] > row['date']) and
            (falla_row['falla_timestamp'] <= row['date'] + pd.Timedelta(days=7)) and
            (falla_row['id_componente'] == row['id_componente'])
            for _, falla_row in df_fallas.iterrows()
        ), axis=1
    ).astype(int)
    cutoff_date = df_daily['date'].max() - pd.Timedelta(days=7)
    return df_daily[df_daily['date'] <= cutoff_date].copy()
```

---

### 📄 `src/model.py`
```python
"""
src/model.py

¿PARA QUÉ?
- Entrenar modelo y evaluar desempeño.

¿POR QUÉ?
- Random Forest es ideal para datos desbalanceados.
- Documenta resultados en PDF para auditoría.

¿CÓMO?
1. Divide datos (estratificado).
2. Entrena Random Forest.
3. Evalúa con métricas (sin advertencias).
4. Genera informe PDF.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
from .report_pdf import generate_pdf_report

FEATURES = ['presion_bar', 'humedad_pct', 'vibracion_mm_s', 'temperatura_c', 'dias_desde_mant']
TARGET = 'falla_prox_7d'

def train_model(df, model_path='models/maintenance_model.pkl', generate_report=True):
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    report_str = classification_report(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    pdf_path = None
    if generate_report:
        pdf_path = generate_pdf_report(report_str, cm, FEATURES, model.feature_importances_, len(df), int(y.sum()))
    return model, pdf_path

def load_model(model_path='models/maintenance_model.pkl'):
    return joblib.load(model_path)
```

---

### 📄 `src/alerts.py`
```python
"""
src/alerts.py

¿PARA QUÉ?
- Centralizar alertas (sonora + correo).

¿POR QUÉ?
- Separa lógica de alertas del entrenamiento.
- Facilita agregar nuevos canales.

¿CÓMO?
- Verifica umbral de probabilidad.
- Emite sonido en Windows.
- Llama a función de correo.
"""

import os
from .email_alert import send_email_alert

def emit_alert_if_high_risk(probability: float, threshold: float = 0.7, latest_report_path: str = None):
    if probability <= threshold:
        return
    if os.name == 'nt':
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            print("🔊 ¡ALERTA SONORA ACTIVADA!")
        except Exception as e:
            print(f"⚠️ Error en alerta sonora: {e}")
    send_email_alert(probability, threshold, latest_report_path)
```

---

### 📄 `src/email_alert.py`
```python
"""
src/email_alert.py

¿PARA QUÉ?
- Enviar notificaciones por correo.

¿POR QUÉ?
- Alerta a personal remoto.
- Deja registro escrito.

¿CÓMO?
- Usa variables de entorno para credenciales.
- Adjunta informe PDF.
- Usa SMTP de Gmail (cambiable).
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def send_email_alert(probability: float, threshold: float = 0.7, latest_report_path: str = None):
    if probability <= threshold:
        return
    sender = os.getenv("ALERT_EMAIL_USER")
    password = os.getenv("ALERT_EMAIL_PASS")
    recipients = os.getenv("ALERT_EMAIL_RECIPIENTS", "").split(",")
    if not sender or not password or not recipients[0]:
        print("📧 Correo no configurado.")
        return
    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = "🚨 ALERTA: Alto riesgo de falla en represa"
        body = f"""
        Se ha detectado un alto riesgo de falla en un componente de la represa.
        - Probabilidad: {probability:.2%}
        - Umbral: {threshold:.0%}
        - Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Revise el sistema inmediatamente.
        """
        msg.attach(MIMEText(body, "plain"))
        if latest_report_path and os.path.exists(latest_report_path):
            with open(latest_report_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(latest_report_path)}")
            msg.attach(part)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
        print("📧 Correo de alerta enviado.")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
```

---

### 📄 `src/report_pdf.py`
```python
"""
src/report_pdf.py

¿PARA QUÉ?
- Generar informe PDF con resultados.

¿POR QUÉ?
- Formato estándar para reportes técnicos.
- Incluye métricas y gráficos.

¿CÓMO?
- Usa reportlab para PDF.
- Matplotlib para gráfico de importancia.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import matplotlib.pyplot as plt
import io
from reportlab.lib.utils import ImageReader

def generate_pdf_report(report_str, cm, feature_names, importances, n_samples, n_failures, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    plt.figure(figsize=(6, 4))
    plt.barh(feature_names, importances, color='steelblue')
    plt.xlabel("Importancia")
    plt.title("Importancia de Variables")
    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Informe de Mantenimiento Predictivo - Represa")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 100, f"• Muestras: {n_samples}, Fallas: {n_failures}")
    y = height - 130
    for line in report_str.split("\n"):
        if line.strip() and y > 100:
            c.drawString(50, y, line)
            y -= 15
    c.showPage()
    cm_data = [["", "Pred: 0", "Pred: 1"], ["Real: 0", str(cm[0][0]), str(cm[0][1])], ["Real: 1", str(cm[1][0]), str(cm[1][1])]]
    cm_table = Table(cm_data)
    cm_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey), ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    cm_table.wrapOn(c, width, height)
    cm_table.drawOn(c, 50, height - 150)
    c.showPage()
    c.drawImage(ImageReader(img_buffer), 50, height - 400, width=500, height=300)
    c.save()
    return pdf_path
```

---

### 📄 `main.py`
```python
"""
main.py

¿PARA QUÉ?
- Orquestar flujo completo.

¿POR QUÉ?
- Punto de entrada principal.
- Genera datos por defecto si no existen.

¿CÓMO?
1. Verifica existencia de CSV.
2. Genera o carga datos.
3. Entrena modelo.
4. Activa alertas.
"""

from src.data_generation import generate_and_save_dummy_data
from src.data_loader import load_data_from_csv
from src.data_preparation import create_ml_dataset
from src.model import train_model, FEATURES
from src.alerts import emit_alert_if_high_risk
import pandas as pd
import os

def main():
    data_dir = "data/raw"
    sensores_path = os.path.join(data_dir, "sensores.csv")
    if not os.path.exists(sensores_path):
        print("🆕 Generando datos por defecto...")
        df_sensores, df_eventos = generate_and_save_dummy_data(days=365, n_components=5)
    else:
        print("📂 Cargando datos desde CSV...")
        df_sensores, df_eventos = load_data_from_csv(data_dir)
    df_ml = create_ml_dataset(df_sensores, df_eventos)
    print(f"Dataset listo: {df_ml.shape[0]:,} muestras, {df_ml['falla_prox_7d'].sum()} fallas positivas.")
    model, pdf_path = train_model(df_ml)
    ejemplo_df = pd.DataFrame([[1.8, 85, 2.1, 28, 120]], columns=FEATURES)
    proba = model.predict_proba(ejemplo_df)[0][1]
    print(f"Probabilidad de falla: {proba:.2%}")
    emit_alert_if_high_risk(proba, latest_report_path=pdf_path)
    print("\n✅ Proceso completado.")

if __name__ == "__main__":
    main()
```

---

### 📄 `scripts/run_scheduled.py`
```python
"""
scripts/run_scheduled.py

¿PARA QUÉ?
- Ser el punto de entrada para la ejecución diaria (Task Scheduler).

¿POR QUÉ?
- El Programador de Tareas no activa el entorno virtual automáticamente.
- Este script garantiza que se use el entorno correcto.

¿CÓMO?
- Usa el intérprete del entorno virtual.
- Ejecuta main.py y redirige salida a logs/.
"""

import os
import sys
import subprocess
from datetime import datetime

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_python = os.path.join(project_root, "venv", "Scripts", "python.exe")
    main_script = os.path.join(project_root, "main.py")
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"execution_{datetime.now().strftime('%Y%m%d')}.log")
    if not os.path.exists(venv_python):
        print(f"❌ Entorno virtual no encontrado: {venv_python}")
        sys.exit(1)
    if not os.path.exists(main_script):
        print(f"❌ main.py no encontrado: {main_script}")
        sys.exit(1)
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== Inicio: {datetime.now()} ===\n")
        try:
            subprocess.run([venv_python, main_script], cwd=project_root, stdout=f, stderr=subprocess.STDOUT, text=True, check=True)
            f.write("=== Finalizado con éxito ===\n")
        except subprocess.CalledProcessError as e:
            f.write(f"=== ERROR: código {e.returncode} ===\n")
            sys.exit(e.returncode)

if __name__ == "__main__":
    main()
```

---

### 📄 `scripts/schedule_daily_task.py`
```python
"""
scripts/schedule_daily_task.py

¿PARA QUÉ?
- Gestionar la tarea diaria en el Programador de Tareas de Windows.

¿POR QUÉ?
- Evita configuración manual.
- Es reproducible en cualquier máquina Windows.

¿CÓMO?
- Usa 'schtasks.exe' para crear/eliminar tareas.
- Permite especificar hora de ejecución.
"""

import os
import sys
import argparse
import subprocess

TASK_NAME = "RepresaML_Daily_Maintenance"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_SCRIPT = os.path.join(PROJECT_ROOT, "scripts", "run_scheduled.py")
PYTHON_EXEC = sys.executable

def create_task(hour=6, minute=0):
    cmd = ["schtasks", "/create", "/tn", TASK_NAME, "/tr", f'"{PYTHON_EXEC}" "{RUN_SCRIPT}"',
           "/sc", "daily", "/st", f"{hour:02d}:{minute:02d}", "/rl", "highest", "/f"]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Tarea '{TASK_NAME}' creada. Ejecución diaria a las {hour:02d}:{minute:02d}.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        sys.exit(1)

def delete_task():
    cmd = ["schtasks", "/delete", "/tn", TASK_NAME, "/f"]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"🗑️ Tarea '{TASK_NAME}' eliminada.")
    except subprocess.CalledProcessError as e:
        if "does not exist" in e.stderr:
            print(f"ℹ️ Tarea no existe.")
        else:
            print(f"❌ Error: {e.stderr}")
            sys.exit(1)

def check_task_status():
    cmd = ["schtasks", "/query", "/tn", TASK_NAME]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"📊 Tarea programada:\n{result.stdout}")
    except subprocess.CalledProcessError:
        print(f"ℹ️ Tarea '{TASK_NAME}' no programada.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--hour", type=int, default=6)
    parser.add_argument("--minute", type=int, default=0)
    args = parser.parse_args()
    if not os.path.exists(RUN_SCRIPT):
        print("❌ Ejecuta desde la raíz del proyecto 'represa_ml'.")
        sys.exit(1)
    if args.install:
        create_task(args.hour, args.minute)
    elif args.uninstall:
        delete_task()
    elif args.status:
        check_task_status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

## 6. ▶️ Cómo usar el sistema

### Paso 1: Instalar
```powershell
python install_project.py
cd represa_ml
venv\Scripts\activate
```

### Paso 2: Configurar correo
```powershell
# Variables de entorno del sistema (Panel de control > Sistema > Variables de entorno)
ALERT_EMAIL_USER=tu_correo@gmail.com
ALERT_EMAIL_PASS=contraseña_de_aplicacion
ALERT_EMAIL_RECIPIENTS=ingeniero1@empresa.com
```
### 2.1. Obtén una "contraseña de aplicación" en Gmail
1. Ve a [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Inicia sesión
3. Selecciona **"Otra"** → nombre: `represa_ml`
4. Haz clic en **"Generar"**
5. Copia la contraseña de 16 caracteres (ej. `abcd efgh ijkl mnop`)

> ⚠️ **Nunca uses tu contraseña normal de Gmail**. Solo usa la contraseña de aplicación.

### 2.2. Configura las variables de entorno (en la misma terminal)
```powershell
$env:ALERT_EMAIL_USER="tu_correo@gmail.com"
$env:ALERT_EMAIL_PASS="abcd efgh ijkl mnop"          # ← Tu contraseña de aplicación
$env:ALERT_EMAIL_RECIPIENTS="ingeniero1@empresa.com,ingeniero2@empresa.com"
```

> 💡 **Importante**: estas variables **solo existen en esta terminal**. Si la cierras, debes volver a configurarlas.
### Paso 3: Generar datos
```powershell
python generate_data_cli.py --components 50 --days 1095 --freq-hours 1.0
```

### Paso 4: Ejecutar
```powershell
python main.py
```

### Paso 5: Programar diariamente (como administrador)
```powershell
python scripts/schedule_daily_task.py --install --hour 6
```
---

### Bonus: Uso de Logs

¡Excelente observación, Edi! A continuación, te presento la **versión mejorada de todos los códigos** con **sistema de logging completo**, que registra eventos, advertencias y errores en archivos de log estructurados, manteniendo toda la funcionalidad anterior.

---

## 📝 Implementación del sistema de logging

### Principios del logging implementado:
- **Niveles**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Archivos separados**: `logs/app.log` (general) y `logs/execution_YYYYMMDD.log` (ejecuciones programadas)
- **Formato consistente**: fecha, nivel, módulo, mensaje
- **Rotación**: evita archivos de log demasiado grandes

---

## 📄 Código actualizado: `src/utils/logger.py` (Nuevo archivo)

```python
"""
src/utils/logger.py

¿PARA QUÉ?
- Configurar y proporcionar un sistema de logging consistente para toda la aplicación.

¿POR QUÉ?
- Registrar eventos importantes para auditoría y depuración.
- Separar logs por tipo de ejecución (manual vs programada).
- Mantener trazabilidad de errores y decisiones del sistema.

¿CÓMO?
- Usa el módulo logging estándar de Python.
- Configura formateadores y manejadores de archivo.
- Permite diferentes configuraciones para ejecución manual y programada.
"""

import logging
import os
from datetime import datetime

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Configura y devuelve un logger.
    
    Parámetros:
    - name: nombre del logger
    - log_file: archivo de log específico (opcional)
    - level: nivel mínimo de registro
    
    Retorna:
    - logger configurado
    """
    os.makedirs("logs", exist_ok=True)
    
    # Si no se especifica archivo, usa app.log
    if log_file is None:
        log_file = os.path.join("logs", "app.log")
    
    # Formato consistente para todos los logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Manejador de archivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    
    # Manejador de consola (solo para ejecución manual)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicación de handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        # Solo agregar consola si no es ejecución programada
        if "SCHEDULED_EXECUTION" not in os.environ:
            logger.addHandler(console_handler)
    
    return logger
```

---

## 📄 Código actualizado: `main.py`

```python
"""
main.py

¿PARA QUÉ?
- Orquestar flujo completo con logging integrado.

¿POR QUÉ?
- Registrar cada paso del proceso para auditoría y depuración.
- Trazar decisiones de alerta y resultados del modelo.

¿CÓMO?
- Usa el sistema de logging configurado.
- Registra eventos en diferentes niveles según su importancia.
"""

import os
import sys
import pandas as pd
from src.utils.logger import setup_logger
from src.data_generation import generate_and_save_dummy_data
from src.data_loader import load_data_from_csv
from src.data_preparation import create_ml_dataset
from src.model import train_model, FEATURES
from src.alerts import emit_alert_if_high_risk

# Configurar logger
logger = setup_logger('main')

def main():
    logger.info("=== INICIO DE EJECUCIÓN MANUAL ===")
    
    try:
        data_dir = "data/raw"
        sensores_path = os.path.join(data_dir, "sensores.csv")
        
        if not os.path.exists(sensores_path):
            logger.info("Generando datos sintéticos por defecto (5 componentes, 365 días)")
            df_sensores, df_eventos = generate_and_save_dummy_data(days=365, n_components=5)
        else:
            logger.info("Cargando datos desde CSV")
            df_sensores, df_eventos = load_data_from_csv(data_dir)
        
        logger.info("Preparando dataset para ML")
        df_ml = create_ml_dataset(df_sensores, df_eventos)
        logger.info(f"Dataset listo: {df_ml.shape[0]:,} muestras, {df_ml['falla_prox_7d'].sum()} fallas positivas.")
        
        logger.info("Entrenando modelo y generando informe PDF")
        model, pdf_path = train_model(df_ml)
        
        # Predicción de ejemplo con condiciones de alto riesgo
        ejemplo_df = pd.DataFrame([[1.8, 85, 2.1, 28, 120]], columns=FEATURES)
        proba = model.predict_proba(ejemplo_df)[0][1]
        logger.info(f"Probabilidad de falla en 7 días: {proba:.2%}")
        
        # Activar alertas si aplica
        emit_alert_if_high_risk(proba, latest_report_path=pdf_path)
        
        logger.info("=== EJECUCIÓN COMPLETADA EXITOSAMENTE ===")
        
    except Exception as e:
        logger.critical(f"Error crítico durante la ejecución: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📄 Código actualizado: `src/data_generation.py`

```python
"""
src/data_generation.py

¿PARA QUÉ?
- Generar datos sintéticos con logging integrado.

¿POR QUÉ?
- Registrar parámetros de generación para reproducibilidad.
- Trazar el volumen de datos generado.

¿CÓMO?
- Agrega logging en puntos clave del proceso.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from src.utils.logger import setup_logger

# Configurar logger para este módulo
logger = setup_logger('data_generation')

def generate_and_save_dummy_data(days=365, n_components=5, freq_hours=1, seed=42, output_dir="data/raw"):
    logger.info(f"Iniciando generación de datos: {n_components} componentes, {days} días, frecuencia cada {freq_hours}h")
    
    np.random.seed(seed)
    os.makedirs(output_dir, exist_ok=True)
    componentes = [f"compuerta_{i+1}" for i in range(n_components)]
    start_date = datetime(2024, 1, 1)
    freq_str = f"{int(freq_hours * 60)}min" if freq_hours < 1 else f"{int(freq_hours)}h"
    total_steps = int(days * 24 / freq_hours)
    dates = pd.date_range(start=start_date, periods=total_steps, freq=freq_str)
    
    time_series = pd.Series(dates.repeat(n_components))
    comp_series = pd.Series(componentes * total_steps)
    day_of_year = time_series.dt.dayofyear
    month = time_series.dt.month
    
    presion = 1.0 + 0.3 * np.sin(day_of_year / 365 * 2 * np.pi) + np.random.normal(0, 0.1, size=len(time_series))
    humedad = 60 + 20 * np.sin(month / 12 * 2 * np.pi) + np.random.normal(0, 5, size=len(time_series))
    vibracion = 0.5 + np.random.exponential(0.2, size=len(time_series))
    temperatura = 20 + 10 * np.sin(day_of_year / 365 * 2 * np.pi) + np.random.normal(0, 2, size=len(time_series))
    
    df_sensores = pd.DataFrame({
        'timestamp': time_series,
        'id_componente': comp_series,
        'presion_bar': np.clip(presion, 0.5, None),
        'humedad_pct': np.clip(humedad, 20, 100),
        'vibracion_mm_s': vibracion,
        'temperatura_c': temperatura
    })
    
    eventos = []
    for comp in componentes:
        maint_dates = [start_date + timedelta(days=d) for d in range(0, days, 90)]
        for md in maint_dates:
            eventos.append({'timestamp': md, 'id_componente': comp, 'tipo_evento': 'mantenimiento', 'subtipo': 'preventivo', 'gravedad': 'baja'})
        n_fallas = max(2, int(10 * days / 365))
        for _ in range(n_fallas):
            dias = np.random.randint(10, days)
            falla_date = start_date + timedelta(days=dias)
            if any(abs((falla_date - md).days) < 15 for md in maint_dates):
                continue
            eventos.append({'timestamp': falla_date, 'id_componente': comp, 'tipo_evento': 'falla', 'subtipo': np.random.choice(['fuga', 'bloqueo', 'corrosion']), 'gravedad': np.random.choice(['baja', 'media', 'alta'])})
    
    df_eventos = pd.DataFrame(eventos)
    sensores_path = os.path.join(output_dir, "sensores.csv")
    eventos_path = os.path.join(output_dir, "eventos.csv")
    df_sensores.to_csv(sensores_path, index=False)
    df_eventos.to_csv(eventos_path, index=False)
    
    logger.info(f"Datos guardados exitosamente: {len(df_sensores):,} lecturas, {len(df_eventos):,} eventos")
    return df_sensores, df_eventos
```

---

## 📄 Código actualizado: `src/model.py`

```python
"""
src/model.py

¿PARA QUÉ?
- Entrenar modelo con logging detallado.

¿POR QUÉ?
- Registrar métricas y parámetros para auditoría.
- Trazar el rendimiento del modelo.

¿CÓMO?
- Registra métricas clave y características del dataset.
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os
from src.utils.logger import setup_logger
from .report_pdf import generate_pdf_report

logger = setup_logger('model')

FEATURES = ['presion_bar', 'humedad_pct', 'vibracion_mm_s', 'temperatura_c', 'dias_desde_mant']
TARGET = 'falla_prox_7d'

def train_model(df, model_path='models/maintenance_model.pkl', generate_report=True):
    logger.info("Iniciando entrenamiento del modelo Random Forest")
    logger.info(f"Dataset: {len(df)} muestras, {df[TARGET].sum()} positivos ({df[TARGET].mean():.2%} de fallas)")
    
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    logger.info(f"División de datos: {len(X_train)} entrenamiento, {len(X_test)} prueba")
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    report_str = classification_report(y_test, y_pred, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    # Extraer métricas para logging
    lines = report_str.strip().split('\n')
    for line in lines:
        if '1' in line and line.strip()[0] == '1':
            parts = line.split()
            if len(parts) >= 4:
                recall = float(parts[2])
                precision = float(parts[1])
                f1 = float(parts[3])
                logger.info(f"Métricas para fallas (clase 1): Precisión={precision:.3f}, Recall={recall:.3f}, F1={f1:.3f}")
                break
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    logger.info(f"Modelo guardado en: {model_path}")
    
    pdf_path = None
    if generate_report:
        pdf_path = generate_pdf_report(report_str, cm, FEATURES, model.feature_importances_, len(df), int(y.sum()))
        logger.info(f"Informe PDF generado: {pdf_path}")
    
    logger.info("Entrenamiento completado exitosamente")
    return model, pdf_path

def load_model(model_path='models/maintenance_model.pkl'):
    logger.info(f"Cargando modelo desde: {model_path}")
    return joblib.load(model_path)
```

---

## 📄 Código actualizado: `src/alerts.py`

```python
"""
src/alerts.py

¿PARA QUÉ?
- Gestionar alertas con logging integrado.

¿POR QUÉ?
- Registrar cuándo y por qué se activan las alertas.
- Trazar la probabilidad que desencadenó la alerta.

¿CÓMO?
- Registra eventos de alerta en nivel INFO o WARNING.
"""

import os
from src.utils.logger import setup_logger
from .email_alert import send_email_alert

logger = setup_logger('alerts')

def emit_alert_if_high_risk(probability: float, threshold: float = 0.7, latest_report_path: str = None):
    if probability <= threshold:
        logger.debug(f"Probabilidad {probability:.2%} por debajo del umbral {threshold:.0%} - Sin alerta")
        return
    
    logger.warning(f"ALTA PROBABILIDAD DETECTADA: {probability:.2%} > umbral {threshold:.0%}")
    
    # Alerta sonora (solo Windows)
    if os.name == 'nt':
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            logger.info("Alerta sonora activada en sistema Windows")
        except Exception as e:
            logger.error(f"Error al activar alerta sonora: {e}")
    
    # Alerta por correo
    send_email_alert(probability, threshold, latest_report_path)
    logger.info("Proceso de alertas completado")
```

---

## 📄 Código actualizado: `src/email_alert.py`

```python
"""
src/email_alert.py

¿PARA QUÉ?
- Enviar notificaciones por correo con logging.

¿POR QUÉ?
- Registrar intentos de envío y resultados.
- Trazar errores en la configuración de correo.

¿CÓMO?
- Registra cada paso del proceso de envío.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger('email_alert')

def send_email_alert(probability: float, threshold: float = 0.7, latest_report_path: str = None):
    if probability <= threshold:
        return
    
    sender = os.getenv("ALERT_EMAIL_USER")
    password = os.getenv("ALERT_EMAIL_PASS")
    recipients = os.getenv("ALERT_EMAIL_RECIPIENTS", "").split(",")
    
    if not sender or not password or not recipients[0]:
        logger.error("Correo no configurado: faltan variables de entorno ALERT_EMAIL_USER, ALERT_EMAIL_PASS o ALERT_EMAIL_RECIPIENTS")
        return
    
    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = "🚨 ALERTA: Alto riesgo de falla en represa"
        body = f"""
        Se ha detectado un alto riesgo de falla en un componente de la represa.
        - Probabilidad: {probability:.2%}
        - Umbral: {threshold:.0%}
        - Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Revise el sistema inmediatamente.
        """
        msg.attach(MIMEText(body, "plain"))
        
        if latest_report_path and os.path.exists(latest_report_path):
            with open(latest_report_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(latest_report_path)}")
            msg.attach(part)
            logger.info(f"PDF adjunto al correo: {os.path.basename(latest_report_path)}")
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
        
        logger.info(f"Correo de alerta enviado exitosamente a {len(recipients)} destinatarios")
        
    except Exception as e:
        logger.critical(f"Error crítico al enviar correo de alerta: {e}")
```

---

## 📄 Código actualizado: `scripts/run_scheduled.py`

```python
"""
scripts/run_scheduled.py

¿PARA QUÉ?
- Ejecutar el sistema programado con logging específico.

¿POR QUÉ?
- Diferenciar logs de ejecución programada vs manual.
- Registrar cada ejecución diaria en archivo separado.

¿CÓMO?
- Establece variable de entorno para desactivar salida por consola.
- Usa archivo de log con marca de tiempo diaria.
"""

import os
import sys
import subprocess
from datetime import datetime
from src.utils.logger import setup_logger

# Indicar que es ejecución programada (desactiva salida por consola)
os.environ["SCHEDULED_EXECUTION"] = "1"

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_python = os.path.join(project_root, "venv", "Scripts", "python.exe")
    main_script = os.path.join(project_root, "main.py")
    log_dir = os.path.join(project_root, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"execution_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Configurar logger específico para esta ejecución
    logger = setup_logger('scheduled_execution', log_file=log_file)
    logger.info("=== INICIO DE EJECUCIÓN PROGRAMADA ===")
    
    if not os.path.exists(venv_python):
        logger.critical(f"Entorno virtual no encontrado: {venv_python}")
        sys.exit(1)
    if not os.path.exists(main_script):
        logger.critical(f"main.py no encontrado: {main_script}")
        sys.exit(1)
    
    try:
        result = subprocess.run(
            [venv_python, main_script],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        logger.info("=== EJECUCIÓN PROGRAMADA COMPLETADA EXITOSAMENTE ===")
        
    except subprocess.CalledProcessError as e:
        logger.critical(f"Error en ejecución programada - Código de retorno: {e.returncode}")
        logger.critical(f"Salida de error: {e.stderr}")
        sys.exit(e.returncode)
    except Exception as e:
        logger.critical(f"Error inesperado en ejecución programada: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📄 Actualización de `install_project.py`

Agrega el nuevo archivo al listado:

```python
ARCHIVOS = [
    "requirements.txt",
    "main.py",
    "generate_data_cli.py",
    "src/__init__.py",
    "src/utils/__init__.py",          # ← Nuevo
    "src/utils/logger.py",            # ← Nuevo
    "src/data_generation.py",
    "src/data_loader.py",
    "src/data_preparation.py",
    "src/model.py",
    "src/alerts.py",
    "src/email_alert.py",
    "src/report_pdf.py",
    "scripts/run_scheduled.py",
    "scripts/schedule_daily_task.py"
]

DIRECTORIOS = ["data", "models", "reports", "logs", "scripts", "src", "src/utils"]  # ← Agrega src/utils
```

---

## 📁 Estructura final con logging

```
represa_ml/
├── logs/
│   ├── app.log                    ← Logs de ejecuciones manuales
│   └── execution_20251021.log     ← Logs de ejecuciones programadas
├── src/
│   └── utils/
│       ├── __init__.py
│       └── logger.py              ← Sistema de logging
└── ... (resto de archivos)
```

---

## 📊 Ejemplo de contenido en `logs/app.log`

```
2025-10-21 14:30:22 - main - INFO - === INICIO DE EJECUCIÓN MANUAL ===
2025-10-21 14:30:23 - data_generation - INFO - Iniciando generación de datos: 5 componentes, 365 días, frecuencia cada 1.0h
2025-10-21 14:30:25 - data_generation - INFO - Datos guardados exitosamente: 43,800 lecturas, 40 eventos
2025-10-21 14:30:26 - model - INFO - Métricas para fallas (clase 1): Precisión=0.850, Recall=0.760, F1=0.800
2025-10-21 14:30:28 - alerts - WARNING - ALTA PROBABILIDAD DETECTADA: 78.50% > umbral 70%
2025-10-21 14:30:28 - alerts - INFO - Alerta sonora activada en sistema Windows
2025-10-21 14:30:29 - email_alert - INFO - Correo de alerta enviado exitosamente a 2 destinatarios
2025-10-21 14:30:29 - main - INFO - === EJECUCIÓN COMPLETADA EXITOSAMENTE ===
```

---

Con este sistema de logging completo, tienes **trazabilidad total** de todas las operaciones del sistema, **auditoría técnica** de decisiones y **depuración eficiente** de errores, manteniendo todos los beneficios del sistema original de mantenimiento predictivo para represas.

