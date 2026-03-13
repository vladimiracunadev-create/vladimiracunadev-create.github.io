# 🚀 Vladimir Acuña | Portafolio Profesional

[![CI Pipeline](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml)
[![Wiki Sync](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml)
[![Bilingual](https://img.shields.io/badge/Language-ES%2FEN-blue?style=flat-square)](index.html)
[![Themes](https://img.shields.io/badge/Theme-Dark%2FLight-blueviolet?style=flat-square)](index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Este repositorio alberga un **Portafolio de Alto Rendimiento** diseñado bajo la filosofía **KISS (Keep It Simple, Stupid)**. Se presenta como un núcleo estático puro, optimizado para la eficiencia extrema, que sirve de base para una arquitectura multiplataforma escalable (PWA + Mobile).

---

## 🏗️ Filosofía de Ingeniería: Minimalismo Estratégico

A diferencia de las soluciones sobre-ingenierizadas con frameworks masivos, este proyecto utiliza un **Vanilla Stack** para garantizar:

* **Rendimiento Imbatible**: Tiempos de carga casi instantáneos y mínima carga cognitiva para el navegador.
* **Sostenibilidad Técnica**: Código agnóstico al tiempo que funcionará durante décadas sin mantenimiento de dependencias.
* **Control de Payloads**: Cada línea de código tiene un propósito directo en la experiencia del usuario.

> [!IMPORTANT]
> El soporte **PWA** y **Capacitor** son extensiones naturales del núcleo. La arquitectura permite esta evolución multiplataforma sin comprometer el rendimiento base ni introducir complejidad innecesaria.

---

## ⚡ Rendimiento & Calidad: Lighthouse 100

| Métrica | Puntaje | Impacto |
| :--- | :--- | :--- |
| **Performance** | ![100](https://img.shields.io/badge/100-success?style=flat-square&logo=lighthouse&logoColor=white) | Carga instantánea (< 1s LCP) |
| **Accesibilidad** | ![100](https://img.shields.io/badge/100-success?style=flat-square&logo=lighthouse&logoColor=white) | Cumplimiento total de estándares ARIA |
| **Best Practices** | ![100](https://img.shields.io/badge/100-success?style=flat-square&logo=lighthouse&logoColor=white) | Código seguro y moderno |
| **SEO** | ![100](https://img.shields.io/badge/100-success?style=flat-square&logo=lighthouse&logoColor=white) | Optimización semántica y metadatos |

---

## 📈 Evolución Reciente: Hitos Consolidados al 13 de Marzo de 2026

Este proyecto ha escalado de un portafolio personal a un **Demostrador Industrial** de ingeniería de software. La revisión de repositorios activos en GitHub y GitLab confirma 7 pilares estratégicos:

1. **Observabilidad Aplicada**: Prometheus/Grafana, dashboards locales y visibilidad operativa para labs reproducibles.
2. **Resiliencia (Circuit Breakers)**: Patrones para manejo de fallas en microservicios.
3. **DevOps & DX**: Pipelines de CI/CD que validan desde la sintaxis hasta la accesibilidad.
4. **Cloud Governance (FinOps)**: Estrategias de optimización de costos, IAM/OIDC y casos visibles en AWS/GitLab Pages.
5. **Platform Engineering & DX**: Hub CLI, pruebas `doctor`/`smoke`, documentación por perfil y entornos reproducibles.
6. **Multiplatform Core**: Un solo código fuente para Web, PWA y Apps Nativas (Capacitor).
7. **Agentic AI Ready + LLM Discoverability**: Arquitectura compatible con asistentes de IA, flujos autónomos y discoverability semántica vía `llm.txt`.

---

## 🌐 Internacionalización & UI

El sistema cuenta con un motor de **i18n (Internationalization)** e **Theming** de alto rendimiento:

* **Bilingüe (ES/EN)**: Implementado mediante CSS pasivo para un cambio de idioma instantáneo sin recarga de página.
* **Temas Dinámicos**: Modo Oscuro/Claro totalmente reactivo, respetando las preferencias del sistema y del usuario.
* **Layout Adaptativo**: Estructura industrial capaz de manejar contenidos densos sin colapso visual.

---

---

## 📱 Capacidades Multiplataforma

El portafolio está preparado para operar como una aplicación nativa instalable:

* **Progressive Web App**: Instalación directa en Windows, macOS, Android e iOS.
* **Android & iOS Ready**: Estructura compatible con Capacitor para despliegue en tiendas de aplicaciones.

### Instrucciones de Instalación (PWA)

* **Desktop (Chrome/Edge):** Haz clic en el icono de instalación en la barra de direcciones.
* **Android (Chrome):** Menú de tres puntos > "Instalar aplicación".
* **iOS (Safari):** Botón de compartir > "Añadir a la pantalla de inicio".

---

## 🛠️ Quick Start / Inicio Rápido

Si eres desarrollador y quieres explorar o extender este proyecto:

```bash
# 1. Clonar el repositorio
git clone https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io.git

# 2. Entrar al directorio
cd vladimiracunadev-create.github.io

# 3. Servir localmente (opcional pero recomendado para PWA)
npx http-server .
```

---

## 📚 Documentación Especializada

Explora las guías detalladas según tu interés:

### 💼 Perfiles de Negocio & Reclutamiento

* [🎯 **Guía para Reclutadores**](docs/RECRUITER.md): Propuesta de valor y métricas de impacto.
* [🧠 **Racional Técnico**](docs/TECHNICAL_RATIONAL.md): Justificación radical de por qué no usamos frameworks.

### 🛠️ Perfiles Técnicos & DevOps

* [🛠️ **Guía de Construcción**](docs/BUILD_GUIDE.md): Pasos para generar APK, IPA y PWA Desktop.
* [🚀 **Construcción Directa (Android)**](docs/MOBILE_DIRECT_BUILD.md): Flujo rápido para generar APK desde Windows.
* [📱 **Manual Mobile (Android/iOS)**](docs/GUIA_MAESTRA_MOBILE.md): Configuración profunda de Capacitor.
* [🩹 **Solución de Problemas iOS**](docs/IOS_TROUBLESHOOTING.md): Guía de supervivencia en Xcode.

Nota mobile:
el flujo directo genera `app-debug.apk` en `apps/mobile/android/app/build/outputs/apk/debug/`.
Para compartir ese binario, usa una **GitHub Release**; no lo subas al árbol normal del repositorio.

### 🎨 Personalización

* [🎨 **Manual para Novatos**](docs/BEGINNER_GUIDE.md): Cómo cambiar tus fotos y textos en 5 minutos.

### 🗺️ Entornos Interactivos y Visuales

* [🧘 **Recorrido 3D / Experiencia Inmersiva**](experiencia-3d/docs/README.md): Galería 3D en WebGL integrada al ecosistema como Arquitectura Desvinculada. Se mantiene como prototipo experimental de código y rendimiento de Three.js puro, pero su acceso público desde la Interfaz de Usuario (UI) principal está *desactivado* por filosofía de producto (no restar atención al flujo de lectura ágil exigido por reclutadores TI).

---

## 📂 Arquitectura del Proyecto

```text
├── apps/                    # Contenedores móviles nativos (Capacitor)
├── docs/                    # Documentación profunda y guías de sistema
├── scripts/                 # Automatización de build, sync y correcciones
├── assets/                  # Recursos estáticos (Imágenes, Iconos, PDFs)
├── .agents/skills/          # Skills de IA para automatizar el portafolio
├── api/v1/                  # CV Data API — endpoints JSON estáticos
├── data/                    # JSON Resume canónico (resume.json)
├── sources/extracted/       # Textos extraídos de PDFs (auditoría)
├── .github/workflows/       # Pipelines CI/CD (calidad, SEO, Lighthouse)
├── index.html               # Núcleo de la aplicación (Vanilla i18n Ready)
├── robots.txt               # Directivas para crawlers de búsqueda
├── sitemap.xml              # Mapa del sitio para SEO
├── llm.txt                  # Contexto semántico para AI/LLMs (llmstxt.org)
├── cv-data-api.md           # Manual de la CV Data API
├── manifest.webmanifest     # Configuración PWA
├── service-worker.js        # Gestión de Cache & Offline
└── portfolio-bundle.zip     # Paquete portable para despliegue (Amplify)
```

---

## Skills System (IA + Automatizacion)

El repositorio incluye un sistema de **Skills de IA** para mantenimiento por capas del portafolio.

| Skill | Cuando usarlo |
|---|---|
| [`portfolio-full-update`](.agents/skills/portfolio-full-update/SKILL.md) | Cuando cambian CV, experiencia, proyectos, PDFs o quieres refrescar todo el portafolio |
| [`portfolio-consistency-audit`](.agents/skills/portfolio-consistency-audit/SKILL.md) | Cuando quieres detectar contradicciones entre sitio, API, documentacion, wiki y archivos SEO |
| [`portfolio-release-guard`](.agents/skills/portfolio-release-guard/SKILL.md) | Antes de commit, push o release para validar lint, build e integridad de `dist/` |
| [`portfolio-doc-sync`](.agents/skills/portfolio-doc-sync/SKILL.md) | Cuando cambio codigo, build, API o arquitectura y hace falta alinear README, docs y wiki |
| [`portfolio-seo-llm-maintainer`](.agents/skills/portfolio-seo-llm-maintainer/SKILL.md) | Cuando cambian rutas, metadatos, `llm.txt`, `robots.txt`, `sitemap.xml` o discoverability |
| [`portfolio-mobile-wrapper-check`](.agents/skills/portfolio-mobile-wrapper-check/SKILL.md) | Cuando cambian web, PWA o assets y quieres confirmar alineacion con Android/iOS |
| [`portfolio-mobile-direct-build`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-mobile-direct-build/SKILL.md) | Transformar la web en app Android y generar el APK directamente en Windows |

**Uso recomendado:**

* `portfolio-consistency-audit` para revisar coherencia general.
* `portfolio-doc-sync` o `portfolio-seo-llm-maintainer` segun el tipo de cambio.
* `portfolio-mobile-wrapper-check` si tocaste manifest, PWA o assets.
* `portfolio-release-guard` antes de publicar.
* `portfolio-full-update` cuando el cambio afecta varias capas a la vez.

---

## 📑 CV Data API (GitHub Pages)

El currículum está publicado como **API JSON estática de solo lectura**, extraída directamente desde los PDFs del repositorio.

📑 [Manual completo → `cv-data-api.md`](cv-data-api.md)

Los artefactos públicos ahora disponen de variantes **ES/EN** y el selector de idioma del sitio cambia automáticamente las descargas al PDF equivalente cuando existe. Además, se incorporó una **Declaración de Logros y Validación** como respaldo separado: resume logros observables y facilita validación externa sin reemplazar el CV ni el portafolio principal.

El sitio también enlaza documentación pública de repos clave cuando existe (`README.md` y, en algunos casos, `RECRUITER.md`) para reducir fricción de evaluación técnica y de reclutamiento.

### Endpoints v1

| Endpoint | Descripción |
|---|---|
| [`/api/v1/profile.json`](https://vladimiracunadev-create.github.io/api/v1/profile.json) | Perfil público |
| [`/api/v1/experience.json`](https://vladimiracunadev-create.github.io/api/v1/experience.json) | Experiencia laboral |
| [`/api/v1/projects.json`](https://vladimiracunadev-create.github.io/api/v1/projects.json) | Proyectos |
| [`/api/v1/skills.json`](https://vladimiracunadev-create.github.io/api/v1/skills.json) | Skills, educación, idiomas |
| [`/api/v1/artifacts.json`](https://vladimiracunadev-create.github.io/api/v1/artifacts.json) | PDFs con URLs directas |
| [`/api/v1/meta.json`](https://vladimiracunadev-create.github.io/api/v1/meta.json) | Metadatos de la API |

### CV PDF principal

📄 **[CV ATS (PDF)](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf)**

### Artefacto de validación complementario

📄 **[Declaración de Logros y Validación (PDF)](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion.pdf)**

---
© 2026 Vladimir Acuña | Arquitecto de Software Senior

## 📚 Documentación del Proyecto

Como parte de los estándares de este ecosistema, la documentación detallada se divide en:

* [📖 Guía de Instalación y Despliegue (INSTALL.md)](INSTALL.md)
* [📝 Historial de Cambios (CHANGELOG.md)](CHANGELOG.md)
* [🤝 Guía de Contribución (CONTRIBUTING.md)](CONTRIBUTING.md)
* [🛡️ Política de Seguridad (SECURITY.md)](SECURITY.md)
* [⚖️ Código de Conducta (CODE_OF_CONDUCT.md)](CODE_OF_CONDUCT.md)
