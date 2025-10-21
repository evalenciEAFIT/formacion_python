# 📘 Guía Completa: Mantenimiento Predictivo en Represas con Machine Learning  
## Enfoque Profundo en Random Forest y Comparación con Otros Modelos

## 1. 🌊 Situación del problema: El desafío del mantenimiento en represas

### 1.1. Contexto operativo
Las represas son **infraestructuras críticas** que:
- Almacenan agua para consumo humano, riego y generación hidroeléctrica.
- Controlan caudales para prevenir inundaciones.
- Soportan cargas hidrostáticas, ambientales y estructurales extremas durante décadas.

### 1.2. Consecuencias de una falla no anticipada
| Tipo de impacto | Descripción |
|----------------|-------------|
| **Seguridad** | Riesgo de colapso, inundaciones, pérdida de vidas humanas |
| **Ambiental** | Contaminación por liberación de sedimentos, alteración de ecosistemas acuáticos |
| **Económico** | Costos de reparación de emergencia (hasta 10x más caros que mantenimiento preventivo) |
| **Operativo** | Interrupción del suministro de agua o energía eléctrica |

### 1.3. Limitaciones de los enfoques tradicionales
| Enfoque | Descripción | Problemas |
|--------|-------------|----------|
| **Correctivo** | Se actúa después de la falla | Alto riesgo, alto costo, daño colateral |
| **Preventivo por tiempo** | Mantenimiento programado cada X meses | Ineficiente: se mantiene lo que no necesita, se descuida lo que sí |
| **Preventivo por condición** | Inspecciones visuales periódicas | Subjetivo, costoso, no predictivo |

### 1.4. La solución con Machine Learning
El **mantenimiento predictivo** transforma datos en **acciones anticipadas**:
- **Predecir fallas 7 días antes** de que ocurran.
- **Optimizar recursos**: intervenir solo cuando es necesario.
- **Reducir riesgos**: anticipar problemas críticos con base en evidencia.

> **Objetivo del sistema**:  
> **Predecir si un componente crítico (compuerta, muro, turbina) fallará en los próximos 7 días**, usando datos de sensores, condiciones ambientales e historial de mantenimiento.

---

## 2. 🤖 Modelos de Machine Learning para Mantenimiento Predictivo: Análisis Comparativo Profundo

### 2.1. Características del problema en represas
Antes de elegir un modelo, debemos entender las **características del problema**:

| Característica | Descripción | Implicación para el modelo |
|---------------|-------------|---------------------------|
| **Datos desbalanceados** | Pocas fallas reales vs muchos días sin falla (ej. 400 fallas / 1.3M observaciones) | El modelo debe manejar clases desbalanceadas |
| **Interpretabilidad** | Los ingenieros deben entender por qué se predice una falla | Se requiere un modelo interpretable |
| **Robustez al ruido** | Los sensores pueden tener lecturas erróneas | El modelo debe ser resistente a valores atípicos |
| **No linealidades** | Las relaciones entre variables no son lineales (ej. presión vs falla) | Se necesitan modelos no lineales |
| **Características mixtas** | Variables numéricas (presión) y derivadas (días desde mantenimiento) | El modelo debe manejar ambos tipos |

---

### 2.2. Comparación detallada de modelos candidatos

#### 📊 Tabla comparativa: Random Forest vs Otros Modelos

| Criterio | **Random Forest** | Regresión Logística | SVM | Redes Neuronales | Árbol de Decisión |
|---------|-------------------|---------------------|-----|------------------|-------------------|
| **Manejo de datos desbalanceados** | ✅ Excelente (con ajustes) | ❌ Pobre | ⚠️ Moderado | ⚠️ Requiere balanceo | ❌ Pobre |
| **Interpretabilidad** | ✅ Alta (importancia de variables) | ✅ Alta (coeficientes) | ❌ Baja | ❌ Muy baja | ✅ Alta |
| **Robustez al ruido** | ✅ Alta (promedio de árboles) | ❌ Baja | ⚠️ Moderada | ⚠️ Moderada | ❌ Baja |
| **No linealidades** | ✅ Excelente | ❌ No maneja | ✅ Con kernels | ✅ Excelente | ✅ Buena |
| **Requiere normalización** | ❌ No | ✅ Sí | ✅ Sí | ✅ Sí | ❌ No |
| **Tiempo de entrenamiento** | ⚠️ Moderado | ✅ Rápido | ❌ Lento (grandes datos) | ❌ Muy lento | ✅ Rápido |
| **Parámetros a ajustar** | ⚠️ Pocos | ✅ Muy pocos | ❌ Muchos | ❌ Muchos | ✅ Pocos |
| **Sobreajuste** | ✅ Bajo (ensemble) | ✅ Bajo | ⚠️ Moderado | ❌ Alto | ❌ Muy alto |

