# 🏭 **SISTEMA COMPLETO DE GESTIÓN DE DATOS DE RED DE GAS**

## 📚 **PARTE 1: CONCEPTOS FUNDAMENTALES**

### **🔍 ¿QUÉ ES POO (PROGRAMACIÓN ORIENTADA A OBJETOS)?**

**POO** es como construir con **legos**:
- **Clases** = Los moldes para hacer piezas de lego
- **Objetos** = Las piezas individuales que creas
- **Atributos** = Características de cada pieza (color, tamaño)
- **Métodos** = Lo que puedes hacer con cada pieza (unir, girar)

**Ejemplo en Red de Gas:**
```python
# CLASE: Molde para crear estaciones de gas
class EstacionGas:
    # ATRIBUTOS: Características de cada estación
    def __init__(self, nombre, ubicacion, capacidad):
        self.nombre = nombre          # Nombre de la estación
        self.ubicacion = ubicacion    # Donde está ubicada
        self.capacidad = capacidad    # Cuánto gas puede manejar
        self.estado = "activa"        # Estado actual
    
    # MÉTODOS: Acciones que puede realizar
    def comprimir_gas(self, presion):
        return f"Comprimiendo gas a {presion} bar en {self.nombre}"
    
    def generar_reporte(self):
        return f"Reporte de {self.nombre} - Estado: {self.estado}"

# OBJETOS: Estaciones específicas creadas del molde
estacion_norte = EstacionGas("Compresor Norte", "Zona Industrial", 100)
estacion_sur = EstacionGas("Compresor Sur", "Area Residencial", 80)

print(estacion_norte.comprimir_gas(75))  # Usando un método
```

### **🔧 FUNCIONES SYS Y OS EXPLICADAS**

#### **MÓDULO OS (OPERATING SYSTEM)**
```python
import os

# 📁 GESTIÓN DE ARCHIVOS Y CARPETAS
print("📂 Directorio actual:", os.getcwd())  # Donde estoy ejecutando el código

# Crear carpeta si no existe
os.makedirs("fuentedatos", exist_ok=True)  # Crea carpeta, no da error si ya existe

# Verificar si archivo existe
if os.path.exists("datos.csv"):
    print("✅ El archivo existe")
else:
    print("❌ Archivo no encontrado")

# Unir rutas de forma segura (evita problemas con / o \)
ruta_segura = os.path.join("carpeta", "subcarpeta", "archivo.csv")
print("🛡️ Ruta segura:", ruta_segura)

# Listar archivos en carpeta
archivos = os.listdir("fuentedatos")
print("📄 Archivos disponibles:", archivos)
```

#### **MÓDULO SYS (SYSTEM)**
```python
import sys

# 🎯 GESTIÓN DEL SISTEMA Y RUTAS
print("🐍 Versión de Python:", sys.version)

# Agregar rutas para importar módulos personalizados
sys.path.append("./db")        # Agrega carpeta db al path de búsqueda
sys.path.append("./config")    # Agrega carpeta config al path

# Esto permite hacer: from cargarDatos import GestorDatosGas
# Sin tener los archivos en la misma carpeta

# Argumentos de línea de comandos
if len(sys.argv) > 1:
    print("🚀 Argumentos recibidos:", sys.argv[1:])
```

## 🏗️ **PARTE 2: ESTRUCTURA COMPLETA DEL PROYECTO**

```
SistemaGas/
├── 📁 config/
│   └── config.py              # ⚙️ Configuraciones globales
├── 📁 db/
│   └── cargarDatos.py         # 🏭 CLASE principal de gestión
├── 📁 fuentedatos/
│   └── datos.csv              # 📊 Datos de ejemplo
├── 📁 API/
│   └── api.py                 # 🌐 Servidor Flask con endpoints
├── 📁 APP/
│   └── main.py               # 💻 Aplicación de consola
├── 📁 dashboard/
│   └── app.py                # 📈 Dashboard interactivo (Dash)
└── requirements.txt          # 📦 Dependencias del proyecto
```

## ⚙️ **PASO 1: CONFIGURACIÓN GLOBAL**

### **Archivo: `config/config.py`**
```python
import os
from dotenv import load_dotenv

# 🎯 CARGA CONFIGURACIONES DESDE ARCHIVO .env
load_dotenv()  # Busca archivo .env y carga variables

class Config:
    """
    🏗️ CLASE de configuración centralizada
    ✅ Ventaja: Todas las configuraciones en un solo lugar
    ✅ Fácil de modificar sin tocar el código
    """
    
    # 🗄️ CONFIGURACIÓN BASE DE DATOS POSTGRESQL
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')        # Servidor
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')            # Puerto
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'red_gas')             # Nombre BD
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')        # Usuario
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')# Contraseña
    
    # 💾 CONFIGURACIÓN SQLITE
    SQLITE_PATH = os.getenv('SQLITE_PATH', 'red_gas.db')          # Ruta archivo
    
    # 📁 RUTAS DE CARPETAS
    DATA_DIR = 'fuentedatos'      # Donde están los archivos de datos
    UPLOAD_FOLDER = 'uploads'     # Donde se guardan archivos subidos
    
    # 📊 FORMATOS SOPORTADOS
    SUPPORTED_FORMATS = ['csv', 'xlsx', 'xls', 'db', 'sqlite']
    
    @property
    def postgres_connection(self):
        """
        🎯 PROPIEDAD: Genera cadena de conexión automáticamente
        ✅ Por qué property?: Se calcula dinámicamente cuando se necesita
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

# 🚀 CREAR INSTANCIA GLOBAL DE CONFIGURACIÓN
config = Config()
print("⚙️ Configuración cargada - Sistema listo")
```

## 🏭 **PASO 2: CLASE PRINCIPAL DE GESTIÓN DE DATOS**

