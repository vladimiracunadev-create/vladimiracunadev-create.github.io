---
name: portfolio-mobile-direct-build
description: >
  Orquestra la transformación de la web en app Android directamente desde
  Windows. Gestiona sincronización, dependencias (npm install), plataforma
  (cap add android), sincronización de Capacitor y build final de APK vía
  Gradle con GRADLE_USER_HOME local. Úsalo para generar el APK o validar
  el wrapper Android de forma reproducible.
---

# Skill: Portfolio Mobile Direct Build

Este skill automatiza el flujo completo de construcción Android para este portafolio en entornos Windows.

## Capacidades del Script

El script orquestador (`/scripts/mobile-android-build.ps1`) realiza:
- **Sincronización**: Copia la web raíz a `apps/mobile/www`.
- **Dependencias**: Ejecuta `npm install` en el módulo móvil si faltan o si se usa `-ForceNpmInstall`.
- **Plataforma**: Añade automáticamente la carpeta `android` si no existe.
- **Entorno**: Configura `.gradle-user-home/` localmente para evitar fallos de permisos.
- **Build**: Genera el APK debug mediante `gradlew.bat assembleDebug`.

## Comandos y Parámetros

```powershell
# Ejecución estándar (Sync + Build)
./scripts/mobile-android-build.ps1

# Variantes
./scripts/mobile-android-build.ps1 -SkipGradle        # Solo sincronizar
./scripts/mobile-android-build.ps1 -ForceNpmInstall   # Refrescar dependencias
./scripts/mobile-android-build.ps1 -OpenAndroidStudio # Abrir IDE tras sync
```

## Resultado Esperado

- **Ruta APK**: `apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`.
- **Validación**: Flujo verificado con generación real de APK de ~4.32 MB.

## Documentación de Referencia

- `docs/MOBILE_DIRECT_BUILD.md`: Guía de operación detallada.
- `docs/GUIA_MAESTRA_MOBILE.md`: Visión general del ecosistema móvil.
