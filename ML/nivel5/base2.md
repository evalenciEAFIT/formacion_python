# 📘 Guía Paso a Paso: Sistema de Mantenimiento Predictivo para Represas con Machine Learning

---

## 1. 🎯 Objetivo del sistema

**Problema**:  
Las represas son infraestructuras críticas. Fallas no anticipadas pueden causar daños estructurales, interrupciones energéticas o riesgos ambientales.

**Solución**:  
Un sistema automatizado que:
- Monitorea sensores y condiciones operativas.
- **Predice fallas 7 días antes** usando ML.
- **Alerta al equipo técnico** mediante:
  - Sonido local (en centro de control)
  - Correo electrónico (para personal remoto)
- **Documenta resultados** en informes PDF.
- **Se ejecuta diariamente sin intervención humana**.

---

## 2. ❓ Preguntas que resuelve el ML

| Tipo | Pregunta | Acción derivada |
|------|--------|------------------|
| Clasificación | ¿Fallará el componente X en los próximos 7 días? | Activar alerta si prob > 70% |
| Ranking | ¿Qué componente tiene mayor riesgo hoy? | Priorizar inspección |
| Tendencia | ¿Está empeorando la vibración en la turbina? | Programar mantenimiento preventivo |

> Enfoque principal: **clasificación binaria con umbral de probabilidad**.

---

## 3. 📊 Datos necesarios

### Fuentes:
- **Sensores IoT**: presión, humedad, vibración, temperatura.
- **Ambientales**: lluvia acumulada, nivel del embalse.
- **Históricos**: fechas de mantenimiento y fallas.

### Etiqueta (`target`):
- `falla_prox_7d = 1` si hubo falla en los 7 días posteriores a la observación.
- `= 0` en caso contrario.

> **Importante**: la etiqueta se construye mirando al futuro, pero el modelo solo usa datos pasados → evita *data leakage*.

---

## 4. 🤖 Modelo de ML

- **Algoritmo**: `RandomForestClassifier`
- **Ventajas**:
  - Maneja datos desbalanceados (pocas fallas).
  - No requiere normalización.
  - Proporciona **importancia de variables** → interpretable.
- **Salida**:
  - Predicción binaria
  - Probabilidad de falla
  - Métricas de desempeño (precisión, recall, F1)

---

## 5. 🗂️ Estructura del proyecto

```
represa_ml/
├── install_project.py          ← Instalador automático
├── requirements.txt
├── main.py
├── data/
├── models/
├── reports/                    ← Informes PDF
├── logs/                       ← Registros diarios
├── scripts/
│   ├── schedule_daily_task.py  ← Gestiona tarea programada
│   └── run_scheduled.py        ← Ejecuta main.py diariamente
├── src/
│   ├── __init__.py
│   ├── data_generation.py      ← Genera datos dummy
│   ├── data_preparation.py     ← Crea features y etiquetas
│   ├── model.py                ← Entrena y evalúa modelo
│   ├── alerts.py               ← Alerta sonora
│   ├── email_alert.py          ← Notificación por correo ✨
│   └── report_pdf.py           ← Genera informe PDF
└── venv/
```

---

## 6. 💻 Código clave (con comentarios explicativos)

### 📄 `src/email_alert.py`
```python
"""
Envía notificaciones por correo electrónico cuando se detecta ALTO RIESGO.

Propósito:
- Alertar a ingenieros o supervisores remotos cuando la probabilidad de falla > umbral.
- Complementa la alerta sonora local (útil si nadie está en el centro de control).

¿Por qué correo?
- Es universal, asíncrono y deja registro.
- Ideal para equipos distribuidos.

Configuración requerida:
- Correo remitente (ej. Gmail, Outlook)
- Contraseña de aplicación (no contraseña personal)
- Lista de destinatarios

Cómo funciona:
1. Usa SMTP (estándar de envío de correo).
2. Crea mensaje con asunto y cuerpo claro.
3. Adjunta informe PDF si está disponible.
4. Maneja errores silenciosamente (no detiene el flujo principal).
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def send_email_alert(
    probability: float,
    threshold: float = 0.7,
    latest_report_path: str = None
):
    """
    Envía un correo si la probabilidad supera el umbral.

    Parámetros:
    - probability: probabilidad de falla (0.0–1.0)
    - threshold: umbral para activar alerta (por defecto 0.7)
    - latest_report_path: ruta al último informe PDF (opcional, para adjuntar)
    """
    if probability <= threshold:
        return  # No hay alerta

    # Configuración desde variables de entorno (mejor que hardcodear)
    sender_email = os.getenv("ALERT_EMAIL_USER")
    sender_password = os.getenv("ALERT_EMAIL_PASS")
    recipients = os.getenv("ALERT_EMAIL_RECIPIENTS", "").split(",")

    if not sender_email or not sender_password or not recipients[0]:
        print("📧 Correo no configurado. Define ALERT_EMAIL_USER, ALERT_EMAIL_PASS y ALERT_EMAIL_RECIPIENTS.")
        return

    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = "🚨 ALERTA: Alto riesgo de falla en represa"

        body = f"""
        Se ha detectado un alto riesgo de falla en un componente de la represa.

        - Probabilidad estimada: {probability:.2%}
        - Umbral de alerta: {threshold:.0%}
        - Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        Por favor, revise el sistema inmediatamente.
        """
        msg.attach(MIMEText(body, "plain"))

        # Adjuntar informe PDF si existe
        if latest_report_path and os.path.exists(latest_report_path):
            with open(latest_report_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(latest_report_path)}"
            )
            msg.attach(part)

        # Enviar correo
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Cambia si usas Outlook, etc.
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()

        print("📧 Correo de alerta enviado exitosamente.")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")
```