---

### 2.3. ¿Por qué Random Forest es la mejor opción para represas?

#### ✅ Ventajas específicas para el contexto de represas:

1. **Manejo natural de datos desbalanceados**  
   Random Forest puede ajustarse para dar más peso a la clase minoritaria (fallas) mediante el parámetro `class_weight='balanced'`, lo que es crucial cuando las fallas representan menos del 0.1% de los datos.

2. **Interpretabilidad operativa**  
   La **importancia de variables** permite a los ingenieros entender qué factores contribuyen más a la predicción:
   - Si `dias_desde_mant` es la variable más importante → refuerza la importancia del mantenimiento periódico.
   - Si `vibracion_mm_s` es clave → indica problemas mecánicos inminentes.

3. **Robustez sin preprocesamiento complejo**  
   No requiere normalización, maneja valores faltantes razonablemente bien, y es resistente a outliers (común en sensores).

4. **Captura de interacciones complejas**  
   Puede modelar relaciones no lineales como:  
   *"Alta presión + alta humedad + muchos días sin mantenimiento = alto riesgo"*  
   sin necesidad de crear manualmente variables de interacción.

5. **Estabilidad y reproducibilidad**  
   El promedio de muchos árboles reduce la varianza, haciendo que el modelo sea estable ante pequeños cambios en los datos.

#### 🆚 Comparación con casos específicos:

- **vs Regresión Logística**:  
  La regresión logística asume relaciones lineales y no captura interacciones complejas sin ingeniería de características manual. En represas, las relaciones son inherentemente no lineales.

- **vs Redes Neuronales**:  
  Aunque las redes neuronales pueden modelar cualquier función, son "cajas negras" que no permiten a los ingenieros entender por qué se predice una falla. En infraestructuras críticas, la interpretabilidad es tan importante como la precisión.

- **vs Árbol de Decisión individual**:  
  Un solo árbol se sobreajusta fácilmente a los datos de entrenamiento, especialmente con ruido en sensores. Random Forest promedia muchos árboles, reduciendo drásticamente el sobreajuste.

---

### 2.4. ¿Cuándo NO usar Random Forest?

Aunque Random Forest es ideal para la mayoría de escenarios de mantenimiento predictivo, hay casos donde otros modelos podrían ser mejores:

| Escenario | Modelo alternativo | Razón |
|----------|-------------------|-------|
| **Datos en tiempo real con latencia crítica** (< 10ms) | Regresión Logística | Random Forest es más lento en predicción |
| **Imágenes de inspección visual** | Redes Neuronales Convolucionales | Random Forest no maneja imágenes |
| **Series temporales con patrones complejos** | LSTM | Random Forest no modela secuencias |
| **Dataset extremadamente grande** (> 10M filas) | XGBoost | Más eficiente computacionalmente |

> **En el caso de represas con sensores tabulares**: **Random Forest sigue siendo la mejor opción**.

---

## 3. 🗃️ Modelo de datos para mantenimiento predictivo

### 3.1. Fuentes de datos y variables clave

| Fuente | Variables | Frecuencia | Importancia |
|--------|----------|------------|-------------|
| **Sensores IoT** | Presión (bar), Humedad (%), Vibración (mm/s), Temperatura (°C) | Cada hora | Alta: indican estado físico |
| **Condiciones ambientales** | Lluvia acumulada (24h, 72h), Caudal del río, Nivel del embalse | Diaria | Media: contexto operativo |
| **Historial de mantenimiento** | Fecha último mantenimiento, Tipo de mantenimiento, Componente intervenido | Eventual | Alta: predictor clave |
| **Registros de fallas** | Fecha, Tipo de falla, Gravedad, Componente afectado | Eventual | Crítica: etiqueta para supervisión |

