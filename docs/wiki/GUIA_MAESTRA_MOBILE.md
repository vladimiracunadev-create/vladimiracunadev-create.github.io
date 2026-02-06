# Guía Maestra Mobile

Esta guía proporciona una visión completa del ecosistema móvil del proyecto, combinando hardware, software y procesos de puesta en marcha para Android e iOS.

## 📱 Hardware y Entorno

Para trabajar en el desarrollo móvil de este portafolio, se recomienda el siguiente perfil de hardware:

### Perfil Recomendado
* **CPU**: Procesador de alto rendimiento (ej. Apple M2/M3 o Intel i7/i9).
* **RAM**: 16GB - 32GB (crucial para emuladores y compilación).
* **Almacenamiento**: SSD dedicado con al menos 20GB libres para SDKs.

---

## 🚀 Puesta en Marcha (Fast-Track)

### 1. Clonación e Instalación
```bash
git clone https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io.git
cd vladimiracunadev-create.github.io
npm install
```

### 2. Preparación de Aplicaciones
El proyecto utiliza **Capacitor** para transformar el portafolio web en apps nativas.

```bash
cd apps/mobile
npm install
```

---

## 🤖 Android (Desde Windows/Linux/Mac)

### Proceso de Construcción (APK/AAB)

1. **Sincronización**: Asegura que el contenido web esté listo para la app:
    ```bash
    ./scripts/mobile-android.ps1  # (Windows PowerShell)
    ```

2. **Apertura en Android Studio**: Abre la carpeta `apps/mobile/android`.

3. **Generación del Binario**:
    * Ve a `Build` > `Build Bundle(s) / APK(s)` > `Build APK(s)`.
    * El archivo generado estará en: `app/build/outputs/apk/debug/app-debug.apk`.

---

## 🍎 iOS (Desde macOS)

El desarrollo de iOS requiere un entorno Mac con Xcode.

### Proceso de Construcción (IPA)

1. **Sincronización**:
    ```bash
    ./scripts/mobile-ios.sh
    ```

2. **Apertura en Xcode**:
    ```bash
    npx cap open ios
    ```

3. **Firma y Distribución**:
    * Configura tu **Development Team** en *Signing & Capabilities*.
    * Destino: `Any iOS Device (arm64)`.
    * Menú: `Product` > `Archive`.
    * Exporta mediante `Distribute App`.

---

## 🛠 Troubleshooting Common Issues

Para soluciones detalladas a problemas comunes, consulta:
* [Guía de Construcción Detallada](BUILD_GUIDE)
* [Solución de Problemas iOS](IOS_TROUBLESHOOTING)

---

## 📦 Reglas de Distribución

1. **NO subir binarios** (`.apk`, `.ipa`) al repositorio Git.
2. **Usar Releases**: Carga los ejecutables como Assets en las [Releases de GitHub](../../releases).
3. **Versiones**: Cada subida debe ir acompañada de una descripción de los cambios técnicos y de UI.

---
**Vladimir Acuña** - Senior Software Engineer
