# Changelog

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

### sync-portfolio (automático)

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
