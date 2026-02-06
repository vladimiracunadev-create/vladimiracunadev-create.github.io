# 🚀 Vladimir Acuña | Portafolio Profesional

[![CI Pipeline](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml)
[![Wiki Sync](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Vanilla JS](https://img.shields.io/badge/Vanilla-JS-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

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

## 🔄 Roadmap de Transformación del Sistema

Este proyecto demuestra la madurez técnica necesaria para llevar un sitio estático minimalista hacia un entorno de producto completo:

1. **Estrategia Core**: Desarrollo nativo con HTML5, CSS3 y JS (ES6+).
2. **Capa de Productización (PWA)**: Implementación de Service Workers y Manifests para resiliencia offline.
3. **Contenedor Nativo (Capacitor)**: Integración en `/apps/mobile` para encapsulamiento en Android e iOS.
4. **Tooling de Sincronización**: Automatización robusta para despliegues web y móviles unificados.

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
├── assets/             # Recursos estáticos (Imágenes, Iconos)
├── index.html          # Núcleo de la aplicación (Vanilla)
├── manifest.webmanifest # Definición de PWA
└── service-worker.js   # Gestión de Cache & Offline
```

---
© 2026 Vladimir Acuña | Arquitecto de Software Senior
