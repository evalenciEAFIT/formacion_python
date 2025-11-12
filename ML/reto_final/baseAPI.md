# 🚀 **GUÍA RÁPIDA: Crear API Flask con Pandas y JSON**

## 📁 **ESTRUCTURA DEL PROYECTO**

```
proyecto/
├── API/
│   └── api.py                 # 🌐 Tu archivo API principal
├── db/
│   └── cargaDatos/
│       └── cargar.py         # 📊 Clase/función para cargar datos
└── datos/
    └── datos.csv             # 📁 Tus datos de entrada
```

## 🛠️ **PASO 1: CONFIGURAR cargar.py**

### **Archivo: `db/cargaDatos/cargar.py`**
```python
import pandas as pd
import json
import os

def cargar_datos_csv(ruta_archivo):
    """
    📊 FUNCIÓN: Cargar CSV y convertir a JSON
    🎯 PROPÓSITO: Leer datos CSV y transformarlos a formato JSON
    📥 ENTRADA: Ruta del archivo CSV
    📤 SALIDA: Diccionario con datos en JSON
    """
    try:
        print(f"📂 Cargando archivo: {ruta_archivo}")
        
        # 📥 CARGAR CSV CON PANDAS
        df = pd.read_csv(ruta_archivo)
        
        # 🔄 CONVERTIR A DIFERENTES FORMATOS JSON
        resultado = {
            'estado': 'éxito',
            'mensaje': 'Datos cargados correctamente',
            'total_registros': len(df),
            'total_columnas': len(df.columns),
            'nombres_columnas': df.columns.tolist(),
            
            # 📊 FORMATOS JSON DISPONIBLES
            'formatos_json': {
                'simple': df.to_dict('records'),           # Lista de diccionarios
                'orientado': df.to_dict('orient'),         # Diferentes orientaciones
                'split': df.to_dict('split'),              # Estructura dividida
                'valores': df.values.tolist()              # Solo valores
            },
            
            # 📈 ESTADÍSTICAS BÁSICAS
            'estadisticas': {
                'primera_fila': df.iloc[0].to_dict() if len(df) > 0 else {},
                'ultima_fila': df.iloc[-1].to_dict() if len(df) > 0 else {},
                'tipos_datos': df.dtypes.astype(str).to_dict()
            }
        }
        
        print(f"✅ CSV convertido: {len(df)} filas, {len(df.columns)} columnas")
        return resultado
        
    except Exception as e:
        print(f"❌ Error al cargar CSV: {str(e)}")
        return {
            'estado': 'error',
            'mensaje': f'Error: {str(e)}',
            'total_registros': 0,
            'total_columnas': 0,
            'formatos_json': {},
            'estadisticas': {}
        }

# 🎯 FUNCIÓN ESPECÍFICA PARA DATOS DE GAS
def cargar_datos_gas(ruta_archivo):
    """
    🏭 FUNCIÓN ESPECIALIZADA: Para datos de red de gas
    🎯 PROPÓSITO: Análisis específico de datos de gas
    """
    try:
        df = pd.read_csv(ruta_archivo)
        
        # 🎯 IDENTIFICAR COLUMNAS DE GAS AUTOMÁTICAMENTE
        columnas_estacion = [col for col in df.columns if 'estacion' in col.lower()]
        columnas_presion = [col for col in df.columns if 'presion' in col.lower()]
        columnas_caudal = [col for col in df.columns if 'caudal' in col.lower()]
        
        resultado = {
            'estado': 'éxito',
            'sistema': 'red_gas',
            'datos_brutos': df.to_dict('records'),
            'analisis_especifico': {
                'estaciones_encontradas': columnas_estacion,
                'metricas_presion': columnas_presion,
                'metricas_caudal': columnas_caudal,
                'total_estaciones': df[columnas_estacion[0]].nunique() if columnas_estacion else 0
            }
        }
        
        return resultado
        
    except Exception as e:
        return {
            'estado': 'error',
            'mensaje': f'Error en datos de gas: {str(e)}'
        }
```

## 🌐 **PASO 2: CREAR API FLASK**

