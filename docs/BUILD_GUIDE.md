# ðŸ› ï¸ GuÃ­a de ConstrucciÃ³n y DistribuciÃ³n

Esta guÃ­a detalla los pasos tÃ©cnicos necesarios para transformar el nÃºcleo web del portafolio en aplicaciones instalables para Windows, macOS y dispositivos mÃ³viles (Android/iOS).

---

## ðŸ’» Escritorio (Windows & macOS)

Para sistemas de escritorio, utilizamos la tecnologÃ­a **PWA (Progressive Web App)**, que permite una integraciÃ³n nativa con el sistema operativo sin la sobrecarga de un framework como Electron.

> [!IMPORTANT]
> **Requisito TÃ©cnico CrÃ­tico**: Las PWA (y especÃ­ficamente sus *Service Workers*) **solo funcionan en Contextos Seguros**. Esto significa que **no puedes crear una PWA simplemente abriendo el archivo `index.html` en tu navegador** (ruta `file:///...`).
>
> Para que el navegador permita la instalaciÃ³n:
>
> 1. **En ProducciÃ³n**: El sitio debe servirse vÃ­a **HTTPS** (como ya lo hace GitHub Pages).
> 2. **En Desarrollo**: El sitio debe servirse vÃ­a **localhost** (usando un servidor local).

### Pasos para la InstalaciÃ³n como App

1. **Servidor**: El sitio debe estar desplegado en un servidor seguro (HTTPS) o `localhost`.
2. **Navegador**: Abre Chrome o Microsoft Edge.
3. **InstalaciÃ³n**:
    * En la barra de direcciones, haz clic en el icono de **"Instalar"** (un monitor con una flecha hacia abajo).
    * Confirma la instalaciÃ³n.
4. **Resultado**: Se crearÃ¡ un acceso directo en tu escritorio y menÃº de inicio. La aplicaciÃ³n se abrirÃ¡ en una ventana independiente, sin barras de navegaciÃ³n, comportÃ¡ndose como una app nativa.

---

## ðŸ¤– Android (Desde Windows/Linux)

La transformaciÃ³n a Android se realiza mediante **Capacitor**, encapsulando el cÃ³digo web en un WebView nativo.

### Requisitos Previos (Android)

* Node.js instalado.
* Android Studio instalado y configurado.

### Proceso de ConstrucciÃ³n (Android)

1. **SincronizaciÃ³n y Build**: Ejecuta el script de construcciÃ³n directa desde la raÃ­z:

    ```powershell
    # Flujo recomendado: Sincroniza y genera APK automÃ¡ticamente
    ./scripts/mobile-android-build.ps1
    ```

2. **Apertura de Proyecto (Opcional)**:
    * Si prefieres usar el entorno visual:
    * Abre **Android Studio**.
    * Selecciona *Open* y navega hasta la carpeta `apps/mobile/android`.

3. **LocalizaciÃ³n**: El APK generado se encontrarÃ¡ en:
`apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`

> [!NOTE]
> **Flujo Validado**: El sistema de construcciÃ³n directa desde Windows ha sido validado con Ã©xito, generando un APK funcional de ~4.32 MB. Para detalles tÃ©cnicos de orquestaciÃ³n y parÃ¡metros, consulta la [GuÃ­a de ConstrucciÃ³n Directa](MOBILE_DIRECT_BUILD.md).

### DistribuciÃ³n del binario

* El archivo generado por defecto es `app-debug.apk`.
* Úsalo para pruebas, validación interna o distribución manual.
* No lo subas como archivo normal dentro del repositorio.
* Publícalo como asset en una **GitHub Release**.
* Si necesitas publicar en tienda, genera una build firmada desde Android Studio.

### ðŸ“‰ OptimizaciÃ³n de TamaÃ±o (APK)

Es natural que un APK ocupe mÃ¡s que el cÃ³digo HTML puro (tÃ­picamente entre 3MB y 8MB) porque incluye el motor de renderizado y el puente de comunicaciÃ³n de Capacitor. Sin embargo, este proyecto estÃ¡ configurado para ser lo mÃ¡s ligero posible:

1. **MinificaciÃ³n**: El proyecto usa `minifyEnabled true` para eliminar cÃ³digo muerto de las librerÃ­as nativas.
2. **Resource Shrinking**: Se eliminan automÃ¡ticamente recursos no utilizados.
3. **OptimizaciÃ³n de Activos**: AsegÃºrate de que las imÃ¡genes en `/assets` estÃ©n optimizadas antes de sincronizar.

> [!TIP]
> **Sobre la Carpeta `android`**: Es normal que veas muchos archivos nuevos al abrir Android Studio (Gradle, metadatos). No te preocupes: el repositorio estÃ¡ configurado para ignorar el "ruido" y solo guardar lo estrictamente necesario para que cualquier desarrollador pueda reconstruir la app.

### â“ SoluciÃ³n de Problemas (Troubleshooting Android)

Si encuentras dificultades al generar el APK, revisa estas contingencias comunes:

