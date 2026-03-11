# 📖 Wiki del Proyecto | Centro de Conocimiento

[![CI Pipeline](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/ci.yml)
[![Wiki Sync](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml/badge.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/actions/workflows/wiki-sync.yml)
[![Performance](https://img.shields.io/badge/Lighthouse-100%2F100-success.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io)
[![Stack](https://img.shields.io/badge/Stack-Vanilla%20JS%20%2B%20Capacitor-blue.svg)](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io)

Bienvenido al HUB de documentación técnica y estratégica. Este espacio está diseñado para proporcionar una visión de 360° sobre la arquitectura, el despliegue y la filosofía de ingeniería detrás de este portafolio de alto rendimiento.

---

## 💎 Filosofía de Ingeniería

Nuestra arquitectura se basa en el **Minimalismo Radical (KISS)**. No construimos con frameworks pesados porque priorizamos el control total del DOM, la velocidad de carga instantánea y la longevidad del código.

> 💡 **Productización**: Lo que comenzó como un sitio estático puro, hoy es un ecosistema multiplataforma (Web, PWA, Android e iOS) utilizando un único núcleo de código.

---

## 🗺️ Mapa de Navegación

### 💼 Perfiles Ejecutivos y Reclutamiento

*Documentación enfocada en la propuesta de valor y racional técnico.*

| Guía | Propósito | Valor Clave |
| :--- | :--- | :--- |
| [🎯 **Reclutadores**](RECRUITER) | Tour guiado por el sistema | Visión de negocio y métricas |
| [🧠 **Racional Técnico**](TECHNICAL_RATIONAL) | Justificación de arquitectura | Por qué Vanilla JS > Frameworks |
| [🏠 **Propósito**](Home) | Visión general | Alineación de objetivos |

---

### 📱 Ecosistema Mobile & PWA

*Deep-dives sobre la transformación del core web en aplicaciones nativas.*

| Guía | Propósito | Tecnología |
| :--- | :--- | :--- |
| [🚀 **Maestra Mobile**](GUIA_MAESTRA_MOBILE) | Visión general del ecosistema | Capacitor + Hardware |
| [🚀 **Construcción Directa**](MOBILE_DIRECT_BUILD) | Generación rápida de APK | Windows + PowerShell |
| [🛠️ **Construcción**](BUILD_GUIDE) | Guía técnica de compilación | Android SDK / Xcode |
| [🍏 **Soporte iOS**](IOS_TROUBLESHOOTING) | Resolución de conflictos Apple | provisioning & Signing |

---

### 🛡️ Calidad, Seguridad y Performance

*Estándares aplicados para garantizar un producto de nivel industrial.*

| Guía | Propósito | Impacto |
| :--- | :--- | :--- |
| [🔐 **Seguridad y Cache**](SECURITY_HEADERS) | Protección y velocidad | CSP A+ & Cache Inmutable |
| [📊 **Validación Local**](VALIDATION) | Control de calidad integral | Lighthouse CI |
| [📂 **Arquitectura Asíncrona**](ASINCRONO) | Lógica de validación avanzada | Promesas y flujos de datos |

---

### 📡 CV Data API

*Currículum publicado como API JSON estática, extraído desde PDFs del repo.*

| Endpoint | Descripción |
| :--- | :--- |
| [`/api/v1/profile.json`](https://vladimiracunadev-create.github.io/api/v1/profile.json) | Perfil público |
| [`/api/v1/experience.json`](https://vladimiracunadev-create.github.io/api/v1/experience.json) | Experiencia |
| [`/api/v1/projects.json`](https://vladimiracunadev-create.github.io/api/v1/projects.json) | Proyectos |
| [`/api/v1/skills.json`](https://vladimiracunadev-create.github.io/api/v1/skills.json) | Skills / Educación |
| [`/api/v1/artifacts.json`](https://vladimiracunadev-create.github.io/api/v1/artifacts.json) | PDFs con URLs directas |
| [`/api/v1/meta.json`](https://vladimiracunadev-create.github.io/api/v1/meta.json) | Metadatos de la API |

> 📖 Manual completo → [`cv-data-api.md`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/cv-data-api.md)

---

### Skills System

*Skills de IA para mantenimiento por capas del portafolio.*

| Skill | Cuando usar |
| :--- | :--- |
| [`portfolio-full-update`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-full-update/SKILL.md) | Refrescar CV, proyectos, PDFs, JSON API, sitio y documentacion completa |
| [`portfolio-consistency-audit`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-consistency-audit/SKILL.md) | Detectar contradicciones entre sitio, API, docs, wiki y SEO |
| [`portfolio-release-guard`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-release-guard/SKILL.md) | Validar lint, build e integridad antes de publicar |
| [`portfolio-doc-sync`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-doc-sync/SKILL.md) | Sincronizar README, docs y wiki despues de cambios tecnicos o narrativos |
| [`portfolio-seo-llm-maintainer`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-seo-llm-maintainer/SKILL.md) | Mantener `llm.txt`, `robots.txt`, `sitemap.xml` y discoverability actualizados |
| [`portfolio-mobile-wrapper-check`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-mobile-wrapper-check/SKILL.md) | Verificar alineacion entre nucleo web, PWA y wrappers Android/iOS |
| [`portfolio-mobile-direct-build`](https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io/blob/main/.agents/skills/portfolio-mobile-direct-build/SKILL.md) | Transformar web en app Android y generar APK directamente en Windows |
---

## 📈 Benchmarks de Calidad (Lighthouse)

Mantenemos un estándar innegociable de excelencia técnica en cada despliegue:

| Categoría | Puntaje | Métrica Clave |
| :--- | :--- | :--- |
| **Performance** | ![100](https://img.shields.io/badge/100-success?style=flat-square) | LCP < 800ms |
| **Accesibilidad** | ![100](https://img.shields.io/badge/100-success?style=flat-square) | WCAG 2.1 |
| **Best Practices** | ![100](https://img.shields.io/badge/100-success?style=flat-square) | CSP / HTTPS |
| **SEO** | ![100](https://img.shields.io/badge/100-success?style=flat-square) | Semántica + `llm.txt` |

---

**Vladimir Acuña** - Senior Software Engineer | © 2026 · Marzo 2026
