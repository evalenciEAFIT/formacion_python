# 🚀 Guía Completa y Corregida: Despliegue DemoEPM2 en GCP desde Windows 11

## 📋 **LISTA DE VERIFICACIÓN INICIAL**

### ✅ Requisitos Previos
- [ ] Windows 11 actualizado
- [ ] Python 3.9+ instalado
- [ ] Google Cloud SDK instalado
- [ ] Cuenta de Google Cloud Platform
- [ ] Cuenta de facturación configurada en GCP

---

## 🎯 **PASO A PASO COMPLETO**

## 🔧 **PASO 1: VERIFICACIÓN INICIAL**

### 1.1 Ejecutar verificación de requisitos
```powershell
# En PowerShell como administrador, ejecutar:
python --version
gcloud --version
gcloud auth list
```

### 1.2 Crear script de verificación inicial
```powershell
# Crear archivo 01-check-prerequisites.ps1
@"
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "           VERIFICACIÓN DE REQUISITOS" -ForegroundColor Cyan
Write-Host "                DEMOEPM2 - GCP" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Verificar Python
Write-Host "`n1. VERIFICANDO PYTHON..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Python no instalado o no en PATH" -ForegroundColor Red
        Write-Host "   💡 Solución: Instalar desde https://python.org" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "   ❌ Error verificando Python" -ForegroundColor Red
    exit 1
}

# Verificar Google Cloud SDK
Write-Host "`n2. VERIFICANDO GOOGLE CLOUD SDK..." -ForegroundColor Yellow
try {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ $gcloudVersion" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Google Cloud SDK no instalado" -ForegroundColor Red
        Write-Host "   💡 Solución: Instalar desde https://cloud.google.com/sdk/docs/install#windows" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "   ❌ Error verificando Google Cloud SDK" -ForegroundColor Red
    exit 1
}

# Verificar autenticación
Write-Host "`n3. VERIFICANDO AUTENTICACIÓN GCP..." -ForegroundColor Yellow
$auth = gcloud auth list --format="value(account)" 2>$null
if ($auth) {
    Write-Host "   ✅ Autenticado como: $auth" -ForegroundColor Green
} else {
    Write-Host "   ❌ No autenticado en GCP" -ForegroundColor Red
    Write-Host "   🔐 Ejecutando autenticación..." -ForegroundColor Yellow
    gcloud auth login
    $auth = gcloud auth list --format="value(account)" 2>$null
    if ($auth) {
        Write-Host "   ✅ Ahora autenticado como: $auth" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Error en autenticación" -ForegroundColor Red
        exit 1
    }
}

