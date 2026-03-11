# Mobile Direct Build (Windows + Android Studio)

Este documento es la guía operativa principal para transformar el núcleo web del portafolio en una aplicación Android instalable de forma directa desde Windows.

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

## Distribución del APK

El archivo generado por este flujo es un **APK debug**. Sirve para:

- pruebas locales;
- instalación manual en dispositivos;
- compartir binarios en una **GitHub Release**.

No está pensado para **Google Play**. Para publicación formal se debe generar un binario firmado (`signed APK` o `AAB`) desde Android Studio.

### Subida recomendada a GitHub Release

No subas el APK directamente al árbol del repositorio. Publícalo como asset de una release:

1. Abre la página de releases del repositorio en GitHub.
2. Crea una release nueva o edita una existente.
3. Arrastra `app-debug.apk` a la zona de assets.
4. Publica la release.

Ruta del archivo:
`C:\portfolio-pages\apps\mobile\android\app\build\outputs\apk\debug\app-debug.apk`

## Configuración y Notas Técnicas

- **GRADLE_USER_HOME**: Para garantizar la reproducibilidad y evitar problemas de permisos en Windows, el script configura el home de Gradle dentro del repositorio en `.gradle-user-home/`.
- **Recuperación automática**: Si el caché base de Gradle falla, el script reintenta una vez con un `GRADLE_USER_HOME` limpio para evitar bloqueos por caché corrupto.
- **Automatización**: Usa el skill `portfolio-mobile-direct-build` para que un asistente de IA ejecute este flujo de forma autónoma.
- **Requisitos**: Node.js en el PATH y Android Studio instalado.