### 3.2. Modelo conceptual (entidades y relaciones)

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│  Componente │───────│   LecturaSensor  │       │   Evento    │
└─────────────┘       └──────────────────┘       └─────────────┘
• id_componente        • timestamp                • timestamp
• tipo                 • id_componente            • id_componente
• ubicacion            • presion_bar              • tipo_evento
• fecha_instalacion    • humedad_pct              • subtipo
                       • vibracion_mm_s           • gravedad
                       • temperatura_c
```

### 3.3. Dataset para Machine Learning (vista lógica)

Cada fila representa **una observación diaria por componente**:

| Campo | Tipo | Descripción | Ejemplo |
|------|------|-------------|---------|
| `presion_bar` | float | Presión promedio del día | 1.45 |
| `humedad_pct` | float | Humedad relativa promedio | 78.2 |
| `vibracion_mm_s` | float | Vibración promedio | 1.8 |
| `temperatura_c` | float | Temperatura promedio | 24.5 |
| `dias_desde_mant` | int | Días desde último mantenimiento | 142 |
| `lluvia_72h_mm` | float | Lluvia acumulada en 72h | 125.0 |
| `falla_prox_7d` | binario | **Etiqueta**: ¿falla en próximos 7 días? | 1 |

> **Clave metodológica**: la etiqueta `falla_prox_7d` se construye **mirando al futuro**, pero el modelo solo usa datos **hasta el momento de la predicción** → evita fuga de información (data leakage).

---

## 4. 🗂️ Estructura del proyecto y justificación

```
represa_ml/
│
├── data/                    ← Datos crudos y procesados
│   └── raw/                 ← CSV generados o reales
│
├── models/                  ← Modelos entrenados (.pkl)
│
├── reports/                 ← Informes PDF automáticos
│
├── logs/                    ← Registros de ejecuciones programadas
│
├── src/                     ← Código fuente modular
│   ├── data_generation.py   ← Genera datos sintéticos
│   ├── data_loader.py       ← Carga datos desde CSV
│   ├── data_preparation.py  ← Crea features y etiquetas
│   ├── model.py             ← Entrena y evalúa modelo
│   ├── alerts.py            ← Gestiona alertas (sonora + correo)
│   ├── email_alert.py       ← Envía notificaciones por email
│   └── report_pdf.py        ← Genera informe PDF
│
├── scripts/                 ← Automatización
│   ├── run_scheduled.py     ← Wrapper para tarea programada
│   └── schedule_daily_task.py ← Gestiona Task Scheduler
│
├── main.py                  ← Flujo principal de ejecución
├── generate_data_cli.py     ← CLI para generar datos personalizados
├── requirements.txt         ← Dependencias
└── install_project.py       ← Instalador automático
```

### Justificación de la arquitectura
- **Separación de responsabilidades**: cada módulo tiene un propósito único y claro.
- **Reproducibilidad**: datos, código y resultados están organizados para auditoría.
- **Escalabilidad**: fácil agregar nuevos sensores, modelos o canales de alerta.
- **Mantenibilidad**: código modular, bien comentado y con manejo de errores.

---

## 5. 💻 Implementación en Python: Códigos Completos y Explicados

*(Los códigos completos con comentarios detallados "¿para qué?, ¿por qué?, ¿cómo?" se mantienen igual que en la versión anterior, ya que ya cumplen con los requisitos de documentación profunda.)*

---

## 6. 📊 Evaluación del modelo: Métricas explicadas para represas

### 6.1. Matriz de confusión adaptada al contexto

|                     | **Predicho: Seguro** | **Predicho: Riesgo** |
|---------------------|----------------------|----------------------|
| **Real: Seguro**    | VN = Correcto        | FP = Falsa alarma    |
| **Real: Riesgo**    | **FN = FALLA NO DETECTADA** | VP = Detección correcta |

> **Prioridad operativa**: minimizar **FN** (falsos negativos), ya que representan fallas reales no detectadas.

### 6.2. Métricas clave y su interpretación

| Métrica | Fórmula | Interpretación en represas | Objetivo |
|--------|--------|----------------------------|----------|
| **Recall (Sensibilidad)** | VP / (VP + FN) | ¿Qué porcentaje de fallas reales detectamos? | **Maximizar** (> 70%) |
| **Precisión** | VP / (VP + FP) | ¿Qué porcentaje de alertas fueron reales? | Aceptar (> 70%) |
| **F1-Score** | 2·(Prec·Rec)/(Prec+Rec) | Equilibrio entre precisión y recall | > 0.75 |
| **Especificidad** | VN / (VN + FP) | ¿Qué porcentaje de días seguros identificamos? | > 99% |

### 6.3. Umbral de decisión
- **Umbral por defecto**: 0.5 (50% de probabilidad)
- **Umbral operativo en represas**: **0.7** (70% de probabilidad)
  - **Razón**: preferimos algunas falsas alarmas (FP) antes que fallas no detectadas (FN).

---

## 7. ▶️ Flujo de ejecución paso a paso

### Paso 1: Instalar el proyecto
```powershell
python install_project.py
cd represa_ml
venv\Scripts\activate
```

### Paso 2: Configurar notificaciones por correo
- Obtener contraseña de aplicación en Gmail.
- Configurar variables de entorno del sistema.

### Paso 3: Generar datos sintéticos densos
```powershell
python generate_data_cli.py --components 50 --days 1095 --freq-hours 1.0
```

### Paso 4: Ejecutar flujo completo
```powershell
python main.py
```

### Paso 5: Programar ejecución diaria
- Abrir PowerShell como administrador.
- Ejecutar:
  ```powershell
  python scripts/schedule_daily_task.py --install --hour 6
  ```

---

## 8. 📄 Resultados y salidas del sistema

### 8.1. Alertas multicanal
- **Sonora**: beep del sistema en Windows (centro de control).
- **Correo electrónico**: notificación a ingenieros remotos con PDF adjunto.

### 8.2. Informe PDF técnico (5 secciones)
1. **Encabezado**: título y fecha/hora de generación.
2. **Resumen de datos**: tamaño del dataset y grado de desbalance.
3. **Métricas del modelo**: precisión, recall, F1-score por clase.
4. **Matriz de confusión**: visualización de tipos de errores.
5. **Gráfico de importancia**: qué variables influyen más en las predicciones.

### 8.3. Métricas típicas esperadas
```
              precision    recall  f1-score   support
           0       1.00      1.00      1.00    262400
           1       0.85      0.76      0.80       400
