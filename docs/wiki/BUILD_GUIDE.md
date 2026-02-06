# Guía de Construcción Detallada

Este documento profundiza en los pasos técnicos para generar ejecutables móviles y resolver conflictos específicos de entorno.

## 🛠 Requisitos de Software

* **Node.js**: v18 o superior.
* **Android Studio**: Ladybug (o versión estable reciente) con SDK 34+.
* **Xcode**: v15+ (solo macOS).
* **Capacitor CLI**: Instalado localmente en `apps/mobile/node_modules`.

---

## 🤖 Android Deep-Dive

### Solución de Problemas (Troubleshooting)

#### 1. Error de Ejecución de Scripts (PowerShell)
Si recibes `PSSecurityException` en Windows:
```powershell
powershell.exe -ExecutionPolicy Bypass -File ./scripts/mobile-android.ps1
```

#### 2. Menú "Build" Deshabilitado
* **Sincronización**: `File` > `Sync Project with Gradle Files`.
* **Directorio**: Asegúrate de abrir `apps/mobile/android` específicamente.

#### 3. Errores de Codificación
Asegúrate de que los archivos `.ps1` estén guardados en **UTF-8**.

---

## 🍎 iOS Deep-Dive

### Solución de Problemas (Troubleshooting)

Consulta la [Guía Específica de iOS](IOS_TROUBLESHOOTING) para detalles sobre certificados y simuladores.

---

## 📜 Reglas de Limpieza y Sincronización

* Mantener el repositorio libre de carpetas `.idea`, `.vscode` y `node_modules` de nivel nativo.
* En Windows, evitar subir cambios accidentales en permisos de archivos Unix (`gradlew`).

---
**Vladimir Acuña** - Senior Software Engineer