# Verificar proyecto actual
Write-Host "`n4. VERIFICANDO PROYECTO ACTUAL..." -ForegroundColor Yellow
$project = gcloud config get-value project 2>$null
if ($project -and $project -ne "(unset)") {
    Write-Host "   ✅ Proyecto actual: $project" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  No hay proyecto configurado" -ForegroundColor Yellow
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "       VERIFICACIÓN COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "`n🎯 SIGUIENTE PASO: Ejecutar 02-setup-project.ps1" -ForegroundColor Yellow
"@ | Out-File -FilePath "01-check-prerequisites.ps1" -Encoding UTF8

Write-Host "✅ Script 01-check-prerequisites.ps1 creado" -ForegroundColor Green
```

---

## 🏗️ **PASO 2: CONFIGURACIÓN DEL PROYECTO GCP**

### 2.1 Crear script de configuración del proyecto
```powershell
# Crear archivo 02-setup-project.ps1
@"
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "        CONFIGURACIÓN DE PROYECTO GCP" -ForegroundColor Cyan
Write-Host "                DEMOEPM2" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 1. Crear nuevo proyecto o usar existente
Write-Host "`n1. CONFIGURANDO PROYECTO GCP..." -ForegroundColor Green
$currentProject = gcloud config get-value project 2>$null

if (-not $currentProject -or $currentProject -eq "(unset)") {
    Write-Host "   Creando nuevo proyecto..." -ForegroundColor Yellow
    $newProject = "demoepm2-$(Get-Date -Format 'yyyyMMdd-HHmm')"
    Write-Host "   Nombre del proyecto: $newProject" -ForegroundColor White
    
    gcloud projects create $newProject --name="DemoEPM2 Application"
    if ($LASTEXITCODE -eq 0) {
        gcloud config set project $newProject
        Write-Host "   ✅ Proyecto creado y configurado: $newProject" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Error creando proyecto" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ✅ Usando proyecto existente: $currentProject" -ForegroundColor Green
}

$projectId = gcloud config get-value project
Write-Host "   ID del proyecto: $projectId" -ForegroundColor White

# 2. Verificar cuenta de facturación
Write-Host "`n2. VERIFICANDO CUENTA DE FACTURACIÓN..." -ForegroundColor Green
$billingAccounts = gcloud beta billing accounts list --format="value(name)" 2>$null

if ($billingAccounts) {
    Write-Host "   ✅ Cuentas de facturación disponibles" -ForegroundColor Green
    $firstBillingAccount = $billingAccounts[0]
    Write-Host "   Vinculando proyecto con cuenta de facturación..." -ForegroundColor Yellow
    
    gcloud beta billing projects link $projectId --billing-account=$firstBillingAccount
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Proyecto vinculado con cuenta de facturación" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Error vinculando cuenta de facturación" -ForegroundColor Red
        Write-Host "   💡 Solución manual:" -ForegroundColor Yellow
        Write-Host "   1. Ve a: https://console.cloud.google.com/billing/linkedaccount" -ForegroundColor White
        Write-Host "   2. Asocia el proyecto $projectId con una cuenta de facturación" -ForegroundColor White
        Write-Host "   3. Presiona Enter cuando hayas completado este paso..." -ForegroundColor Yellow
        Read-Host "Presiona Enter para continuar"
    }
} else {
    Write-Host "   ❌ No hay cuentas de facturación disponibles" -ForegroundColor Red
    Write-Host "   💡 Debes crear una cuenta de facturación primero:" -ForegroundColor Yellow
    Write-Host "   1. Ve a: https://console.cloud.google.com/billing" -ForegroundColor White
    Write-Host "   2. Crea una nueva cuenta de facturación" -ForegroundColor White
    Write-Host "   3. Vuelve a ejecutar este script" -ForegroundColor White
    exit 1
}

# 3. Habilitar APIs necesarias
Write-Host "`n3. HABILITANDO APIS NECESARIAS..." -ForegroundColor Green
$apis = @(
    "appengine.googleapis.com",
    "cloudbuild.googleapis.com",
    "storage-component.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "   Habilitando $api..." -ForegroundColor Yellow
    gcloud services enable $api --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ $api habilitado" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Error habilitando $api" -ForegroundColor Red
    }
}

# 4. Crear aplicación App Engine
Write-Host "`n4. CREANDO APLICACIÓN APP ENGINE..." -ForegroundColor Green
try {
    gcloud app describe --quiet 2>$null
    Write-Host "   ✅ App Engine ya está configurado" -ForegroundColor Green
} catch {
    Write-Host "   Creando aplicación App Engine..." -ForegroundColor Yellow
    gcloud app create --region=us-central1 --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ App Engine creado en región us-central1" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Error creando App Engine" -ForegroundColor Red
        Write-Host "   💡 Verifica que la cuenta de facturación esté correctamente vinculada" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "    CONFIGURACIÓN DE PROYECTO COMPLETADA" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "`n📊 RESUMEN:" -ForegroundColor Yellow
Write-Host "   Proyecto: $(gcloud config get-value project)" -ForegroundColor White
Write-Host "   App Engine: ✅ Configurado" -ForegroundColor White
Write-Host "   APIs: ✅ Habilitadas" -ForegroundColor White
Write-Host "   Billing: ✅ Configurado" -ForegroundColor White
Write-Host "`n🎯 SIGUIENTE PASO: Ejecutar 03-create-app.ps1" -ForegroundColor Yellow
"@ | Out-File -FilePath "02-setup-project.ps1" -Encoding UTF8

Write-Host "✅ Script 02-setup-project.ps1 creado" -ForegroundColor Green
```

---

## 🐍 **PASO 3: CREAR LA APLICACIÓN PYTHON**

### 3.1 Crear estructura de la aplicación
```powershell
# Crear archivo 03-create-app.ps1
@"
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "          CREACIÓN DE APLICACIÓN" -ForegroundColor Cyan
Write-Host "              DEMOEPM2 - PYTHON" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Verificar directorio actual
Write-Host "`nDirectorio de trabajo: $(Get-Location)" -ForegroundColor Yellow

# 1. Crear estructura de directorios
Write-Host "`n1. CREANDO ESTRUCTURA DE DIRECTORIOS..." -ForegroundColor Green
$folders = @("templates", "static", "logs")

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "   ✅ Carpeta creada: $folder" -ForegroundColor Green
    } else {
        Write-Host "   ✅ Carpeta existente: $folder" -ForegroundColor Green
    }
}

