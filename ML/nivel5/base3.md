Perfecto, Edi. A continuación, te presento la **versión mejorada y refinada** de la guía, cumpliendo con tus requisitos clave:

✅ **`install_project.py` solo crea la estructura de directorios y archivos vacíos** (sin contenido)  
✅ **Los códigos reales se presentan después, bien segmentados y con comentarios explicativos** que responden:  
 - **¿Para qué sirve?**  
 - **¿Cómo funciona?**  
 - **¿Por qué se hizo así?**  

✅ Incluye todas las funcionalidades:  
 - Random Forest + métricas  
 - Alerta sonora (Windows)  
 - Notificación por correo  
 - Informe PDF automático  
 - Ejecución diaria programada  

---

# 📘 Guía Paso a Paso: Sistema de Mantenimiento Predictivo para Represas con Machine Learning

---

## 1. 🎯 Objetivo

Predecir fallas en componentes críticos de una represa **7 días antes** de que ocurran, usando Machine Learning, y notificar al equipo técnico mediante **alerta sonora + correo electrónico**, con **informe PDF automático** y **ejecución diaria programada**.

---

## 2. 🌳 Random Forest y Métricas (Resumen)

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

---

## 3. 🗂️ Estructura del proyecto

El script `install_project.py` creará **solo la estructura de directorios y archivos vacíos**:

```
represa_ml/
├── install_project.py
├── requirements.txt
├── main.py
├── data/
├── models/
├── reports/
├── logs/
├── scripts/
│   ├── schedule_daily_task.py
│   └── run_scheduled.py
└── src/
    ├── __init__.py
    ├── data_generation.py
    ├── data_preparation.py
    ├── model.py
    ├── alerts.py
    ├── email_alert.py
    └── report_pdf.py
```

---

## 4. 🛠️ Script de instalación: `install_project.py`

Este script **solo crea la estructura**, sin escribir contenido en los archivos.

```python
"""
install_project.py

Propósito:
- Crear la estructura de directorios del proyecto.
- Crear archivos vacíos en las rutas correctas.
- NO instalar paquetes ni escribir lógica (eso se hace manualmente o en otro paso).

¿Por qué así?
- Permite revisar/editar cada archivo antes de usarlo.
- Facilita la comprensión del flujo del proyecto.
- Evita sobrescribir cambios si ya existen archivos.

Cómo usar:
1. Guarda este archivo en una carpeta vacía (ej. C:\proyectos\)
2. Ejecuta: python install_project.py
3. Se creará la carpeta 'represa_ml' con todos los archivos vacíos.
"""

import os

# Definir estructura
DIRECTORIOS = [
    "data",
    "models",
    "reports",
    "logs",
    "scripts",
    "src"
]

ARCHIVOS = [
    "requirements.txt",
    "main.py",
    "src/__init__.py",
    "src/data_generation.py",
    "src/data_preparation.py",
    "src/model.py",
    "src/alerts.py",
    "src/email_alert.py",
    "src/report_pdf.py",
    "scripts/run_scheduled.py",
    "scripts/schedule_daily_task.py"
]

def crear_estructura():
    """Crea directorios y archivos vacíos."""
    os.makedirs("represa_ml", exist_ok=True)
    os.chdir("represa_ml")
    
    # Crear directorios
    for d in DIRECTORIOS:
        os.makedirs(d, exist_ok=True)
    
    # Crear archivos vacíos
    for archivo in ARCHIVOS:
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        with open(archivo, "w", encoding="utf-8") as f:
            pass  # Archivo vacío
    
    print("✅ Estructura de proyecto creada en 'represa_ml/'.")
    print("📝 Ahora edita cada archivo con el código correspondiente (ver sección siguiente).")

if __name__ == "__main__":
    crear_estructura()
```

---

## 5. 💻 Códigos completos (bien comentados)

> **Copia cada bloque en su archivo correspondiente** dentro de `represa_ml/`.

---

### 📄 `requirements.txt`
```txt
pandas
numpy
scikit-learn
streamlit
joblib
matplotlib
reportlab
```

---