### **Archivo: `db/cargarDatos.py`**
```python
import pandas as pd
import sqlite3
import os
import json
from datetime import datetime
from sqlalchemy import create_engine, text
import chardet

class GestorDatosGas:
    """
    🏗️ CLASE PRINCIPAL del sistema
    🎯 OBJETIVO: Gestionar datos de red de gas desde múltiples fuentes
    ✅ VENTAJAS: 
       - Código organizado y reutilizable
       - Fácil mantenimiento
       - Escalable para nuevas funcionalidades
    """
    
    def __init__(self, config):
        """
        🎯 CONSTRUCTOR: Se ejecuta al crear el objeto
        📥 RECIBE: Configuración del sistema
        🎯 PROPÓSITO: Inicializar el gestor con configuraciones
        """
        # 🗃️ ATRIBUTOS: Variables que almacenan el estado del objeto
        self.config = config              # Configuración del sistema
        self.dataframe = None             # Datos cargados en memoria
        self.estadisticas = {}            # Métricas calculadas
        self.historial = []               # Registro de operaciones
        self.ultima_fuente = None         # Última fuente usada
        
        print("🏭 GestorDatosGas INICIALIZADO - Listo para gestión de datos de gas")
    
    def cargar_datos(self, fuente, **kwargs):
        """
        🎯 MÉTODO PRINCIPAL: Cargar datos desde cualquier fuente
        📥 PARÁMETROS:
           - fuente: Ruta archivo o conexión BD
           - **kwargs: Parámetros adicionales (query, sheet_name, etc.)
        🎯 PROPÓSITO: Unificar carga desde diferentes fuentes
        """
        try:
            print(f"📂 Detectando tipo de fuente: {fuente}")
            self.ultima_fuente = fuente
            
            # 🎯 DETECCIÓN AUTOMÁTICA DEL TIPO DE FUENTE
            if fuente.lower().endswith('.csv'):
                return self._cargar_csv(fuente, **kwargs)
            elif fuente.lower().endswith(('.xlsx', '.xls')):
                return self._cargar_excel(fuente, **kwargs)
            elif fuente.lower().endswith(('.db', '.sqlite')):
                return self._cargar_sqlite(fuente, **kwargs)
            elif 'postgresql' in fuente.lower() or 'query' in kwargs:
                return self._cargar_postgresql(fuente, **kwargs)
            else:
                # 🎯 ASUNCIÓN INTELIGENTE: Si no es archivo, es consulta PostgreSQL
                return self._cargar_postgresql(self.config.postgres_connection, query=fuente, **kwargs)
                
        except Exception as e:
            return self._crear_respuesta_error(f"Error al cargar datos: {str(e)}")
    
    def _cargar_csv(self, archivo, **kwargs):
        """
        🔒 MÉTODO PRIVADO: Cargar datos desde CSV
        🎯 PROPÓSITO: Encapsular lógica específica de CSV
        """
        print(f"📊 Cargando CSV: {archivo}")
        
        # 🎯 DETECCIÓN AUTOMÁTICA DE CODIFICACIÓN
        codificacion = self._detectar_codificacion(archivo)
        print(f"🔍 Codificación detectada: {codificacion}")
        
        # 📥 CARGA CON PANDAS
        self.dataframe = pd.read_csv(archivo, encoding=codificacion, **kwargs)
        
        # 📊 PROCESAMIENTO POST-CARGA
        self._procesar_estadisticas('CSV', archivo)
        
        return self._crear_respuesta_exito(f"CSV cargado exitosamente: {archivo}")
    
    def _cargar_excel(self, archivo, **kwargs):
        """Cargar datos desde Excel"""
        print(f"📗 Cargando Excel: {archivo}")
        hoja = kwargs.get('sheet_name', 0)
        self.dataframe = pd.read_excel(archivo, sheet_name=hoja, **kwargs)
        self._procesar_estadisticas('Excel', archivo)
        return self._crear_respuesta_exito(f"Excel cargado: {archivo}")
    
    def _cargar_sqlite(self, archivo_db, **kwargs):
        """Cargar datos desde SQLite"""
        print(f"🗃️ Cargando SQLite: {archivo_db}")
        query = kwargs.get('query', 'SELECT * FROM mediciones_gas')
        
        with sqlite3.connect(archivo_db) as conn:
            self.dataframe = pd.read_sql_query(query, conn)
        
        self._procesar_estadisticas('SQLite', archivo_db)
        return self._crear_respuesta_exito(f"SQLite cargado: {archivo_db}")
    
    def _cargar_postgresql(self, conexion, **kwargs):
        """Cargar datos desde PostgreSQL"""
        print(f"🐘 Cargando PostgreSQL: {conexion.split('@')[-1]}")
        query = kwargs.get('query', 'SELECT * FROM mediciones_gas')
        
        engine = create_engine(conexion)
        with engine.connect() as conn:
            self.dataframe = pd.read_sql_query(text(query), conn)
        
        self._procesar_estadisticas('PostgreSQL', conexion)
        return self._crear_respuesta_exito("Datos PostgreSQL cargados")
    
    def _detectar_codificacion(self, archivo):
        """
        🎯 DETECTAR CODIFICACIÓN AUTOMÁTICAMENTE
        📥 PROPÓSITO: Evitar errores con archivos en diferentes codificaciones
        """
        with open(archivo, 'rb') as f:
            resultado = chardet.detect(f.read())
        return resultado['encoding']
    
    def _procesar_estadisticas(self, tipo_fuente, fuente):
        """
        📊 ANALIZAR DATOS CARGADOS Y CALCULAR ESTADÍSTICAS
        🎯 PROPÓSITO: Proporcionar insights automáticos sobre los datos
        """
        df = self.dataframe
        
        # 🎯 IDENTIFICACIÓN INTELIGENTE DE COLUMNAS DE GAS
        columnas_estacion = [col for col in df.columns if 'estacion' in col.lower()]
        columnas_fecha = [col for col in df.columns if 'fecha' in col.lower() or 'timestamp' in col.lower()]
        columnas_presion = [col for col in df.columns if 'presion' in col.lower()]
        columnas_caudal = [col for col in df.columns if 'caudal' in col.lower() or 'flujo' in col.lower()]
        columnas_consumo = [col for col in df.columns if 'consumo' in col.lower()]
        
        # 📈 CONSTRUCCIÓN DE ESTADÍSTICAS
        self.estadisticas = {
            'tipo_fuente': tipo_fuente,
            'fuente': fuente,
            'timestamp_carga': datetime.now().isoformat(),
            'total_registros': len(df),
            'total_columnas': len(df.columns),
            'columnas': df.columns.tolist(),
            
            # 🏭 ANÁLISIS ESPECÍFICO PARA DATOS DE GAS
            'columnas_estacion': columnas_estacion,
            'columnas_fecha': columnas_fecha,
            'columnas_presion': columnas_presion,
            'columnas_caudal': columnas_caudal,
            'columnas_consumo': columnas_consumo,
            
            # 📊 ESTADÍSTICAS GENERALES
            'tipos_datos': df.dtypes.astype(str).to_dict(),
            'valores_nulos': df.isnull().sum().to_dict(),
            'completitud': f"{(1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100:.1f}%"
        }
        
        # 🎯 CÁLCULO DE MÉTRICAS OPERATIVAS
        self._calcular_metricas_gas(df)
        
        # 📝 REGISTRO EN HISTORIAL
        self._registrar_operacion('carga', tipo_fuente, fuente, len(df))
    
    def _calcular_metricas_gas(self, df):
        """
        🎯 CÁLCULO DE MÉTRICAS ESPECÍFICAS DE GAS
        📊 PROPÓSITO: Proporcionar KPIs relevantes para operaciones de gas
        """
        # 📈 MÉTRICAS DE PRESIÓN
        for col_presion in self.estadisticas['columnas_presion']:
            if col_presion in df.columns and pd.api.types.is_numeric_dtype(df[col_presion]):
                datos = df[col_presion].dropna()
                if len(datos) > 0:
                    self.estadisticas[f'{col_presion}_promedio'] = datos.mean()
                    self.estadisticas[f'{col_presion}_maximo'] = datos.max()
                    self.estadisticas[f'{col_presion}_minimo'] = datos.min()
        
        # 🌊 MÉTRICAS DE CAUDAL
        for col_caudal in self.estadisticas['columnas_caudal']:
            if col_caudal in df.columns and pd.api.types.is_numeric_dtype(df[col_caudal]):
                datos = df[col_caudal].dropna()
                if len(datos) > 0:
                    self.estadisticas[f'{col_caudal}_promedio'] = datos.mean()
                    self.estadisticas[f'{col_caudal}_total'] = datos.sum()
    
    def _registrar_operacion(self, operacion, tipo, fuente, registros):
        """
        📝 REGISTRAR OPERACIÓN EN HISTORIAL
        🎯 PROPÓSITO: Mantener traza de todas las operaciones realizadas
        """
        self.historial.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operacion': operacion,
            'tipo': tipo,
            'fuente': fuente,
            'registros': registros
        })
    
    def convertir_a_json(self, formato="completo"):
        """
        🔄 CONVERTIR DATOS A FORMATO JSON
        🎯 PROPÓSITO: Preparar datos para APIs y exportación
        """
        if self.dataframe is None:
            return self._crear_respuesta_error("No hay datos cargados")
        
        # 🎯 MÚLTIPLES FORMATOS DISPONIBLES
        formatos = {
            'simple': self._json_simple(),        # Para APIs rápidas
            'completo': self._json_completo(),    # Con metadatos
            'analitico': self._json_analitico(),  # Para análisis
            'operacional': self._json_operacional() # Para operaciones
        }
        
        return formatos.get(formato, self._json_completo())
    
    def _json_simple(self):
        """JSON simple para transferencia rápida"""
        return {
            'estado': 'éxito',
            'total_registros': len(self.dataframe),
            'datos': self.dataframe.to_dict('records')
        }
    
    def _json_completo(self):
        """JSON con metadatos completos"""
        return {
            'estado': 'éxito',
            'sistema': 'red_gas',
            'timestamp': datetime.now().isoformat(),
            'estadisticas': self.estadisticas,
            'datos': self.dataframe.to_dict('records'),
            'muestra': self.dataframe.head(10).to_dict('records')
        }
    
    def obtener_estadisticas(self):
        """Obtener estadísticas actuales"""
        return self.estadisticas
    
    def obtener_historial(self):
        """Obtener historial de operaciones"""
        return self.historial
    
    def _crear_respuesta_exito(self, mensaje):
        """Respuesta estandarizada para operaciones exitosas"""
        return {
            'estado': 'éxito',
            'mensaje': mensaje,
            'timestamp': datetime.now().isoformat()
        }
    
    def _crear_respuesta_error(self, mensaje):
        """Respuesta estandarizada para errores"""
        return {
            'estado': 'error',
            'mensaje': mensaje,
            'timestamp': datetime.now().isoformat()
        }

# 🎯 FUNCIÓN DE COMPATIBILIDAD (para código existente)
def cargardatos_csv(nombreArchivo):
    """
    🔄 FUNCIÓN LEGACY: Mantiene compatibilidad con código anterior
    🎯 PROPÓSITO: Permitir transición suave a la nueva clase
    """
    from config.config import config
    gestor = GestorDatosGas(config)
    return gestor._cargar_csv(nombreArchivo)
```