#### 1. Error de EjecuciÃ³n de Scripts (PowerShell)

Si al ejecutar `./scripts/mobile-android.ps1` recibes un error de "ejecuciÃ³n deshabilitada" (`PSSecurityException`), usa este comando para saltar la restricciÃ³n temporalmente:

```powershell
powershell.exe -ExecutionPolicy Bypass -File ./scripts/mobile-android.ps1
```

#### 2. MenÃº "Build" Deshabilitado en Android Studio

Si el botÃ³n de generar APK estÃ¡ en gris:

* **Espera**: Android Studio suele tardar un par de minutos en sincronizar Gradle. Mira la barra de progreso en la esquina inferior derecha.
* **SincronizaciÃ³n Manual**: Ve a `File` > `Sync Project with Gradle Files`.
* **Carpeta Correcta**: AsegÃºrate de haber abierto especÃ­ficamente la carpeta `apps/mobile/android` y no la raÃ­z del repositorio.

#### 3. Error de Sintaxis en Scripts (.ps1)

Si el script falla con errores de "terminador faltante", asegÃºrate de que el archivo estÃ© guardado con codificaciÃ³n **UTF-8** y sin caracteres especiales invisibles. Los scripts en este repositorio han sido simplificados para evitar estos problemas.

---

## ðŸŽ iOS (Desde macOS)

Para iOS, es obligatorio el uso de un entorno Mac con Xcode.

### Requisitos Previos (iOS)

* Node.js instalado.
* Xcode instalado y configurado con un Apple ID.

### Proceso de ConstrucciÃ³n (iOS)

1. **SincronizaciÃ³n**: Ejecuta el script de preparaciÃ³n:

    ```bash
    ./scripts/mobile-ios.sh
    ```

2. **Apertura en Xcode**:

    ```bash
    npx cap open ios
    ```

3. **ConfiguraciÃ³n de Firma**:
    * Selecciona el proyecto **App** en el panel izquierdo.
    * En la pestaÃ±a **Signing & Capabilities**, selecciona tu *Team* (Apple ID).

4. **GeneraciÃ³n del Ejecutable (IPA)**:
    * En el menÃº superior, selecciona el destino `Any iOS Device (arm64)`.
    * Ve a `Product` > `Archive`.
    * Una vez finalizado el archivo, haz clic en `Distribute App` para exportar el archivo `.ipa`.

---

## ðŸ“¦ Despliegue PortÃ¡til Industrial (Bundle ZIP)

Para escenarios donde se requiere un despliegue inmediato y autÃ³nomo (ej. AWS Amplify, S3, o transferencia rÃ¡pida de activos), el proyecto cuenta con un sistema de bundling simplificado.

### El Paquete `portfolio-bundle.zip`

1. **CÃ³digo**: `index.html`, `styles.css`, `app.js`.
2. **Activos**: Carpeta `assets/` (incluyendo los PDFs y multimedia).
3. **PWA**: `manifest.webmanifest`, `service-worker.js`.
4. **SEO**: `robots.txt`, `sitemap.xml`, `llm.txt`.

> [!NOTE]
> Los archivos `robots.txt`, `sitemap.xml` y `llm.txt` estÃ¡n commiteados **directamente en la raÃ­z del repositorio** (no en `.gitignore`). Esto garantiza que GitHub Pages los sirva siempre en las URLs canÃ³nicas:
> `https://vladimiracunadev-create.github.io/robots.txt`
> `https://vladimiracunadev-create.github.io/sitemap.xml`
> `https://vladimiracunadev-create.github.io/llm.txt`

### CÃ³mo desplegar en segundos (AWS Amplify)

1. **Descarga o localiza el archivo `portfolio-bundle.zip`.**
2. **Ve a la consola de **AWS Amplify**.**
3. **Selecciona "Deploy without a Git provider".**
4. **Arrastra el archivo ZIP al Ã¡rea de carga. Â¡Tu portafolio estarÃ¡ en vivo en menos de 1 minuto!**

---

## ðŸš€ Reglas de DistribuciÃ³n en el Repositorio

Para mantener el repositorio limpio y profesional, sigue estas reglas al subir los ejecutables:

1. **PROHIBIDO** subir archivos `.apk`, `.ipa`, `.exe` o `.zip` directamente a las carpetas del repositorio.
2. **Uso de Releases**:
    * Crea un nuevo **Tag** de versiÃ³n (ej. `v1.2.0`) en GitHub.
    * Crea una nueva **Release** asociada a ese Tag.
    * Carga los binarios (APK, AAB, IPA) como *Assets* de la Release.
    * Para APK debug, usa la ruta local `apps/mobile/android/app/build/outputs/apk/debug/app-debug.apk`.
3. **DocumentaciÃ³n de VersiÃ³n**: Describe brevemente los cambios e innovaciones incluidos en cada ejecutable subido.

---
---
[â† Volver al README](../README.md) | **Vladimir AcuÃ±a** - Senior Software Engineer