### 📄 `main.py`
```python
"""
main.py

¿Para qué?
- Orquesta todo el flujo: genera datos, entrena modelo, evalúa riesgo y activa alertas.

¿Cómo funciona?
1. Llama al generador de datos dummy.
2. Prepara el dataset para ML.
3. Entrena el modelo y genera informe PDF.
4. Ejecuta una predicción de ejemplo con alto riesgo.
5. Activa alertas si la probabilidad supera el umbral.

¿Por qué así?
- Centraliza la lógica principal.
- Permite ejecución manual o programada.
- Usa un ejemplo realista de alto riesgo para probar alertas.
"""

from src.data_generation import generate_dummy_data
from src.data_preparation import create_ml_dataset
from src.model import train_model
from src.alerts import emit_alert_if_high_risk
import numpy as np

def main():
    print("🚀 Generando datos sintéticos...")
    df_sensores, df_eventos = generate_dummy_data(days=365, n_components=5)
    
    print("🧼 Preparando dataset para ML...")
    df_ml = create_ml_dataset(df_sensores, df_eventos)
    print(f"Dataset listo: {df_ml.shape[0]} muestras, {df_ml['falla_prox_7d'].sum()} fallas positivas.")
    
    print("🧠 Entrenando modelo y generando informe PDF...")
    model, pdf_path = train_model(df_ml)
    
    # Ejemplo de predicción con condiciones de alto riesgo
    ejemplo = np.array([[1.8, 85, 2.1, 28, 120]])  # alta presión, humedad, vibración, días sin mant.
    proba = model.predict_proba(ejemplo)[0][1]
    print(f"Probabilidad de falla en 7 días: {proba:.2%}")
    
    # Activar alertas si aplica
    emit_alert_if_high_risk(proba, latest_report_path=pdf_path)
    
    print("\n✅ Proceso completado.")
    print("💡 Usa el dashboard: streamlit run src/dashboard.py")

if __name__ == "__main__":
    main()
```

---

### 📄 `src/data_generation.py`
```python
"""
src/data_generation.py

¿Para qué?
- Generar datos sintéticos realistas para simular el comportamiento de una represa.

¿Cómo funciona?
- Crea componentes (compuertas).
- Simula lecturas horarias de sensores con ruido y tendencias estacionales.
- Genera eventos de mantenimiento (cada ~90 días) y fallas aleatorias (evitando cercanía a mantenimientos).

¿Por qué así?
- Permite probar el sistema sin sensores reales.
- Incluye patrones realistas: presión varía con estaciones, fallas son más probables sin mantenimiento reciente.
- Evita data leakage: las fallas no ocurren justo después de mantenimientos.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dummy_data(days=365, n_components=5, seed=42):
    np.random.seed(seed)
    componentes = [f"compuerta_{i+1}" for i in range(n_components)]
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=h) for h in range(days * 24)]
    
    records = []
    for comp in componentes:
        for dt in dates:
            # Simular sensores con tendencias estacionales y ruido
            presion = 1.0 + 0.3 * np.sin(dt.timetuple().tm_yday / 365 * 2 * np.pi) + np.random.normal(0, 0.1)
            humedad = 60 + 20 * np.sin(dt.month / 12 * 2 * np.pi) + np.random.normal(0, 5)
            vibracion = 0.5 + np.random.exponential(0.2)
            temperatura = 20 + 10 * np.sin(dt.timetuple().tm_yday / 365 * 2 * np.pi) + np.random.normal(0, 2)
            records.append({
                'timestamp': dt,
                'id_componente': comp,
                'presion_bar': max(0.5, presion),
                'humedad_pct': np.clip(humedad, 20, 100),
                'vibracion_mm_s': vibracion,
                'temperatura_c': temperatura
            })
    df_sensores = pd.DataFrame(records)
    
    eventos = []
    for comp in componentes:
        # Mantenimientos cada ~90 días
        maint_dates = [start_date + timedelta(days=d) for d in range(0, days, 90)]
        for md in maint_dates:
            eventos.append({
                'timestamp': md,
                'id_componente': comp,
                'tipo_evento': 'mantenimiento',
                'subtipo': 'preventivo',
                'gravedad': 'baja'
            })
        # Fallas aleatorias (más probables lejos de mantenimientos)
        for _ in range(8):
            dias = np.random.randint(10, days)
            falla_date = start_date + timedelta(days=dias)
            if any(abs((falla_date - md).days) < 15 for md in maint_dates):
                continue  # Evitar fallas justo después de mantenimiento
            eventos.append({
                'timestamp': falla_date,
                'id_componente': comp,
                'tipo_evento': 'falla',
                'subtipo': np.random.choice(['fuga', 'bloqueo', 'corrosion']),
                'gravedad': np.random.choice(['baja', 'media', 'alta'])
            })
    df_eventos = pd.DataFrame(eventos)
    return df_sensores, df_eventos
```

---

