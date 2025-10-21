# 📘 Guía Paso a Paso: Sistema de Mantenimiento Predictivo para Represas con Machine Learning

---

## 1. 🎯 ¿Cuál es el problema?

Las represas son infraestructuras críticas. Una falla no anticipada en compuertas, muros o turbinas puede causar:
- Riesgos de seguridad (inundaciones, colapsos)
- Interrupciones en el suministro de agua o energía
- Costos elevados de reparación de emergencia

**Solución tradicional**: mantenimiento programado cada X meses → ineficiente (se mantiene lo que no necesita, y se descuida lo que sí).

**Solución inteligente**: usar **Machine Learning (ML)** para predecir fallas **antes de que ocurran**, basado en datos reales.

---

## 2. ❓ ¿Qué preguntas responde el ML?

| Pregunta | Tipo de modelo | Acción derivada |
|--------|----------------|------------------|
| ¿Fallará este componente en los próximos 7 días? | Clasificación binaria | Activar alerta si probabilidad > 70% |
| ¿Qué componente tiene mayor riesgo hoy? | Ranking por probabilidad | Priorizar inspección técnica |
| ¿Es normal este aumento de presión? | Detección de anomalías | Revisar sensores o estructura |

> En este proyecto: **clasificación binaria** → "¿Falla en 7 días? Sí/No".

---

## 3. 🌳 ¿Qué es Random Forest? (Explicación clara y completa)

### Definición simple:
**Random Forest** (Bosque Aleatorio) es un algoritmo de ML que combina **muchos árboles de decisión** para tomar una decisión más precisa y robusta.

### ¿Cómo funciona?
1. **Árbol de decisión**: un modelo que hace preguntas tipo "¿presión > 1.5 bar?" y sigue ramas hasta una predicción.
2. **Problema**: un solo árbol puede sobreajustarse (aprender ruido, no patrones reales).
3. **Solución**: Random Forest crea **cientos de árboles**, cada uno entrenado con:
   - Una **muestra aleatoria** de los datos (con reemplazo → *bootstrap*)
   - Un **subconjunto aleatorio** de variables en cada división
4. **Predicción final**: votación mayoritaria (clasificación) o promedio (regresión) de todos los árboles.

### ¿Por qué usarlo en mantenimiento predictivo?
- ✅ Maneja bien datos desbalanceados (pocas fallas vs muchos días sin falla)
- ✅ No requiere normalización de datos
- ✅ Proporciona **importancia de variables** → interpretable
- ✅ Resistente al ruido y a valores atípicos

> En resumen: **más árboles = menos error, más estabilidad**.

---

## 4. 📊 Métricas de desempeño: Precisión, Recall y F1-Score

En problemas de mantenimiento, **no todas las fallas son iguales**. Un falso negativo (decir "no fallará" cuando sí fallará) es mucho más grave que un falso positivo (decir "fallará" cuando no).

### Matriz de confusión (base de todo):
|                     | **Predicho: No falla** | **Predicho: Falla** |
|---------------------|------------------------|---------------------|
| **Real: No falla**  | Verdadero Negativo (VN) | Falso Positivo (FP) |
| **Real: Falla**     | **Falso Negativo (FN)** | Verdadero Positivo (VP) |

> **FN es el peor error**: falla real no detectada.

### Métricas clave:

#### 1. **Precisión (Precision)**
> ¿De todas las veces que dijimos "va a fallar", cuántas veces tuvimos razón?

\[
\text{Precisión} = \frac{VP}{VP + FP}
\]

- Alta precisión → pocas falsas alarmas.
- Útil si el costo de una falsa alarma es alto (ej. parar operación innecesariamente).

#### 2. **Recall (Sensibilidad o Tasa de Verdaderos Positivos)**
> ¿De todas las fallas reales, cuántas detectamos?

\[
\text{Recall} = \frac{VP}{VP + FN}
\]

- Alto recall → detectamos casi todas las fallas.
- **Crítico en mantenimiento predictivo**: queremos minimizar FN.

#### 3. **F1-Score**
> Promedio armónico entre precisión y recall. Útil cuando hay desbalance.

\[
F1 = 2 \cdot \frac{\text{Precisión} \cdot \text{Recall}}{\text{Precisión} + \text{Recall}}
\]

- Valor entre 0 y 1. Cuanto más cerca de 1, mejor.
- Ideal cuando necesitas equilibrar falsas alarmas y fallas no detectadas.

> **En represas: priorizamos RECALL alto**, aunque aumente ligeramente las falsas alarmas.

---

## 5. 📊 Datos necesarios

### Fuentes:
- **Sensores**: presión, humedad, vibración, temperatura (cada hora)
- **Ambientales**: lluvia acumulada (24h, 72h), nivel del embalse
- **Históricos**: fechas de mantenimiento y fallas

