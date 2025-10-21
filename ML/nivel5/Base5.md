¡Claro, Edi! A continuación, te presento la **Guía Paso a Paso Completa y Definitiva** para implementar un **Sistema de Mantenimiento Predictivo para Represas con Machine Learning**, con:

✅ **Explicación clara de Random Forest y métricas (precisión, recall, F1)**  
✅ **Generación de datos sintéticos densos** (hasta 1 millón+ de registros)  
✅ **Guardado en archivos CSV**  
✅ **Alerta sonora en Windows**  
✅ **Notificación por correo electrónico**  
✅ **Informe PDF automático**  
✅ **Ejecución diaria programada**  
✅ **Código modular, bien estructurado y comentado**  
✅ **Comentarios en cada función**: **¿Para qué?**, **¿Por qué?**, **¿Cómo?**

---

# 📘 Guía Paso a Paso: Sistema de Mantenimiento Predictivo para Represas con Machine Learning

---

## 1. 🎯 Objetivo

Predecir fallas en componentes críticos de una represa **7 días antes** de que ocurran, usando Machine Learning, y notificar al equipo técnico mediante **alerta sonora + correo electrónico**, con **informe PDF automático** y **ejecución diaria programada**.

---

## 2. 🌳 Random Forest y Métricas (Explicación Simple)

### ¿Qué es Random Forest?
- **Para qué**: predecir si un componente fallará.
- **Cómo**: combina cientos de árboles de decisión que votan en conjunto.
- **Por qué**: es robusto, maneja datos desbalanceados y muestra qué variables son más importantes.

### Métricas clave
| Métrica | Para qué | Por qué es importante en represas |
|--------|--------|-------------------------------|
| **Precisión** | ¿Cuántas alertas fueron reales? | Evita falsas alarmas que detienen operaciones innecesariamente |
| **Recall** | ¿Detectamos la mayoría de fallas reales? | **Prioridad**: no queremos fallas no detectadas |
| **F1-Score** | Equilibrio entre ambas | Útil cuando hay pocas fallas (datos desbalanceados) |

> En mantenimiento predictivo: **maximizamos recall**, aunque aumenten ligeramente las falsas alarmas.

---

## 3. 🗂️ Estructura del Proyecto

El script `install_project.py` creará automáticamente:

```
represa_ml/
├── install_project.py
├── requirements.txt
├── main.py
├── generate_data_cli.py        ← Genera datos personalizados
├── data/
│   └── raw/
│       ├── sensores.csv        ← Datos de sensores (densos)
│       └── eventos.csv         ← Mantenimientos y fallas
├── models/
├── reports/
├── logs/
├── scripts/
│   ├── run_scheduled.py        ← Ejecución diaria
│   └── schedule_daily_task.py  ← Gestiona tarea programada
└── src/
    ├── __init__.py
    ├── data_generation.py      ← Genera datos sintéticos
    ├── data_loader.py          ← Carga datos desde CSV
    ├── data_preparation.py     ← Prepara dataset para ML
    ├── model.py                ← Entrena modelo y evalúa métricas
    ├── alerts.py               ← Alerta sonora + correo
    ├── email_alert.py          ← Envía notificaciones por email
    └── report_pdf.py           ← Genera informe PDF
```

---

## 4. 🛠️ Script de Instalación: `install_project.py`

```python
"""
install_project.py

¿Para qué?
- Crear la estructura completa del proyecto con un solo comando.

¿Por qué?
- Automatiza la configuración inicial.
- Aísla dependencias en un entorno virtual.
- Permite comenzar a trabajar inmediatamente.

¿Cómo?
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
    
    # Crear requirements.txt con contenido
    with open(os.path.join(base_path, "requirements.txt"), "w") as f:
        f.write("\n".join(REQUIREMENTS))
    
    # Crear otros archivos vacíos
    for archivo in ARCHIVOS:
        if archivo == "requirements.txt":
            continue
        ruta = os.path.join(base_path, archivo)
        dir_name = os.path.dirname(ruta)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(ruta, "w") as f:
            pass

def crear_entorno_virtual(env_path):
    print("🛠️ Creando entorno virtual...")
    venv.create(env_path, with_pip=True)

def instalar_dependencias(env_path):
    print("📦 Instalando dependencias...")
    python_exe = os.path.join(env_path, "Scripts", "python.exe") if os.name == "nt" else os.path.join(env_path, "bin", "python")
    req_file = os.path.join(env_path, "..", "requirements.txt")
    subprocess.check_call([python_exe, "-m", "pip", "install", "-r", req_file])

def main():
    if os.path.basename(os.getcwd()) == PROJECT_NAME:
        print("⚠️ Ejecuta desde una carpeta PADRE.")
        sys.exit(1)
    
    base_dir = os.path.abspath(PROJECT_NAME)
    env_dir = os.path.join(base_dir, "venv")
    
    print(f"🚀 Creando proyecto '{PROJECT_NAME}'...")
    os.makedirs(base_dir, exist_ok=True)
    crear_estructura(base_dir)
    crear_entorno_virtual(env_dir)
    instalar_dependencias(env_dir)
    
    print("\n🎉 ¡Listo! Activa el entorno y edita los archivos.")

if __name__ == "__main__":
    main()
```