```
- **Recall = 76%**: detectamos 76 de cada 100 fallas reales.
- **Precisión = 85%**: 85 de cada 100 alertas fueron reales.
- **F1-Score = 80%**: buen equilibrio para datos desbalanceados.

---

## 9. ✅ Conclusión: Por qué Random Forest es la elección óptima

Random Forest no es solo **uno más** de los modelos de Machine Learning; es la **elección óptima** para el mantenimiento predictivo en represas porque:

1. **Resuelve el problema principal**: maneja eficazmente la **extrema desbalanceo** de datos (pocas fallas).
2. **Proporciona interpretabilidad operativa**: los ingenieros pueden entender y confiar en las predicciones.
3. **Es robusto sin complejidad**: no requiere preprocesamiento sofisticado ni ajuste de muchos hiperparámetros.
4. **Captura la complejidad real**: modela interacciones no lineales entre variables sin intervención manual.
5. **Equilibra precisión y practicidad**: ofrece un excelente rendimiento con implementación relativamente simple.

> **Impacto esperado**:  
> - **Reducción del 30-50% en costos de mantenimiento** al evitar intervenciones innecesarias.  
> - **Disminución significativa del riesgo de fallas no anticipadas** gracias a la detección temprana.  
> - **Toma de decisiones basada en datos**, no en suposiciones o calendarios fijos.

---

**¿Próximos pasos para la implementación real?**  
- Reemplazar datos sintéticos por lecturas reales de sensores IoT.  
- Integrar con sistemas SCADA existentes.  
- Agregar dashboard Streamlit para monitoreo en tiempo real.  
- Implementar reentrenamiento automático cuando hay nuevos datos de fallas.