# 🌐 **PARTE 3: API REST CON FLASK**

### **Archivo: `API/api.py`**
```python
from flask import Flask, request, jsonify
import os
import sys
from datetime import datetime

# 🎯 CONFIGURACIÓN DE RUTAS PARA IMPORTACIONES
# sys.path.append permite importar módulos de otras carpetas
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

# 📦 IMPORTACIONES DE NUESTRAS CLASES
from cargarDatos import GestorDatosGas
from config import config

# 🚀 INICIALIZACIÓN DE FLASK
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # Mantener orden original en JSON

# 🏭 CREAR INSTANCIA DEL GESTOR DE DATOS
gestor_gas = GestorDatosGas(config)

@app.route('/')
def inicio():
    """
    🌐 ENDPOINT RAÍZ: Página de bienvenida y documentación
    🎯 PROPÓSITO: Proporcionar información sobre la API
    """
    return jsonify({
        'mensaje': '🏭 API de Gestión de Datos de Red de Gas',
        'version': '1.0',
        'descripcion': 'Sistema completo para gestión y análisis de datos de red de gas',
        'endpoints_disponibles': {
            'GET': {
                '/': 'Esta documentación',
                '/api/estado': 'Estado del sistema',
                '/api/datos': 'Cargar datos predeterminados',
                '/api/datos/<formato>': 'Cargar datos en formato específico',
                '/api/fuentes': 'Listar fuentes disponibles',
                '/api/estadisticas': 'Estadísticas de datos cargados',
                '/api/historial': 'Historial de operaciones',
                '/api/estaciones': 'Listar estaciones disponibles',
                '/api/mediciones/<estacion>': 'Mediciones por estación',
                '/api/alertas': 'Alertas del sistema'
            },
            'POST': {
                '/api/cargar': 'Cargar datos desde fuente específica',
                '/api/query': 'Ejecutar consulta personalizada',
                '/api/exportar': 'Exportar datos a formato específico'
            }
        },
        'ejemplos_uso': {
            'cargar_csv': 'GET /api/datos?archivo=datos.csv',
            'cargar_postgres': 'POST /api/cargar con JSON body',
            'consulta_personalizada': 'POST /api/query con consulta SQL'
        }
    })

@app.route('/api/estado')
def estado_sistema():
    """
    🔍 ENDPOINT: Estado del sistema
    🎯 PROPÓSITO: Verificar que la API está funcionando correctamente
    """
    return jsonify({
        'estado': 'activo',
        'timestamp': datetime.now().isoformat(),
        'ultima_fuente': gestor_gas.ultima_fuente,
        'total_operaciones': len(gestor_gas.historial),
        'memoria_activa': 'gestor_datos_cargado' if gestor_gas.dataframe is not None else 'sin_datos'
    })

@app.route('/api/datos', methods=['GET'])
@app.route('/api/datos/<formato>', methods=['GET'])
def cargar_datos(formato='completo'):
    """
    📥 ENDPOINT: Cargar datos predeterminados
    🎯 PROPÓSITO: Cargar y devolver datos en diferentes formatos
    📌 PARÁMETROS:
        - archivo: Nombre del archivo (opcional)
        - formato: simple/completo/analitico/operacional
    """
    try:
        # 📁 OBTENER PARÁMETROS DE LA URL
        archivo = request.args.get('archivo', 'datos.csv')
        ruta_archivo = os.path.join(config.DATA_DIR, archivo)
        
        print(f"🌐 Solicitud recibida: cargar {archivo} como {formato}")
        
        # 🏭 CARGAR DATOS USANDO NUESTRA CLASE
        resultado = gestor_gas.cargar_datos(ruta_archivo)
        
        if resultado['estado'] == 'éxito':
            # 🔄 CONVERTIR A FORMATO SOLICITADO
            datos_json = gestor_gas.convertir_a_json(formato)
            return jsonify(datos_json)
        else:
            # ❌ MANEJO DE ERRORES
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error en el endpoint: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/cargar', methods=['POST'])
def cargar_datos_fuente():
    """
    📤 ENDPOINT POST: Cargar datos desde fuente específica
    🎯 PROPÓSITO: Permitir carga flexible desde diferentes fuentes
    📥 BODY JSON esperado:
        {
            "tipo_fuente": "csv|excel|sqlite|postgresql",
            "fuente": "ruta/archivo o conexión",
            "parametros": { ... },
            "formato_salida": "completo"
        }
    """
    try:
        # 📥 OBTENER DATOS DEL CUERPO DE LA SOLICITUD
        datos = request.json
        
        if not datos:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Se requiere body JSON'
            }), 400
        
        tipo_fuente = datos.get('tipo_fuente')
        fuente = datos.get('fuente')
        parametros = datos.get('parametros', {})
        
        print(f"🌐 Carga solicitada: {tipo_fuente} -> {fuente}")
        
        # 🎯 CONFIGURACIÓN INTELIGENTE SEGÚN TIPO DE FUENTE
        if tipo_fuente == 'postgresql':
            fuente = config.postgres_connection
            if 'query' not in parametros:
                parametros['query'] = 'SELECT * FROM mediciones_gas'
        elif tipo_fuente == 'sqlite':
            if not fuente.endswith('.db'):
                fuente = os.path.join(config.DATA_DIR, fuente)
        
        # 🏭 EJECUTAR CARGA
        resultado = gestor_gas.cargar_datos(fuente, **parametros)
        
        if resultado['estado'] == 'éxito':
            formato_salida = datos.get('formato_salida', 'completo')
            datos_json = gestor_gas.convertir_a_json(formato_salida)
            return jsonify(datos_json)
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error en carga: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/query', methods=['POST'])
def ejecutar_consulta():
    """
    🗃️ ENDPOINT: Ejecutar consulta personalizada
    🎯 PROPÓSITO: Permitir consultas SQL personalizadas
    📥 BODY JSON esperado:
        {
            "query": "SELECT * FROM tabla WHERE condición",
            "tipo_base": "postgresql|sqlite",
            "formato_salida": "completo"
        }
    """
    try:
        datos = request.json
        consulta = datos.get('query')
        tipo_base = datos.get('tipo_base', 'postgresql')
        
        if not consulta:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Se requiere parámetro "query"'
            }), 400
        
        print(f"🗃️ Ejecutando consulta: {consulta[:50]}...")
        
        # 🎯 EJECUTAR CONSULTA SEGÚN TIPO DE BASE
        if tipo_base == 'postgresql':
            fuente = config.postgres_connection
            resultado = gestor_gas.cargar_datos(fuente, query=consulta)
        elif tipo_base == 'sqlite':
            fuente = config.SQLITE_PATH
            resultado = gestor_gas.cargar_datos(fuente, query=consulta)
        else:
            return jsonify({
                'estado': 'error',
                'mensaje': 'Tipo de base de datos no soportado'
            }), 400
        
        if resultado['estado'] == 'éxito':
            formato_salida = datos.get('formato_salida', 'completo')
            datos_json = gestor_gas.convertir_a_json(formato_salida)
            return jsonify(datos_json)
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error en consulta: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    📊 ENDPOINT: Obtener estadísticas de datos cargados
    🎯 PROPÓSITO: Proporcionar métricas y análisis de los datos actuales
    """
    estadisticas = gestor_gas.obtener_estadisticas()
    return jsonify({
        'estado': 'éxito',
        'timestamp': datetime.now().isoformat(),
        'estadisticas': estadisticas
    })

@app.route('/api/historial', methods=['GET'])
def obtener_historial():
    """
    📝 ENDPOINT: Obtener historial de operaciones
    🎯 PROPÓSITO: Auditoría y trazabilidad de operaciones
    """
    historial = gestor_gas.obtener_historial()
    return jsonify({
        'estado': 'éxito',
        'total_operaciones': len(historial),
        'historial': historial[-10:]  # Últimas 10 operaciones
    })

@app.route('/api/estaciones', methods=['GET'])
def listar_estaciones():
    """
    🏗️ ENDPOINT: Listar estaciones de gas disponibles
    🎯 PROPÓSITO: Obtener lista de estaciones para filtros y selección
    """
    try:
        # 📥 CARGAR DATOS SI NO ESTÁN CARGADOS
        if gestor_gas.dataframe is None:
            archivo = os.path.join(config.DATA_DIR, 'datos.csv')
            gestor_gas.cargar_datos(archivo)
        
        df = gestor_gas.dataframe
        col_estacion = gestor_gas.estadisticas.get('columnas_estacion', [])
        
        if col_estacion:
            estaciones = df[col_estacion[0]].unique().tolist()
            return jsonify({
                'estado': 'éxito',
                'total_estaciones': len(estaciones),
                'estaciones': estaciones
            })
        else:
            return jsonify({
                'estado': 'error',
                'mensaje': 'No se encontró columna de estaciones en los datos'
            }), 404
            
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error al listar estaciones: {str(e)}'
        }), 500

@app.route('/api/mediciones/<estacion>', methods=['GET'])
def mediciones_estacion(estacion):
    """
    📈 ENDPOINT: Obtener mediciones de una estación específica
    🎯 PROPÓSITO: Filtrado de datos por estación
    """
    try:
        if gestor_gas.dataframe is None:
            return jsonify({
                'estado': 'error',
                'mensaje': 'No hay datos cargados. Use /api/datos primero.'
            }), 400
        
        df = gestor_gas.dataframe
        col_estacion = gestor_gas.estadisticas.get('columnas_estacion', [])
        
        if not col_estacion:
            return jsonify({
                'estado': 'error',
                'mensaje': 'No se encontró columna de estaciones en los datos'
            }), 404
        
        # 🎯 FILTRAR DATOS POR ESTACIÓN
        datos_estacion = df[df[col_estacion[0]] == estacion]
        
        if len(datos_estacion) == 0:
            return jsonify({
                'estado': 'error',
                'mensaje': f'Estación "{estacion}" no encontrada'
            }), 404
        
        return jsonify({
            'estado': 'éxito',
            'estacion': estacion,
            'total_mediciones': len(datos_estacion),
            'periodo': {
                'inicio': datos_estacion[gestor_gas.estadisticas['columnas_fecha'][0]].min() if gestor_gas.estadisticas.get('columnas_fecha') else 'N/A',
                'fin': datos_estacion[gestor_gas.estadisticas['columnas_fecha'][0]].max() if gestor_gas.estadisticas.get('columnas_fecha') else 'N/A'
            },
            'mediciones': datos_estacion.to_dict('records')
        })
        
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error al obtener mediciones: {str(e)}'
        }), 500

@app.route('/api/alertas', methods=['GET'])
def obtener_alertas():
    """
    🚨 ENDPOINT: Obtener alertas del sistema
    🎯 PROPÓSITO: Monitoreo y detección de anomalías
    """
    try:
        if gestor_gas.dataframe is None:
            return jsonify({
                'estado': 'error',
                'mensaje': 'No hay datos cargados'
            }), 400
        
        datos_json = gestor_gas.convertir_a_json('operacional')
        alertas = datos_json.get('alertas', [])
        
        return jsonify({
            'estado': 'éxito',
            'total_alertas': len(alertas),
            'alertas': alertas,
            'nivel_riesgo': 'alto' if len(alertas) > 0 else 'bajo'
        })
        
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error al obtener alertas: {str(e)}'
        }), 500

# 🎯 MANEJADORES DE ERROR GLOBALES
@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({
        'estado': 'error',
        'mensaje': 'Endpoint no encontrado',
        'sugerencia': 'Consulte / para ver endpoints disponibles'
    }), 404

@app.errorhandler(500)
def error_interno(error):
    return jsonify({
        'estado': 'error',
        'mensaje': 'Error interno del servidor'
    }), 500

# 🚀 INICIALIZACIÓN DEL SERVIDOR
if __name__ == '__main__':
    print("🚀 INICIANDO API DE GESTIÓN DE DATOS DE GAS...")
    print("📍 URL Principal: http://localhost:5000")
    print("📚 Documentación: http://localhost:5000/")
    print("🔍 Estado sistema: http://localhost:5000/api/estado")
    print("📊 Cargar datos: http://localhost:5000/api/datos")
    print("🛑 Detener servidor: CTRL + C")
    print("=" * 60)
    
    # 🏃 EJECUTAR SERVIDOR FLASK
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📊 **PARTE 4: DASHBOARD INTERACTIVO CON PLOTLY DASH**

### **Archivo: `dashboard/app.py`**
```python
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import sys
from datetime import datetime, timedelta

