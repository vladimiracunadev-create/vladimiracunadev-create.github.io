#!/bin/bash
# scripts/sync-web.sh
TARGET_DIR="apps/mobile/www"

# Limpieza
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Copia de archivos core
cp index.html styles.css app.js pwa.js manifest.webmanifest service-worker.js offline.html "$TARGET_DIR/"

# Copia de rutas localizadas y contratos públicos usados por la web.
cp -r i18n api "$TARGET_DIR/"
mkdir -p "$TARGET_DIR/data"
cp data/portfolio-i18n.json "$TARGET_DIR/data/"
cp data/portfolio-translations.json "$TARGET_DIR/data/"

# Copia de assets públicos sin respaldos ni documentos privados.
mkdir -p "$TARGET_DIR/assets"
find assets -mindepth 1 -maxdepth 1 \
  ! -name backups ! -name no_aplica ! -name por_solicitud \
  -exec cp -r {} "$TARGET_DIR/assets/" \;

echo "Sincronización Web finalizada con éxito."