### Etiqueta (`target`):
- `falla_prox_7d = 1` si hubo falla en los próximos 7 días desde esa observación.
- `= 0` en caso contrario.

> **Clave**: la etiqueta se construye mirando al futuro, pero el modelo solo usa datos **hasta ese momento** → evita fuga de información.

---

## 6. 🗂️ Estructura del proyecto

```
represa_ml/
├── install_project.py          ← Instalador automático
├── requirements.txt
├── main.py                     ← Flujo principal
├── data/                       ← Datos crudos
├── models/                     ← Modelo entrenado (.pkl)
├── reports/                    ← Informes PDF generados
├── logs/                       ← Registros diarios
├── scripts/
│   ├── schedule_daily_task.py  ← Gestiona tarea programada
│   └── run_scheduled.py        ← Ejecuta main.py diariamente
└── src/
    ├── __init__.py
    ├── data_generation.py      ← Genera datos dummy realistas
    ├── data_preparation.py     ← Crea features y etiquetas
    ├── model.py                ← Entrena modelo y evalúa métricas
    ├── alerts.py               ← Alerta sonora + correo
    ├── email_alert.py          ← Envía notificaciones por email
    └── report_pdf.py           ← Genera informe PDF con métricas y gráficos
```

---

## 7. 💻 Código clave (con comentarios explicativos)

### 📄 `src/model.py` (fragmento relevante)
```python
# Entrenar modelo
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluar
y_pred = model.predict(X_test)
report_str = classification_report(y_test, y_pred)  # Incluye precisión, recall, F1
cm = confusion_matrix(y_test, y_pred)
```

El `classification_report` muestra algo como:
```
              precision    recall  f1-score   support
           0       0.98      0.99      0.99      1420
           1       0.85      0.76      0.80        80
```
→ Para la clase `1` (falla):  
- **Precisión = 85%**: 85 de cada 100 alertas fueron reales.  
- **Recall = 76%**: detectamos 76 de cada 100 fallas reales.  
- **F1 = 80%**: buen equilibrio.

---

## 8. 🔔 Alertas y notificaciones

### Alerta sonora (Windows)
- Usa `winsound.MessageBeep()` → sonido del sistema.
- Solo si `probabilidad > 0.7`.

### Notificación por correo
- Se envía a lista de ingenieros.
- Incluye:
  - Probabilidad de falla
  - Fecha y hora
  - **Informe PDF adjunto** (con métricas y gráficos)

> Configuración segura: credenciales en **variables de entorno**, nunca en código.

---

## 9. 📄 Informe PDF automático

Cada entrenamiento genera un PDF en `reports/` con:
- Resumen de datos (muestras, fallas)
- Métricas (precisión, recall, F1)
- Matriz de confusión
- Gráfico de importancia de variables

Ejemplo de uso en `main.py`:
```python
model, pdf_path = train_model(df_ml)
emit_alert_if_high_risk(proba, latest_report_path=pdf_path)
```

---

## 10. 📅 Ejecución diaria automatizada

### Componentes:
- `scripts/run_scheduled.py`: wrapper que activa venv y ejecuta `main.py`
- `scripts/schedule_daily_task.py`: instala/elimina tarea en Task Scheduler

### Comando para programar a las 6:00 AM:
```powershell
python scripts/schedule_daily_task.py --install --hour 6
```

Cada día:
1. Se generan datos actualizados (o se cargarían datos reales en producción)
2. Se entrena el modelo
3. Se genera informe PDF
4. Se evalúa riesgo → se envían alertas si aplica

---

## 11. ▶️ Cómo empezar (resumen de pasos)

1. **Ejecutar instalador**:
   ```bash
   python install_project.py
   ```

2. **Configurar correo** (PowerShell):
   ```powershell
   $env:ALERT_EMAIL_USER="tu_correo@gmail.com"
   $env:ALERT_EMAIL_PASS="contraseña_de_aplicacion"
   $env:ALERT_EMAIL_RECIPIENTS="ingeniero1@empresa.com,ingeniero2@empresa.com"
   ```

3. **Probar manualmente**:
   ```bash
   venv\Scripts\activate
   python main.py
   ```

4. **Programar diariamente** (como administrador):
   ```bash
   python scripts/schedule_daily_task.py --install --hour 6
   ```

5. **Usar dashboard interactivo**:
   ```bash
   streamlit run src/dashboard.py
   ```

---

## 12. 📌 Beneficios finales

- ✅ **Prevención real**: detecta fallas antes de que ocurran
- ✅ **Decisiones basadas en datos**: no en suposiciones
- ✅ **Alertas multicanal**: sonido local + correo remoto
- ✅ **Auditable**: cada ejecución deja PDF y log
- ✅ **Automático**: funciona sin intervención diaria
- ✅ **Interpretable**: sabes por qué el modelo alerta (importancia de variables)