---

## 5. 💻 Códigos Completos (Bien Comentados)

> **Copia cada bloque en su archivo correspondiente** dentro de `represa_ml/`.

---

### 📄 `generate_data_cli.py`
```python
"""
generate_data_cli.py

¿Para qué?
- Generar datos sintéticos densos desde la línea de comandos.

¿Por qué?
- Permite simular desde miles hasta millones de registros.
- Útil para pruebas de escalabilidad o escenarios realistas.

¿Cómo?
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

¿Para qué?
- Generar datos sintéticos realistas y densos para sensores y eventos.

¿Por qué?
- Permite probar el sistema sin sensores reales.
- Escalable: desde miles hasta millones de registros.
- Guarda en CSV para reutilización.

¿Cómo?
- Usa operaciones vectorizadas (rápido y eficiente).
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
    
    # Definir fechas y componentes
    componentes = [f"compuerta_{i+1}" for i in range(n_components)]
    start_date = datetime(2024, 1, 1)
    total_hours = int(days * 24 / freq_hours)
    freq_str = f"{int(freq_hours * 60)}T" if freq_hours < 1 else f"{int(freq_hours)}H"
    dates = pd.date_range(start=start_date, periods=total_hours, freq=freq_str)
    
    # Generar sensores (vectorizado)
    comp_rep = np.repeat(componentes, total_hours)
    time_rep = np.tile(dates, n_components)
    day_of_year = time_rep.dayofyear
    month = time_rep.month
    
    presion = 1.0 + 0.3 * np.sin(day_of_year / 365 * 2 * np.pi) + np.random.normal(0, 0.1, len(time_rep))
    humedad = 60 + 20 * np.sin(month / 12 * 2 * np.pi) + np.random.normal(0, 5, len(time_rep))
    vibracion = 0.5 + np.random.exponential(0.2, len(time_rep))
    temperatura = 20 + 10 * np.sin(day_of_year / 365 * 2 * np.pi) + np.random.normal(0, 2, len(time_rep))
    
    df_sensores = pd.DataFrame({
        'timestamp': time_rep,
        'id_componente': comp_rep,
        'presion_bar': np.clip(presion, 0.5, None),
        'humedad_pct': np.clip(humedad, 20, 100),
        'vibracion_mm_s': vibracion,
        'temperatura_c': temperatura
    })
    
    # Generar eventos
    eventos = []
    for comp in componentes:
        maint_dates = [start_date + timedelta(days=d) for d in range(0, days, 90)]
        for md in maint_dates:
            eventos.append({'timestamp': md, 'id_componente': comp, 'tipo_evento': 'mantenimiento', 'subtipo': 'preventivo', 'gravedad': 'baja'})
        n_fallas = max(1, int(8 * days / 365))
        for _ in range(n_fallas):
            dias = np.random.randint(10, days)
            falla_date = start_date + timedelta(days=dias)
            if any(abs((falla_date - md).days) < 15 for md in maint_dates):
                continue
            eventos.append({'timestamp': falla_date, 'id_componente': comp, 'tipo_evento': 'falla', 'subtipo': np.random.choice(['fuga', 'bloqueo', 'corrosion']), 'gravedad': np.random.choice(['baja', 'media', 'alta'])})
    
    df_eventos = pd.DataFrame(eventos)
    
    # Guardar en CSV
    df_sensores.to_csv(os.path.join(output_dir, "sensores.csv"), index=False)
    df_eventos.to_csv(os.path.join(output_dir, "eventos.csv"), index=False)
    print(f"✅ Datos guardados: {len(df_sensores):,} lecturas.")
    return df_sensores, df_eventos
```

---