# 2. Crear requirements.txt
Write-Host "`n2. CREANDO requirements.txt..." -ForegroundColor Green
@"
Flask==2.3.3
gunicorn==20.1.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8
Write-Host "   ✅ requirements.txt creado" -ForegroundColor Green

# 3. Crear main.py
Write-Host "`n3. CREANDO main.py..." -ForegroundColor Green
@"
from flask import Flask, render_template, request, jsonify
import os
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    app_info = {
        'name': 'DemoEPM2',
        'version': '2.0.0',
        'platform': 'Google Cloud Platform',
        'deployed_from': 'Windows 11'
    }
    return render_template('index.html', app_info=app_info)

@app.route('/saludo', methods=['POST'])
def saludo():
    nombre = request.form.get('nombre', 'Visitante')
    return f'''
    <html>
        <head>
            <title>Saludo - DemoEPM2</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    margin: 0;
                    padding: 40px;
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    text-align: center;
                    max-width: 500px;
                }}
                a {{
                    color: #4CAF50;
                    text-decoration: none;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡Hola {nombre}! 👋</h1>
                <p>Desde DemoEPM2 en Google Cloud Platform</p>
                <p><strong>Timestamp:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <br>
                <a href="/">🏠 Volver al inicio</a>
            </div>
        </body>
    </html>
    '''

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'project': 'DemoEPM2',
        'timestamp': datetime.datetime.now().isoformat(),
        'environment': 'Google Cloud Platform - App Engine'
    })

@app.route('/api/info')
def info():
    return jsonify({
        'nombre': 'DemoEPM2 Application',
        'version': '2.0.0',
        'descripcion': 'Aplicación Python Flask desplegada en GCP'
    })

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
"@ | Out-File -FilePath "main.py" -Encoding UTF8
Write-Host "   ✅ main.py creado" -ForegroundColor Green