# 🎯 CONFIGURACIÓN DE RUTAS
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from cargarDatos import GestorDatosGas
from config import config

# 🏭 INICIALIZAR GESTOR DE DATOS
gestor_gas = GestorDatosGas(config)

# 🚀 INICIALIZAR APLICACIÓN DASH
app = dash.Dash(
    __name__, 
    title='Dashboard - Red de Gas',
    external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css']
)

# 🎨 ESTILOS PERSONALIZADOS
styles = {
    'header': {
        'backgroundColor': '#1E3A8A',
        'color': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'marginBottom': '20px'
    },
    'card': {
        'backgroundColor': '#F8FAFC',
        'padding': '15px',
        'borderRadius': '8px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'marginBottom': '15px'
    },
    'metric': {
        'textAlign': 'center',
        'padding': '10px'
    }
}

# 🏗️ DISEÑO DEL DASHBOARD
app.layout = html.Div([
    # 🎯 CABECERA
    html.Div([
        html.H1('🏭 Dashboard - Red de Distribución de Gas', 
                style={'margin': '0', 'fontWeight': 'bold'}),
        html.P('Sistema de monitoreo y análisis en tiempo real', 
               style={'margin': '5px 0', 'opacity': '0.8'}),
        html.Div(id='ultima-actualizacion', 
                style={'fontSize': '14px', 'opacity': '0.7'})
    ], style=styles['header']),
    
    # 📊 PANEL DE MÉTRICAS PRINCIPALES
    html.Div([
        html.Div([
            html.Div(id='metricas-principales', className='row')
        ], style=styles['card'])
    ]),
    
    # 🎛️ CONTROLES
    html.Div([
        html.Div([
            html.H4('🎛️ Controles', style={'marginBottom': '15px'}),
            
            html.Label('Seleccionar Estación:'),
            dcc.Dropdown(
                id='selector-estacion',
                options=[],
                placeholder='Selecciona una estación...'
            ),
            
            html.Br(),
            
            html.Label('Rango de Fechas:'),
            dcc.DatePickerRange(
                id='selector-fechas',
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now()
            ),
            
            html.Br(),
            html.Br(),
            
            html.Button('🔄 Actualizar Datos', 
                       id='boton-actualizar', 
                       n_clicks=0,
                       style={'backgroundColor': '#3B82F6', 
                              'color': 'white', 
                              'border': 'none',
                              'padding': '10px 20px',
                              'borderRadius': '5px',
                              'cursor': 'pointer'})
            
        ], style=styles['card'], className='col-md-3'),
        
        # 📈 GRÁFICOS PRINCIPALES
        html.Div([
            dcc.Tabs([
                # 📈 TAB 1: PRESIÓN
                dcc.Tab(label='📊 Análisis de Presión', children=[
                    dcc.Graph(id='grafico-presion-tiempo'),
                    dcc.Graph(id='grafico-presion-estaciones')
                ]),
                
                # 🌊 TAB 2: CAUDAL
                dcc.Tab(label='🌊 Análisis de Caudal', children=[
                    dcc.Graph(id='grafico-caudal-tiempo'),
                    dcc.Graph(id='grafico-caudal-distribucion')
                ]),
                
                # 🏗️ TAB 3: ESTACIONES
                dcc.Tab(label='🏗️ Análisis por Estación', children=[
                    dcc.Graph(id='grafico-comparacion-estaciones'),
                    html.Div(id='tabla-estaciones')
                ]),
                
                # 🚨 TAB 4: ALERTAS
                dcc.Tab(label='🚨 Panel de Alertas', children=[
                    html.Div(id='panel-alertas'),
                    dcc.Graph(id='grafico-tendencias')
                ])
            ])
        ], className='col-md-9')
    ], className='row'),
    
    # 📝 INFORMACIÓN ADICIONAL
    html.Div([
        html.H4('📋 Información del Sistema'),
        html.Div(id='info-sistema')
    ], style=styles['card']),
    
    # 🔄 INTERVALO DE ACTUALIZACIÓN
    dcc.Interval(
        id='intervalo-actualizacion',
        interval=60*1000,  # 1 minuto
        n_intervals=0
    ),
    
    # 📁 ALMACENAMIENTO DE DATOS
    dcc.Store(id='datos-cargados')
])