---

### 📄 `src/alerts.py` (actualizado)
```python
"""
Integra alerta sonora y por correo.

Propósito:
- Centralizar todas las alertas en una sola función.
- Facilitar futuras extensiones (SMS, Slack, etc.).
"""

import os
from .email_alert import send_email_alert

def emit_alert_if_high_risk(
    probability: float,
    threshold: float = 0.7,
    latest_report_path: str = None
):
    """
    Activa alertas sonora y por correo si el riesgo es alto.
    """
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

### 📄 `src/report_pdf.py` (actualizado para devolver ruta)
```python
# ... (código anterior igual) ...

def generate_pdf_report(...):
    # ... (código anterior) ...
    c.save()
    print(f"📄 Informe PDF generado: {pdf_path}")
    return pdf_path  # ← Devuelve la ruta para usar en alertas
```

---

### 📄 `src/model.py` (actualizado)
```python
# ... (al final de train_model) ...
if generate_report:
    pdf_path = generate_pdf_report(...)  # Captura la ruta
    return model, pdf_path
return model, None
```

---

### 📄 `main.py` (actualizado)
```python
# ... (después de entrenar) ...
model, latest_pdf = train_model(df_ml)

# Predicción de ejemplo
ejemplo = np.array([[1.8, 85, 2.1, 28, 120]])
proba = model.predict_proba(ejemplo)[0][1]

# Activar alertas (sonora + correo)
emit_alert_if_high_risk(proba, threshold=0.7, latest_report_path=latest_pdf)
```

---

## 7. 🔐 Configuración de correo (segura)

Nunca guardes contraseñas en el código. Usa **variables de entorno**:

### En Windows (PowerShell):
```powershell
$env:ALERT_EMAIL_USER="tu_correo@gmail.com"
$env:ALERT_EMAIL_PASS="tu_contraseña_de_aplicacion"
$env:ALERT_EMAIL_RECIPIENTS="ingeniero1@empresa.com,ingeniero2@empresa.com"
```

> 💡 **Importante**: usa **contraseña de aplicación** (no tu contraseña de Gmail).  
> Guía: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

---

## 8. 📅 Ejecución diaria automatizada

Ya cubierta en `scripts/schedule_daily_task.py` y `scripts/run_scheduled.py`.

Cada día:
1. Se ejecuta `run_scheduled.py`
2. Se entrena el modelo con datos actualizados (si los hubiera)
3. Se genera nuevo PDF
4. Se evalúa riesgo → se envían alertas si aplica

---

## 9. ▶️ Flujo de uso completo

### Primera vez:
```powershell
# 1. Instalar proyecto
python install_project.py

# 2. Configurar variables de entorno (correo)
$env:ALERT_EMAIL_USER="..."
$env:ALERT_EMAIL_PASS="..."
$env:ALERT_EMAIL_RECIPIENTS="..."

# 3. Probar manualmente
.\venv\Scripts\activate
python main.py
```

### Programar diariamente:
```powershell
# Ejecutar como administrador
python scripts/schedule_daily_task.py --install --hour 6
```

### Usar dashboard:
```powershell
streamlit run src/dashboard.py
```

---

## 10. 📌 Beneficios finales

- ✅ **Alertas multicanal**: sonido + correo
- ✅ **Documentación automática**: PDF diario
- ✅ **Ejecución sin intervención**: Task Scheduler
- ✅ **Seguridad**: contraseñas en variables de entorno
- ✅ **Código explicado**: cada función tiene su "qué, cómo y por qué"
- ✅ **Listo para producción**: estructura profesional y escalable

---

¿Te gustaría ahora agregar **exportación de alertas a Excel** o **integración con una API de sensores reales**? Estoy listo para seguir construyendo contigo este sistema de monitoreo inteligente.
