# **Documento Técnico: Sistema de Monitoreo de Represas Hidroeléctricas**  
### *Versión para entornos industriales reales (inspirado en EPM)*

---

## **1. Introducción**

Este documento describe un **sistema de monitoreo inteligente para represas hidroeléctricas**, diseñado para replicar las necesidades operativas de empresas como **EPM** (Empresas Públicas de Medellín). El sistema combina **generación de datos realista**, **análisis predictivo**, **visualización en tiempo real**, **alertas operativas** y **exportación de reportes**, todo dentro de una arquitectura modular y escalable.

> **Objetivo principal**: Proporcionar una solución que permita a los operadores tomar decisiones informadas basadas en datos en tiempo real, prevenir riesgos operativos y optimizar la generación de energía.

---

## **2. Arquitectura del Sistema**

### **2.1 Diagrama de Componentes**

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFAZ DE USUARIO                      │
│  ┌─────────────┐    ┌─────────────┐    ┌──────────────┐   │
│  │   Modo EDA  │    │ Modo Modelo │    │ Modo Tablero │   │
│  └─────────────┘    └─────────────┘    └──────────────┘   │
└─────────────────────────┬─────────────────────────────────┘
                          │
┌─────────────────────────▼─────────────────────────────────┐
│                   CAPA DE APLICACIÓN                      │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │ Generación  │  │   Modelos   │  │  Visualización   │  │
│  │ de Datos    │  │ Predictivos │  │  y Alertas       │  │
│  └─────────────┘  └─────────────┘  └──────────────────┘  │
└─────────────────────────┬─────────────────────────────────┘
                          │
┌─────────────────────────▼─────────────────────────────────┐
│                   CAPA DE DATOS                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                Base de Datos SQLite                 │  │
│  │  - timestamp (TEXT, UNIQUE)                         │  │
│  │  - nivel_agua_pct (REAL)                            │  │
│  │  - energia_almacenada_gwh (REAL)                    │  │
│  │  - generacion_mw (REAL)                             │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

### **2.2 Características Clave**

| Característica | Descripción | Beneficio para EPM |
|----------------|-------------|-------------------|
| **Generación continua** | 1 dato cada 3 segundos simulando SCADA real | Replica el flujo de datos de sensores reales |
| **Base de datos SQLite** | Almacenamiento local eficiente y confiable | Sin dependencia de servidores externos |
| **Alertas multiplataforma** | Visuales + sonoras en Windows/Linux/macOS | Notificación inmediata de condiciones críticas |
| **Exportación de reportes** | CSV + resúmenes textuales automáticos | Cumplimiento de requisitos de auditoría |
| **Tablero con branding EPM** | Logo oficial y colores corporativos | Integración visual con sistemas existentes |

---

## **3. Modos de Operación**

### **3.1 Modo EDA (Análisis Exploratorio de Datos)**

**Propósito**: Comprender el comportamiento histórico del sistema antes de modelar.

**Comando de ejecución**:
```bash
python run.py --modo eda
```

**Funcionalidad**:
- Genera **1440 datos históricos** (24 horas, 1 por minuto)
- Muestra estadísticas descriptivas:
  - Media, mediana, desviación estándar
  - Valores mínimos y máximos
  - Cuartiles
- Genera **3 gráficos de series temporales**:
  - Nivel de agua (%)
  - Energía almacenada (GWh)
  - Generación de energía (MW)

**Código clave** (`src/modelos/analisis_descriptivo.py`):
```python
def analisis_exploratorio(datos_represa: pd.DataFrame) -> None:
    """Muestra estadísticas y gráficos del comportamiento de la represa."""
    print(datos_represa.describe())  # Estadísticas básicas
    
    # Crear gráficos de series temporales
    fig, ejes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    datos_represa.set_index("timestamp").plot(subplots=True, ax=ejes)
    plt.show()
```

### **3.2 Modo Entrenar (Modelo Predictivo)**

**Propósito**: Entrenar un modelo de Machine Learning para predecir el nivel de agua.

**Comando de ejecución**:
```bash
python run.py --modo entrenar
```

**Funcionalidad**:
- Usa **Random Forest** por su robustez y capacidad para capturar relaciones no lineales
- Extrae características temporales:
  - Hora del día (patrones de consumo)
  - Día de la semana (diferencias laborables/fin de semana)
  - Mes del año (estacionalidad climática)
- Evalúa el modelo con **RMSE** (Root Mean Squared Error)
- Muestra progreso de entrenamiento con barra visual