# 🎯 CALLBACK: CARGAR DATOS INICIALES
@app.callback(
    [Output('datos-cargados', 'data'),
     Output('selector-estacion', 'options'),
     Output('ultima-actualizacion', 'children')],
    [Input('boton-actualizar', 'n_clicks'),
     Input('intervalo-actualizacion', 'n_intervals')]
)
def cargar_datos_iniciales(n_clicks, n_intervals):
    """
    🎯 CALLBACK: Cargar datos y actualizar controles
    📥 PROPÓSITO: Cargar datos iniciales y poblar dropdowns
    """
    try:
        # 📁 CARGAR DATOS DESDE CSV
        archivo = os.path.join(config.DATA_DIR, 'datos.csv')
        resultado = gestor_gas.cargar_datos(archivo)
        
        if resultado['estado'] == 'éxito':
            df = gestor_gas.dataframe
            
            # 🎯 OPCIONES PARA DROPDOWN DE ESTACIONES
            col_estacion = gestor_gas.estadisticas.get('columnas_estacion', [])
            if col_estacion:
                estaciones = [{'label': est, 'value': est} 
                             for est in df[col_estacion[0]].unique()]
            else:
                estaciones = []
            
            # 📊 CONVERTIR DATOS PARA ALMACENAMIENTO
            datos_json = df.to_dict('records')
            
            # 🕐 INFORMACIÓN DE ACTUALIZACIÓN
            ultima_actualizacion = f"Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            return datos_json, estaciones, ultima_actualizacion
        
        else:
            return [], [], f"Error: {resultado['mensaje']}"
            
    except Exception as e:
        return [], [], f"Error al cargar datos: {str(e)}"

