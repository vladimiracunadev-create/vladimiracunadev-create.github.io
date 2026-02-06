#!/bin/bash
# scripts/mobile-ios.sh

# 1. Sincronizar archivos web
echo ">>> Sincronizando archivos web..."
./scripts/sync-web.sh

# 2. Preparar apps/mobile
cd apps/mobile
echo ">>> Instalando dependencias de Capacitor..."
npm install

# 3. Añadir plataforma si no existe
if [ ! -d "ios" ]; then
    echo ">>> Añadiendo plataforma iOS..."
    npx cap add ios
fi

# 4. Sincronizar con Xcode
echo ">>> Sincronizando con iOS..."
npx cap sync ios

echo ""
echo "===================================================="
echo "PREPARACIÓN iOS COMPLETADA"
echo "===================================================="
echo "Instrucciones finales:"
echo "1. Ejecuta: npx cap open ios"
echo "2. En Xcode, selecciona el target 'App'."
echo "3. Configura el 'Signing & Capabilities' con tu Apple ID."
echo "4. Build -> Archive para generar el IPA."
echo "===================================================="
cd ../..
