---
name: portfolio-mobile-direct-build
description: >
  Genera de forma directa la app Android del portafolio desde Windows usando la
  base Capacitor del repositorio, sincronizando la web, actualizando Android y
  construyendo `app-debug.apk`. Úsalo cuando el usuario pida transformar la web
  en app móvil, regenerar el APK o validar el wrapper Android con Android Studio.
---

# Skill: Portfolio Mobile Direct Build

Usar este skill para convertir la versión web actual del portafolio en una app Android reproducible desde este repositorio.

## Flujo recomendado

1. Confirmar que el repo tenga `apps/mobile`, `capacitor.config.ts` y plataforma Android.
2. Ejecutar `./scripts/mobile-android-build.ps1` desde la raíz.
3. Si el usuario solo quiere sincronizar sin compilar, usar `-SkipGradle`.
4. Si el usuario quiere abrir Android Studio después del sync, usar `-OpenAndroidStudio`.
5. Verificar el artefacto final en `apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`.

## Comandos clave

```powershell
./scripts/mobile-android-build.ps1
./scripts/mobile-android-build.ps1 -SkipGradle
./scripts/mobile-android-build.ps1 -OpenAndroidStudio
```

## Qué debe revisar

- `scripts/sync-web.ps1`
- `apps/mobile/capacitor.config.ts`
- `apps/mobile/android/`
- `docs/MOBILE_DIRECT_BUILD.md`

## Resultado esperado

- Web sincronizada en `apps/mobile/www`
- Proyecto Android actualizado vía Capacitor
- APK debug generado o ruta exacta del fallo si el entorno Gradle/JDK no está sano
