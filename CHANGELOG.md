# Changelog

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
