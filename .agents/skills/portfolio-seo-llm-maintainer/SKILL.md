---
name: portfolio-seo-llm-maintainer
description: >
  Mantiene la capa de descubrimiento orgánico y para asistentes de IA del
  portafolio: `llm.txt`, `robots.txt`, `sitemap.xml`, metadatos HTML y claims
  de discoverability. Úsalo cuando cambie contenido público, rutas, stack,
  fecha de actualización o estrategia SEO/LLM.
---

# Skill: Portfolio SEO and LLM Maintainer

Mantener coherentes los archivos que ayudan a buscadores y asistentes a entender el sitio.

## Flujo

1. Revisar `index.html` para metadescripción, título, CSP y enlaces canónicos relevantes.
2. Regenerar `sitemap.xml` y `robots.txt` con `node scripts/generate-seo.js` cuando cambien rutas públicas.
3. Actualizar `llm.txt` si cambian stack, propósito, superficies públicas o fecha.
4. Confirmar que README y docs no contradigan la capa SEO/LLM.

## Checklist rápido

- `robots.txt` apunta al sitemap correcto.
- `sitemap.xml` incluye páginas HTML públicas relevantes.
- `llm.txt` describe el sitio actual, no una versión anterior.
- Los enlaces a `llm.txt` y archivos SEO existen desde el sitio y la documentación.

## Entrega esperada

Resumir qué archivos SEO/LLM se tocaron, por qué y qué impacto público tienen.
