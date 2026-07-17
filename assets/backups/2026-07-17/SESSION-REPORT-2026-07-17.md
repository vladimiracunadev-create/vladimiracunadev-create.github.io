# Reporte de Sesión — 2026-07-17

**Commits generados:** 2 (auto-sync `0aa0a3d` + curaduría manual)
**Rango de commits:** `0aa0a3d` → (commit de cierre de esta sesión)

## Resumen ejecutivo

Sincronización completa del portafolio tras ~1 mes de congelamiento (último push del sitio: 2026-06-20). Se auditaron los 22 repos públicos de GitHub leyendo sus READMEs reales (no solo la descripción corta) + estado del monorepo GitLab. Se integraron 7 repos nuevos, se corrigió drift de versiones en 6 repos existentes, se derogó la regla histórica "RootCause oculto", se limpió la referencia rota a `rootcause-landing` (404), y se regeneraron los 30 PDFs con backup previo.

## Cambios por archivo — detalle estricto

### scripts/sync-portfolio.py

- `HIDDEN_REPOS`: `{"rootcause-windows-inspector", "rootcause-landing"}` → `{"rootcause-landing"}`.
- Motivo: rootcause-windows-inspector es público desde 2026-06-20 (CLAUDE.md regla 9 derogada); rootcause-landing fue eliminado de GitHub (404).

### scripts/rank-repos.py

- `EXCLUDED`: retirado `rootcause-windows-inspector` (ahora entra al ranking); `rootcause-landing` conservado con nota de repo eliminado.

### .agents/skills/sync-portfolio/SKILL.md

- Regla 9: "RootCause permanentemente oculto" → "RootCause PÚBLICO desde 2026-06-20; rootcause-landing eliminado (404), nunca referenciar".
- Contexto de repos ocultos y lista de exclusión del ranking actualizados en consecuencia.

### api/v1/projects.json (+ los 6 JSONs con generated_at → 2026-07-17)

- Cloud/AWS: `cases_completed` 14 → 16, `cases_total` 15 → 16.
- Social Bot Scheduler: nombre v4.3.1 → v4.9.1; `version` v4.3.1 → v4.9.1; +`cases_operational: 19`, +`db_engines: "18+"`; tags +pnpm, +Dependabot.
- Unikernel Labs: nombre → v2.0.0; `version` v1 → v2.0.0; descripción "Docker Desktop para unikernels"; +tags Installer .exe / Hardened local API.
- claude-skills-toolkit: +`version: v0.2.0`, `skills_count` 7 → 10.
- RootCause Windows Inspector: nombre v0.11.0 → v0.19.0; `version` v0.11.0 → v0.19.0; retirado `landing_repo`; +tags Tray icon / Scoop·Winget·Chocolatey / Baseline anomaly detection / Bilingüe ES/EN.
- Automa PC: nombre v0.2.1 → v0.3.0; `version` v0.2.1 → v0.3.0; `flows_count` 20 → 27; `tests_count` 115 → 150; +tags Chromium headless / Web monitoring SHA-256.
- LangGraph: descripción actualizada a v4.15.0 (hardening adversarial).
- +7 entradas nuevas (rootcause-mobile-inspector, modern-gamedev-program, modern-cybersecurity-program, machine-operator-program, rhino-suite, human-genome-labs, wsl-labs).

### index.html

- `#productos` (cards nivel 0): RootCause v0.11.0 → v0.19.0 (+reposicionamiento forense ciberseguridad, CLI Portable .zip, 19+ releases); Automa v0.2.1 → v0.3.0 (27 flows, 150 tests); Unikernel v1.0.0 → v2.0.0; ChofyAI, Docker Labs, Microsistemas, GabySQL verificados; enlaces de descarga corregidos a assets reales de cada release.
- `#proyectos` (cards nivel 1-2): AWS 14→16 casos (6 idiomas); Social Bot v4.9.1 (6 idiomas); Unikernel v2.0.0 (6 idiomas); ChofyAI v0.5.1 (6 idiomas); LangGraph verificado; GabySQL reposicionado a proyecto de investigación; Claude Skills 10 skills.
- 7 cards nuevas curadas con las 6 traducciones reales (ES/EN/PT/IT/FR/ZH), títulos y tags limpios, `data-min-level` correcto (machine-operator → nivel 2 por ser WIP documental).
- Fix estructural: card Human Genome Labs tenía span `data-it` truncado y faltaban `data-fr`/`data-zh` → completadas.
- `buildDate`: 2026-06-19 → 2026-07-17.
- Hero tag: "Nuevo · May 2026" → "Nuevo · Jul 2026" (6 idiomas).

### CHANGELOG.md

- Entrada 2026-07-17 expandida de 4 bullets a detalle completo de auditoría + curaduría.

### scripts/generate-cv-capacitaciones.py (nuevo)

- CV de instructor/relator de programación → `assets/no_aplica/cv-capacitaciones.pdf`. Añadido al repo.

## PDFs — estado final

| Documento | Variantes | Estado |
|---|---|---|
| CV Reclutador | ×6 | Regenerado |
| CV ATS | ×6 | Regenerado |
| Portafolio | ×6 | Regenerado |
| Declaración de Logros | ×6 | Regenerado |
| Carta de Recomendación | ×6 | Regenerado |

Backup previo: `assets/backups/2026-07-17/` (30 PDFs). Spot-check `portafolio.pdf`: 0 caracteres de reemplazo (sin puntos negros), repos nuevos presentes.

## Errores encontrados y resueltos

| Error | Causa | Fix |
|---|---|---|
| `detect_stale_projects` marcaba rootcause-windows-inspector como inexistente | El repo estaba en `HIDDEN_REPOS`, no se consultaba | Retirado de HIDDEN_REPOS; ahora se sincroniza normal |
| Referencia rota `landing_repo` → rootcause-landing | Repo eliminado de GitHub (404) | Campo retirado de projects.json |
| Card Human Genome Labs con HTML roto | Span `data-it` truncado, faltaban FR/ZH | Completadas las 6 traducciones |

## Validación final

- npm test: **51 PASSED · 0 ERRORS** (5 warnings preexistentes: gap bilingüe 5.1% idéntico en HEAD, rel=noopener).
- npx markdownlint-cli2: **0 error(s)**.
- Perfil GitHub README: verificado ya al día (footer 2026-07-16, sin versiones stale).
- git push: pendiente de commit de cierre.
- GitHub Pages: desplegará en ~1–2 min tras push (Ctrl+F5 para forzar recarga sin caché).
