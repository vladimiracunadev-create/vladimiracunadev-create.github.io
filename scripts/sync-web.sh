#!/bin/bash
# scripts/sync-web.sh
TARGET_DIR="apps/mobile/www"

# Limpieza
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Copia de archivos core
cp index.html styles.css app.js pwa.js manifest.webmanifest service-worker.js offline.html "$TARGET_DIR/"

# Copia de assets
cp -r assets "$TARGET_DIR/"

echo "Sincronización Web finalizada con éxito."
