# Mobile Direct Build (Windows + Android Studio)

Este documento es la guía técnica para transformar el núcleo web del portafolio en una aplicación Android directamente desde Windows.

## Propósito del Flujo

El script `scripts/mobile-android-build.ps1` automatiza la orquestación completa del build móvil:
1. Sincroniza los activos web en `apps/mobile/www`.
2. Gestiona dependencias en `apps/mobile` (ejecuta `npm install` si es necesario).
3. Asegura la existencia de la plataforma Android (`cap add android` si falta).
4. Sincroniza el bridge de Capacitor.
5. Ejecuta Gradle para generar el binario final.

## Script de Orquestación

```powershell
./scripts/mobile-android-build.ps1
```

### Parámetros Disponibles

| Parámetro | Descripción |
| :--- | :--- |
| `-SkipWebSync` | Omite la copia de archivos de la raíz a `apps/mobile/www`. |
| `-SkipGradle` | Solo orquestra la sincronización; no genera el APK. |
| `-ForceNpmInstall` | Fuerza la reinstalación de dependencias en el módulo móvil. |
| `-OpenAndroidStudio` | Abre el proyecto en Android Studio tras finalizar la sincronización. |

## Resultado y Validación

Tras una ejecución exitosa, el APK debug se localiza en:
`apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`

**Estado de Validación**: Este flujo ha sido verificado con una construcción real (`BUILD SUCCESSFUL`), generando un APK funcional de aproximadamente **4.32 MB**.

## Configuración y Notas Técnicas

- **GRADLE_USER_HOME**: El script configura el home de Gradle dentro del repositorio en `.gradle-user-home/` para evitar problemas de permisos.
- **IA**: Usa el skill `portfolio-mobile-direct-build` para automatizar este flujo.

---

[🏠 Volver al Home](Home) | **Vladimir Acuña** - Senior Software Engineer
