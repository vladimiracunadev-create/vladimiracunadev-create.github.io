# scripts/mobile-android.ps1
Set-Location -Path "$PSScriptRoot/.."

# 1. Sincronizar archivos web
Write-Host ">>> Sincronizando archivos web..." -ForegroundColor Cyan
powershell.exe -ExecutionPolicy Bypass -File .\scripts\sync-web.ps1

# 2. Preparar apps/mobile
Set-Location -Path "apps/mobile"
Write-Host ">>> Instalando dependencias de Capacitor..." -ForegroundColor Cyan
npm install

# 3. Añadir plataforma si no existe
if (-not (Test-Path "android")) {
    Write-Host ">>> Añadiendo plataforma Android..." -ForegroundColor Cyan
    npx cap add android
}

# 4. Sincronizar con Android Studio
Write-Host ">>> Sincronizando con Android..." -ForegroundColor Cyan
npx cap sync android

Write-Host "`n====================================================" -ForegroundColor Green
Write-Host "PREPARACIÓN ANDROID COMPLETADA" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
Write-Host "Instrucciones finales:"
Write-Host "1. Abre Android Studio."
Write-Host "2. Importa el proyecto existente en: $(Get-Location)\android"
Write-Host "3. Espera a que Gradle termine de sincronizar."
Write-Host "4. Ve a 'Build' -> 'Generate Signed Bundle / APK' para producir el binario final."
Write-Host "===================================================="

Set-Location -Path "../../"
