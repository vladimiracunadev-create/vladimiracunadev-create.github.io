# Changelog

## 2026-06-20 (V) — Nueva vista "Freelance" (curaduría para clientes que evalúan contratación por proyecto)

Las 3 vistas existentes (Reclutador / Normal / Profundo) son **jerárquicas** (cada una incluye la anterior). Se agrega una **4ª vista paralela** específica para el pitch freelance: muestra lo que un cliente potencial necesita para decidir si contratar trabajo por proyecto, oculta lo que pertenece más al pitch de empleo corporativo o a la narrativa interna.

### Botón nuevo · "Freelance" (6 idiomas)

- ES/EN/PT/IT/FR: `Freelance` · ZH: `自由职业` (matches el nav existente `#modalidades`).
- Tooltip: _"Vista curada para clientes que evalúan contratación por proyecto"_.

### Curaduría

**Visible en Freelance** (lo relevante para un cliente):

- Hero · `#resultados` · `#productos` · `#demos` · `#experiencia` · `#servicios` · `#modalidades` · `#descargas` · `#contacto`.

**Oculto en Freelance** (no aporta al pitch de contratación por proyecto):

- `#evolucion` — pilares técnicos genéricos.
- `#proyectos` — duplica `#productos` (productos = proof of execution, repos = catálogo técnico).
- `#roles` — alcance corporativo (junior/senior/staff…).
- `#flujo-ia` — narrativa meta de flujo IA.
- `#referencias` — cartas corporativas (ya cubierto por carta de recomendación en `#descargas`).

### Implementación

- **Atributo `data-freelance-hide="true"`** agregado a las 5 secciones a ocultar + 2 entradas de nav (`#proyectos`, `#roles`).
- **`app.js`** — `setView()` extendido: cuando `view === "freelance"` ignora la jerarquía de niveles (muestra todo lo de `data-min-level`) y luego oculta los marcados con `data-freelance-hide`. Cuando se vuelve a un nivel jerárquico, limpia el flag freelance-only.
- La vista persiste en `localStorage.portfolio_view` igual que las otras.

### Por qué "Freelance" como nombre

- Es el término universal y bilingüe (ES/EN).
- Coincide con el label del nav `#modalidades` que ya dice "Freelance" en todos los idiomas.
- Otras alternativas consideradas y descartadas: "Cliente" (ambiguo), "Independiente" (largo + no se usa fuera de español), "Contratar" (acción, no perfil).

---

## 2026-06-20 (IV) — Re-balance Normal vs Profundo (identidades claras por nivel)

Tras la primera reorganización (III), la asimetría seguía siendo grande: Normal con 6 secciones, Profundo con apenas 2. Se mueven `#servicios` y `#modalidades` de nivel 1 → 2 para que cada nivel tenga una identidad clara.

### Identidades por nivel

| Nivel | Identidad | Secciones añadidas |
|---|---|---|
| **0 · Reclutador** | "¿Puedo confiar y qué descargar?" | resultados · productos · experiencia · descargas · contacto |
| **1 · Normal** | "Exploración técnica" | + evolucion · proyectos · demos · roles |
| **2 · Profundo** | "Engagement: comercial + colaboración + meta" | + servicios · modalidades · flujo-ia · referencias |

Distribución final balanceada: **5 / 4 / 4**.

### Cambios

- `#servicios`: nivel 1 → 2 (oferta comercial; el visitante normal explora trabajo, el profundo evalúa contratar).
- `#modalidades`: nivel 1 → 2 (formatos de colaboración con sliders — detalle deep).
- Nav entries actualizadas: `#servicios` y `#modalidades` reciben `data-min-level="2"`.

---

## 2026-06-20 (III) — Reorganización de niveles (reducir sobrecarga visual sin perder funcionalidad)

Aprovechando el sistema de 3 vistas que ya existía (Reclutador / Normal / Profundo), se redistribuyen las secciones para que el reclutador en nivel 0 vea solo lo esencial. Sin tocar contenido, sin perder funcionalidad — todo sigue accesible escalando de vista.

### Reorganización por nivel

| Sección | Antes | Ahora |
|---|---|---|
| `#resultados` | nivel 0 | nivel 0 (sin cambio) |
| `#productos` | nivel 0 | nivel 0 (sin cambio — vitrina principal) |
| `#experiencia` | nivel 0 | nivel 0 (sin cambio) |
| `#descargas` | nivel 0 | nivel 0 (sin cambio — CVs y cartas) |
| `#contacto` | nivel 0 | nivel 0 (sin cambio) |
| `#evolucion` | nivel 1 | nivel 1 (sin cambio) |
| `#proyectos` | nivel 0 | **nivel 1** ← evita duplicación con #productos |
| `#demos` | nivel 0 | **nivel 1** |
| `#roles` | nivel 0 | **nivel 1** |
| `#servicios` | nivel 0 | **nivel 1** |
| `#modalidades` | nivel 0 | **nivel 1** |
| `#flujo-ia` | nivel 1 | **nivel 2** ← narrativa meta, recruiter no la necesita |
| `#referencias` | nivel 0 | **nivel 2** ← ya cubierto por carta de recomendación en #descargas |

**Resultado:** nivel 0 (Reclutador) baja de 11 secciones visibles a **5 esenciales**: hero + resultados + productos + experiencia + descargas + contacto.

### Cambios complementarios

- **Nav principal**: links a #proyectos, #demos, #roles, #servicios, #modalidades reciben `data-min-level="1"` → desaparecen del nav en vista Reclutador (no quedan links muertos).
- **Hero CTAs**: el botón "Ver proyectos" cambia a "Ver productos" (apunta a `#productos` que sí está en nivel 0). El "Ver proyectos" original baja a `data-min-level="1"`. En 6 idiomas.
- **Ninguna sección eliminada**: todas siguen presentes y funcionales al escalar la vista.

---

## 2026-06-20 (II) — Cierre integral del ciclo RootCause