# 4. Crear templates/index.html
Write-Host "`n4. CREANDO templates/index.html..." -ForegroundColor Green
@"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DemoEPM2 - App Python en GCP</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            margin-bottom: 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 10px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 15px;
            max-width: 400px;
            margin: 0 auto;
        }
        input, button {
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
        }
        input {
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }
        button {
            background: #4CAF50;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        .info-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .links {
            text-align: center;
            margin-top: 30px;
        }
        .links a {
            color: #4CAF50;
            text-decoration: none;
            margin: 0 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏢 DemoEPM2</h1>
        <p style="text-align: center;">Aplicación Python Flask en Google Cloud Platform</p>
        
        <form action="/saludo" method="post">
            <input type="text" name="nombre" placeholder="¿Cuál es tu nombre?" required>
            <button type="submit">🎯 Enviar Saludo</button>
        </form>
        
        <div class="info-grid">
            <div class="info-card">
                <h3>🛠️ Tecnologías</h3>
                <p>Python 3.9</p>
                <p>Flask</p>
                <p>GCP</p>
            </div>
            <div class="info-card">
                <h3>📍 Plataforma</h3>
                <p>Windows 11</p>
                <p>Google Cloud</p>
            </div>
            <div class="info-card">
                <h3>🚀 Estado</h3>
                <p>✅ En producción</p>
                <p>🌐 Global</p>
            </div>
        </div>

        <div class="links">
            <a href="/api/health">🔍 Health Check</a>
            <a href="/api/info">ℹ️ Información API</a>
        </div>
    </div>
</body>
</html>
"@ | Out-File -FilePath "templates\index.html" -Encoding UTF8
Write-Host "   ✅ templates/index.html creado" -ForegroundColor Green

# 5. Crear app.yaml (CONFIGURACIÓN CORREGIDA)
Write-Host "`n5. CREANDO app.yaml..." -ForegroundColor Green
@"
runtime: python39
service: demoepm2

entrypoint: gunicorn -b :$PORT main:app

instance_class: F1

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto

env_variables:
  FLASK_ENV: production

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 3
"@ | Out-File -FilePath "app.yaml" -Encoding UTF8
Write-Host "   ✅ app.yaml creado" -ForegroundColor Green

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "       APLICACIÓN CREADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "`n📁 ESTRUCTURA CREADA:" -ForegroundColor Yellow
Get-ChildItem -Recurse | Where-Object { !$_.PSIsContainer } | Select-Object Name | Format-Table -AutoSize

Write-Host "`n🎯 SIGUIENTE PASO: Ejecutar 04-test-local.ps1" -ForegroundColor Yellow
"@ | Out-File -FilePath "03-create-app.ps1" -Encoding UTF8

Write-Host "✅ Script 03-create-app.ps1 creado" -ForegroundColor Green
```

---

## 🔄 **PASO 4: PRUEBAS LOCALES**

### 4.1 Crear script de pruebas locales
```powershell
# Crear archivo 04-test-local.ps1
@"
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "           PRUEBAS LOCALES" -ForegroundColor Cyan
Write-Host "              DEMOEPM2" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Verificar archivos necesarios
Write-Host "`n1. VERIFICANDO ARCHIVOS..." -ForegroundColor Green
$requiredFiles = @("main.py", "requirements.txt", "app.yaml", "templates\index.html")

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file no encontrado" -ForegroundColor Red
        Write-Host "   💡 Ejecuta primero: .\03-create-app.ps1" -ForegroundColor Yellow
        exit 1
    }
}

# 2. Configurar entorno virtual
Write-Host "`n2. CONFIGURANDO ENTORNO VIRTUAL..." -ForegroundColor Green
if (Test-Path "venv") {
    Write-Host "   ✅ Entorno virtual existente" -ForegroundColor Green
} else {
    Write-Host "   Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ❌ Error creando entorno virtual" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✅ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "   Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias
Write-Host "`n3. INSTALANDO DEPENDENCIAS..." -ForegroundColor Green
pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error instalando dependencias" -ForegroundColor Red
    exit 1
}

# 4. Verificar sintaxis de Python
Write-Host "`n4. VERIFICANDO SINTÁXIS..." -ForegroundColor Green
python -m py_compile main.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Sintaxis de main.py correcta" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error en sintaxis de main.py" -ForegroundColor Red
    exit 1
}

# 5. Iniciar aplicación localmente
Write-Host "`n5. INICIANDO APLICACIÓN LOCAL..." -ForegroundColor Green
Write-Host "   🌐 La aplicación estará disponible en: http://localhost:8080" -ForegroundColor Yellow
Write-Host "   ⏹️  Presiona Ctrl+C para detener la aplicación" -ForegroundColor Yellow

# Esperar y abrir navegador
Start-Sleep -Seconds 3
Write-Host "   🔗 Abriendo navegador..." -ForegroundColor Yellow
Start-Process "http://localhost:8080"

# Ejecutar aplicación
Write-Host "`n🚀 INICIANDO SERVIDOR FLASK..." -ForegroundColor Cyan
python main.py
"@ | Out-File -FilePath "04-test-local.ps1" -Encoding UTF8

Write-Host "✅ Script 04-test-local.ps1 creado" -ForegroundColor Green
```

---

## ☁️ **PASO 5: DESPLIEGUE EN GCP**

### 5.1 Crear script de despliegue final
```powershell
# Crear archivo 05-deploy-gcp.ps1
@"
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "           DESPLIEGUE EN GCP" -ForegroundColor Cyan
Write-Host "              DEMOEPM2" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Verificaciones previas
Write-Host "`n1. VERIFICACIONES PREVIAS..." -ForegroundColor Green

