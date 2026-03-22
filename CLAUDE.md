# CLAUDE.md — Fuente de verdad del proyecto

**Proyecto:** `vladimiracunadev-create.github.io`
**Web:** <https://vladimiracunadev-create.github.io/>
**Última actualización:** 2026-03-19

---

## PRINCIPIO FUNDAMENTAL

> **Nunca destruir. Siempre integrar y complementar.**
> Cualquier archivo a modificar debe tener su versión anterior respaldada antes de tocar una sola línea.

---

## Descripción del proyecto

Portafolio profesional de Vladimir Acuña (Arquitecto de Software / Full-Stack Senior / Polyglot Engineer).
SPA estática en Vanilla HTML/CSS/JS, desplegada en GitHub Pages. Sistema de 6 idiomas, 3 vistas,
PDFs generados por pipeline Python, PWA instalable, y API JSON estática en `api/v1/`.

---

## Mapa de archivos

```text
├── index.html                  # SPA principal — 6 idiomas + 3 vistas + PWA
├── app.js                      # i18n, PDF routing multilingüe, lógica de vistas
├── style.css                   # Estilos principales
├── manifest.webmanifest        # Configuración PWA
├── service-worker.js           # Cache & Offline
├── robots.txt                  # SEO crawlers
├── sitemap.xml                 # Mapa del sitio
├── llm.txt                     # Discoverability para LLMs/AI
├── CHANGELOG.md                # Historial de cambios
├── CLAUDE.md                   # Este archivo — fuente de verdad
├── cv-data-api.md              # Manual de la API JSON
├── api/v1/                     # CV Data API estática
│   ├── meta.json               # Metadatos y capacidades
│   ├── profile.json            # Perfil profesional
│   ├── experience.json         # Experiencia laboral
│   ├── projects.json           # Proyectos del ecosistema
│   ├── skills.json             # Habilidades técnicas
│   └── artifacts.json          # Inventario de PDFs (30+ con 6 variantes c/u)
├── assets/                     # PDFs públicos (30+ archivos)
│   └── no_aplica/              # Versiones descartadas — NO publicar en API
├── scripts/                    # Pipeline de generación
│   ├── generate-all-languages.py           # 12 CVs (reclutador+ATS × 6 idiomas)
│   ├── generate-unified-cv.py              # CV unificado base
│   ├── generate-portfolio.py               # Portafolio × 6 idiomas
│   ├── generate-achievements-statement.py  # Declaración de logros × 6 idiomas
│   ├── generate-recommendation-letter.py   # Carta de recomendación × 6 idiomas
│   ├── generate-ats-cv.py                  # CV ATS standalone
│   └── generate-recruiter-cv.py            # CV reclutador standalone
├── docs/                       # Guías: RECRUITER.md, BUILD_GUIDE.md, etc.
├── .agents/skills/             # Skills de IA para mantenimiento
├── .github/workflows/          # Pipelines CI/CD
├── apps/                       # Capacitor (Android/iOS)
└── data/                       # resume.json canónico
```

---

## Arquitectura técnica

### Sistema de idiomas (6 idiomas)

- **Idiomas:** ES, EN, PT, IT, FR, ZH
- **Sufijos de archivo:** `""` / `-english` / `-portuguese` / `-italian` / `-french` / `-chinese`
- **HTML:** atributos `data-es`, `data-en`, `data-pt`, `data-it`, `data-fr`, `data-zh` en elementos de texto
- **PDFs:** atributos `data-pdf-es`, `data-pdf-en`, `data-pdf-pt`, `data-pdf-it`, `data-pdf-fr`, `data-pdf-zh` en links
- **JS:** `resolveLocalizedPdfHref(link, lang)` en `app.js` resuelve el PDF correcto al cambiar idioma
- **Cambio de idioma:** CSS pasivo — sin recarga de página

### Sistema de vistas (3 niveles)

- `recruiter` (nivel 0): muestra elementos sin `data-min-level` o con `data-min-level="0"`
- `normal` (nivel 1): muestra nivel 0 + 1
- `deep` (nivel 2): muestra todo

### PWA & Capacitor

- `manifest.webmanifest` + `service-worker.js` → instalable en desktop y móvil
- `apps/mobile/` → proyecto Capacitor para APK/IPA
- **NUNCA modificar** manifest ni configuración Capacitor sin documentarlo

### API JSON estática (api/v1/)

- Servida directamente por GitHub Pages — sin servidor
- 6 endpoints: meta, profile, experience, projects, skills, artifacts
- `artifacts.json` contiene las 6 variantes de idioma para cada uno de los 5 documentos públicos
- Actualizar manualmente tras cambios en PDFs o contenido

---

## Sistema de PDFs (30+ archivos)

