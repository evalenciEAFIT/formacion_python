# Guía Completa para Crear un Dashboard Interactivo de Servicios Públicos de EPM

## Introducción

### ¿Por qué crear este dashboard?
Empresas Públicas de Medellín (EPM) es una de las principales prestadoras de servicios públicos en Colombia, enfocada en el suministro de **agua potable y alcantarillado**, **energía eléctrica** y **gas natural** en regiones como Medellín y Antioquia. Según su sitio web oficial (https://www.epm.com.co), EPM gestiona millones de clientes y promueve la sostenibilidad mediante métricas como consumo eficiente (e.g., m³ de agua, kWh de energía, m³ de gas) y reportes ambientales.

Este dashboard interactivo, construido con **Python**, **Pandas** y **Dash**, permite visualizar y analizar datos ficticios pero realistas de consumo por servicio, región y período. **¿Por qué es útil?**
- **Análisis rápido**: Identifica patrones de consumo (e.g., picos en energía durante meses calurosos) para optimizar recursos.
- **Interactividad**: Filtra por servicio (agua, energía, gas), región y fechas, facilitando reportes para stakeholders.
- **Sostenibilidad**: Calcula indicadores como "consumo per cápita" o "emisiones estimadas" para alinear con metas de EPM en eficiencia energética y agua.
- **Escalabilidad**: Fácil integración con datos reales de EPM (e.g., vía APIs o CSV de reportes públicos).

**¿Cómo funciona?** Usa Pandas para procesar datos tabulares, Dash para una interfaz web interactiva y Plotly para gráficos dinámicos. El resultado es un sitio web local (o desplegable) que se actualiza en tiempo real.

### Prerrequisitos
- **Python 3.8+**: Descárgalo desde python.org.
- **Entorno virtual**: Para aislar dependencias (evita conflictos).
- **Librerías**: Instala con `pip install pandas dash plotly dash-table`.
- **Conocimientos básicos**: Python intermedio; no se requiere experiencia en web.
- **Datos**: Usaremos un CSV ficticio inspirado en métricas de EPM (e.g., consumo mensual por región).

**Tiempo estimado**: 30-60 minutos para setup y ejecución.

## Estructura del Proyecto
Adoptamos una estructura modular para **buenas prácticas**: separa datos, lógica y UI. Esto facilita el mantenimiento (e.g., actualizar datos sin tocar el código) y colaboración en equipos.

```
epm_dashboard/
├── app.py                   # Archivo principal: inicia la app Dash
├── requirements.txt         # Dependencias (instala con pip install -r requirements.txt)
├── data/                    # Datos crudos
│   └── consumo_epm.csv      # CSV de ejemplo con datos de servicios
├── components/              # Componentes de Dash
│   ├── layout.py            # Define la estructura visual (layout)
│   └── callbacks.py         # Lógica interactiva (actualizaciones dinámicas)
├── utils/                   # Funciones auxiliares
│   └── data_loader.py       # Carga y procesa datos con Pandas
└── assets/                  # Estilos y recursos estáticos
    └── style.css            # CSS para diseño responsivo
```

**Justificación de la estructura**:
- **Modularidad**: Cada carpeta tiene un propósito único (e.g., `utils/` para reutilización en otros proyectos).
- **Escalabilidad**: Fácil agregar páginas (multi-página en Dash) o más servicios.
- **Buenas prácticas**: Sigue patrones de proyectos Python (PEP 8 para código limpio) y Dash (documentación oficial).

## Preparación de Datos
### ¿Por qué usar Pandas y CSV?
Pandas maneja datos tabulares eficientemente (e.g., filtros, cálculos). Un CSV es simple, portable y simula reportes reales de EPM (e.g., exportados de sus portales de clientes).

### Datos de Ejemplo: `data/consumo_epm.csv`
Creamos datos ficticios basados en métricas típicas de EPM:
- **Columnas**: `Servicio` (Agua, Energía, Gas), `Region` (Medellín, Antioquia), `Mes` (fecha), `Consumo` (unidades: m³ para agua/gas, kWh para energía), `Costo` (COP), `Usuarios` (clientes afectados).
- **Filas**: 12 meses x 3 servicios x 2 regiones = 72 registros.
- **Cálculos derivados**: En el código, agregamos "Consumo per Cápita" para sostenibilidad.

Contenido del CSV (cópialo a un archivo .csv):
```
Servicio,Region,Mes,Consumo,Costo,Usuarios
Agua,Medellín,2025-01-01,50000,15000000,25000
Agua,Medellín,2025-02-01,52000,15600000,25000
Agua,Medellín,2025-03-01,48000,14400000,25000
Agua,Antioquia,2025-01-01,80000,24000000,40000
Agua,Antioquia,2025-02-01,82000,24600000,40000
Agua,Antioquia,2025-03-01,78000,23400000,40000
Energía,Medellín,2025-01-01,1000000,50000000,50000
Energía,Medellín,2025-02-01,1050000,52500000,50000
Energía,Medellín,2025-03-01,950000,47500000,50000
Energía,Antioquia,2025-01-01,1500000,75000000,75000
Energía,Antioquia,2025-02-01,1550000,77500000,75000
Energía,Antioquia,2025-03-01,1450000,72500000,75000
Gas,Medellín,2025-01-01,30000,9000000,15000
Gas,Medellín,2025-02-01,31000,9300000,15000
Gas,Medellín,2025-03-01,29000,8700000,15000
Gas,Antioquia,2025-01-01,45000,13500000,22500
Gas,Antioquia,2025-02-01,46000,13800000,22500
Gas,Antioquia,2025-03-01,44000,13200000,22500
```
*(Extiéndelo a 12 meses para datos completos; aquí mostramos 3 para brevedad).*

**Cómo usarlo**: Coloca este archivo en `data/`. En producción, reemplaza con datos reales de EPM (e.g., descarga de https://www.epm.com.co/clientes o APIs).

## Código Documentado
Cada archivo incluye **docstrings** (explicaciones en código) y comentarios. **¿Por qué documentar?** Facilita la comprensión y depuración; sigue PEP 257.

### 1. `requirements.txt`
```
pandas==2.2.2
dash==2.17.1
plotly==5.22.0
dash-table==5.0.0
```
**Cómo instalar**: `pip install -r requirements.txt`. **Justificación**: Lista exacta de versiones para reproducibilidad.

### 2. `utils/data_loader.py`
```python
import pandas as pd
from datetime import datetime

def load_and_process_data(file_path: str = 'data/consumo_epm.csv') -> pd.DataFrame:
    """
    Carga datos de consumo de EPM desde CSV y procesa métricas derivadas.
    
    :param file_path: Ruta al archivo CSV con datos crudos.
    :return: DataFrame con columnas originales + 'Consumo_Per_Capita' y 'Fecha' como datetime.
    
    ¿Por qué procesar aquí? Separa lógica de datos de la UI (Dash), permitiendo reutilización.
    Ejemplo: Calcula 'Consumo_Per_Capita' = Consumo / Usuarios para indicadores de eficiencia.
    """
    # Cargar datos crudos
    df = pd.read_csv(file_path)
    
    # Convertir 'Mes' a datetime para filtros de fecha
    df['Fecha'] = pd.to_datetime(df['Mes'])
    
    # Calcular métrica derivada: Consumo per cápita (útil para sostenibilidad EPM)
    df['Consumo_Per_Capita'] = df['Consumo'] / df['Usuarios']
    
    # Ordenar por fecha para visualizaciones cronológicas
    df = df.sort_values('Fecha')
    
    return df

# Ejemplo de uso (para testing): df = load_and_process_data()
```
**Justificación**: Esta función es "pura" (no side-effects), fácil de testear. En EPM, métricas como per cápita ayudan a monitorear equidad en servicios.

### 3. `components/layout.py`
```python
from dash import dcc, html, dash_table
import plotly.express as px
from utils.data_loader import load_and_process_data

# Cargar datos globales una vez (eficiente para apps pequeñas)
df = load_and_process_data()

def create_layout() -> html.Div:
    """
    Crea el layout del dashboard con estructura semántica (header, sections).
    
    :return: Componente html.Div con toda la UI.
    
    ¿Cómo funciona? Usa componentes Dash para generar HTML dinámico.
    ¿Por qué esta estructura? Responsiva (CSS grid), accesible y alineada con temas EPM (azul/verde para sostenibilidad).
    Incluye: Filtros, gráficos y tabla para análisis completo.
    """
    return html.Div(className='container', children=[
        # Header: Branding EPM-like
        html.Header(className='header', children=[
            html.H1('Dashboard de Servicios Públicos EPM', className='title'),
            html.P(
                'Visualización interactiva de consumo de Agua, Energía y Gas en Medellín y Antioquia. '
                'Fuente: Datos simulados basados en reportes EPM (2025).',
                className='subtitle'
            )
        ]),
        
        # Controles: Filtros interactivos
        html.Section(className='controls', children=[
            html.Div(className='control-item', children=[
                html.Label('Seleccionar Servicio'),
                dcc.Dropdown(
                    id='dropdown-servicio',
                    options=[{'label': srv, 'value': srv} for srv in df['Servicio'].unique()],
                    value=df['Servicio'].unique(),  # Todos por defecto
                    multi=True
                )
            ]),
            html.Div(className='control-item', children=[
                html.Label('Seleccionar Región'),
                dcc.Dropdown(
                    id='dropdown-region',
                    options=[{'label': reg, 'value': reg} for reg in df['Region'].unique()],
                    value=df['Region'].unique(),
                    multi=True
                )
            ]),
            html.Div(className='control-item', children=[
                html.Label('Rango de Fechas'),
                dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=df['Fecha'].min(),
                    max_date_allowed=df['Fecha'].max(),
                    start_date=df['Fecha'].min(),
                    end_date=df['Fecha'].max()
                )
            ])
        ]),
        
        # Gráficos: Visualizaciones clave
        html.Section(className='graphs', children=[
            html.Div(className='graph-item', children=[
                dcc.Graph(id='grafico-consumo')
            ]),
            html.Div(className='graph-item', children=[
                dcc.Graph(id='grafico-per-capita')
            ])
        ]),
        
        # Tabla: Datos detallados
        html.Section(className='table-section', children=[
            html.H2('Tabla de Datos Detallados'),
            dash_table.DataTable(
                id='tabla-consumo',
                columns=[
                    {'name': col, 'id': col, 'type': 'numeric' if col in ['Consumo', 'Costo', 'Usuarios', 'Consumo_Per_Capita'] else 'text'}
                    for col in df.columns
                ],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px', 'fontSize': '12px'},
                page_size=10,  # Paginación para grandes datasets
                sort_action='native'  # Ordenamiento nativo
            )
        ]),
        
        # Footer: Información adicional
        html.Footer(className='footer', children=[
            html.P('Desarrollado para análisis de sostenibilidad EPM. Actualizado: Octubre 2025.')
        ])
    ])
```
**Justificación**: El layout es declarativo (fácil de leer). Filtros permiten "drill-down" (e.g., ver solo Energía en Antioquia), clave para reportes gerenciales en EPM.

### 4. `components/callbacks.py`
```python
from dash import Input, Output, callback
import plotly.express as px
from utils.data_loader import load_and_process_data

# Cargar datos globales
df = load_and_process_data()

def register_callbacks(app):
    """
    Registra funciones callback para actualizar UI dinámicamente.
    
    :param app: Instancia de Dash.
    
    ¿Cómo funcionan? Los callbacks responden a cambios en inputs (e.g., dropdown) y actualizan outputs (gráficos).
    ¿Por qué? Proporciona interactividad sin recargar la página, ideal para dashboards en tiempo real.
    En EPM: Filtra datos para escenarios como "consumo post-pandemia".
    """
    @callback(
        [Output('grafico-consumo', 'figure'),
         Output('grafico-per-capita', 'figure'),
         Output('tabla-consumo', 'data')],
        [Input('dropdown-servicio', 'value'),
         Input('dropdown-region', 'value'),
         Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date')]
    )
    def update_dashboard(selected_servicios, selected_regiones, start_date, end_date):
        # Filtrar DataFrame paso a paso
        filtered_df = df.copy()
        
        if selected_servicios:
            filtered_df = filtered_df[filtered_df['Servicio'].isin(selected_servicios)]
        if selected_regiones:
            filtered_df = filtered_df[filtered_df['Region'].isin(selected_regiones)]
        if start_date and end_date:
            filtered_df = filtered_df[
                (filtered_df['Fecha'] >= pd.to_datetime(start_date)) &
                (filtered_df['Fecha'] <= pd.to_datetime(end_date))
            ]
        
        # Gráfico 1: Consumo total por servicio y región (barras apiladas)
        fig_consumo = px.bar(
            filtered_df,
            x='Mes',
            y='Consumo',
            color='Servicio',
            facet_col='Region',
            title='Consumo Mensual por Servicio y Región (EPM 2025)',
            labels={'Consumo': 'Consumo (m³/kWh)'}
        )
        
        # Gráfico 2: Consumo per cápita (línea para tendencias)
        fig_per_capita = px.line(
            filtered_df,
            x='Mes',
            y='Consumo_Per_Capita',
            color='Servicio',
            markers=True,
            title='Consumo Per Cápita por Servicio (Eficiencia Sostenible)',
            labels={'Consumo_Per_Capita': 'm³/kWh por Usuario'}
        )
        
        # Datos para tabla
        table_data = filtered_df.to_dict('records')
        
        return fig_consumo, fig_per_capita, table_data
```
**Justificación**: Callbacks son asíncronos y eficientes. Usamos `facet_col` para subgráficos (e.g., comparar regiones), útil para análisis geográficos en EPM.

### 5. `assets/style.css`
```css
/* Estilos personalizados para tema EPM (azules y verdes para agua/energía) */
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f0f8ff; /* Azul claro */
}

.header { text-align: center; margin-bottom: 30px; }
.title { color: #004080; font-size: 2.5em; } /* Azul EPM */
.subtitle { color: #006400; font-size: 1.1em; } /* Verde sostenibilidad */

.controls {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin-bottom: 30px;
    padding: 15px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.graphs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.table-section { background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.footer { text-align: center; color: #666; font-size: 0.9em; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; }
```
**Justificación**: CSS hace el dashboard profesional y mobile-friendly. Colores inspirados en EPM para branding.

### 6. `app.py`
```python
import dash
from dash import Dash
from components.layout import create_layout
from components.callbacks import register_callbacks

# Inicializar app Dash
app = Dash(__name__)

# Configurar layout
app.layout = create_layout()

# Registrar callbacks para interactividad
register_callbacks(app)

# Servidor (debug=True para desarrollo)
if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
```
**Justificación**: Archivo mínimo; delega complejidad a módulos. `debug=True` muestra errores en navegador durante desarrollo.

## Instrucciones de Ejecución
1. **Crear carpeta**: `mkdir epm_dashboard && cd epm_dashboard`.
2. **Entorno virtual**: `python -m venv venv` → Activa: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows).
3. **Instalar dependencias**: `pip install -r requirements.txt`.
4. **Crear archivos**: Copia los códigos arriba en sus respectivas ubicaciones; genera el CSV en `data/`.
5. **Ejecutar**: `python app.py`.
6. **Acceder**: Abre http://127.0.0.1:8050 en tu navegador. Interactúa con dropdowns para filtrar.
7. **Detener**: Ctrl+C en terminal.

**Problemas comunes**:
- **Error de import**: Verifica paths (e.g., `data/` existe).
- **Datos vacíos**: Extiende el CSV a más meses.
- **Producción**: Cambia `debug=False`; despliega en Heroku/Render.