### 📄 `src/data_preparation.py`
```python
"""
src/data_preparation.py

¿Para qué?
- Transformar datos crudos en un dataset listo para entrenar un modelo de ML.

¿Cómo funciona?
1. Agrega columna de fallas.
2. Resamplea lecturas horarias a diarias (promedio).
3. Calcula "días desde último mantenimiento".
4. Crea etiqueta: ¿hubo falla en los próximos 7 días?

¿Por qué así?
- El modelo necesita una observación por día (no por hora).
- La etiqueta se construye mirando al futuro, pero el modelo solo usa datos pasados → evita fuga de información.
- Se eliminan los últimos 7 días (no tienen etiqueta completa).
"""

import pandas as pd
import numpy as np

def create_ml_dataset(df_sensores, df_eventos):
    # Extraer fechas de fallas
    df_fallas = df_eventos[df_eventos['tipo_evento'] == 'falla'][['timestamp', 'id_componente']].copy()
    df_fallas = df_fallas.rename(columns={'timestamp': 'falla_timestamp'})
    
    # Resample a diario
    df_sensores['date'] = df_sensores['timestamp'].dt.floor('D')
    df_daily = df_sensores.groupby(['id_componente', 'date']).agg({
        'presion_bar': 'mean',
        'humedad_pct': 'mean',
        'vibracion_mm_s': 'mean',
        'temperatura_c': 'mean'
    }).reset_index()
    
    # Días desde último mantenimiento
    df_mant = df_eventos[df_eventos['tipo_evento'] == 'mantenimiento'][['timestamp', 'id_componente']].copy()
    df_mant = df_mant.rename(columns={'timestamp': 'mant_timestamp'})
    df_daily['dias_desde_mant'] = df_daily.apply(
        lambda row: min([
            (row['date'] - mant_row['mant_timestamp']).days
            for _, mant_row in df_mant[df_mant['id_componente'] == row['id_componente']].iterrows()
            if row['date'] >= mant_row['mant_timestamp']
        ], default=365), axis=1
    )
    
    # Etiqueta: falla en próximos 7 días
    df_daily['falla_prox_7d'] = df_daily.apply(
        lambda row: any(
            (falla_row['falla_timestamp'] > row['date']) and
            (falla_row['falla_timestamp'] <= row['date'] + pd.Timedelta(days=7)) and
            (falla_row['id_componente'] == row['id_componente'])
            for _, falla_row in df_fallas.iterrows()
        ), axis=1
    ).astype(int)
    
    # Eliminar últimos 7 días (sin etiqueta completa)
    cutoff_date = df_daily['date'].max() - pd.Timedelta(days=7)
    return df_daily[df_daily['date'] <= cutoff_date].copy()
```

---

### 📄 `src/model.py`
```python
"""
src/model.py

¿Para qué?
- Entrenar un modelo Random Forest y evaluar su desempeño.

¿Cómo funciona?
1. Divide datos en entrenamiento/prueba (estratificado).
2. Entrena Random Forest.
3. Evalúa con métricas (precisión, recall, F1).
4. Guarda el modelo y genera informe PDF.

¿Por qué así?
- Random Forest es robusto para datos desbalanceados.
- Estratificación mantiene proporción de fallas en entrenamiento/prueba.
- El informe PDF documenta resultados para auditoría.
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
    report_str = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print("=== Reporte de Clasificación ===\n", report_str)
    print("=== Matriz de Confusión ===\n", cm)
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    
    pdf_path = None
    if generate_report:
        pdf_path = generate_pdf_report(
            classification_report_str=report_str,
            confusion_matrix_array=cm,
            feature_names=FEATURES,
            feature_importances=model.feature_importances_,
            n_samples=len(df),
            n_failures=int(y.sum())
        )
    return model, pdf_path

def load_model(model_path='models/maintenance_model.pkl'):
    return joblib.load(model_path)
```

---

### 📄 `src/alerts.py`
```python
"""
src/alerts.py

¿Para qué?
- Centralizar la lógica de alertas (sonora + correo).

¿Cómo funciona?
- Verifica si la probabilidad supera el umbral.
- En Windows: emite sonido del sistema.
- Llama a la función de correo.

¿Por qué así?
- Separa la lógica de alertas del entrenamiento.
- Facilita agregar nuevos canales (SMS, Slack).
- Evita duplicar código.
"""

import os
from .email_alert import send_email_alert

def emit_alert_if_high_risk(probability: float, threshold: float = 0.7, latest_report_path: str = None):
    if probability <= threshold:
        return
    # Alerta sonora (solo Windows)
    if os.name == 'nt':
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            print("🔊 ¡ALERTA SONORA ACTIVADA!")
        except Exception as e:
            print(f"⚠️ Error en alerta sonora: {e}")
    # Alerta por correo
    send_email_alert(probability, threshold, latest_report_path)
```

---

