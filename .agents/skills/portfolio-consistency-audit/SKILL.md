---
name: portfolio-consistency-audit
description: >
  Audita consistencia entre el sitio, la CV Data API, la documentación, los
  archivos SEO/LLM y los artefactos públicos. Úsalo cuando el usuario pida
  revisar coherencia, detectar desalineaciones, verificar fechas, enlaces,
  claims o fuentes duplicadas antes de publicar cambios.
---

# Skill: Portfolio Consistency Audit

Auditar el repositorio cuando el objetivo sea detectar deriva entre superficies públicas.

## Flujo

1. Comparar `index.html`, `api/v1/*.json`, `data/resume.json`, `README.md`, `docs/`, `docs/wiki/`, `llm.txt`, `robots.txt` y `sitemap.xml`.
2. Revisar fechas visibles y metadatos (`generated_at`, `buildDate`, `Last Updated`, changelog).
3. Buscar archivos referenciados que no existan y archivos públicos que no estén documentados.
4. Reportar contradicciones primero; resumir fortalezas después.

## Focos de revisión

- URLs y nombres de PDFs en `assets/` vs `api/v1/artifacts.json` vs `index.html`.
- Endpoints listados en README/wiki/manuales vs archivos reales en `api/v1/`.
- Claims de stack, experiencia y fechas entre sitio, API y docs.
- Existencia de archivos enlazados como `INSTALL.md`, `CHANGELOG.md` o guías del wiki.
- Coherencia entre `robots.txt`, `sitemap.xml` y `llm.txt`.

## Entrega esperada

Entregar hallazgos priorizados con archivo afectado y corrección sugerida. Si no hay problemas, decirlo explícitamente y mencionar riesgos residuales.
