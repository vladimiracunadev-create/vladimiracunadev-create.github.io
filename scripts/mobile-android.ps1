# scripts/mobile-android.ps1
# Script ultra-simplificado para evitar errores de parseo

$ErrorActionPreference = 'Stop'

# 1. Navegar a la raiz del proyecto
Set-Location -Path "$PSScriptRoot/.."

# 2. Sincronizar archivos web
Write-Host 'Sincronizando archivos web...'
powershell.exe -ExecutionPolicy Bypass -File '.\scripts\sync-web.ps1'

# 3. Preparar apps/mobile
Write-Host 'Instalando dependencias de Capacitor...'
Set-Location -Path 'apps/mobile'
npm install

# 4. Sincronizar plataforma Android
Write-Host 'Sincronizando con Android...'
npx cap sync android

Write-Host '--------------------------------------------'
Write-Host 'PREPARACION COMPLETADA'
Write-Host 'Ya puedes abrir Android Studio en apps/mobile/android'
Write-Host '--------------------------------------------'