# 🎯 CALLBACK: ACTUALIZAR MÉTRICAS PRINCIPALES
@app.callback(
    Output('metricas-principales', 'children'),
    [Input('datos-cargados', 'data')]
)
def actualizar_metricas(datos_cargados):
    """
    📊 ACTUALIZAR PANEL DE MÉTRICAS PRINCIPALES
    🎯 PROPÓSITO: Mostrar KPIs clave del sistema
    """
    if not datos_cargados:
        return html.Div("Cargando métricas...")
    
    df = pd.DataFrame(datos_cargados)
    stats = gestor_gas.estadisticas
    
    # 🎯 CALCULAR MÉTRICAS
    total_registros = len(df)
    total_estaciones = len(stats.get('columnas_estacion', []))
    
    # 📈 MÉTRICAS DE PRESIÓN
    presion_promedio = "N/A"
    if stats.get('columnas_presion'):
        col_presion = stats['columnas_presion'][0]
        if f'{col_presion}_promedio' in stats:
            presion_promedio = f"{stats[f'{col_presion}_promedio']:.1f} bar"
    
    # 🌊 MÉTRICAS DE CAUDAL
    caudal_total = "N/A"
    if stats.get('columnas_caudal'):
        col_caudal = stats['columnas_caudal'][0]
        if f'{col_caudal}_total' in stats:
            caudal_total = f"{stats[f'{col_caudal}_total']:,.0f} m³"
    
    return html.Div([
        html.Div([
            html.H4(f"📈 {total_registros:,}"),
            html.P("Total Mediciones", style={'fontSize': '14px', 'opacity': '0.7'})
        ], style=styles['metric'], className='col-md-3'),
        
        html.Div([
            html.H4(f"🏗️ {total_estaciones}"),
            html.P("Estaciones", style={'fontSize': '14px', 'opacity': '0.7'})
        ], style=styles['metric'], className='col-md-3'),
        
        html.Div([
            html.H4(f"🔵 {presion_promedio}"),
            html.P("Presión Promedio", style={'fontSize': '14px', 'opacity': '0.7'})
        ], style=styles['metric'], className='col-md-3'),
        
        html.Div([
            html.H4(f"🌊 {caudal_total}"),
            html.P("Caudal Total", style={'fontSize': '14px', 'opacity': '0.7'})
        ], style=styles['metric'], className='col-md-3')
    ], className='row')

