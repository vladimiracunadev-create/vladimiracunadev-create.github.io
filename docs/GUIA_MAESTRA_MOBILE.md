# 📱 Guía Maestra: Desarrollo y Construcción Mobile (Android & iOS)

Esta guía proporciona instrucciones detalladas para la puesta en marcha, desarrollo y generación de archivos finales (APK e IPA) del portafolio.

---

## 🛠️ Requisitos de Hardware y Software

### 🤖 Android (Universal: Windows, macOS, Linux)
Para generar archivos **APK** o **AAB**:

| Componente | Requisito Mínimo | Recomendado |
| :--- | :--- | :--- |
| **Hardware** | 8GB RAM, procesador i5 | 16GB RAM, procesador i7/Apple Silicon, SSD |
| **SO** | Windows 10, macOS 11, Ubuntu 20.04 | Últimas versiones estables |
| **Software** | Node.js v18+, JDK 17 | Node.js v22+, JDK 21 |
| **IDE** | Android Studio Jellyfish+ | Android Studio (Última versión) |

### 🍎 iOS (Solo macOS)
Para generar archivos **IPA**:

| Componente | Requisito Mínimo | Recomendado |
| :--- | :--- | :--- |
| **Hardware** | MacBook Air/Pro (Intel o M1) | Mac con Apple Silicon (M1/M2/M3) |
| **SO** | macOS Ventura (13.0) | macOS Sonoma (14.0) o superior |
| **Software** | Xcode 15, CocoaPods 1.12 | Xcode 16, CocoaPods (Última versión) |
| **Cuenta** | Apple ID básico | Apple Developer Program (para App Store) |

---

## 🚀 Fase 1: Puesta en Marcha (Setup Inicial)

1. **Clonar el Repositorio**:
   ```bash
   git clone [URL-DEL-REPO]
   cd vladimiracunadev-create.github.io
   ```
2. **Instalar Dependencias Base**:
   ```bash
   npm install
   ```
3. **Preparar Módulo Mobile**:
   ```bash
   cd apps/mobile
   npm install
   ```

---

## 🏗️ Fase 2: Ciclo de Desarrollo y Sincronización

Cada vez que realices un cambio en el código web (raíz del proyecto), debes sincronizarlo con las plataformas móviles:

### Operación en un solo paso:
- **Para iOS (en macOS)**:
  ```bash
  ./scripts/mobile-ios.sh
  ```
- **Para Android (en Windows/PowerShell)**:
  ```powershell
  ./scripts/mobile-android.ps1
  ```

---

## 📦 Fase 3: Creación Efectiva de Archivos

### 🤖 Generación de APK (Android)
1. Abre **Android Studio**.
2. Selecciona **Open** y elige la carpeta `apps/mobile/android`.
3. Espera a que Gradle termine la sincronización (barra de progreso abajo a la derecha).
4. Ve al menú **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
5. **Resultado**: El archivo se generará en `apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`.

> [!TIP]
> Para producción, usa **Generate Signed Bundle / APK** para crear una versión optimizada y firmada.

### 🍎 Generación de IPA (iOS)
1. Ejecuta `npx cap open ios` desde `apps/mobile/`.
2. En Xcode, selecciona el proyecto **App** y ve a **Signing & Capabilities**.
3. Selecciona tu **Development Team** (tu Apple ID).
4. Selecciona como destino **Any iOS Device (arm64)** en la barra superior.
5. Ve al menú **Product > Archive**.
6. Una vez finalizado, haz clic en **Distribute App** y selecciona **Development** o **Ad Hoc**.
7. **Resultado**: Sigue los pasos para exportar y guardar el archivo `.ipa` en tu disco.

---

## 📝 Notas de Mantenimiento
- **Actualización de Plugins**: Si añades un nuevo plugin de Capacitor, ejecuta siempre `npx cap sync`.
- **Limpieza**: Si encuentras errores extraños, borra `node_modules` y las carpetas `android` o `ios` (y vuelve a crearlas con `npx cap add [platform]`).

---

## 🛠️ Solución de Problemas Comunes

### ☕ Error de Java / JDK (Android)
Si encuentras errores de "Unsupported class file major version" o problemas de compatibilidad de Java al ejecutar Gradle:

1.  **Script de Reparación**: Ejecuta `./scripts/fix-java.sh` (en macOS) para configurar la versión correcta.
2.  **Configuración de Android Studio**:
    - Ve a **Settings > Build, Execution, Deployment > Build Tools > Gradle**.
    - Asegúrate de que **Gradle JDK** apunte a una versión 17 o 21.

### 🍎 Error de CocoaPods (iOS)
Si al sincronizar iOS recibes errores de pods:
- Ejecuta `pod install` manualmente dentro de `apps/mobile/ios/App`.
- Asegúrate de abrir siempre el archivo `.xcworkspace` y no el `.xcodeproj`.

---
**Vladimir Acuña** - Senior Software Engineer
