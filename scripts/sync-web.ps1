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

# Copia de rutas localizadas y del contrato JSON público usado por la web.
Copy-Item "i18n" -Destination $TargetDir -Recurse -Force
Copy-Item "api" -Destination $TargetDir -Recurse -Force
New-Item -ItemType Directory -Path (Join-Path $TargetDir 'data') -Force | Out-Null
Copy-Item "data/portfolio-i18n.json" -Destination (Join-Path $TargetDir 'data') -Force

# Copia de assets, excluyendo lo que el sitio NO publica.
# Copiar 'assets' entero metia dentro del APK:
#   - backups/       ~3 MB de PDFs historicos ya superados (41% del APK)
#   - no_aplica/     versiones descartadas que CLAUDE.md prohibe publicar
#   - por_solicitud/ la carta de recomendacion FIRMADA, que se entrega
#                    a peticion y no esta enlazada en la web
# index.html no referencia ninguna de las tres.
$excluir = @('backups', 'no_aplica', 'por_solicitud')
$assetsTarget = Join-Path $TargetDir 'assets'
New-Item -ItemType Directory -Path $assetsTarget -Force | Out-Null
Get-ChildItem -Path 'assets' -Force | Where-Object { $excluir -notcontains $_.Name } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $assetsTarget -Recurse -Force
}

Write-Host "Sincronización Web finalizada con éxito." -ForegroundColor Green
