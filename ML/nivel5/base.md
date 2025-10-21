# 📘 Guía Paso a Paso: Mantenimiento Predictivo de una Represa con Machine Learning

---

## 1. 🎯 ¿Cuál es la situación que queremos resolver?

**Contexto**:  
Una represa hidroeléctrica requiere mantenimiento continuo en componentes críticos (compuertas, muros, turbinas). Las fallas no anticipadas pueden causar interrupciones operativas, daños estructurales o riesgos ambientales.

**Objetivo del ML**:  
**Predecir la probabilidad de falla de un componente en los próximos 7 días**, usando datos históricos y en tiempo real, para planificar mantenimientos **antes** de que ocurran fallos.

---

## 2. ❓ ¿Qué preguntas puede responder el ML?

| Tipo de pregunta | Ejemplo concreto |
|------------------|------------------|
| **Clasificación binaria** | ¿Fallará el componente X en los próximos 7 días? (Sí/No) |
| **Regresión** | ¿Cuántos días faltan para que el sellado de la compuerta falle? |
| **Detección de anomalías** | ¿Es anómalo el aumento repentino de presión en el muro este? |
| **Priorización** | ¿Qué componente tiene mayor riesgo hoy y debe revisarse primero? |

> En este documento nos enfocamos en **clasificación binaria**: predecir falla sí/no en ventana de 7 días.

---

## 3. 📊 ¿Qué datos necesitamos y cómo los entendemos?

### 3.1. Fuentes de datos
- **Sensores IoT**: presión, humedad, vibración, temperatura.
- **Condiciones ambientales**: lluvia, caudal, nivel del embalse.
- **Registros de mantenimiento**: fechas, tipo, componente.
- **Registros de fallas**: cuándo y cómo falló un componente.

### 3.2. Características clave (features)
- Valores promedio, máximos y tendencias en ventanas móviles (ej. últimas 24h).
- Días desde el último mantenimiento.
- Acumulado de lluvia en 72h.
- Edad del componente.

### 3.3. Etiqueta (target)
- `falla_prox_7d = 1` si hubo falla en los 7 días posteriores a la observación.
- `= 0` en caso contrario.

> **Importante**: La etiqueta se construye **mirando al futuro**, pero el modelo solo usa datos **hasta el momento de la predicción**.

---

## 4. 🤖 ¿Qué modelo de ML usar y cómo interpretarlo?

### Modelo recomendado: **Random Forest**
- Robusto ante datos ruidosos.
- Maneja bien variables numéricas y categóricas.
- Permite interpretar la importancia de las variables.

### Interpretación:
- **Feature importance**: ¿Qué variable influye más en la predicción? (ej. "días desde mantenimiento").
- **Predicción por probabilidad**: `modelo.predict_proba()` → permite establecer umbrales (ej. alerta si prob > 0.7).

---

## 5. 🗂️ Estructura del proyecto

```
represa_ml/
│
├── data/
│   └── raw/                 # Datos crudos (vacío al inicio)
│
├── notebooks/               # Exploración inicial (opcional)
│
├── src/
│   ├── __init__.py
│   ├── data_generation.py   # Generador de datos dummy
│   ├── data_preparation.py  # Creación de features y etiquetas
│   ├── model.py             # Entrenamiento y evaluación
│   └── dashboard.py         # Dashboard interactivo (Streamlit)
│
├── models/
│   └── maintenance_model.pkl  # Modelo guardado
│
├── reports/                 # Salidas (gráficos, alertas)
│
├── requirements.txt
└── main.py                  # Script principal de ejecución
```

---

## 6. 💻 Código completo (con buenas prácticas)

### 📄 `requirements.txt`
```txt
pandas
numpy
scikit-learn
streamlit
joblib
matplotlib
```

---

