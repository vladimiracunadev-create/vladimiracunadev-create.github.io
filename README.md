# 🚀 Vladimir Acuña | Portafolio Profesional

[![CI Pipeline](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml)
[![Wiki Sync](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este repositorio alberga un **Portafolio de Alto Rendimiento** diseñado bajo la filosofía **KISS (Keep It Simple, Stupid)**. Se presenta como un núcleo estático puro, optimizado para la eficiencia extrema, que sirve de base para una arquitectura multiplataforma escalable (PWA + Mobile).

---

## 🏗️ Filosofía de Ingeniería: Minimalismo Estratégico

A diferencia de las soluciones sobre-ingenierizadas con frameworks masivos, este proyecto utiliza un **Vanilla Stack** para garantizar:

* **Rendimiento Imbatible**: Tiempos de carga casi instantáneos y mínima carga cognitiva para el navegador.
* **Sostenibilidad Técnica**: Código agnóstico al tiempo que funcionará durante décadas sin mantenimiento de dependencias.
* **Control de Payloads**: Cada línea de código tiene un propósito directo en la experiencia del usuario.

> [!NOTE]
> El soporte **PWA** y **Capacitor** son extensiones naturales del núcleo. La arquitectura permite esta evolución multiplataforma sin comprometer el rendimiento base ni introducir complejidad innecesaria.

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

## 🛠 Stack Tecnológico & CI/CD

* **Frontend**: HTML5 Semántico, CSS3 Vanilla (Grid/Flexbox/Custom Properties).
* **JavaScript**: Lógica reactiva ligera sin dependencias de terceros.
* **Automatización**: GitHub Actions para validación estática y sincronización de documentación.
* **Optimización**: 95+ en todas las métricas de Lighthouse (Performance, SEO, Accesibilidad).

---

## 📚 Guías de Revisión Especializada

| Perfil | Documentación | Objetivo |
| :--- | :--- | :--- |
| **Recrutadores** | [🎯 Guía para Reclutadores](docs/RECRUITER.md) | Propuesta de valor y métricas de impacto. |
| **Tech Leads** | [🧠 Racional Técnico](docs/TECHNICAL_RATIONAL.md) | Justificación de arquitectura y decisiones de diseño. |
| **Developers** | [🔰 Manual para Novatos](docs/BEGINNER_GUIDE.md) | Guía técnica de personalización y contribución. |
| **Operación** | [🛠️ Guía de Construcción](docs/BUILD_GUIDE.md) | Pasos para generar APK, IPA y PWA Desktop. |

---

## 💻 Entorno de Desarrollo

```bash
git clone https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io.git
cd vladimiracunadev-create.github.io
# Abre index.html o usa npx http-server .
```

---

## 📂 Arquitectura de Archivos

```text
├── apps/               # Contenedores móviles nativos
├── docs/               # Documentación y Wiki compartida
├── scripts/            # Automatización de build y sincronización
├── assets/             # Recursos estáticos y activos de marca
├── index.html          # Punto de entrada (Vanilla)
├── manifest.webmanifest # Definición de PWA
└── service-worker.js   # Gestión de Cache & Offline
```

---
© 2026 Vladimir Acuña | Arquitecto de Software Senior