**Código clave** (`src/modelos/modelo_predictivo.py`):
```python
def crear_caracteristicas_temporales(datos: pd.DataFrame) -> pd.DataFrame:
    datos["hora_del_dia"] = datos["timestamp"].dt.hour
    datos["dia_de_la_semana"] = datos["timestamp"].dt.dayofweek
    datos["mes_del_año"] = datos["timestamp"].dt.month
    return datos

def entrenar_modelo_predictivo(datos_represa: pd.DataFrame):
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_entrenamiento, y_entrenamiento)
    rmse = root_mean_squared_error(y_prueba, predicciones)
    return modelo
```

### **3.3 Modo Tablero (Monitoreo en Tiempo Real)**

**Propósito**: Visualización operativa continua con alertas.

**Comando de ejecución**:
```bash
python run.py --modo tablero
```

**Funcionalidad**:
- **Generación continua**: 1 dato cada 3 segundos en segundo plano
- **4 KPIs en tiempo real**:
  - Nivel actual de agua (%)
  - Generación actual (MW)
  - Estado del embalse (Alto/Normal/Bajo/Crítico)
  - Fecha y hora del sistema
- **Dos gráficos separados**:
  - Nivel de agua con líneas de referencia (30%, 60%, 85%)
  - Generación de energía
- **Selector de ventana de tiempo**:
  - Última hora, 6 horas, 24 horas, 7 días
- **Alertas automáticas**:
  - Nivel < 25% → Alerta CRÍTICA (roja)
  - Nivel > 90% → Alerta ALTA (naranja)

**Código clave** (`src/visualizacion/tablero_tiempo_real.py`):
```python
@app.callback(
    [Output("kpi-nivel", "children"), Output("kpi-generacion", "children"), ...],
    [Input("intervalo-actualizacion", "n_intervals"), Input("selector-tiempo", "value")]
)
def actualizar_todo(n_intervals: int, ventana: str):
    # Cargar datos, filtrar por ventana, actualizar KPIs y gráficos
    alerta = verificar_alertas(ultimo['nivel_agua_pct'])
    if alerta["activa"]:
        logger.warning(f"🚨 ALERTA: {alerta['mensaje']}")
```

---

## **4. Sistema de Alertas**

### **4.1 Umbrales Operativos**

