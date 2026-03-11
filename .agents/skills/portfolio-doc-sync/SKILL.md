---
name: portfolio-doc-sync
description: >
  Sincroniza README, documentación técnica, wiki y manuales del portafolio para
  reflejar cambios reales de arquitectura, build, CV Data API, mobile o skills.
  Úsalo cuando el código o contenido cambie y haya que alinear la narrativa del
  proyecto sin rehacer toda la actualización integral.
---

# Skill: Portfolio Doc Sync

Actualizar documentación sin perder consistencia entre audiencias técnicas, reclutamiento y wiki.

## Flujo

1. Identificar qué cambió en código, assets, API o build.
2. Actualizar primero `README.md` y luego los manuales afectados en `docs/`.
3. Reflejar los cambios equivalentes en `docs/wiki/` cuando exista mirror.
4. Mantener links funcionales, tablas coherentes y ejemplos ejecutables.

## Archivos habituales

- `README.md`
- `cv-data-api.md`
- `docs/BUILD_GUIDE.md`
- `docs/VALIDATION.md`
- `docs/TECHNICAL_RATIONAL.md`
- `docs/RECRUITER.md`
- `docs/wiki/Home.md`
- `docs/wiki/_Sidebar.md`

## Reglas

- No prometer automatizaciones o archivos que no existan.
- Corregir primero comandos rotos y enlaces inválidos.
- Mantener el tono del repo: claro, técnico y orientado a producto.
- Si hay duplicación entre docs y wiki, actualizar ambas en el mismo cambio.
