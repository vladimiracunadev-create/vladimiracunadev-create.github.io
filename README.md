Este repositorio contiene el código fuente de mi portafolio personal. Un proyecto diseñado bajo la filosofía **KISS (Keep It Simple, Stupid)**: una web estática pura de alto rendimiento que sirve como núcleo sólido para ser extendido hacia ecosistemas PWA y Aplicaciones Móviles.

---

## 🏗️ Filosofía Core: Minimalismo Vanilla

A diferencia de los portafolios modernos sobrecargados de frameworks, este proyecto elige deliberadamente **HTML, CSS y JS puro**.

- **Rendimiento Imbatible**: Sin librerías pesadas, carga instantánea.
- **Sostenibilidad**: El código funcionará en décadas sin actualizaciones de dependencias constantes.
- **Control Total**: Sin abstracciones innecesarias entre el código y el navegador.

> [!NOTE]
> La PWA y el soporte móvil son **capacidades añadidas** que no comprometen la simplicidad del núcleo. Si eliminas el Service Worker, el sitio sigue funcionando perfectamente.

---

## 🔄 Proceso de Transformación (Paso a Paso)

Este repositorio demuestra cómo un sitio estático minimalista puede transformarse en un producto multiplataforma sin cambiar su arquitectura base:

1. **Núcleo (HTML/CSS/JS)**: Definición de la estructura semántica y diseño responsivo.
2. **Productización (PWA)**: Implementación de `manifest.webmanifest` y `service-worker.js` para permitir la instalación y el funcionamiento offline.
3. **Habilitación Móvil (Capacitor)**: Integración de un contenedor nativo en `/apps/mobile` que encapsula el núcleo web.
4. **Sincronización Automatizada**: Uso de scripts en `/scripts` para mover el código del núcleo hacia el contenedor móvil de forma segura.
5. **Despliegue Multiplataforma**: Generación de APK/IPA (móvil) y despliegue a GitHub Pages (web) de forma independiente.

---

## 📱 Extensión de Capacidades: PWA & Mobile

El portafolio incluye una capa de **Productización** que permite utilizarlo como una aplicación nativa:

- **PWA**: Instalable en Windows/Android/iOS con soporte offline.
- **Android**: Preparado para generar APK/AAB vía Capacitor.
- **iOS**: Estructura lista para Xcode en macOS.

### Cómo instalar (PWA)

- **Windows / macOS (Chrome/Edge):** Haz clic en el icono de instalación en la barra de direcciones.
- **Android (Chrome):** Toca los tres puntos y elige "Instalar aplicación".
- **iOS (Safari):** Toca "Compartir" y elige "Añadir a la pantalla de inicio".

---

## 🛠 Stack Tecnológico

El proyecto se rige por la filosofía **KISS (Keep It Simple, Stupid)**, priorizando el rendimiento nativo sobre la sobre-ingeniería de frameworks.

- **🌐 Frontend Core**: HTML5 Semántico y CSS3 Vanilla (Custom Properties, Flexbox, Grid).
- **⚡ JavaScript (ES6+)**: Lógica reactiva ligera sin dependencias externas.
- **🏗 CI/CD**: Automatización con GitHub Actions para validación (Linting) y sincronización de Wiki.
- **📈 SEO & Performance**: Optimización extrema (95+ en Lighthouse), generación dinámica de sitemaps.

---

## 📚 Documentación Especializada

Para una revisión detallada del proyecto, selecciona la guía que mejor se adapte a tu perfil:

| Perfil | Guía | Enfoque |
| :--- | :--- | :--- |
| **Recrutadores** | [🎯 Guía para Reclutadores](docs/RECRUITER.md) | Valor técnico, métricas y "Por qué contratar". |
| **Tech Leads** | [🧠 Racional Técnico](docs/TECHNICAL_RATIONAL.md) | Decisiones arquitectónicas y uso de Vanilla Stack. |
| **Developers** | [🔰 Manual para Novatos](docs/BEGINNER_GUIDE.md) | Guía de personalización y despliegue rápido. |

> [!TIP]
> También puedes consultar nuestra **[📖 Wiki del Proyecto](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/wiki)** para ver detalles técnicos adicionales.

---

## 💻 Desarrollo Local

No se requiere de un entorno complejo para empezar a colaborar o editar.

### 1. Clonar

```bash
git clone https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io.git
cd vladimiracunadev-create.github.io
```

### 2. Ejecución

Al ser una web estática pura, puedes simplemente abrir `index.html` en tu navegador. Si prefieres un servidor local:

- **Node**: `npx http-server .`
- **Python**: `python -m http.server`

---

## 📂 Estructura del Proyecto

```text
├── apps/               # Contenedores móviles (Capacitor)
├── docs/               # Documentación y Wiki
├── scripts/            # Sincronización web-to-mobile y SEO
├── assets/             # Imágenes, Iconos y PDFs
├── index.html          # Núcleo Web
├── manifest.webmanifest # Metadatos PWA
├── service-worker.js   # Lógica Offline
└── styles.css          # Estilos Vanilla
```

---

## 📱 Compatibilidad

- **📱 Mobile**: Totalmente responsivo, optimizado para navegación táctil.
- **💻 Desktop**: Compatible con Windows, Linux y macOS.
- **🌐 Browsers**: Chrome, Firefox, Safari, Edge (ES6+).

---
© 2026 Vladimir Acuña | Desarrollado con ❤️ y Vanilla JS.
