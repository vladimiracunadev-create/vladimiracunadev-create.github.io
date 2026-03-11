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

1. **Sincronización y Build**: Ejecuta el script de construcción directa desde la raíz:

    ```powershell
    # Flujo recomendado: Sincroniza y genera APK automáticamente
    ./scripts/mobile-android-build.ps1
    ```

2. **Apertura de Proyecto (Opcional)**:
    * Si prefieres usar el entorno visual:
    * Abre **Android Studio**.
    * Selecciona *Open* y navega hasta la carpeta `apps/mobile/android`.

3. **Localización**: El APK generado se encontrará en:
`apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`

> [!NOTE]
> **Flujo Validado**: El sistema de construcción directa desde Windows ha sido validado con éxito, generando un APK funcional de ~4.32 MB. Para detalles técnicos de orquestación y parámetros, consulta la [Guía de Construcción Directa](MOBILE_DIRECT_BUILD.md).

### 📉 Optimización de Tamaño (APK)

Es natural que un APK ocupe más que el código HTML puro (típicamente entre 3MB y 8MB) porque incluye el motor de renderizado y el puente de comunicación de Capacitor. Sin embargo, este proyecto está configurado para ser lo más ligero posible:

1. **Minificación**: El proyecto usa `minifyEnabled true` para eliminar código muerto de las librerías nativas.
2. **Resource Shrinking**: Se eliminan automáticamente recursos no utilizados.
3. **Optimización de Activos**: Asegúrate de que las imágenes en `/assets` estén optimizadas antes de sincronizar.

> [!TIP]
> **Sobre la Carpeta `android`**: Es normal que veas muchos archivos nuevos al abrir Android Studio (Gradle, metadatos). No te preocupes: el repositorio está configurado para ignorar el "ruido" y solo guardar lo estrictamente necesario para que cualquier desarrollador pueda reconstruir la app.

### ❓ Solución de Problemas (Troubleshooting Android)

Si encuentras dificultades al generar el APK, revisa estas contingencias comunes:

#### 1. Error de Ejecución de Scripts (PowerShell)

Si al ejecutar `./scripts/mobile-android.ps1` recibes un error de "ejecución deshabilitada" (`PSSecurityException`), usa este comando para saltar la restricción temporalmente:

```powershell
powershell.exe -ExecutionPolicy Bypass -File ./scripts/mobile-android.ps1
```

#### 2. Menú "Build" Deshabilitado en Android Studio

Si el botón de generar APK está en gris:

* **Espera**: Android Studio suele tardar un par de minutos en sincronizar Gradle. Mira la barra de progreso en la esquina inferior derecha.
* **Sincronización Manual**: Ve a `File` > `Sync Project with Gradle Files`.
* **Carpeta Correcta**: Asegúrate de haber abierto específicamente la carpeta `apps/mobile/android` y no la raíz del repositorio.

#### 3. Error de Sintaxis en Scripts (.ps1)

Si el script falla con errores de "terminador faltante", asegúrate de que el archivo esté guardado con codificación **UTF-8** y sin caracteres especiales invisibles. Los scripts en este repositorio han sido simplificados para evitar estos problemas.

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

## 📦 Despliegue Portátil Industrial (Bundle ZIP)

Para escenarios donde se requiere un despliegue inmediato y autónomo (ej. AWS Amplify, S3, o transferencia rápida de activos), el proyecto cuenta con un sistema de bundling simplificado.

### El Paquete `portfolio-bundle.zip`

1. **Código**: `index.html`, `styles.css`, `app.js`.
2. **Activos**: Carpeta `assets/` (incluyendo los PDFs y multimedia).
3. **PWA**: `manifest.webmanifest`, `service-worker.js`.
4. **SEO**: `robots.txt`, `sitemap.xml`, `llm.txt`.

> [!NOTE]
> Los archivos `robots.txt`, `sitemap.xml` y `llm.txt` están commiteados **directamente en la raíz del repositorio** (no en `.gitignore`). Esto garantiza que GitHub Pages los sirva siempre en las URLs canónicas:
> `https://vladimiracunadev-create.github.io/robots.txt`
> `https://vladimiracunadev-create.github.io/sitemap.xml`
> `https://vladimiracunadev-create.github.io/llm.txt`

### Cómo desplegar en segundos (AWS Amplify)

1. **Descarga o localiza el archivo `portfolio-bundle.zip`.**
2. **Ve a la consola de **AWS Amplify**.**
3. **Selecciona "Deploy without a Git provider".**
4. **Arrastra el archivo ZIP al área de carga. ¡Tu portafolio estará en vivo en menos de 1 minuto!**

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
---
[← Volver al README](../README.md) | **Vladimir Acuña** - Senior Software Engineer