### **Archivo: `API/api.py`**
```python
from flask import Flask, jsonify, request
import os
import sys

# 🎯 CONFIGURAR RUTAS PARA IMPORTAR MÓDULOS
# IMPORTANTE: Agregar rutas al path de Python
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_proyecto = os.path.join(ruta_actual, '..')
ruta_db = os.path.join(ruta_proyecto, 'db', 'cargaDatos')
ruta_datos = os.path.join(ruta_proyecto, 'datos')

# 📁 AGREGAR RUTAS AL SISTEMA
sys.path.append(ruta_db)
sys.path.append(ruta_proyecto)

# 📦 IMPORTAR NUESTRA FUNCIÓN
from cargar import cargar_datos_csv, cargar_datos_gas

# 🚀 INICIALIZAR APLICACIÓN FLASK
app = Flask(__name__)

# 🎯 CONFIGURACIÓN
RUTA_CSV = os.path.join(ruta_datos, 'datos.csv')

@app.route('/')
def inicio():
    """
    🌐 ENDPOINT RAÍZ: Página de bienvenida
    🎯 PROPÓSITO: Mostrar que la API está funcionando
    """
    return jsonify({
        'mensaje': '🚀 API de Datos funcionando!',
        'endpoints': {
            '/datos': 'Cargar todos los datos',
            '/datos/<formato>': 'Cargar datos en formato específico',
            '/gas': 'Análisis específico para datos de gas',
            '/estadisticas': 'Estadísticas de los datos'
        },
        'ejemplos': {
            'cargar_todo': 'GET /datos',
            'formato_simple': 'GET /datos/simple',
            'analisis_gas': 'GET /gas'
        }
    })

@app.route('/datos', methods=['GET'])
@app.route('/datos/<formato>', methods=['GET'])
def obtener_datos(formato='simple'):
    """
    📊 ENDPOINT: Obtener datos del CSV
    🎯 PROPÓSITO: Cargar datos.csv y devolverlos en JSON
    📌 PARÁMETROS:
        - formato: simple, orientado, split, valores
    """
    try:
        print(f"🌐 Solicitud recibida para formato: {formato}")
        
        # 📥 USAR NUESTRA FUNCIÓN PARA CARGAR DATOS
        resultado = cargar_datos_csv(RUTA_CSV)
        
        if resultado['estado'] == 'éxito':
            # 🎯 SELECCIONAR FORMATO SOLICITADO
            datos_formateados = resultado['formatos_json'].get(formato, resultado['formatos_json']['simple'])
            
            respuesta = {
                'estado': 'éxito',
                'formato_solicitado': formato,
                'total_registros': resultado['total_registros'],
                'total_columnas': resultado['total_columnas'],
                'columnas': resultado['nombres_columnas'],
                'datos': datos_formateados
            }
            
            return jsonify(respuesta)
        else:
            # ❌ MANEJAR ERROR
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error en el servidor: {str(e)}'
        }), 500

@app.route('/gas', methods=['GET'])
def analisis_gas():
    """
    🏭 ENDPOINT: Análisis específico para datos de gas
    🎯 PROPÓSITO: Proporcionar análisis especializado
    """
    try:
        resultado = cargar_datos_gas(RUTA_CSV)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error en análisis de gas: {str(e)}'
        }), 500

@app.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    📈 ENDPOINT: Obtener estadísticas de los datos
    🎯 PROPÓSITO: Métricas y análisis de los datos cargados
    """
    try:
        resultado = cargar_datos_csv(RUTA_CSV)
        
        if resultado['estado'] == 'éxito':
            return jsonify({
                'estado': 'éxito',
                'estadisticas': resultado['estadisticas'],
                'resumen': {
                    'total_registros': resultado['total_registros'],
                    'total_columnas': resultado['total_columnas'],
                    'columnas': resultado['nombres_columnas']
                }
            })
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'estado': 'error', 
            'mensaje': f'Error al obtener estadísticas: {str(e)}'
        }), 500

@app.route('/buscar', methods=['GET'])
def buscar_datos():
    """
    🔍 ENDPOINT: Buscar datos específicos
    🎯 PROPÓSITO: Filtrar datos por parámetros
    📌 PARÁMETROS URL:
        - columna: Columna donde buscar
        - valor: Valor a buscar
        - limite: Límite de resultados
    """
    try:
        # 📥 OBTENER PARÁMETROS DE LA URL
        columna = request.args.get('columna', '')
        valor = request.args.get('valor', '')
        limite = request.args.get('limite', type=int, default=10)
        
        # 📊 CARGAR DATOS
        resultado = cargar_datos_csv(RUTA_CSV)
        
        if resultado['estado'] == 'éxito':
            datos = resultado['formatos_json']['simple']
            
            # 🎯 APLICAR FILTROS SI SE ESPECIFICARON
            if columna and valor:
                datos_filtrados = [
                    item for item in datos 
                    if str(valor).lower() in str(item.get(columna, '')).lower()
                ]
            else:
                datos_filtrados = datos
            
            # 📏 APLICAR LÍMITE
            datos_filtrados = datos_filtrados[:limite]
            
            return jsonify({
                'estado': 'éxito',
                'busqueda': {
                    'columna': columna,
                    'valor': valor,
                    'limite': limite
                },
                'resultados': len(datos_filtrados),
                'datos': datos_filtrados
            })
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'estado': 'error',
            'mensaje': f'Error en búsqueda: {str(e)}'
        }), 500

# 🚀 EJECUCIÓN DEL SERVIDOR
if __name__ == '__main__':
    print("🚀 INICIANDO API FLASK...")
    print(f"📁 Ruta datos: {RUTA_CSV}")
    print("📍 URL: http://localhost:5000")
    print("📚 Endpoints disponibles en: http://localhost:5000/")
    print("🛑 Detener: CTRL + C")
    print("=" * 50)
    
    # ✅ VERIFICAR QUE EL ARCHIVO EXISTE
    if os.path.exists(RUTA_CSV):
        print("✅ Archivo datos.csv encontrado")
    else:
        print("❌ ADVERTENCIA: Archivo datos.csv no encontrado")
        print(f"💡 Buscando en: {RUTA_CSV}")
    
    # 🏃 EJECUTAR SERVIDOR
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📁 **PASO 3: ARCHIVO DE DATOS DE EJEMPLO**

### **Archivo: `datos/datos.csv`**
```csv
id,estacion,fecha,presion,caudal,consumo,temperatura,estado
1,Compresor_Norte,2024-01-01 08:00,25,4500,12000,15,operativo
2,Compresor_Norte,2024-01-01 09:00,26,4600,12200,16,operativo
3,Compresor_Norte,2024-01-01 10:00,24,4400,11800,15,operativo
4,Compresor_Sur,2024-01-01 08:00,20,3200,8500,14,operativo
5,Compresor_Sur,2024-01-01 09:00,21,3300,8700,15,operativo
6,Estacion_Centro,2024-01-01 08:00,18,2800,7500,13,operativo
7,Estacion_Centro,2024-01-01 09:00,17,2700,7200,13,operativo
```

## 🚀 **PASO 4: EJECUTAR LA API**

### **Desde la terminal:**
```bash
# 📁 Navegar a la carpeta API
cd proyecto/API

