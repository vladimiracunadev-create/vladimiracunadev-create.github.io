# Mobile Direct Build (Windows + Android Studio)

Este flujo permite generar la app Android del portafolio de forma directa desde Windows usando la base Capacitor ya incluida en el repositorio.

## Qué resuelve

- Sincroniza la web en `apps/mobile/www`
- Sincroniza Capacitor con Android
- Ejecuta Gradle para generar `app-debug.apk`
- Opcionalmente abre Android Studio

## Script directo

```powershell
./scripts/mobile-android-build.ps1
```

## Variantes útiles

```powershell
./scripts/mobile-android-build.ps1 -SkipGradle
./scripts/mobile-android-build.ps1 -ForceNpmInstall
./scripts/mobile-android-build.ps1 -OpenAndroidStudio
```

## Resultado esperado

El APK debug queda en:

```text
apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk
```

## Skill recomendado

Usa `portfolio-mobile-direct-build` cuando quieras que un agente transforme y regenere la web como app Android desde este entorno Windows.

## Requisitos

- Node.js disponible en PATH
- Android Studio instalado
- JDK/Gradle funcionando para el proyecto Android
- Dependencias de `apps/mobile` instaladas o instalables

## Nota de entorno

El script configura GRADLE_USER_HOME dentro del repositorio para evitar fallos de permisos en entornos Windows restringidos o sandboxes.