| Nivel de Agua | Estado | Color | Acción Recomendada |
|---------------|--------|-------|-------------------|
| ≥ 85% | **Alto** | Verde (#43a047) | Monitoreo normal |
| 60-84% | **Normal** | Azul (#1e88e5) | Monitoreo normal |
| 30-59% | **Bajo** | Naranja (#fb8c00) | Alerta amarilla - Revisar operaciones |
| < 30% | **Crítico** | Rojo (#e53935) | Alerta roja - Acción inmediata |

### **4.2 Implementación Técnica**

**Verificación de alertas** (`src/utilidades/alertas.py`):
```python
def verificar_alertas(nivel_agua: float) -> dict:
    if nivel_agua < 25:
        return {
            "activa": True,
            "nivel": "CRÍTICO",
            "mensaje": "¡Nivel de agua muy bajo! Riesgo operativo.",
            "color": "#e53935"
        }
    elif nivel_agua > 90:
        return {
            "activa": True,
            "nivel": "ALTO",
            "mensaje": "¡Nivel de agua muy alto! Riesgo de desbordamiento.",
            "color": "#fb8c00"
        }
    else:
        return {"activa": False}
```

**Reproducción de sonido** (multiplataforma):
```python
def reproducir_alerta_sonora():
    sistema = platform.system()
    if sistema == "Windows":
        winsound.Beep(800, 500)  # Windows
    elif sistema == "Darwin":
        os.system("afplay /System/Library/Sounds/Ping.aiff")  # macOS
    else:
        os.system("paplay /usr/share/sounds/generic.wav")  # Linux
```

---

## **5. Exportación de Reportes**

### **5.1 Tipos de Reportes**

| Tipo | Formato | Contenido | Frecuencia |
|------|---------|-----------|------------|
| **Reporte Completo** | CSV | Todos los datos históricos | A demanda |
| **Resumen Operativo** | TXT | Estadísticas clave + estado actual | A demanda |

### **5.2 Implementación**

**Exportación CSV** (`src/utilidades/exportador.py`):
```python
def exportar_reporte_csv(datos: pd.DataFrame, nombre_archivo: str = None):
    carpeta = Path("reportes")
    carpeta.mkdir(exist_ok=True)
    if nombre_archivo is None:
        nombre_archivo = f"reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    datos.to_csv(carpeta / nombre_archivo, index=False)
```

**Resumen textual**:
```python
def exportar_resumen_texto(datos: pd.DataFrame) -> str:
    return f"""
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
```

---

## **6. Inicialización del Proyecto**

### **6.1 Script de Configuración**

El archivo `setup_project.py` automatiza toda la configuración:

```python
def main():
    crear_estructura_proyecto()      # Crea carpetas y archivos
    crear_entorno_virtual()          # Configura venv
    instalar_dependencias()          # Instala paquetes
    generar_script_activacion_powershell()  # Facilita uso en Windows
```

### **6.2 Flujo de Uso**

```powershell
# 1. Ejecutar configuración (solo una vez)
python setup_project.py

# 2. Activar entorno virtual
.\monitoreo-represas-ml\activar.ps1

# 3. Ejecutar sistema
python run.py --modo tablero
```

---

## **7. Mejoras para Entornos Reales (EPM)**

### **7.1 Integración con Infraestructura Existente**

| Mejora | Descripción | Beneficio |
|--------|-------------|-----------|
| **Conexión a SCADA real** | Reemplazar generador de datos con API de sensores reales | Datos reales en tiempo real |
| **Base de datos empresarial** | Migrar de SQLite a PostgreSQL/Oracle | Escalabilidad y alta disponibilidad |
| **Autenticación de usuarios** | Integrar con Active Directory de EPM | Control de acceso y auditoría |
| **Integración con SIEM** | Enviar alertas a sistema de monitoreo corporativo | Centralización de eventos de seguridad |

### **7.2 Funcionalidades Avanzadas**

| Mejora | Descripción | Implementación |
|--------|-------------|----------------|
| **Predicción a 24h** | Modelo LSTM para pronóstico de nivel | `src/modelos/modelo_lstm.py` |
| **Optimización de generación** | Algoritmo para maximizar producción | Módulo de optimización matemática |
| **Geolocalización** | Mapa interactivo con ubicación de represas | Integración con Leaflet/Mapbox |
| **Notificaciones móviles** | Alertas por SMS/Email/WhatsApp | Servicio de mensajería externo |

### **7.3 Cumplimiento Normativo**

| Requisito | Implementación | Estándar |
|-----------|----------------|----------|
| **Respaldo de datos** | Copias de seguridad automáticas diarias | ISO 27001 |
| **Registro de auditoría** | Log detallado de todas las operaciones | NTC 4577 |
| **Disponibilidad 99.9%** | Monitoreo de salud del sistema | SLA corporativo |
| **Seguridad de datos** | Cifrado de base de datos sensible | GDPR/LOPD |

### **7.4 Escalabilidad**

| Capacidad | Solución | Tecnología |
|-----------|----------|------------|
| **Múltiples represas** | Arquitectura multi-tenant | Microservicios |
| **Alta frecuencia** | Procesamiento de streaming | Apache Kafka |
| **Visualización masiva** | Dashboard corporativo | Grafana/Power BI |
| **Machine Learning avanzado** | Entrenamiento distribuido | Spark MLlib |

---

## **8. Validación y Pruebas**

### **8.1 Casos de Prueba**

| Caso | Entrada | Salida Esperada |
|------|---------|-----------------|
| **Nivel crítico** | nivel_agua_pct = 20 | Alerta roja + sonido |
| **Nivel alto** | nivel_agua_pct = 95 | Alerta naranja + log |
| **Datos históricos** | Modo EDA | 3 gráficos + estadísticas |
| **Predicción** | Modo entrenar | RMSE < 5.0 |

### **8.2 Métricas de Calidad**

- **Precisión del modelo**: RMSE < 5% del rango de nivel
- **Latencia de alertas**: < 5 segundos desde condición crítica
- **Disponibilidad del tablero**: 99.9% uptime
- **Capacidad de datos**: 1 millón de registros sin degradación

---

## **9. Conclusión**

Este sistema proporciona una **base sólida y escalable** para el monitoreo de represas hidroeléctricas, con características que se alinean directamente con las necesidades operativas de empresas como **EPM**:

**Simulación realista** de datos SCADA  
**Alertas operativas** con umbrales definidos por ingenieros  
**Visualización profesional** con branding corporativo  
**Exportación de reportes** para cumplimiento normativo  
**Arquitectura modular** lista para integración empresarial  

La implementación actual sirve como **prueba de concepto (PoC)** que puede evolucionar hacia un sistema de producción.

---



**Elaborado por**: Equipo de Innovación en Monitoreo Hidroeléctrico  
**Fecha**: Octubre 2025  
**Versión**: 1.0