# 🐍 Ejecutar la API
python api.py
```

### **📋 DEPENDENCIAS NECESARIAS:**
```txt
# requirements.txt
Flask==2.3.3
pandas==2.0.3
```

Instalar con:
```bash
pip install -r requirements.txt
```

## 🎯 **PASO 5: PROBAR LA API**

### **🌐 URLs para probar:**

1. **http://localhost:5000/** - Página de inicio
2. **http://localhost:5000/datos** - Todos los datos (formato simple)
3. **http://localhost:5000/datos/split** - Datos en formato split
4. **http://localhost:5000/gas** - Análisis específico de gas
5. **http://localhost:5000/estadisticas** - Estadísticas
6. **http://localhost:5000/buscar?columna=estacion&valor=norte** - Buscar

### **🔧 Ejemplo con curl:**
```bash
# Obtener todos los datos
curl http://localhost:5000/datos

# Obtener análisis de gas
curl http://localhost:5000/gas

# Buscar datos específicos
curl "http://localhost:5000/buscar?columna=estacion&valor=norte&limite=5"
```

## 📊 **RESULTADO ESPERADO:**

Cuando accedas a **http://localhost:5000/datos**, verás:

```json
{
  "estado": "éxito",
  "formato_solicitado": "simple",
  "total_registros": 7,
  "total_columnas": 8,
  "columnas": ["id", "estacion", "fecha", "presion", "caudal", "consumo", "temperatura", "estado"],
  "datos": [
    {
      "id": 1,
      "estacion": "Compresor_Norte",
      "fecha": "2024-01-01 08:00",
      "presion": 25,
      "caudal": 4500,
      "consumo": 12000,
      "temperatura": 15,
      "estado": "operativo"
    },
    ...
  ]
}
```