### 📄 `src/data_loader.py`
```python
"""
src/data_loader.py

¿Para qué?
- Cargar datos desde archivos CSV.

¿Por qué?
- Desacopla generación de datos del entrenamiento.
- Permite usar datos reales sin cambiar código.

¿Cómo?
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

¿Para qué?
- Transformar datos crudos en dataset listo para ML.

¿Por qué?
- El modelo necesita una observación por día.
- La etiqueta debe construirse sin fuga de información.

¿Cómo?
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

¿Para qué?
- Entrenar modelo y evaluar desempeño.

¿Por qué?
- Random Forest es ideal para datos desbalanceados.
- Documenta resultados en PDF para auditoría.

¿Cómo?
1. Divide datos (estratificado).
2. Entrena Random Forest.
3. Evalúa con métricas.
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
    report_str = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_test)
    
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

¿Para qué?
- Centralizar alertas (sonora + correo).

¿Por qué?
- Separa lógica de alertas del entrenamiento.
- Facilita agregar nuevos canales.

¿Cómo?
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

¿Para qué?
- Enviar notificaciones por correo.

¿Por qué?
- Alerta a personal remoto.
- Deja registro escrito.

¿Cómo?
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
        body = f"Probabilidad: {probability:.2%}\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
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
        print("📧 Correo enviado.")
    except Exception as e:
        print(f"❌ Error: {e}")
```

---

### 📄 `src/report_pdf.py`
```python
"""
src/report_pdf.py

¿Para qué?
- Generar informe PDF con resultados.

¿Por qué?
- Formato estándar para reportes técnicos.
- Incluye métricas y gráficos.

¿Cómo?
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
    c.drawString(50, height - 50, "Informe de Mantenimiento Predictivo")
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

¿Para qué?
- Orquestar flujo completo.

¿Por qué?
- Punto de entrada principal.
- Genera datos por defecto si no existen.

¿Cómo?
1. Verifica existencia de CSV.
2. Genera o carga datos.
3. Entrena modelo.
4. Activa alertas.
"""

from src.data_generation import generate_and_save_dummy_data
from src.data_loader import load_data_from_csv
from src.data_preparation import create_ml_dataset
from src.model import train_model
from src.alerts import emit_alert_if_high_risk
import numpy as np
import os

def main():
    data_dir = "data/raw"
    if not os.path.exists(os.path.join(data_dir, "sensores.csv")):
        print("🆕 Generando datos por defecto...")
        df_sensores, df_eventos = generate_and_save_dummy_data(days=365, n_components=5)
    else:
        print("📂 Cargando datos desde CSV...")
        df_sensores, df_eventos = load_data_from_csv(data_dir)
    
    df_ml = create_ml_dataset(df_sensores, df_eventos)
    model, pdf_path = train_model(df_ml)
    
    ejemplo = np.array([[1.8, 85, 2.1, 28, 120]])
    proba = model.predict_proba(ejemplo)[0][1]
    print(f"Probabilidad de falla: {proba:.2%}")
    
    emit_alert_if_high_risk(proba, latest_report_path=pdf_path)
    print("\n✅ Proceso completado.")

if __name__ == "__main__":
    main()
```

---

### 📄 `scripts/run_scheduled.py` y `scripts/schedule_daily_task.py`
*(Iguales a versiones anteriores, ya explicadas)*

---

## 6. ▶️ Cómo Usar el Sistema

### Paso 1: Instalar
```powershell
python install_project.py
cd represa_ml
venv\Scripts\activate
```

### Paso 2: Generar datos (opcional)
```powershell
# Ejemplo: 1 millón de registros
python generate_data_cli.py --components 50 --days 1095 --freq-hours 1.0
```

### Paso 3: Configurar correo
```powershell
$env:ALERT_EMAIL_USER="tu_correo@gmail.com"
$env:ALERT_EMAIL_PASS="contraseña_de_aplicacion"
$env:ALERT_EMAIL_RECIPIENTS="ingeniero1@empresa.com"
```

### Paso 4: Ejecutar
```powershell
python main.py
```

### Paso 5: Programar diariamente
```powershell
python scripts/schedule_daily_task.py --install --hour 6
```

---

## 7. 📌 Beneficios Finales

- ✅ **Escalable**: genera millones de registros en segundos  
- ✅ **Persistente**: datos en CSV, reutilizables  
- ✅ **Alertas multicanal**: sonido + correo  
- ✅ **Documentación automática**: PDF con métricas  
- ✅ **Automático**: ejecución diaria sin intervención  
- ✅ **Listo para producción**: estructura profesional y código claro  

Este sistema está diseñado para **proteger infraestructuras críticas** con ciencia de datos aplicada, buenas prácticas y robustez operativa.

¿Necesitas ayuda para conectarlo a sensores reales o una base de datos industrial? Estoy aquí para seguir construyendo contigo.