### 📄 `src/data_generation.py`
```python
"""
Genera datos sintéticos realistas para una represa.
Simula componentes, sensores y eventos de falla/mantenimiento.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_dummy_data(days=365, n_components=5, seed=42):
    np.random.seed(seed)
    
    # Definir componentes
    componentes = [f"compuerta_{i+1}" for i in range(n_components)]
    
    # Fechas
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(hours=h) for h in range(days * 24)]
    
    records = []
    for comp in componentes:
        for dt in dates:
            # Simular lecturas de sensores con ruido y tendencias
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
    
    # Generar eventos de falla (más probables si no hay mantenimiento reciente)
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
        for _ in range(8):  # ~8 fallas por componente en el año
            dias = np.random.randint(10, days)
            falla_date = start_date + timedelta(days=dias)
            # Evitar fallas justo después de mantenimiento
            if any(abs((falla_date - md).days) < 15 for md in maint_dates):
                continue
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
Prepara los datos para entrenamiento de ML:
- Agrega features derivados
- Crea la etiqueta 'falla_prox_7d'
"""
import pandas as pd
import numpy as np

def create_ml_dataset(df_sensores, df_eventos, window_hours=24):
    """
    Crea un dataset por componente y ventana de tiempo.
    """
    # Agregar columna de fallas
    df_fallas = df_eventos[df_eventos['tipo_evento'] == 'falla'][['timestamp', 'id_componente']].copy()
    df_fallas = df_fallas.rename(columns={'timestamp': 'falla_timestamp'})
    
    # Resample sensores a ventanas diarias (promedio)
    df_sensores['date'] = df_sensores['timestamp'].dt.floor('D')
    df_daily = df_sensores.groupby(['id_componente', 'date']).agg({
        'presion_bar': 'mean',
        'humedad_pct': 'mean',
        'vibracion_mm_s': 'mean',
        'temperatura_c': 'mean'
    }).reset_index()
    
    # Calcular días desde último mantenimiento
    df_mant = df_eventos[df_eventos['tipo_evento'] == 'mantenimiento'][['timestamp', 'id_componente']].copy()
    df_mant = df_mant.rename(columns={'timestamp': 'mant_timestamp'})
    
    # Para cada día, encontrar último mantenimiento
    df_daily['dias_desde_mant'] = df_daily.apply(
        lambda row: min([
            (row['date'] - mant_row['mant_timestamp']).days
            for _, mant_row in df_mant[df_mant['id_componente'] == row['id_componente']].iterrows()
            if row['date'] >= mant_row['mant_timestamp']
        ], default=365), axis=1
    )
    
    # Etiqueta: ¿hubo falla en los próximos 7 días?
    df_daily['falla_prox_7d'] = df_daily.apply(
        lambda row: any(
            (falla_row['falla_timestamp'] > row['date']) and
            (falla_row['falla_timestamp'] <= row['date'] + pd.Timedelta(days=7)) and
            (falla_row['id_componente'] == row['id_componente'])
            for _, falla_row in df_fallas.iterrows()
        ), axis=1
    ).astype(int)
    
    # Eliminar filas con datos futuros (últimos 7 días no tienen etiqueta completa)
    cutoff_date = df_daily['date'].max() - pd.Timedelta(days=7)
    df_final = df_daily[df_daily['date'] <= cutoff_date].copy()
    
    return df_final
```

---

### 📄 `src/model.py`
```python
"""
Entrena y evalúa un modelo de clasificación para predicción de fallas.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

FEATURES = ['presion_bar', 'humedad_pct', 'vibracion_mm_s', 'temperatura_c', 'dias_desde_mant']
TARGET = 'falla_prox_7d'

def train_model(df, model_path='models/maintenance_model.pkl'):
    X = df[FEATURES]
    y = df[TARGET]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluar
    y_pred = model.predict(X_test)
    print("=== Reporte de Clasificación ===")
    print(classification_report(y_test, y_pred))
    print("=== Matriz de Confusión ===")
    print(confusion_matrix(y_test, y_pred))
    
    # Guardar modelo
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Modelo guardado en: {model_path}")
    return model

def load_model(model_path='models/maintenance_model.pkl'):
    return joblib.load(model_path)
```

