# Changelog

## 2026-04-03

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