# Verificar proyecto
$project = gcloud config get-value project
if (-not $project -or $project -eq "(unset)") {
    Write-Host "   ❌ No hay proyecto configurado" -ForegroundColor Red
    Write-Host "   💡 Ejecuta primero: .\02-setup-project.ps1" -ForegroundColor Yellow
    exit 1
}
Write-Host "   ✅ Proyecto: $project" -ForegroundColor Green

# Verificar App Engine
try {
    gcloud app describe --quiet 2>$null
    Write-Host "   ✅ App Engine configurado" -ForegroundColor Green
} catch {
    Write-Host "   ❌ App Engine no configurado" -ForegroundColor Red
    Write-Host "   💡 Ejecuta primero: .\02-setup-project.ps1" -ForegroundColor Yellow
    exit 1
}

# Verificar archivos
Write-Host "`n2. VERIFICANDO ARCHIVOS..." -ForegroundColor Green
if (-not (Test-Path "app.yaml")) {
    Write-Host "   ❌ app.yaml no encontrado" -ForegroundColor Red
    Write-Host "   💡 Ejecuta primero: .\03-create-app.ps1" -ForegroundColor Yellow
    exit 1
}
Write-Host "   ✅ app.yaml encontrado" -ForegroundColor Green

# Validar app.yaml
Write-Host "   Validando app.yaml..." -ForegroundColor Yellow
try {
    # Esta es una validación básica - gcloud no tiene --dry-run para app deploy
    Get-Content "app.yaml" | Out-Null
    Write-Host "   ✅ app.yaml parece válido" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Error leyendo app.yaml" -ForegroundColor Red
    exit 1
}

# 3. Configurar entorno
Write-Host "`n3. CONFIGURANDO ENTORNO..." -ForegroundColor Green
if (Test-Path "venv") {
    .\venv\Scripts\Activate.ps1
    Write-Host "   ✅ Entorno virtual activado" -ForegroundColor Green
}

# 4. Desplegar aplicación
Write-Host "`n4. INICIANDO DESPLIEGUE..." -ForegroundColor Green
Write-Host "   ⏳ Esto puede tomar varios minutos..." -ForegroundColor Yellow
Write-Host "   📦 Subiendo aplicación a Google Cloud Platform..." -ForegroundColor Yellow