---

### 📄 `src/dashboard.py`
```python
"""
Dashboard interactivo con Streamlit para visualizar predicciones.
"""
import streamlit as st
import pandas as pd
import numpy as np
from model import load_model, FEATURES

def run_dashboard():
    st.set_page_config(page_title="Mantenimiento Predictivo - Represa", layout="wide")
    st.title("🔍 Dashboard de Mantenimiento Predictivo")
    st.markdown("Predice fallas en componentes de la represa en los próximos 7 días.")
    
    try:
        model = load_model()
    except:
        st.error("⚠️ Modelo no encontrado. Ejecuta `main.py` primero para entrenarlo.")
        return
    
    st.sidebar.header("🔧 Parámetros del componente")
    presion = st.sidebar.slider("Presión (bar)", 0.5, 3.0, 1.2)
    humedad = st.sidebar.slider("Humedad (%)", 20, 100, 65)
    vibracion = st.sidebar.slider("Vibración (mm/s)", 0.0, 5.0, 0.8)
    temperatura = st.sidebar.slider("Temperatura (°C)", 0, 40, 22)
    dias_mant = st.sidebar.number_input("Días desde último mantenimiento", 0, 365, 45)
    
    input_data = np.array([[presion, humedad, vibracion, temperatura, dias_mant]])
    proba = model.predict_proba(input_data)[0]
    prediccion = model.predict(input_data)[0]
    
    st.subheader("📊 Resultado de la predicción")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Riesgo de falla (7 días)", f"{proba[1]:.1%}")
    with col2:
        if prediccion == 1 and proba[1] > 0.7:
            st.error("🚨 ALTA PROBABILIDAD DE FALLA")
        else:
            st.success("✅ Riesgo bajo")
    
    st.subheader("📈 Importancia de variables")
    importances = model.feature_importances_
    importance_df = pd.DataFrame({'Variable': FEATURES, 'Importancia': importances})
    st.bar_chart(importance_df.set_index('Variable'))
```

---

### 📄 `main.py`
```python
"""
Script principal: genera datos, entrena modelo y guarda resultados.
"""
from src.data_generation import generate_dummy_data
from src.data_preparation import create_ml_dataset
from src.model import train_model

def main():
    print("🚀 Generando datos sintéticos...")
    df_sensores, df_eventos = generate_dummy_data(days=365, n_components=5)
    
    print("🧼 Preparando dataset para ML...")
    df_ml = create_ml_dataset(df_sensores, df_eventos)
    print(f"Dataset listo: {df_ml.shape[0]} muestras, {df_ml['falla_prox_7d'].sum()} fallas positivas.")
    
    print("🧠 Entrenando modelo...")
    train_model(df_ml)
    
    print("✅ Proceso completado. Ejecuta 'streamlit run src/dashboard.py' para ver el dashboard.")

if __name__ == "__main__":
    main()
```

---

## 7. ▶️ Cómo ejecutar el proyecto

1. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generar datos y entrenar modelo**:
   ```bash
   python main.py
   ```

4. **Iniciar dashboard**:
   ```bash
   streamlit run src/dashboard.py
   ```

---

## 8. 📌 Conclusión

Este proyecto te entrega:

- Una **base sólida** para mantenimiento predictivo en represas.
- **Datos realistas** generados programáticamente.
- Un **modelo interpretable** con métricas claras.
- Un **dashboard interactivo** para toma de decisiones.
- Código **modular, documentado y escalable**.

Puedes extenderlo fácilmente:
- Agregar más sensores.
- Usar XGBoost para mejor precisión.
- Exportar alertas a Excel o correo.
- Integrar con APIs de sensores reales.

¿Te gustaría que prepare un script adicional para **exportar reportes automáticos en PDF** o **activar alertas sonoras en Windows** cuando el riesgo es alto? Estoy listo para ayudarte a llevarlo al siguiente nivel.
