# Guía de Resolución de Problemas - iOS (Capacitor)

Este documento detalla los problemas encontrados durante la configuración inicial de la aplicación iOS y cómo se resolvieron.

## 1. Error de "Signing & Capabilities" (Development Team)
**Problema:** Xcode arrojaba el error: *"Signing for App requires a development team. Select a development team in the Signing & Capabilities editor."*

**Solución:**
- Es necesario seleccionar un Apple ID en la pestaña **Signing & Capabilities** del target principal en Xcode.
- Esto es obligatorio para compilar hacia un dispositivo físico o generar un archivo `.ipa`.

## 2. Error de "Communication with Apple failed" (No Devices)
**Problema:** *"Your team has no devices from which to generate a provisioning profile."*

**Solución:**
- Este error ocurre cuando intentas compilar para un dispositivo físico sin tener uno conectado o registrado.
- **Opción A:** Conectar un iPhone real al Mac.
- **Opción B:** Usar un **Simulador**. Para el simulador no es estrictamente necesario el aprovisionamiento de Apple.

## 3. Simuladores faltantes
**Problema:** No aparecían simuladores en la lista de destinos de Xcode.

**Solución:**
- Se verificó que el runtime de iOS no estaba instalado.
- Se instaló mediante **Xcode > Settings > Platforms > iOS**.
- Se crearon simuladores manualmente desde **Window > Devices and Simulators**.

## 4. Sincronización de Archivos Web
**Problema:** Asegurar que los cambios en la web se reflejen en la app móvil.

**Solución:**
- Se utilizó el script `./scripts/mobile-ios.sh`, el cual ejecuta:
  1. `./scripts/sync-web.sh` (Copia de `index.html`, `assets/`, etc. a `apps/mobile/www`).
  2. `npx cap sync ios` (Sincroniza la carpeta `www` con el proyecto nativo de Xcode).

---
[← Volver al README](../README.md) | **Vladimir Acuña** - Senior Software Engineer