Tras pasar a público `rootcause-windows-inspector`, se sincroniza el resto del ecosistema (CLAUDE.md, #proyectos, README, llm.txt, PDFs) + auditoría completa de enlaces.

### CLAUDE.md — regla 9 derogada

Antes: _"RootCause es permanentemente oculto — no mencionarlo en ningún output público"_.
Ahora: _"RootCause es **público desde 2026-06-20**: el repo `rootcause-windows-inspector` pasó de privado a público y el producto está en el portafolio (sección #productos, card propio en #proyectos, mención en README/llm.txt/PDFs). Regla histórica derogada por autorización explícita del usuario en la sesión 2026-06-19/20."_

### `index.html` — sección `#proyectos`

- Nuevo card RootCause (8º card) en 6 idiomas, después de Python Data Science Program.
- Tags: Forensics · Rust, chips: Rust edition 2024 / Windows 10/11 / ETW · WPR / 5 ediciones / 11 releases.
- Botones: GitHub (repo principal) + Release v0.11.0 + Landing.

### `README.md` pilar 9 (nuevo)

Pilar dedicado: _"Producto comercial Windows: RootCause Windows Inspector v0.11.0 — diagnóstico forense escrito en Rust (edition 2024) con 5 ediciones publicadas, ETW · WPR, SHA256SUMS por release, 11+ releases tagueadas."_

### `llm.txt`

- About párrafo: añadido _"Windows forensic diagnostics product (RootCause Windows Inspector v0.11.0 in Rust edition 2024, 5 editions: GUI Setup.exe / Portable .zip / CLI single-binary rootcause.exe / PowerShell .psm1 / VS Code .vsix)"_.
- Technology Stack: añadida línea _"Rust forensics (RootCause Windows Inspector): ETW + WPR, 5 editions per release, SHA256SUMS"_.

### PDFs — 18 regenerados con backup

- `[BACKUP] assets/backups/2026-06-20/*.pdf` — 30 PDFs previos.
- `scripts/generate-all-languages.py`: bullet RootCause agregado en `projects` y `projects_ats` + entrada `"rootcause"` en `PROJECTS_URLS`.
- `scripts/generate-portfolio.py`: bullet RootCause agregado en los 6 bloques de idioma (separadores `:`, `:` con espacio inicial, y `：`).
- Regeneración: 12 CVs (cv-reclutador × 6 + cv-ats × 6) + 6 portafolios. Carta de recomendación y declaración de logros sin cambio (no enumeran proyectos).

### Auditoría integral de enlaces

Extracción y verificación HEAD de los 58 URLs `github.com`/`gitlab.com` en `index.html`:

- **57/58 → 200 OK**.
- **1 → 404 detectado y corregido**: `…/releases/latest/download/app-debug.apk` (nombre del asset cambió en v2.2.0). Reemplazado por `portfolio-app-v2.2.0-debug.apk` en la sección `#descargas` (botón Android · APK de "Otras versiones"). Verificado 200 OK.
- **58/58 → 200 OK final**.

---

## 2026-06-20 — rootcause-windows-inspector pasó a público · card RootCause reajustado

El usuario migró `rootcause-windows-inspector` de **privado → público** (push 2026-06-20). Esto cambia la arquitectura del card:

### Cambios en el ecosistema RootCause

- **`rootcause-windows-inspector`** ahora es público — es el repo principal del producto (Rust edition 2024), con 11+ releases (v0.5.0 → v0.11.0).
- **`rootcause-landing/` Pages → 404**: la landing del repo separado fue deshabilitada. La landing real ahora vive en `/rootcause-windows-inspector/` (200 OK).
- Releases del rootcause-landing → 404 (movidas/desactivadas; la fuente única son ahora las releases del repo principal).

### Card RootCause en `#productos` (rehecho)

- **Landing**: `https://vladimiracunadev-create.github.io/rootcause-windows-inspector/` (antes: rootcause-landing — broken).
- **GitHub**: `vladimiracunadev-create/rootcause-windows-inspector` (antes: rootcause-landing).
- **Descargas directas** (todas desde el repo principal, `/releases/latest/download/`):
  - `RootCause-Setup.exe` (GUI installer)
  - `RootCause-Portable.zip` (GUI portable)
  - `rootcause.exe` (CLI single-binary — **nuevo**, aparece en v0.11.0)
  - `RootCause-VSCode-Extension.vsix`
- **Botón "Todas las ediciones"** → `/releases/latest` (incluye CLI-Portable.zip y .psm1).
- **`editions_count: 4 → 5`** (CLI single-binary se cuenta como edición separada).
- Descripción enriquecida con síntomas concretos (disco 100%, %TEMP%, etc.) y filosofía del producto ("diagnóstico primero, intervención después").

### `api/v1/projects.json`

- `url`: `rootcause-landing → rootcause-windows-inspector`.
- `site_url`: actualizado a `/rootcause-windows-inspector/`.
- `release_url`: actualizado al repo principal.
- Nuevo campo `landing_repo` (apunta al repo legacy `rootcause-landing` para referencia).
- Tags ampliados con `Rust edition 2024`, `Windows 10/11`, `CLI single-binary`, `rootcause.exe`, `SHA256SUMS`.

### Verificación HEAD 200 (RootCause migración)

11/11 URLs nuevas con HEAD 200. `rootcause-landing/` ya retorna 404 (esperado tras la migración).

---

## 2026-06-19 (VII) — RootCause incorporado como producto (override autorizado)

El usuario autorizó explícitamente esta sesión: "te autorizo que agreggues root cause como producto". Esta autorización **sobreescribe la regla 9 de CLAUDE.md** ("RootCause es permanentemente oculto — no mencionarlo en ningún output público") solo para este cambio. La regla en CLAUDE.md sigue intacta — el usuario decidirá si la actualiza/elimina en otro momento.

### Card agregada en `#productos` (primera posición)

- **RootCause · Windows Inspector v0.11.0** — Diagnóstico forense Windows escrito en Rust, ETW · WPR.
- 4 ediciones: GUI Desktop (Setup .exe v0.9.0), CLI-only (Portable .zip), PowerShell Module (.psm1), VS Code Extension (.vsix).
- Landing: `/rootcause-landing/` (repo público).
- Botones: Landing + Portable .zip (v0.11.0) + Setup .exe (v0.9.0) + VS Code .vsix + Todas las ediciones.
- URLs verificadas con HEAD 200.

### `api/v1/projects.json` (entrada RootCause inicial)

- Nueva entry RootCause con `category: tooling`, `editions_count: 4`, tags incluyendo todos los formatos de release.

`#productos` queda con **8 cards** (RootCause + los 7 previos).

> Nota: el repo principal `rootcause-windows-inspector` es privado; el card apunta al repo público `rootcause-landing` donde están publicadas las releases del producto.

---

## 2026-06-19 (VI) — quitar card "Portfolio App" de #productos

El propio portafolio (este sitio) listado como producto dentro de su sección de productos es recursivo y confunde al visitante. Se elimina la card. La APK del propio sitio sigue disponible vía la sección `#descargas` y el menú móvil/PWA.

`#productos` queda con 7 cards: Automa, Python DS Program, ChofyAI Studio, Docker Labs, Microsistemas, Unikernel Control Center, GabySQL + Modeler.

---

## 2026-06-19 (V) — nueva sección #productos (descargables: landing + .exe/.zip/.apk)

Auditoría de los repos para detectar landing pages y artefactos descargables. Verificación con HEAD 200 de todas las URLs (landing y direct-download).

### Productos detectados (8 cards)

| Producto | Versión | Landing | Descarga directa |
|---|---|---|---|
| Automa · PC Orchestrator | v0.2.1 | `/automa-pc/` | `Automa-Setup-v0.2.1.exe` |
| Python Data Science Program | v3.8.0 | `/python-data-science-program/` | `.exe` + `.zip` portable + `.apk` |
| ChofyAI Studio | v0.5.1 | `/chofyai-studio/` | — (sin releases todavía) |
| Portfolio App (este repo) | v2.2.0 | este mismo sitio | `portfolio-app-v2.2.0-debug.apk` |
| Docker Labs Control Center | v1.5.0 | — | `docker-labs-setup-1.5.0.exe` |
| Microsistemas | v1.1.0 | — | `microsistemas-v1.1.0.zip` |
| Unikernel Control Center | v1.0.0 | — | `UnikernelControlCenter-1.0.0-win-x64-setup.exe` |
| GabySQL + Modeler | engine v0.2.0 / modeler v0.1.0 | — | `gabymodeler_0.1.0_x64-setup.exe` + `gabysql-v0.2.0-windows-x86_64.zip` + builds macOS arm64 / Linux x86_64 |

### Cambios en `index.html`

- Nueva sección `<section id="productos">` insertada ANTES de `#proyectos` (orden: hero → resultados → evolución → **#productos** → #proyectos → #demos → …).
- 8 cards con: título + tag de versión/plataforma · descripción en 6 idiomas · chips de plataforma · botones (Landing si existe + Descarga directa `.exe/.zip/.apk` + Release + GitHub).
- Botones usan `/releases/latest/download/<asset>` para que sigan funcionando al publicar nuevas versiones (gabysql excepción: engine apuntando a `v0.2.0` específico porque `/latest` resuelve a Modeler `desktop-v0.1.0`).
- Menú de navegación: nuevo link "Productos / Products / Produtos / Prodotti / Produits / 产品" antes de "Proyectos" (6 idiomas).

### Verificación HEAD 200 (productos)

11/11 URLs probadas con `curl -sIL -o /dev/null -w "%{http_code}"`:

- 3 landings → 200
- 8 direct downloads → 200 (incluido fix gabysql usando ruta específica v0.2.0 en lugar de `/latest`)

---

## 2026-06-19 (IV) — social-bot-scheduler: Release v4.3.1 incorporada

El usuario publicó los tags faltantes en `social-bot-scheduler`. Estado actualizado:

- `v4.3.1` (2026-06-19) — Supply-chain hardening (npm → pnpm v11)
- `v4.3.0` (2026-06-19) — Master Dashboard interactivo
- `v4.2.0` (2026-06-19) — Auditoría de seguridad de 8 capas
- `v2.2.0` (2026-01-26) — release previa

### Cambios (social-bot-scheduler)

- `api/v1/projects.json`: `version: v4.3.0 → v4.3.1`, `name: "Social Bot Scheduler v4.3 → v4.3.1"`, descripción enriquecida con los hitos de v4.2/v4.3/v4.3.1, nuevo campo `release_url`.
- `index.html` (card social-bot): nuevo botón `Release v4.3.1` entre `GitHub` y `README`. URL verificada (HEAD 200).

Cierra el caso pendiente del commit anterior.

---

## 2026-06-19 (III) — verificación de enlaces + botones Release/Commits

Auditoría completa de los 14 repos enlazados desde `index.html`:

- **14/14 repos existen** (200 OK vía `gh api`).
- **8 repos tienen releases publicadas**: automa-pc (**v0.2.1** — release del 19-jun), docker-labs (v1.5.0), gabysql (desktop-v0.1.0), microsistemas (v1.1.0), python-data-science-program (v3.8.0), social-bot-scheduler (v2.2.0 — único tag), unikernel-labs (v1.0.0), `.github.io` (v2.2.0).
- **5 repos sin releases**: chofyai-studio, claude-skills-toolkit, langgraph-realworld, mcp-ollama-local, problem-driven-systems-lab, proyectos-aws.

### Cambios aplicados en `index.html`

Botón nuevo por cada card del bloque `#proyectos` (los 13 URLs nuevos verificados con HEAD 200):

| Card | Botón nuevo |
|---|---|
| microsistemas | Release v1.1.0 |
| docker-labs | Release v1.5.0 |
| proyectos-aws | Commits |
| langgraph-realworld | Commits |
| mcp-ollama-local | Commits |
| unikernel-labs | Release v1.0.0 |
| chofyai-studio | Commits |
| problem-driven-systems-lab | Commits |
| claude-skills-toolkit | Commits |
| gabysql | Release desktop-v0.1.0 |
| automa-pc | Release v0.2.1 (entre GitHub y Sitio) |
| python-data-science-program | Release v3.8.0 |

### Bump automa-pc v0.2.0 → v0.2.1

- `api/v1/projects.json`: `version: v0.2.1` + nuevo campo `release_url`.

### social-bot-scheduler — caso pendiente

El repo tiene solo `v2.2.0` (2026-01-26) como tag/release público, pero el portfolio (y el repo mismo internamente) reportan v4.3.0. **No se agrega botón Release todavía** — quedó task spawned para que el usuario publique el tag v4.3 en el repo correspondiente. Hasta entonces el card mantiene solo `GitHub` + `README`.

---

## 2026-06-19 (II) — agregar Automa · PC Orchestrator

Repo nuevo detectado tras auditoría adicional de `gh repo list` (no estaba en la primera pasada). Incorporación quirúrgica sin tocar el resto.

- `api/v1/projects.json`: nueva entrada **Automa · PC Orchestrator v0.2.0** (category `tooling`, `flows_count: 20`, `tests_count: 115`) — Python 3.10+, Playwright (headless/visible), pywebview + PyInstaller, SQLite historial, OCR/visión, uv packaging, instalador Windows firmado, local-first.
- `index.html`: nuevo `<article class="card project">` con descripción en 6 idiomas (ES/EN/PT/IT/FR/ZH), pills y dos acciones (GitHub + Sitio `vladimiracunadev-create.github.io/automa-pc/`). Insertado antes de Python Data Science Program.
- `scripts/generate-portfolio.py`: bullet Automa añadido en cada uno de los 6 bloques de idioma (preservando los separadores `:`, `:` con espacio inicial, y `：`).
- `scripts/generate-all-languages.py`: bullet Automa añadido en los bloques `projects` y `projects_ats` + entrada `"automa"` en el mapa `PROJECTS_URLS`.
- PDFs regenerados: 12 CVs (cv-reclutador × 6 + cv-ats × 6) + 6 portafolios. Carta de recomendación y declaración de logros no requieren cambio (no enumeran proyectos).

Repos públicos descartados de esta incorporación:

- `retail-sales-analysis` (2026-06-18): descripción "Proyecto Skillnest" sugiere ejercicio de curso, no pieza de portafolio.
- `rootcause-landing` (2026-04-29): aunque público, menciona RootCause — bloqueado por **regla 9 de CLAUDE.md** ("RootCause es permanentemente oculto — no mencionarlo en ningún output público").

---

## 2026-06-19

Actualización integral del portafolio (skill `portfolio-full-update`) — sincroniza el sitio, la CV Data API, los 30 PDFs y la documentación con el estado real de los repositorios al 19-jun-2026.

### chore(api): refresh dates + reflejar deltas de repos

- `api/v1/meta.json`, `profile.json`, `experience.json`, `projects.json`, `skills.json`, `artifacts.json` → `generated_at: 2026-06-19`.
- `data/resume.json` → `generated_at: 2026-06-19`.

### feat(projects): incorporar versiones y métricas confirmadas vía auditoría de repos

- **microsistemas v1.1.0** (CapacitySim Pro): `tools_count: 11 → 12`, agrega `katas_count: 195`, `technologies_covered: 67`.
- **chofyai-studio v0.5.1** (antes "Fase 4"): soporte experimental Windows + NVIDIA GPU, `pnpm + SHA-512 lockfile`, `.dmg releases`, descargas guiadas con progreso.
- **problem-driven-systems-lab**: `operational_cases: 12 → 60` (12 desafíos × 5 stacks: PHP 8 · Python · Node.js · Java 21 · .NET 8), dashboards con métricas en tiempo real, AWS_MIGRATION.md con cost estimates.
- **claude-skills-toolkit**: `skills_count: 7` con tags completos (security-audit, yaml-control, md-lint-fix, docker-cleanup, docker-compose-doctor, pre-push-guard, web-snap).
- **gabysql v0.2.0** + desktop-v0.1.0 (Fase 3): cost-based optimizer, SAVEPOINT/ROLLBACK TO, sesiones HTTP cross-request, fuzzing 503.8M queries (zero panics), 828 tests passing.
- **python-data-science-program v3.8.0**: `classes_count: 197 → 232`, app Windows nativa PySide6+Qt+kernel Jupyter, app Android Expo SDK 51, 232 PDFs + 232 PPTX generados, categoría → `education`.
- **mcp-ollama-local**: blueprint AWS migration (`docs/aws-migration.md`), supply-chain scanning (Semgrep, CodeQL, SBOM).

### feat(skills): nuevos elementos de stack

- `frontend`: Tauri + React, PySide6 / Qt Desktop, Expo SDK 51 (Android), pnpm (corepack).
- `security`: grype, Semgrep, CodeQL, Bandit, detect-secrets, TruffleHog, SBOM, OSV/KEV/EPSS scanning, SHA-512 lockfile verification.
- `data`: GabySQL (embedded Rust, WAL, cost-based optimizer), parser fuzzing.

### feat(site): index.html refleja deltas en 6 idiomas

- `buildDate: 2026-05-21 → 2026-06-19`.
- Hero "Pilares Técnicos Consolidados" (6 idiomas): "11 microsistemas → 12 microsistemas" + nuevo "60 casos operativos en Problem Driven Systems Lab (12 × 5 stacks)".
- Card Problem Driven Systems Lab (6 idiomas): "12 casos reales en 5 stacks" → "12 desafíos × 5 stacks = 60 casos operativos" + métricas en tiempo real + cost estimates.
- Card Python Data Science Program (6 idiomas): "197 clases" → "232 clases" + PySide6+Qt+Jupyter + Expo SDK 51 + "232 PDFs + 232 PPTX".
- Pills: "197 clases" → "232 clases" + PySide6 + Android.
- Card IA Agéntica (6 idiomas): ChofyAI Studio "Fase 4 macOS" → "v0.5.1 macOS + soporte experimental Windows + NVIDIA GPU + pnpm + SHA-512 lockfile" + blueprint AWS migration en MCP+Ollama.

### feat(docs+seo): README, llm.txt, sitemap.xml

- `README.md` pilar 6: Python Data Science Program v1.1 → v3.8.0 (232 clases, PySide6+Qt+Jupyter, Expo SDK 51), ChofyAI Studio Fase 4 → v0.5.1 (Windows + NVIDIA GPU, pnpm + SHA-512).
- `README.md` pilar 7: LangGraph v4.2 (25 / 10 backends) → v4.15 (25/25 cobertura 100%); MCP+Ollama Local con Semgrep + CodeQL + SBOM + blueprint AWS migration.
- `llm.txt`: párrafo "About" reescrito (14 AWS cases, LangGraph v4.15 25/25, Problem Driven 60 operational cases, Python Data Science 232 lessons, GabySQL v0.2 828 tests).
- `llm.txt` y `sitemap.xml`: `lastmod / Last Updated → 2026-06-19`.

### chore(pdfs): backup + regeneración de los 30 PDFs (5 docs × 6 idiomas)

- `[BACKUP] assets/backups/2026-06-19/*.pdf` — copia íntegra de los 30 PDFs previos antes de la regeneración.
- Scripts actualizados (`generate-all-languages.py`, `generate-portfolio.py`) con los nuevos conteos:
  - "Python Data Science Program — 197 clases" → "232 clases en 9 partes [...] app de escritorio Windows nativa (PySide6 + Qt + kernel Jupyter) + app Android (Expo SDK 51). 232 PDFs + 232 PPTX generados".
  - "Problem Driven Systems Lab — 12 casos reales [...]" → "12 desafíos × 5 stacks = 60 casos operativos".
- Regeneración exitosa: cv-reclutador × 6, cv-ats × 6, portafolio × 6, declaracion-logros-validacion × 6, carta-recomendacion_sin_firma × 6.

### Estructura preservada

Conforme a la regla 2026-05-22 ("preservar estructura aprobada, solo actualizar contenido"): el layout, las columnas, la paleta y el orden de secciones de los CVs reclutador/ATS se mantienen idénticos. Sólo se actualizó el contenido enumerado arriba.

### No incorporado (descartado por sospecha de misread del agente)

- "social-bot-scheduler v4.3 → v2.2.0": preservado v4.3.0 actual hasta verificación manual del usuario (la regresión de versión major no concuerda con el patrón de versionado del repo).
- "proyectos-aws 14/15 → 2/11 operativos": preservado 14/15 hasta verificación (probable lectura de pestaña/README desactualizado).

---

## 2026-05-22

Sesión exhaustiva de auditoría + rediseño + enriquecimiento de los CVs reclutador (6 idiomas). Estructura aprobada visualmente por el usuario tras revisión PDF a PDF.

### feat(cv-reclutador): rewrite EXPERIENCIA con suite real de productos CEIS + métricas verificadas

El bloque EXPERIENCIA del cv-reclutador era genérico ("Desarrollo, mantención y evolución de plataforma…") y no reflejaba la riqueza real del período en Fundación CEIS Maristas, contradiciendo lo que dicen la carta de recomendación y la declaración de logros. Rewrite completo en los 6 idiomas:

- **Cargo combinado**: "Arquitecto de Software · Analista y Desarrollador Full-Stack" (mezcla la autotitulación con el cargo oficial de la carta de recomendación).
- **Fecha precisa**: "mayo 2011 — octubre 2025" (antes "2011-2025"; ahora coincide con la carta).
- **5 bullets densos** que reemplazan los 5 genéricos previos:
  1. **Suite de productos**: PCA (aprendizaje), Baterías Psicoeducativas (desarrollo social/personal), Batería Online (plataforma online), más mailing institucional, LimeSurvey y WordPress.
  2. **Métricas verificadas**: 80% mejora reportes/carga Batería Online · 90% menos fricción atención clientes (2020-2025) · 45% optimización DB/código · hasta 5 frentes concurrentes.
  3. **Pandemia 2020**: migración de servicios presenciales a online en tiempo breve (citado en carta de recomendación).
  4. Modernización PHP 5.4 → 8.2+, refactor módulos críticos, traslado de lógica a JavaScript, eliminación de duplicidades en DB.
  5. Mailing masivo (PHP + Constant Contact) y **adopción interna de IA (2024-2025)** para análisis y resolución de problemas técnicos.

NO se incluyen en el CV (por decisión deliberada, ver discusión de sesión): datos de contacto del referee (mejor práctica internacional: solo "disponible a solicitud" — además el link a la carta ya lo cubre) ni razón de salida (contenido defensivo que pertenece a entrevista, no a CV).

### feat(cv-reclutador): mejoras de contenido en header, idiomas y referencia a logros

- **Subtítulo más corto y posicionado** (6 idiomas, en `subtitle_rec` + `subtitle_ats`):
  - Antes: "Arquitecto de Soluciones | Senior Full-Stack | Modernización, Automatización e IA Aplicada"
  - Ahora: "Arquitecto de Software · 14 años modernizando plataformas críticas con IA aplicada"
- **Línea de inglés reformulada** (6 idiomas, en `language_skill`):
  - Antes: "Inglés: intermedio en lectura; básico en escritura y conversación." (red flag para roles internacionales)
  - Ahora: "Inglés técnico: lectura fluida (documentación, código, papers, IA tooling). Conversación: básica, en mejora activa."
- **Referencia inline a logros**: al final de la línea `Tecnologías:` se añade un link italica azul `→ Métricas y logros cuantificados del periodo CEIS Maristas` apuntando a `declaracion-logros-validacion{suffix}.pdf` (label per-idioma vía nuevo campo `exp_logros_label`). Implementado en `build_recruiter_section` como concatenación a `exp_tech` para no añadir párrafo extra (preserva conteo de páginas).

### fix(cv-reclutador): layout 2-columnas estable + 4 páginas en los 6 idiomas

El layout aprobado por commit `9dab81c` estaba roto visualmente: el `main_frame` desbordaba a la sidebar en pág 1 y el sidebar (CONTACTO/SKILLS/EDUCACIÓN/IDIOMAS) terminaba ocupando una página propia (pág 2). Total 5 páginas, layout 2-columnas no se cumplía.

Causa: estilos demasiado holgados en `recruiter_styles()` (`fontSize=9.2, leading=12.5`) sumados al volumen del main (12 proyectos + experiencia + trayectoria previa + formación). El `FrameBreak()` quedaba inalcanzable dentro de pág 1.

Fix en `scripts/generate-unified-cv.py:47-106` (`recruiter_styles`): reducción gradual de fontSize/leading/spaceBefore/spaceAfter — bullet 8.5pt → 8.0pt, leading 11.5 → 10.5, heading 11 → 10.5, tech 8 → 7.5, spaceBefore heading 5 → 4. Sumado al rewrite del bloque EXPERIENCIA (bullets más densos pero más informativos), el main entero entra en su frame y el sidebar fluye correctamente al lado en pág 1.

Resultado: los 6 PDFs tienen 4 páginas (recruiter 2-col → transición → ATS 2 págs), sidebar a la izquierda con fondo gris, FORMACIÓN al pie de la columna principal.

### feat(generate-unified-cv): soporte de fuente CJK para chino

Antes, los caracteres chinos se renderizaban como cuadros ■ porque ningún estilo registraba fuente CJK (Helvetica no tiene glifos). Fix:

- Registro de `UnicodeCIDFont("STSong-Light")` (incluida en ReportLab, sin fuente externa requerida) al import de `generate-unified-cv.py`.
- Helper `_apply_cjk(styles_dict)` que swap-ea `fontName` a `STSong-Light` en todos los estilos del dict.
- `UnifiedCV.__init__` ahora acepta `lang="es"` y guarda `self.lang` (tras `BaseDocTemplate.__init__`, que lo reseteaba si se asignaba antes — bug encontrado mediante monkey-patching).
- `_draw_recruiter_page` usa CJK para el header drawing (canvas-level) cuando `self.lang == "zh"`.
- `build_recruiter_section`, `build_transition_section`, `build_ats_section` reciben `lang` y aplican `_apply_cjk` al crear sus estilos.
- `build_cv` (ATS standalone) también acepta `lang` y aplica CJK condicional.

Resultado verificado: `cv-reclutador-chinese.pdf` y `cv-ats-chinese.pdf` ahora renderizan chino real (`概述`, `主要经验`, `技能`, etc.) con 0 cuadros ■.

### fix(cv-reclutador): SKILLS solo en sidebar izquierda + restaura FORMACIÓN Y ACTIVIDAD RECIENTE

Revertido el hijack del bloque `h_training` en `scripts/generate-all-languages.py:813-815` introducido por commit `9dab81c`. Aquel cambio reemplazó el contenido de "FORMACIÓN Y ACTIVIDAD RECIENTE" en la columna derecha por una **duplicación** del bloque SKILLS — violación regla #1 CLAUDE.md (nunca destruir, solo integrar).

- `make_rmain()` vuelve a usar `h_training=T["h_training"]` y `training=T["training"]`.
- SKILLS queda únicamente en la sidebar izquierda (`make_sidebar`, posición correcta tras `contact_links`).
- FORMACIÓN/ACTIVIDAD RECIENTE recupera sus bullets originales.

### fix(cv-chino): limpieza de bugs preexistentes en bloque `zh`

- `ats_experience`: 5 líneas huérfanas mezcladas (strings en español + tuple mal formada) — eliminadas.
- `projects_rec`: cerraba con 2 tuples `("texto", "key")` cuando la lista esperaba strings — se filtraban como `('Claude Skills Toolkit…', 'claude')` literal en el PDF. Eliminadas.
- Indentación de cierres `],` corregida.

### fix(content): emoji huérfano y texto duplicado en bullets de proyectos

- **Gabysql**: `️` (variation selector-16) huérfano antes de "GabySQL" — el emoji original se había perdido en algún round-trip de edición, dejando solo el modificador que renderizaba como ■. Eliminado en las 10 ocurrencias (`projects_rec` × 6 langs + `projects_ats` × 6 langs… equivalente).
- **Python Data Science Program**: el texto se duplicaba literalmente — "Python Data Science Program — Python Data Science Program · 197 clases…". Acortado a "Python Data Science Program — 197 clases en 9 partes: Python, ML, Deep Learning, MLOps, ingeniería de datos. Lab Flask + apps Windows/Android". 7 ocurrencias.
- **doc_links bullet**: cambiado de `•` a `<b>→</b>` para distinguir visualmente "Ver declaración de logros" / "Ver carta de recomendación" de los bullets de proyectos en pág 1 (antes parecían 2 proyectos más).

### chore(repo): protocolo de backups + integridad binaria + huérfanos

- **Backup obligatorio**: `assets/backups/2026-05-22/` con los 13 PDFs CV pre-sesión (regla #2 CLAUDE.md). Incluye las 6 variantes de `cv-ats*` y `cv-reclutador*` + el huérfano `cv-reclutador-ats.pdf`.
- **Archivo huérfano movido**: `assets/cv-reclutador-ats.pdf` (66 KB, PDF 1.7, marzo 2026, no referenciado en HTML/JS/JSON, fuera del naming pattern) → `assets/no_aplica/cv-reclutador-ats.pdf` (carpeta gitignored, no se publica en API).
- **`.gitattributes` creado**: marca `*.pdf *.png *.jpg *.woff* *.zip` etc. como `binary` para evitar la conversión LF↔CRLF que Git estaba intentando aplicar a los PDFs en Windows (warnings reales detectados; riesgo de corrupción cross-platform).
- **`.gitignore`**: añadido `__pycache__/` y `*.py[cod]` (faltaban; el caché de bytecode estaba apareciendo en `git status`).

### docs

PDFs regenerados: 12 PDFs CV (6 reclutador + 6 ATS), 4 páginas cada reclutador, layout 2-columnas con sidebar a la izquierda, CJK funcional para chino.

**Follow-up pendiente** (no abordado en esta sesión): los otros 3 generators de PDFs en chino (`generate-portfolio.py`, `generate-achievements-statement.py`, `generate-recommendation-letter.py`) tampoco registran fuente CJK. Si se abren las versiones `-chinese.pdf` de portafolio, declaración y carta, los caracteres seguirán como ■. Aplicar el mismo patrón es trabajo separado.

## 2026-05-21

### fix(content): eliminar residuos del repo renombrado python-data-science-bootcamp

Auditoría exhaustiva tras detectar incoherencias remanentes. El repo fue renombrado a `python-data-science-program` pero quedaban 25+ menciones del nombre viejo en archivos vivos:

- `scripts/generate-portfolio.py`: 6 entradas "Python Data Science Bootcamp" eliminadas (× 6 idiomas en listas de proyectos del PDF portafolio). `project_link_labels.python`: "Bootcamp" → "Program" en los 6 idiomas.
- `scripts/generate-all-languages.py`: 12 entradas eliminadas (6 reclutador + 6 ATS, × idiomas). `PROJECTS_URLS.python`: URL `/python-data-science-bootcamp` → `/python-data-science-program`.
- `api/v1/experience.json`: línea "Python Data Science Bootcamp v1.1.0: expansión a 31 clases…" reemplazada por "Python Data Science Program: 197 clases en 9 partes…".
- `data/repo-scores.json`: entrada `python-data-science-bootcamp` eliminada del caché.
- **PDFs regenerados**: 12 CVs + 6 portafolios (× 6 idiomas), ahora sin contaminación.

Validación: `grep -nE "Python Data Science Bootcamp|python-data-science-bootcamp" scripts api index.html styles.css` → **0 hits** en archivos vivos. Solo persisten en CHANGELOG histórico y backups (`assets/backups/`), donde es correcto.

`pnpm test` 51 PASSED / 0 ERRORS, `pnpm run lint:md` 0 errors.

### style(proyectos): jerarquía visual hero/secondary + reducción de pills (-32%)

Sección `#proyectos` rediseñada para reducir sobrecarga visual sin perder contenido.

- **Hero cards (5)** sin `data-min-level` — siempre visibles, con border-left accent: Batería Online, Cloud Portfolio AWS, LangGraph Agentic Resilience, MCP Ollama Local, Docker Labs, Social Bot Scheduler. Cards bandera con tamaño/peso original.
- **Secondary cards (7)** con `data-min-level="1"` — compactas (padding 12px, h3 0.95em, pills 11px): Microsistemas, Unikernel Labs, ChofyAI Studio, Problem-Driven Systems Lab, Claude Skills Toolkit, Python Data Science Program.
- **Supplementary (1)** con `data-min-level="2"` — solo en vista Profundo: GabySQL.
- **Eliminada** card duplicada `Python Data Science Bootcamp` (repo renombrado a `-program`).
- **Pills reducidos de 79 → 54** (-32%): cada card ahora tiene 3-5 pills priorizando stack + diferenciador. Ejemplos: AWS 8→5, Unikernel 7→4, Problem-Driven 7→5 (ahora reflejan los 5 stacks PHP/Python/Node/Java 21/.NET 8 + AWS_MIGRATION).
- **CSS añadido** en `styles.css`: selectores `.card.project:not([data-min-level])` para hero y `.card.project[data-min-level="1"|"2"]` para compactas (padding, h3, p, .pill, .chips, .actions .btn).

Validación: `pnpm test` 51 PASSED / 0 ERRORS, `pnpm run lint:md` 0 errors.

### feat(sync): detecciones de auditoría profunda en el dry-run + bump langgraph v4.15

Tres detecciones nuevas en `scripts/sync-portfolio.py` que eliminan el principal "ciego" del flujo automático:

- `detect_stale_projects()` — repos en `projects.json` cuyo URL ya no existe en GitHub público (renombrados, eliminados o vueltos privados).
- `detect_version_drift()` — compara `version` en JSON contra el primer `vX.Y.Z` del README real (primeras 60 líneas). Detectó automáticamente que langgraph saltó a v4.15.0 mientras estaba a v4.14.0.
- `detect_stale_pushes()` — repos con push <=7 días que pueden tener features nuevas no reflejadas en la descripción corta.

Integradas en `main()` como parte del reporte de dry-run. Documentadas en `.agents/skills/sync-portfolio/SKILL.md`.

**Bump langgraph v4.14 → v4.15.0** (release de hardening de seguridad: 4 critical fixes inline, `shared/lgrw_common/` canónico, `python-jose` → `joserfc`, CI extendido a los 25 casos):

- `api/v1/projects.json`: name `v4.14` → `v4.15`, version `v4.14.0` → `v4.15.0`, tags + joserfc/CodeQL/shared/lgrw_common/Security Hardening v4.15.
- `index.html`: 6 idiomas × múltiples ubicaciones — `LangGraph v4.14` → `v4.15`.
- `scripts/generate-{portfolio,all-languages}.py`: idem.

### profile README: pasada completa de coherencia (commits `f888276` + `9e0a14c`)

Auditoría exhaustiva de TODAS las menciones de versión y stack:

- Stack en header: + `Java 21 · .NET 8` (presente en problem-driven-systems-lab).
- Avance #6 "IA aplicada": `10 backends operativos` → `25/25 backends operativos (cobertura 100%, v4.15.0)`.
- Card Social Bot Scheduler: title `v4.2.0` → `v4.3.0`.
- Card LangGraph RealWorld: title + body — `v4.2.0 · 10 backends` → `v4.15.0 · 25/25 backends · cobertura 100%`, + streaming NDJSON, + cadena de custodia SHA-256, + release v4.15 hardening adversarial (`shared/lgrw_common/`, `python-jose` → `joserfc`).
- Card Problem-Driven Systems Lab: title `12 casos · multi-stack` → `12 casos · 5 stacks (PHP 8 · Python · Node · Java 21 · .NET 8)`. Body con primitivas concretas de Java 21 (`ConcurrentHashMap`, `CompletableFuture.orTimeout`) y .NET 8 (`ConcurrentDictionary`, `CancellationTokenSource`). + plan **AWS_MIGRATION.md** (ECS Fargate · Lambda · EKS) con mapping explícito a SECURITY.md.
- Ruta D "Si tengo 10 minutos": `10 backends operativos` → `25 backends operativos (cobertura 100%): casos 01-25`.
- Rol "AI Orchestration Engineer": LangGraph `v4.14.0` → `v4.15.0` (eliminada referencia stale tras bump).
- Card Python Data Science Program: eliminada referencia a `python-data-science-bootcamp v1.1 (31 clases)` (repo renombrado, mantener limpia la línea).
- Footer: `Última actualización: 2026-05-02` → `2026-05-21`.

### profile README (vladimiracunadev-create): cleanup + enriquecimiento

- Eliminada entrada `Python Data Science Bootcamp v1.1.0` (repo renombrado a `-program`).
- Reescritas con detalle técnico real las 3 secciones nuevas: Claude Skills Toolkit (12 capas explicadas), GabySQL (Rust + WAL + single-file engine), Python Data Science Program (197 clases en 9 partes + Flask + Windows + Android).
- Sección "Expansión natural — cargos asumibles": LangGraph v4.2.0 → v4.14.0 (luego v4.15.0 en commit subsiguiente), Social Bot v4.2 → v4.3, Technical Trainer ahora cita python-data-science-program / 197 clases.
- Commit remoto: `1ab243c4f0`.

### deep-audit: versiones, features y rebrands no detectados por el dry-run

Auditoría profunda manual sobre READMEs y releases reales de cada repo. Cierra brechas entre el estado vivo de los repos y el portafolio.

**api/v1/projects.json:**

- `LangGraph · Agentic Resilience v4.2` → `v4.14`; `version: v4.2.0` → `v4.14.0`; `operational_cases: 10 → 25`; `demos_count: 25`.
- `Social Bot Scheduler v4.2` → `v4.3`; `version: v4.2.0` → `v4.3.0` (alineado con el badge actual del README).
- `Unikernel Labs · Control Center`: `version: v1` añadido; tags ampliados con kraft, QEMU/KVM, .NET, Launcher, Low-latency, High-performance.
- `Problem Driven Systems Lab`: descripción reescrita a "12 problemas reales en 5 stacks (PHP 8 · Python · Node.js · Java 21 · .NET 8)" con Dashboards Interactivos por caso, patrones (Adapter, Strangler, Circuit Breaker, LRU, Cancellation) y plan AWS_MIGRATION.md (ECS Fargate · Lambda · EKS). Tags ampliados.
- Eliminada entrada duplicada `Python Data Science Bootcamp v1.1` (el repo fue renombrado a `python-data-science-program`, que ya está presente).

**api/v1/profile.json:**

- `summary`: "10 backends LangGraph operativos" → "25/25 backends LangGraph operativos (cobertura 100%, v4.14.0) con auditoría de seguridad de 8 capas y cadena de custodia SHA-256".

**index.html (6 idiomas cada item):**

- Sección "Estándares Consolidados" — todas las referencias `LangGraph v4.2` → `v4.14`; `Social Bot v4.2` → `v4.3` en 6 idiomas.
- Card `Problem Driven Systems Lab`: descripción reescrita con 5 stacks (PHP 8, Python, Node.js, Java 21, .NET 8), Dashboards Interactivos UI, patrones (Adapter/Strangler/Circuit Breaker/LRU/Cancellation), AWS_MIGRATION.md (ECS Fargate/Lambda/EKS).
- Card `Unikernel Labs · Control Center`: descripción amplificada a "Unikernel Control Center v1" con kraft + QEMU/KVM, Dashboard REST en localhost:9091 y Launcher .NET WinForms. Pills ampliados (kraft, QEMU/KVM, .NET).

**scripts/generate-*.py:**

- `generate-portfolio.py`: 5 idiomas + ZH — `LangGraph v4.2 + Ollama, 25 casos / 10 operativos` → `LangGraph v4.14 + Ollama, 25/25 backends operativos (cobertura 100%)`.
- `generate-all-languages.py`: 6 idiomas — `LangGraph v4.2 (25 casos / 10 operativos…)` → `LangGraph v4.14 (25/25 backends operativos, cobertura 100%…)`.
- 18 PDFs regenerados (12 CV ATS/Reclutador + 6 Portafolios).

**Validación:** `pnpm test` 51 PASSED / 0 ERRORS · `pnpm run lint:md` 0 error(s).

### sync-portfolio (automático — 2026-05-21)

- `api/v1/`: generated_at → 2026-05-21
- Repos nuevos integrados: claude-skills-toolkit, gabysql, python-data-science-program
- Cards HTML agregados en `#proyectos` (index.html)
- Scripts PDF y api/v1/projects.json actualizados
- 30 PDFs regenerados (5 tipos × 6 idiomas)
- Backup en `assets/backups/2026-05-21/`

### fix(sync): manual post-sync — buildDate + LangGraph 25/25 + grid + traducciones

- `index.html` `buildDate`: 2026-05-01 → 2026-05-21.
- Párrafo "Pilares Técnicos Consolidados" (6 idiomas): `10 backends LangGraph operativos` → `25 backends LangGraph operativos (cobertura 100%)`.
- Card "Stack & arquitectura" (6 idiomas): `LangGraph v4.2 / 25 casos / 10 backends operativos` → `LangGraph v4.14 / 25/25 backends operativos (cobertura 100%)`.
- Card "LangGraph · Agentic Resilience" (6 idiomas): descripción reescrita a `v4.14.0 · 25/25 backends operativos (cobertura 100%, casos 01–25)` con streaming NDJSON, DEMO/LIVE, OAuth2 opt-in, observabilidad LangSmith, /metrics, 8 capas de seguridad, cadena de custodia SHA-256.
- 3 cards nuevas (Claude Skills Toolkit · GabySQL · Python Data Science Program) **movidas dentro del `<div class="grid grid--2">`** (el script las había inyectado fuera, causando layout full-width). Traducciones limpias en los 6 idiomas, sin artefactos de emojis ni dobles espacios. Pills temáticos por proyecto.
- `CHANGELOG.md`: renombrado `### sync-portfolio (automático)` de 2026-04-13 a `### sync-portfolio (automático — 2026-04-13)` para resolver MD024 (duplicate heading).
- `assets/backups/2026-05-21/SESSION-REPORT-2026-05-21.md`: reporte detallado de la sesión.

Validación: `pnpm test` → 51 PASSED · 0 ERRORS; `pnpm run lint:md` → 0 error(s).

## 2026-05-01

### sync-portfolio — auditoría profunda + integración 18 días de avances

Cierre del gap entre 2026-04-13 (último sync con regeneración de assets) y hoy.
12 repos analizados (10 públicos + GitLab `proyectos-aws-gitlab` + portfolio).

**API JSON (api/v1/) — generated_at → 2026-05-01:**

- `projects.json`:
  - AWS: `cases_completed: 11 → 14`, añadido `cert_coverage` (SAA-C03 ~68% / DVA-C02 ~68% / SOA-C02 ~50%), tags +Bedrock +Claude Haiku 4.5 +TruffleHog +detect-secrets
  - LangGraph: `operational_cases: 4 → 10`, version v4.2.0, tags +LangSmith +OAuth2/OIDC +nginx TLS +grype +detect-secrets +Hardening 8 capas
  - Docker Labs: name v1.4 → v1.5, version v1.5.0, tag +Security Hardening
  - Social Bot Scheduler: name → v4.2, version v4.2.0, tags +Trivy +Hardened Runtime
  - Microsistemas: tags +TruffleHog +Trivy +Dependabot +SBOM +Security Hardening 3 fases
  - MCP + Ollama Local: tags +Bandit +pip-audit +Security & Trust Profile
  - ChofyAI Studio: name → Fase 4, version Fase 4, tags +Qwen3-TTS +FaceFusion +AceForge +uv +Disco dual +Empaquetado ad-hoc
  - Problem Driven Systems Lab: tags poblados (PHP 8.3, Python, Node.js, Docker, Prometheus, Grafana, MySQL, 12 casos OPERATIVOS, Observability, Performance), `operational_cases: 12`
  - python-data-science-bootcamp → "Python Data Science Bootcamp v1.1", version v1.1.0, tags poblados (Python, Jupyter Notebook, Data Science, 31 clases, Desktop Windows, Edge WebView2, Android Expo, Google Colab, Security Scan), `classes_count: 31`
- `experience.json` `recent_activity`: reescritura completa — 11 ítems con eventos de alto valor (AWS Caso I Bedrock + Caso O X-Ray, LangGraph v4.2 hardening 8 capas, Social Bot v4.2 Hardened, Docker Labs v1.5, Microsistemas v3.x SBOM, Bootcamp v1.1 31 clases + Desktop + Android, ChofyAI Fase 4, problem-driven 12 OPERATIVOS, MCP Ollama Trust Profile, portafolio i18n)
- `profile.json` `summary`: 11 → 14 casos AWS + GenAI Bedrock + 10 backends LangGraph + Hardening industrial (Trivy, TruffleHog, grype, SBOM, OIDC) + Prometheus/Grafana/X-Ray

**index.html cards × 6 idiomas:**

- LangGraph card (líneas 645–650): "8 backends operativos" → "v4.2.0 · 10 backends operativos (01,02,03,04,05,09,10,13,19,25) · auditoría 8 capas (non-root, 127.0.0.1, grype fail-build, nginx TLS, detect-secrets) · LangSmith · /metrics · OAuth2/OIDC opt-in"
- AWS card (líneas 611–616): "15 casos prácticos AWS (A–O) · gitleaks/tfsec/pre-commit hooks" → "14 completados (incluyendo GenAI Caso I: Bedrock + Claude Haiku 4.5 + Lambda + xray-sdk; Caso O: X-Ray distribuido), 1 proyectado (Caso M Resiliencia/Failover) · Cobertura ~68% SAA-C03 / ~68% DVA-C02 / ~50% SOA-C02 · TruffleHog + detect-secrets"
- `buildDate`: 2026-04-13 → 2026-05-01
- Hero tag (6 idiomas): "Abr 2026 / Apr 2026 / 2026年4月" → "May 2026 / Mai 2026 / Mag 2026 / 2026年5月"

**Scripts PDF:**

- `generate-portfolio.py` (5 idiomas afectados): "LangGraph + Ollama, 25 demos" → "LangGraph v4.2 + Ollama, 25 casos / 10 operativos, auditoría 8 capas, CI/CD hardened"
- `generate-all-languages.py`: subtítulos al día (sin cambios)
- 31 PDFs regenerados (5 tipos × 6 idiomas) por los 4 scripts

**Backups:** `assets/backups/2026-05-01/` — 31 PDFs respaldados antes de regenerar.

**Origen de hallazgos:** dry-run del script + auditoría profunda manual (READMEs vía gh api, GitLab vía API REST, comparación de literales numéricos en JSONs vs realidad).

## 2026-04-29 (2)

### feat: repos recientes — GitLab + forks count

- `app.js` `loadRecentRepos()`: fetch paralelo GitHub + GitLab API; normaliza datos; ordena por fecha; muestra top 12 combinados
- `app.js`: meta-línea actualizada a `★ stars · ⑂ forks · fecha`; badge GH/GL por repo
- `index.html` CSP: añadido `https://gitlab.com` a `connect-src`
- `index.html` repos section: descripción actualizada para mencionar ambas plataformas y los íconos ★/⑂

## 2026-04-29

### feat: integración rol Líder Tecnológico / Tech Lead

- `index.html`: título, meta description, og:title, og:description, twitter:title, twitter:description — añadido "Líder Tecnológico"
- `index.html` hero lead: rol expandido a "Arquitecto de Soluciones · Senior Full-Stack · Líder Tecnológico" en 6 idiomas
- `index.html` hero badges: nuevos pills "👔 Liderazgo Tecnológico" y "📋 Dirección Técnica"
- `index.html` recruiter card: añadido pill "Tech Lead" a identidad principal; párrafo multilingüe sobre rol de Tech Lead para reclutadores
- `index.html` roles#capa2: nueva article card "Líder Tecnológico / Tech Lead" con descripción y chips en 6 idiomas
- `index.html` roles#capa2b: nueva card "Qué tipo de liderazgo tecnológico ofrezco" (data-min-level=1) con 6 bullets en 6 idiomas
- `index.html` roles#capa3: eliminado pill "Tech Lead" (elevado a Capa 2)
- `index.html` roles#capa4: añadido bullet "Liderazgo tecnológico" en primera columna (ES+EN)
- `README.md`: nueva sección "Rol adicional: Líder Tecnológico / Tech Lead"

## 2026-04-13

### rank-repos — ranking automático de repositorios

- `scripts/rank-repos.py`: nuevo script de ranking exhaustivo (100 pts: docs/repro/calidad/obs/actividad/polyglot)
- `data/repo-scores.json`: cache incremental — solo re-analiza repos con pushed_at distinto al cache
- `.agents/skills/sync-portfolio/SKILL.md`: documentación completa del script (criterios, flags, limitación de pinning)
- Ranking actual (top 6 para pinning manual): docker-labs(91) > python-data-science-bootcamp(81) = social-bot-scheduler(81) > mcp-ollama-local(80) > langgraph-realworld(78) > microsistemas(76)
- Limitación documentada: GitHub no expone API pública de pinning; guía de 4 pasos incluida en output del script

### sync-portfolio (automático — 2026-04-13)

- `api/v1/`: generated_at → 2026-04-13
- Repos nuevos integrados: problem-driven-systems-lab, python-data-science-bootcamp
- Cards HTML agregados en `#proyectos` (index.html)
- Scripts PDF y api/v1/projects.json actualizados
- 30 PDFs regenerados (5 tipos × 6 idiomas)
- Backup en `assets/backups/2026-04-13/`

### app.js — forks en Repos recientes

- `app.js`: eliminado filtro `!r.fork` en `loadRecentRepos()` — los forks ahora aparecen en la sección "Repos recientes (auto)"
- Badge visual `⑂ fork` agregado al `repo__meta` para identificar forks
- Slice ampliado de 8 → 10 repos para acomodar mayor volumen

## 2026-04-07

### CV por solicitud — Instructor de Programación y Pensamiento Computacional

- `assets/no_aplica/cv-capacitaciones.pdf`: CV en español, formato visual (no ATS), 2 páginas
  - Generado con `scripts/generate-cv-capacitaciones.py`
  - Responde a solicitud de Ana Matus de la Parra (SkillNest, <amatusdelaparra@skillnest.com>, 08-abr-2026)
  - Incluye: 445+ hrs de relatorías (Centro Europeo 2003–2004, E-syste 2011), proyecto titulación nota 6.7, 14 años plataforma educativa, formación completa
  - NO incluye: RUT, domicilio, pretensión de sueldo, estado civil, fecha de nacimiento
  - En `no_aplica` — no publicar en API ni en assets públicos

### Ampliación de alcance profesional — Instructor de Programación

- `index.html`: nueva card en Capa 2 "Expansión natural" para "Instructor de Programación y Pensamiento Computacional" (6 idiomas)
  - Respaldada por 445+ horas de relatorías reales (Centro Europeo 2003–2004, E-syste 2011)
  - Titulación UTA (nota 6.7): entorno educativo web para niños con Síndrome de Down
- `api/v1/experience.json`: agregadas 2 entradas de Relator Técnico (Centro Europeo 2003–2004 y E-syste 2011) extraídas desde `assets/no_aplica/cv-completo.pdf`

## 2026-04-03

### sync-portfolio (automático) — sesión 2

- Descripciones de proyectos actualizadas en `index.html`, `generate-all-languages.py` y `generate-portfolio.py` (6 idiomas)
- LangGraph: incorpora "Docker por caso" y "CI en GitHub Actions" en todas las variantes
- `api/v1/projects.json`: 8 descripciones sincronizadas desde GitHub
- `scripts/sync-portfolio.py`: agrega detección de cambios en repos existentes (`detect_updated_repos`)
- 30 PDFs regenerados (5 tipos × 6 idiomas)

### sync-portfolio (automático) — sesión 1

- `api/v1/`: generated_at → 2026-04-03
- 30 PDFs regenerados (5 tipos × 6 idiomas)
- Backup en `assets/backups/2026-04-03/`

## 2026-04-03 — Expansión multilingüe

### Expansión multilingüe completa (PT/IT/FR/ZH)

- `index.html`: soporte de 6 idiomas (ES/EN/PT/IT/FR/ZH) en todas las secciones:
  hero, resultados, evolución, proyectos, demos, experiencia, flujo-IA,
  alcance/roles, servicios, descargas, referencias y contacto.
- `styles.css`: sistema de visibilidad CSS extendido a 6 idiomas con reglas
  `display: revert` y `display: block` para elementos en línea y de bloque.
- `app.js`: `resolveLocalizedPdfHref` actualizado — PT/IT usan PDFs en español,
  FR/ZH usan PDFs en inglés.

### Sincronización API v1

- `api/v1/profile.json`: `label` actualizado a "Arquitecto de Soluciones |
  Senior Full-Stack | Modernización Legacy, Automatización e Integración de IA
  Aplicada". `summary` ampliado con los 6 idiomas y repos 2026.
- `api/v1/projects.json`: agregados `unikernel-labs` (PUBLIC) y
  `chofyai-studio` (PUBLIC). Repos privados excluidos.
- Todos los `api/v1/*.json`: `generated_at` actualizado a `2026-04-03`.

## 2026-03-22

### Detección automática de idioma del navegador

- `app.js`: en la primera visita sin preferencia guardada, el idioma se
  detecta automáticamente desde `navigator.language`. Si el idioma del
  navegador está entre los 6 soportados (ES/EN/PT/IT/FR/ZH) se aplica
  directamente; si no, se usa español por defecto. La preferencia manual
  del usuario siempre prevalece (localStorage).

### Skills nuevos — automatización del portafolio

- `build-deploy-zip`: skill + `scripts/build-zip.py` — genera
  `portfolio-bundle-YYYY-MM-DD.zip` con todos los archivos web públicos
  (HTML/CSS/JS, 31 PDFs en 6 idiomas, 6 JSONs api/v1, icons,
  experiencia-3d). Excluye backups, no_aplica, node_modules y archivos
  de desarrollo. Incluye flag `--output` para nombre personalizado.
- `md-lint-fix`: skill + `scripts/fix-md-lint.py` — detecta archivos
  `.md` modificados según git, auto-corrige MD040 (infiere lenguaje del
  bloque por contexto: bash/python/json/yaml/hcl/html/sql/text), aplica
  `markdownlint-cli2 --fix` para MD031/MD032/MD034/MD028, reporta lo que
  requiere intervención manual. Resuelve el patrón recurrente de 15+
  commits de corrección lint en el historial.
- `.gitignore`: `portfolio-bundle-*.zip` excluido del repositorio.

### READMEs de perfil GitHub y GitLab actualizados

- Estructura de roles reorganizada en 3 capas: Identidad principal /
  Expansión natural / Alcance complementario — alineada con el sitio web.
- Nueva sección "Flujo de desarrollo asistido por IA" con tabla de
  herramientas (Claude Code, ChatGPT Plus, Codex, Antigravity, VS Code).
- GitLab: eliminada subsección "Completados y Validados" — todos los
  casos bajo "Completados" en orden secuencial (A→L). Eliminado el
  término (VALIDADO) del monorepo `proyectos-aws-gitlab`.

### Documentación actualizada

- `README.md`: tabla de skills actualizada con `build-deploy-zip` y
  `md-lint-fix`; arquitectura actualizada con `build-zip.py` y
  `fix-md-lint.py`; referencia al ZIP de despliegue.
- `CLAUDE.md`: registrados ambos skills y comando de generación de ZIP.
- `llm.txt`: sección de automatización añadida; fecha actualizada a 2026-03-22.

## 2026-03-19

### Sistema de 6 idiomas — PDFs completos

- Ampliado el sistema de idiomas de ES/EN a **ES/EN/PT/IT/FR/ZH** en toda la web y en todos los documentos.
- Generados 30+ PDFs vía pipeline Python/reportlab: CVs (reclutador + ATS), portafolio, carta de recomendación, declaración de logros — en las 6 variantes.
- Nuevos scripts de generación: `scripts/generate-recommendation-letter.py`, `scripts/generate-achievements-statement.py`, `scripts/generate-portfolio.py`.
- Actualizado `scripts/generate-all-languages.py` con labels traducidos y URLs multilingüe.
- Actualizado `scripts/generate-unified-cv.py`: estilo `link` en el CV reclutador + sección de enlaces a declaración de logros y carta de recomendación, con URLs específicas por idioma, entre PROYECTOS DESTACADOS y FORMACIÓN.

### Enlace dinámico de PDFs en la web

- `app.js`: función `resolveLocalizedPdfHref()` simplificada para resolver 6 idiomas vía `data-pdf-{lang}`.
- `index.html`: atributos `data-pdf-pt/it/fr/zh` añadidos a todos los links de descarga (CV reclutador, CV ATS, carta de recomendación, declaración de logros, portafolio).

### API v1 actualizada

- `api/v1/artifacts.json`: 5 documentos con 6 variantes de idioma cada uno (30 URLs).
- `api/v1/meta.json`: capacidades multilingüe y mapa de sufijos documentados.
- `api/v1/profile.json`, `experience.json`, `projects.json`, `skills.json`: actualizados para reflejar estado real del ecosistema (16 años experiencia, 15 casos AWS, polyglot persistence, agentes IA).

### Documentación

- `README.md`: actualizado a 6 idiomas, nueva sección de scripts, skills system y estado real del ecosistema.
- `cv-data-api.md`: tabla de PDFs expandida a 6 idiomas.
- `llm.txt`: identidad, tech stack y artefactos actualizados a estado 2026-03-19.
- `CLAUDE.md`: creado como fuente de verdad del proyecto (arquitectura, protocolo de backups, ecosistema de repos, reglas).

## 2026-03-11

- Fixed HTML lint coverage so the validation step targets real site files.
- Improved `scripts/build.js` to use local CLI binaries, making CSS and JS minification work in Windows environments where `npx` via PowerShell can fail.
- Expanded the build output to include `llm.txt`, `api/v1/` and `experiencia-3d/` so `dist/` matches the public site more closely.
- Corrected the API manual to distinguish SEO generation from versioned JSON data maintenance.