| Documento | Script generador | Variantes |
|---|---|---|
| CV ATS | `generate-all-languages.py` | cv-ats{suffix}.pdf × 6 |
| CV Reclutador | `generate-all-languages.py` | cv-reclutador{suffix}.pdf × 6 |
| Portafolio | `generate-portfolio.py` | portafolio{suffix}.pdf × 6 |
| Carta de Recomendación | `generate-recommendation-letter.py` | carta-recomendacion_sin_firma{suffix}.pdf × 6 |
| Declaración de Logros | `generate-achievements-statement.py` | declaracion-logros-validacion{suffix}.pdf × 6 |

**Regenerar todos:**

```bash
cd C:/portfolio-pages
python scripts/generate-all-languages.py
python scripts/generate-portfolio.py
python scripts/generate-achievements-statement.py
python scripts/generate-recommendation-letter.py
```

**Generar ZIP de despliegue (para AWS/S3/Amplify/Netlify):**

```bash
python scripts/build-zip.py
# Salida: portfolio-bundle-YYYY-MM-DD.zip (raíz del proyecto)
```

---

## Protocolo de backups — OBLIGATORIO antes de modificar PDFs

1. Crear carpeta: `assets/backups/YYYY-MM-DD/`
2. Copiar los archivos originales con sufijo `_vN` (las 6 variantes)
3. Registrar en `CHANGELOG.md`: `[BACKUP] assets/backups/YYYY-MM-DD/archivo_vN — motivo`
4. NUNCA sobrescribir un backup existente
5. La versión activa siempre está en `assets/`

---

## Ecosistema de repos

### GitHub (vladimiracunadev-create)

| Repo | Propósito |
|---|---|
| `vladimiracunadev-create.github.io` | Este repo — portafolio web |
| `proyectos-aws` | Mirror/docs de los 15 casos AWS |
| `social-bot-scheduler` | n8n + polyglot persistence (9 lenguajes × 12+ DBs) + observabilidad |
| `docker-labs` | 12 labs integrados con Hub CLI, Prometheus/Grafana, K8s |
| `microsistemas` | 11 herramientas de productividad + MCP server |
| `langgraph-realworld` | 25 casos agentes IA con estado tipado |
| `mcp-ollama-local` | IA local: FastAPI + MCP tools + SQLite + K8s |
| `vladimiracunadev-create` | README del perfil GitHub |

### GitLab (vladimir.acuna.dev-group)

| Repo | Propósito |
|---|---|
| `proyectos-aws-gitlab` | Monorepo de 15 casos AWS (11 completados, 4 proyectados) |
| `vladimir.acuna.dev-group` | README del perfil GitLab |

**REGLA:** Solo leer repos externos. Nunca modificar.

---

## Skills de IA disponibles (.agents/skills/)

| Skill | Cuándo |
|---|---|
| `sync-portfolio` | Sincronización completa: audita repos, actualiza JSONs, READMEs, PDFs, hace push |
| `portfolio-full-update` | Cambios en CV, experiencia, proyectos, PDFs |
| `portfolio-consistency-audit` | Detectar contradicciones entre sitio, API, docs, wiki |
| `portfolio-release-guard` | Antes de commit/push — valida lint, build, integridad |
| `portfolio-doc-sync` | Alinear README, docs y wiki tras cambios de código/API |
| `portfolio-seo-llm-maintainer` | Cambios en rutas, metadatos, llm.txt, robots, sitemap |
| `portfolio-mobile-wrapper-check` | Confirmar alineación web/PWA con Android/iOS |
| `portfolio-mobile-direct-build` | Generar APK desde Windows |
| `build-deploy-zip` | Generar ZIP de despliegue para AWS/S3/Amplify/Netlify |
| `md-lint-fix` | Auto-corregir errores MDxxx en archivos .md antes de git push |

---

## Validación

```bash
npm test              # 51 checks de integridad
npm run lint:html     # HTML validation
```

---

## Reglas que NUNCA se deben violar

1. NUNCA destruir contenido — solo integrar y complementar
2. NUNCA modificar un PDF sin backup previo en `assets/backups/`
3. NUNCA sobrescribir un backup existente
4. NUNCA romper el sistema de 6 idiomas
5. NUNCA tocar la lógica de vistas Reclutador/Normal/Profundo
6. NUNCA modificar manifest PWA ni configuración Capacitor sin documentarlo
7. NUNCA hacer commit sin actualizar CHANGELOG.md primero
8. NUNCA modificar repos externos — solo leerlos
9. RootCause es permanentemente oculto — no mencionarlo en ningún output público
10. Si algo está roto: reportar primero, arreglar con autorización

---

## Remisión al CHANGELOG

Ver `CHANGELOG.md` para historial completo de cambios, backups y sesiones.
