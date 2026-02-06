# scripts/sync-web.ps1
$TargetDir = "apps/mobile/www"

# Limpieza
if (Test-Path $TargetDir) {
    Remove-Item -Path "$TargetDir\*" -Recurse -Force
} else {
    New-Item -ItemType Directory -Path $TargetDir -Force
}

# Copia de archivos core
Copy-Item "index.html", "styles.css", "app.js", "pwa.js", "manifest.webmanifest", "service-worker.js", "offline.html" -Destination $TargetDir

# Copia de assets
Copy-Item "assets" -Destination $TargetDir -Recurse

Write-Host "Sincronización Web finalizada con éxito." -ForegroundColor Green
