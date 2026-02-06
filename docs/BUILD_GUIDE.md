# 🛠️ Guía de Construcción y Distribución

Esta guía detalla los pasos técnicos necesarios para transformar el núcleo web del portafolio en aplicaciones instalables para Windows, macOS y dispositivos móviles (Android/iOS).

---

## 💻 Escritorio (Windows & macOS)

Para sistemas de escritorio, utilizamos la tecnología **PWA (Progressive Web App)**, que permite una integración nativa con el sistema operativo sin la sobrecarga de un framework como Electron.

> [!IMPORTANT]
> **Requisito Técnico Crítico**: Las PWA (y específicamente sus *Service Workers*) **solo funcionan en Contextos Seguros**. Esto significa que **no puedes crear una PWA simplemente abriendo el archivo `index.html` en tu navegador** (ruta `file:///...`).
>
> Para que el navegador permita la instalación:
>
> 1. **En Producción**: El sitio debe servirse vía **HTTPS** (como ya lo hace GitHub Pages).
> 2. **En Desarrollo**: El sitio debe servirse vía **localhost** (usando un servidor local).

### Pasos para la Instalación como App

1. **Servidor**: El sitio debe estar desplegado en un servidor seguro (HTTPS) o `localhost`.
2. **Navegador**: Abre Chrome o Microsoft Edge.
3. **Instalación**:
    * En la barra de direcciones, haz clic en el icono de **"Instalar"** (un monitor con una flecha hacia abajo).
    * Confirma la instalación.
4. **Resultado**: Se creará un acceso directo en tu escritorio y menú de inicio. La aplicación se abrirá en una ventana independiente, sin barras de navegación, comportándose como una app nativa.

---

## 🤖 Android (Desde Windows/Linux)

La transformación a Android se realiza mediante **Capacitor**, encapsulando el código web en un WebView nativo.

### Requisitos Previos (Android)

* Node.js instalado.
* Android Studio instalado y configurado.

### Proceso de Construcción (Android)

1. **Sincronización**: Ejecuta el script de preparación desde la raíz del proyecto:

    ```powershell
    ./scripts/mobile-android.ps1
    ```

2. **Apertura de Proyecto**:
    * Abre **Android Studio**.
    * Selecciona *Open* y navega hasta la carpeta `apps/mobile/android`.

3. **Generación del Ejecutable (APK/AAB)**:
    * Ve al menú `Build` > `Generate Signed Bundle / APK`.
    * Sigue el asistente para crear una nueva clave de firma (Keystore) si es tu primera vez.
    * Selecciona `release` como build variant.

4. **Localización**: El archivo `.apk` o `.aab` generado se encontrará en `apps/mobile/android/app/release/`.

---

## 🍎 iOS (Desde macOS)

Para iOS, es obligatorio el uso de un entorno Mac con Xcode.

### Requisitos Previos (iOS)

* Node.js instalado.
* Xcode instalado y configurado con un Apple ID.

### Proceso de Construcción (iOS)

1. **Sincronización**: Ejecuta el script de preparación:

    ```bash
    ./scripts/mobile-ios.sh
    ```

2. **Apertura en Xcode**:

    ```bash
    npx cap open ios
    ```

3. **Configuración de Firma**:
    * Selecciona el proyecto **App** en el panel izquierdo.
    * En la pestaña **Signing & Capabilities**, selecciona tu *Team* (Apple ID).

4. **Generación del Ejecutable (IPA)**:
    * En el menú superior, selecciona el destino `Any iOS Device (arm64)`.
    * Ve a `Product` > `Archive`.
    * Una vez finalizado el archivo, haz clic en `Distribute App` para exportar el archivo `.ipa`.

---

## 🚀 Reglas de Distribución en el Repositorio

Para mantener el repositorio limpio y profesional, sigue estas reglas al subir los ejecutables:

1. **PROHIBIDO** subir archivos `.apk`, `.ipa`, `.exe` o `.zip` directamente a las carpetas del repositorio.
2. **Uso de Releases**:
    * Crea un nuevo **Tag** de versión (ej. `v1.2.0`) en GitHub.
    * Crea una nueva **Release** asociada a ese Tag.
    * Carga los binarios (APK, AAB, IPA) como *Assets* de la Release.
3. **Documentación de Versión**: Describe brevemente los cambios e innovaciones incluidos en cada ejecutable subido.

---
**Vladimir Acuña** - Arquitecto de Software Senior
