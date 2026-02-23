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

## 🔄 Evolución Reciente: Hitos de Febrero 2026

Este proyecto ha escalado de un portafolio personal a un **Demostrador Industrial** de ingeniería de software. Las recientes actualizaciones integran 6 pilares estratégicos:

1.  **Observabilidad (OpenTelemetry/Logs)**: Estándares de traza para sistemas distribuidos.
2.  **Resiliencia (Circuit Breakers)**: Patrones para manejo de fallas en microservicios.
3.  **DevOps & DX**: Pipelines de CI/CD que validan desde la sintaxis hasta la accesibilidad.
4.  **Cloud Governance (FinOps)**: Estrategias de optimización de costos y OIDC para identidad segura.
5.  **Multiplatform Core**: Un solo código fuente para Web, PWA y Apps Nativas (Capacitor).
6.  **Agentic AI Ready**: Arquitectura compatible con asistentes de IA y flujos de trabajo autónomos.

---

## 🌎 Internacionalización & UI

El sistema cuenta con un motor de **i18n (Internationalization)** y **Theming** de alto rendimiento:
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

## 🏃 Quick Start / Inicio Rápido

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
* [📱 **Manual Mobile (Android/iOS)**](docs/GUIA_MAESTRA_MOBILE.md): Configuración profunda de Capacitor.
* [⚠️ **Solución de Problemas iOS**](docs/IOS_TROUBLESHOOTING.md): Guía de supervivencia en Xcode.

### 🔰 Personalización

* [🔰 **Manual para Novatos**](docs/BEGINNER_GUIDE.md): Cómo cambiar tus fotos y textos en 5 minutos.

---

## 📂 Arquitectura del Proyecto

```text
├── apps/               # Contenedores móviles nativos (Capacitor)
├── docs/               # Documentación profunda y guías de sistema
├── scripts/            # Automatización de build, sync y correcciones
├── assets/             # Recursos estáticos (Imágenes, Iconos, PDFs Industriales)
├── index.html          # Núcleo de la aplicación (Vanilla i18n Ready)
├── portfolio-bundle.zip # Paquete portable para despliegue rápido (Amplify)
└── service-worker.js   # Gestión de Cache & Offline
```

---
© 2026 Vladimir Acuña | Arquitecto de Software Senior