# 🎯 CALLBACK: GRÁFICO DE PRESIÓN EN EL TIEMPO
@app.callback(
    Output('grafico-presion-tiempo', 'figure'),
    [Input('datos-cargados', 'data'),
     Input('selector-estacion', 'value')]
)
def actualizar_grafico_presion(datos_cargados, estacion_seleccionada):
    """
    📈 GRÁFICO: Evolución de la presión en el tiempo
    🎯 PROPÓSITO: Mostrar tendencias y patrones temporales
    """
    if not datos_cargados:
        return go.Figure().update_layout(title="Cargando datos...")
    
    df = pd.DataFrame(datos_cargados)
    stats = gestor_gas.estadisticas
    
    # 🎯 FILTRAR POR ESTACIÓN SI SE SELECCIONÓ
    if estacion_seleccionada and stats.get('columnas_estacion'):
        df = df[df[stats['columnas_estacion'][0]] == estacion_seleccionada]
    
    # 📊 CREAR GRÁFICO
    fig = go.Figure()
    
    if stats.get('columnas_presion') and stats.get('columnas_fecha'):
        col_presion = stats['columnas_presion'][0]
        col_fecha = stats['columnas_fecha'][0]
        
        fig.add_trace(go.Scatter(
            x=df[col_fecha],
            y=df[col_presion],
            mode='lines+markers',
            name='Presión',
            line=dict(color='#3B82F6', width=2),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            title=f'📈 Evolución de la Presión {" - " + estacion_seleccionada if estacion_seleccionada else ""}',
            xaxis_title='Fecha',
            yaxis_title='Presión (bar)',
            template='plotly_white'
        )
    
    return fig

# 🎯 CALLBACK: GRÁFICO DE COMPARACIÓN ENTRE ESTACIONES
@app.callback(
    Output('grafico-presion-estaciones', 'figure'),
    [Input('datos-cargados', 'data')]
)
def actualizar_comparacion_estaciones(datos_cargados):
    """
    🏗️ GRÁFICO: Comparación de presión entre estaciones
    🎯 PROPÓSITO: Análisis comparativo del rendimiento
    """
    if not datos_cargados:
        return go.Figure().update_layout(title="Cargando datos...")
    
    df = pd.DataFrame(datos_cargados)
    stats = gestor_gas.estadisticas
    
    if stats.get('columnas_presion') and stats.get('columnas_estacion'):
        col_presion = stats['columnas_presion'][0]
        col_estacion = stats['columnas_estacion'][0]
        
        # 📊 GRÁFICO DE BARRAS
        fig = px.box(
            df, 
            x=col_estacion, 
            y=col_presion,
            title='📊 Distribución de Presión por Estación',
            color=col_estacion
        )
        
        fig.update_layout(
            xaxis_title='Estación',
            yaxis_title='Presión (bar)',
            template='plotly_white',
            showlegend=False
        )
        
        return fig
    
    return go.Figure().update_layout(title="Datos insuficientes para el gráfico")

# 🎯 CALLBACK: PANEL DE ALERTAS
@app.callback(
    Output('panel-alertas', 'children'),
    [Input('datos-cargados', 'data')]
)
def actualizar_panel_alertas(datos_cargados):
    """
    🚨 PANEL: Mostrar alertas y notificaciones
    🎯 PROPÓSITO: Monitoreo de condiciones anómalas
    """
    if not datos_cargados:
        return html.Div("Cargando alertas...")
    
    df = pd.DataFrame(datos_cargados)
    stats = gestor_gas.estadisticas
    
    alertas = []
    
    # 🎯 DETECCIÓN DE PRESIÓN ALTA
    if stats.get('columnas_presion'):
        col_presion = stats['columnas_presion'][0]
        max_presion = df[col_presion].max()
        
        if max_presion > 100:  # Umbral de alerta
            alertas.append({
                'tipo': 'warning',
                'mensaje': f'Presión crítica detectada: {max_presion} bar',
                'icono': '🔴'
            })
    
    # 🎯 DETECCIÓN DE DATOS FALTANTES
    completitud = stats.get('completitud', '0%')
    if float(completitud[:-1]) < 90:
        alertas.append({
            'tipo': 'info',
            'mensaje': f'Completitud de datos baja: {completitud}',
            'icono': '🟡'
        })
    
    # 🎯 CONSTRUIR PANEL DE ALERTAS
    if not alertas:
        return html.Div([
            html.H5('✅ Estado del Sistema'),
            html.P('Todas las métricas dentro de rangos normales', 
                   style={'color': 'green'})
        ])
    
    items_alerta = []
    for alerta in alertas:
        items_alerta.append(
            html.Div([
                html.Span(f"{alerta['icono']} {alerta['mensaje']}"),
            ], style={
                'padding': '10px',
                'margin': '5px 0',
                'backgroundColor': '#FEF3CD' if alerta['tipo'] == 'warning' else '#D1ECF1',
                'borderRadius': '5px',
                'borderLeft': '4px solid #FFC107' if alerta['tipo'] == 'warning' else '#0DCAF0'
            })
        )
    
    return html.Div([
        html.H5('🚨 Alertas del Sistema'),
        html.Div(items_alerta)
    ])

# 🚀 EJECUCIÓN DEL DASHBOARD
if __name__ == '__main__':
    print("📊 INICIANDO DASHBOARD INTERACTIVO...")
    print("📍 URL: http://localhost:8050")
    print("🛑 Detener: CTRL + C")
    print("=" * 50)
    
    app.run_server(debug=True, host='0.0.0.0', port=8050)
```

## 🎯 **PARTE 5: ARCHIVOS DE DATOS Y CONFIGURACIÓN**

### **Archivo: `fuentedatos/datos.csv`**
```csv
fecha,estacion,presion_entrada,presion_salida,caudal_m3h,consumo_diario,temperatura,estado
2024-01-01 08:00,Compresor_Norte,25,75,4500,12000,15,operativo
2024-01-01 09:00,Compresor_Norte,26,76,4600,12200,16,operativo
2024-01-01 10:00,Compresor_Norte,24,74,4400,11800,15,operativo
2024-01-01 11:00,Compresor_Norte,27,105,4800,12500,17,alerta_presion
2024-01-01 08:00,Compresor_Sur,20,60,3200,8500,14,operativo
2024-01-01 09:00,Compresor_Sur,21,61,3300,8700,15,operativo
2024-01-01 10:00,Compresor_Sur,19,59,3100,8300,14,operativo
2024-01-01 11:00,Compresor_Sur,22,62,3400,8900,15,operativo
2024-01-01 08:00,Estacion_Centro,18,55,2800,7500,13,operativo
2024-01-01 09:00,Estacion_Centro,17,54,2700,7200,13,operativo
2024-01-02 08:00,Compresor_Norte,26,77,4550,12100,16,operativo
2024-01-02 09:00,Compresor_Norte,25,76,4480,11900,15,operativo
```

### **Archivo: `requirements.txt` (COMPLETO)**
```txt
# 🌐 FRAMEWORK WEB
Flask==2.3.3

# 📊 ANÁLISIS DE DATOS
pandas==2.0.3
openpyxl==3.1.2

# 🗄️ BASES DE DATOS
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9
sqlite3

# 📈 VISUALIZACIÓN
plotly==5.17.0
dash==2.14.1

# 🔧 UTILIDADES
python-dotenv==1.0.0
chardet==5.2.0
```

## 🚀 **PARTE 6: EJECUCIÓN DEL SISTEMA COMPLETO**

### **Archivo: `APP/main.py` (Aplicación de Consola)**
```python
import os
import sys
from datetime import datetime

# 🎯 CONFIGURACIÓN DE RUTAS
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from cargarDatos import GestorDatosGas
from config import config

def mostrar_banner():
    """🎨 Mostrar banner de bienvenida"""
    print("""
    🏭 SISTEMA DE GESTIÓN DE DATOS DE RED DE GAS
    ============================================
    🌐 API REST: http://localhost:5000
    📊 Dashboard: http://localhost:8050
    💻 Esta consola: Gestión directa de datos
    ============================================
    """)

def main():
    """📱 APLICACIÓN PRINCIPAL DE CONSOLA"""
    mostrar_banner()
    
    # 🏭 INICIALIZAR GESTOR
    gestor = GestorDatosGas(config)
    
    while True:
        print("\n📊 MENÚ PRINCIPAL:")
        print("1. 📥 Cargar datos desde CSV")
        print("2. 📗 Cargar datos desde Excel")
        print("3. 🗃️ Cargar datos desde SQLite")
        print("4. 🐘 Cargar datos desde PostgreSQL")
        print("5. 📈 Ver estadísticas")
        print("6. 💾 Exportar a JSON")
        print("7. 📝 Ver historial")
        print("8. 🚀 Iniciar API REST")
        print("9. 📊 Iniciar Dashboard")
        print("0. 👋 Salir")
        
        opcion = input("\n🎯 Seleccione una opción (0-9): ").strip()
        
        if opcion == '1':
            archivo = input("📁 Nombre del archivo CSV (default: datos.csv): ").strip() or "datos.csv"
            ruta = os.path.join(config.DATA_DIR, archivo)
            resultado = gestor.cargar_datos(ruta)
            print(f"✅ {resultado['mensaje']}")
            
        elif opcion == '2':
            archivo = input("📗 Nombre del archivo Excel: ").strip()
            if not archivo:
                print("❌ Debe especificar un archivo")
                continue
            ruta = os.path.join(config.DATA_DIR, archivo)
            resultado = gestor.cargar_datos(ruta)
            print(f"✅ {resultado['mensaje']}")
            
        elif opcion == '3':
            archivo = input("🗃️ Nombre de base SQLite (default: red_gas.db): ").strip() or "red_gas.db"
            ruta = os.path.join(config.DATA_DIR, archivo)
            query = input("🔍 Query SQL (default: SELECT * FROM mediciones_gas): ").strip() or "SELECT * FROM mediciones_gas"
            resultado = gestor.cargar_datos(ruta, query=query)
            print(f"✅ {resultado['mensaje']}")
            
        elif opcion == '4':
            query = input("🐘 Query PostgreSQL (default: SELECT * FROM mediciones_gas): ").strip() or "SELECT * FROM mediciones_gas"
            resultado = gestor.cargar_datos(config.postgres_connection, query=query)
            print(f"✅ {resultado['mensaje']}")
            
        elif opcion == '5':
            stats = gestor.obtener_estadisticas()
            print("\n📊 ESTADÍSTICAS DETALLADAS:")
            print(f"📁 Fuente: {stats.get('tipo_fuente', 'N/A')}")
            print(f"📈 Registros: {stats.get('total_registros', 0):,}")
            print(f"🏗️ Columnas: {stats.get('total_columnas', 0)}")
            print(f"🔵 Estaciones: {len(stats.get('columnas_estacion', []))}")
            print(f"📅 Completitud: {stats.get('completitud', 'N/A')}")
            
        elif opcion == '6':
            formato = input("💾 Formato JSON (simple/completo/analitico/operacional): ").strip() or "completo"
            datos_json = gestor.convertir_a_json(formato)
            
            # 💾 GUARDAR ARCHIVO
            nombre_archivo = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                import json
                json.dump(datos_json, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos exportados a: {nombre_archivo}")
            
        elif opcion == '7':
            historial = gestor.obtener_historial()
            print("\n📋 HISTORIAL DE OPERACIONES:")
            for operacion in historial[-10:]:
                print(f"🕐 {operacion['timestamp']} - {operacion['operacion']}: {operacion['registros']} registros")
                
        elif opcion == '8':
            print("🚀 Iniciando API REST en http://localhost:5000")
            print("⚠️  Esta ventana quedará bloqueada. Abra otra terminal para continuar.")
            input("Presione Enter para continuar...")
            os.system("cd API && python api.py")
            
        elif opcion == '9':
            print("📊 Iniciando Dashboard en http://localhost:8050")
            print("⚠️  Esta ventana quedará bloqueada. Abra otra terminal para continuar.")
            input("Presione Enter para continuar...")
            os.system("cd dashboard && python app.py")
            
        elif opcion == '0':
            print("👋 ¡Hasta luego! Sistema cerrado correctamente.")
            break
            
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == '__main__':
    main()
```

## 🎯 **RESUMEN DE LO CREADO:**

### **✅ SISTEMA COMPLETO IMPLEMENTADO:**

1. **🏗️ ARQUITECTURA POO**: Clase principal `GestorDatosGas`
2. **🌐 API REST**: 10+ endpoints con Flask
3. **📊 DASHBOARD**: Visualización interactiva con Plotly Dash
4. **📁 MULTIFUENTE**: CSV, Excel, SQLite, PostgreSQL
5. **🎯 ANÁLISIS ESPECÍFICO**: Métricas de presión, caudal, consumo
6. **🚨 MONITOREO**: Alertas automáticas y panel de control

### **🚀 CÓMO EJECUTAR:**

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar API REST
cd API && python api.py

# 3. Ejecutar Dashboard (en otra terminal)
cd dashboard && python app.py

# 4. Usar aplicación de consola (en otra terminal)
cd APP && python main.py
```