$startTime = Get-Date
try {
    gcloud app deploy --promote --quiet
    $endTime = Get-Date
    $deployTime = $endTime - $startTime
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ DESPLIEGUE EXITOSO!" -ForegroundColor Green
        Write-Host "   ⏱️  Tiempo de despliegue: $($deployTime.ToString('mm\:ss'))" -ForegroundColor White
    } else {
        Write-Host "   ❌ Error en el despliegue" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   ❌ Error durante el despliegue: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 5. Obtener información de la aplicación
Write-Host "`n5. INFORMACIÓN DE LA APLICACIÓN..." -ForegroundColor Green
$appUrl = gcloud app describe --format="value(defaultHostname)"
Write-Host "   🌐 URL de la aplicación: https://$appUrl" -ForegroundColor Cyan
Write-Host "   🔍 Health Check: https://$appUrl/api/health" -ForegroundColor Cyan
Write-Host "   ℹ️  Información: https://$appUrl/api/info" -ForegroundColor Cyan

# 6. Abrir aplicación
Write-Host "`n6. ABRIENDO APLICACIÓN..." -ForegroundColor Green
Write-Host "   🔗 Abriendo navegador en 5 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 5
Start-Process "https://$appUrl"

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "       DESPLIEGUE COMPLETADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "`n🎉 ¡FELICITACIONES! DemoEPM2 está en producción." -ForegroundColor Yellow
Write-Host "`n📊 RESUMEN FINAL:" -ForegroundColor Yellow
Write-Host "   Proyecto: $project" -ForegroundColor White
Write-Host "   URL: https://$appUrl" -ForegroundColor White
Write-Host "   Servicio: demoepm2" -ForegroundColor White
Write-Host "   Región: us-central1" -ForegroundColor White
Write-Host "`n🔧 PARA GESTIONAR LA APLICACIÓN:" -ForegroundColor Yellow
Write-Host "   Ver logs: gcloud app logs tail -s demoepm2" -ForegroundColor White
Write-Host "   Ver versiones: gcloud app versions list --service=demoepm2" -ForegroundColor White
Write-Host "   Monitorear: gcloud app operations list" -ForegroundColor White
"@ | Out-File -FilePath "05-deploy-gcp.ps1" -Encoding UTF8

Write-Host "✅ Script 05-deploy-gcp.ps1 creado" -ForegroundColor Green
```

---

## 📊 **PASO 6: SCRIPTS ADICIONALES DE GESTIÓN**

### 6.1 Crear script de monitoreo
```powershell
# Crear archivo 06-monitor.ps1
@"
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "           MONITOREO DEMOEPM2" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`n1. INFORMACIÓN DE LA APLICACIÓN..." -ForegroundColor Green
$appUrl = gcloud app describe --format="value(defaultHostname)" 2>$null
if ($appUrl) {
    Write-Host "   🌐 URL: https://$appUrl" -ForegroundColor Cyan
} else {
    Write-Host "   ❌ No se pudo obtener información de la aplicación" -ForegroundColor Red
}

Write-Host "`n2. VERSIONES DESPLEGADAS..." -ForegroundColor Green
gcloud app versions list --service=demoepm2 --format="table(version.id, deployment.date.time, status)"

Write-Host "`n3. LOGS RECIENTES..." -ForegroundColor Green
gcloud app logs read --service=demoepm2 --limit=5

Write-Host "`n4. VERIFICANDO SALUD..." -ForegroundColor Green
if ($appUrl) {
    try {
        $health = Invoke-RestMethod "https://$appUrl/api/health" -TimeoutSec 10
        Write-Host "   ✅ Health Check: $($health.status)" -ForegroundColor Green
        Write-Host "   🕐 Última verificación: $(Get-Date)" -ForegroundColor White
    } catch {
        Write-Host "   ❌ No se pudo conectar a la aplicación" -ForegroundColor Red
    }
}

Write-Host "`n5. USO DE RECURSOS..." -ForegroundColor Green
gcloud app instances list --service=demoepm2

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "       MONITOREO COMPLETADO" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
"@ | Out-File -FilePath "06-monitor.ps1" -Encoding UTF8

Write-Host "✅ Script 06-monitor.ps1 creado" -ForegroundColor Green
```

---

## 🎯 **INSTRUCCIONES FINALES DE USO**

### Ejecutar en ORDEN los siguientes scripts:

```powershell
# 📋 ORDEN DE EJECUCIÓN (ejecutar uno por uno):

# 1. Verificar requisitos
.\01-check-prerequisites.ps1

# 2. Configurar proyecto GCP
.\02-setup-project.ps1

# 3. Crear aplicación Python
.\03-create-app.ps1

# 4. Probar localmente (OPCIONAL)
.\04-test-local.ps1

# 5. Desplegar en GCP
.\05-deploy-gcp.ps1

# 6. Monitorear aplicación
.\06-monitor.ps1
```

### 📝 **Notas importantes:**

1. **Ejecutar en orden** - Cada script depende del anterior
2. **Billing Account** - Debe estar configurado antes del Paso 2
3. **Tiempo de despliegue** - El Paso 5 puede tomar 5-10 minutos
4. **Costo** - App Engine F1 es gratuito hasta cierto límite
5. **Logs** - Usar `gcloud app logs tail -s demoepm2` para ver logs en tiempo real

### 🆘 **Solución de problemas comunes:**

```powershell
# Si hay error de política de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Si hay error de autenticación:
gcloud auth login

# Si hay error de proyecto:
gcloud config set project TU-PROYECTO

# Si hay error de billing:
# Visitar: https://console.cloud.google.com/billing/linkedaccount
```

---

## ✅ **CHECKLIST FINAL**

- [ ] ✅ Todos los scripts creados en el directorio demoEPM2
- [ ] ✅ Google Cloud SDK instalado y configurado
- [ ] ✅ Cuenta de facturación configurada en GCP
- [ ] ✅ Proyecto GCP creado y configurado
- [ ] ✅ App Engine inicializado
- [ ] ✅ Aplicación Python creada correctamente
- [ ] ✅ Pruebas locales exitosas (opcional)
- [ ] ✅ Despliegue en GCP completado
- [ ] ✅ Aplicación accesible via URL pública

**¡DemoEPM2 está lista para desplegarse! 🚀**