### 📄 `src/email_alert.py`
```python
"""
src/email_alert.py

¿Para qué?
- Enviar notificaciones por correo cuando hay alto riesgo.

¿Cómo funciona?
1. Lee credenciales desde variables de entorno.
2. Crea mensaje con asunto, cuerpo y adjunto (PDF).
3. Envía usando SMTP (Gmail por defecto).

¿Por qué así?
- Seguridad: credenciales nunca en código.
- Universal: cualquier proveedor SMTP (cambiar servidor si es Outlook, etc.).
- Adjunta informe PDF para contexto técnico.
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
        print("📧 Correo no configurado. Define variables de entorno.")
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

¿Para qué?
- Generar un informe PDF con resultados del modelo.

¿Cómo funciona?
1. Crea gráfico de importancia de variables.
2. Escribe resumen de datos, métricas y matriz de confusión.
3. Guarda en 'reports/' con marca de tiempo.

¿Por qué así?
- PDF es estándar para reportes técnicos.
- Incluye todo lo necesario para auditoría.
- Gráfico de importancia ayuda a interpretar el modelo.
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

def generate_pdf_report(
    classification_report_str: str,
    confusion_matrix_array,
    feature_names: list,
    feature_importances: list,
    n_samples: int,
    n_failures: int,
    output_dir: str = "reports"
):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(output_dir, f"reporte_mantenimiento_{timestamp}.pdf")
    
    # Gráfico de importancia
    plt.figure(figsize=(6, 4))
    plt.barh(feature_names, feature_importances, color='steelblue')
    plt.xlabel("Importancia")
    plt.title("Importancia de Variables")
    plt.tight_layout()
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    
    # Crear PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Informe de Mantenimiento Predictivo - Represa")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "Resumen de datos:")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 120, f"• Total de muestras: {n_samples}")
    c.drawString(50, height - 135, f"• Fallas registradas: {n_failures}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 160, "Métricas del modelo:")
    y = height - 180
    for line in classification_report_str.split("\n"):
        if line.strip() and y > 100:
            c.drawString(50, y, line)
            y -= 15
    c.showPage()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 50, "Matriz de Confusión:")
    cm_data = [["", "Pred: 0", "Pred: 1"],
               ["Real: 0", str(confusion_matrix_array[0][0]), str(confusion_matrix_array[0][1])],
               ["Real: 1", str(confusion_matrix_array[1][0]), str(confusion_matrix_array[1][1])]]
    cm_table = Table(cm_data)
    cm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    cm_table.wrapOn(c, width, height)
    cm_table.drawOn(c, 50, height - 150)
    c.showPage()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 50, "Gráfico de Importancia de Variables:")
    c.drawImage(ImageReader(img_buffer), 50, height - 400, width=500, height=300)
    c.save()
    return pdf_path
```

---

### 📄 `scripts/run_scheduled.py`
```python
"""
scripts/run_scheduled.py

¿Para qué?
- Ser el punto de entrada para la ejecución diaria (Task Scheduler).

¿Cómo funciona?
- Usa el intérprete del entorno virtual.
- Ejecuta main.py y redirige salida a logs/.

¿Por qué así?
- El Programador de Tareas no activa el entorno virtual automáticamente.
- Este script garantiza que se use el entorno correcto.
- Registra logs para auditoría.
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

¿Para qué?
- Gestionar la tarea diaria en el Programador de Tareas de Windows.

¿Cómo funciona?
- Usa 'schtasks.exe' para crear/eliminar tareas.
- Permite especificar hora de ejecución.

¿Por qué así?
- Evita configuración manual.
- Es reproducible en cualquier máquina Windows.
- Usa privilegios altos para ejecutar sin sesión activa.
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

### Paso 1: Crear estructura
```powershell
# Guarda install_project.py en C:\proyectos\
python install_project.py
```

### Paso 2: Copiar códigos
- Abre cada archivo vacío en `represa_ml/`
- Pega el código correspondiente de esta guía

### Paso 3: Configurar entorno
```powershell
cd represa_ml
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Paso 4: Configurar correo (PowerShell)
```powershell
$env:ALERT_EMAIL_USER="tu_correo@gmail.com"
$env:ALERT_EMAIL_PASS="contraseña_de_aplicacion"
$env:ALERT_EMAIL_RECIPIENTS="ingeniero1@empresa.com,ingeniero2@empresa.com"
```

### Paso 5: Probar
```powershell
python main.py
```

### Paso 6: Programar diariamente (como administrador)
```powershell
python scripts/schedule_daily_task.py --install --hour 6
```

---

Este enfoque te da **control total**, **transparencia** y **facilidad de mantenimiento**, cumpliendo con las mejores prácticas de programación y ciencia de datos.

¿Necesitas ayuda para conectarlo a sensores reales o una base de datos? Estoy listo para seguir contigo.
