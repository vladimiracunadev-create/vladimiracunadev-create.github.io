# Guía de Validación Local

**Última ejecución integral:** 2026-10-01.

Este proyecto utiliza **Lighthouse CI** para asegurar calidad, accesibilidad y performance.

## Requisitos Previos

- Node.js 22, igual que en CI.
- pnpm 11, fijado mediante `packageManager` en `package.json`.
- Dependencias instaladas con `pnpm install --frozen-lockfile`.

## Comandos de Validación

Para ejecutar la auditoría completa, usa:

```bash
pnpm build
pnpm lhci
```

### ¿Qué evalúa?

1. **Performance**: Carga inicial, peso de recursos.
2. **Accesibilidad**: Etiquetas ARIA, contraste, nombres de enlaces.
3. **Best Practices**: HTTPS, CSP, sin errores en consola.
4. **SEO**: Metaetiquetas, títulos, `robots.txt`, `sitemap.xml`, `llm.txt`.

## Sanidad PWA

El `service-worker` usa una estrategia híbrida para evitar que cambios visibles del sitio queden "pegados" en caché:

- **`network-first`** para navegación y archivos de shell (`index.html`, `styles.css`, `app.js`, `pwa.js`, `manifest.webmanifest`).
- **`cache-first`** para assets estáticos más estables.
- **Invalidación por versión** mediante `CACHE_NAME` y versión en `pwa.js` cuando hay cambios importantes de entrega.

Si un cambio visual no aparece tras publicar, revisar primero:

```text
service-worker.js
pwa.js
CACHE_NAME
```

La política del proyecto es priorizar que la home se actualice correctamente antes que mantener una caché agresiva del shell principal.

## Coherencia y codificación

- `python scripts/mojibake_probe.py .` detecta degradación UTF-8 mediante un round-trip conservador; `--fix` repara solo cuando reduce marcadores de mojibake.
- Las fechas de `api/v1/*.json`, `data/resume.json`, `index.html`, `llm.txt` y `sitemap.xml` se contrastan con la sincronización vigente.
- Los valores históricos del `CHANGELOG.md` se preservan; solo se actualizan marcadores de estado actual.

## Control de PDFs

- El pipeline debe producir 36 PDFs públicos: 6 familias por 6 idiomas.
- `node scripts/check-pdf.js` valida estructura básica y `pdfinfo` confirma que todos los archivos se abren.
- Las páginas se renderizan a PNG para revisar tipografía, márgenes, saltos y enlaces visibles antes de publicar.

## Política de Seguridad (CSP)

El sitio implementa una **Content Security Policy (CSP)** estricta en `index.html`:

- **Sin `unsafe-inline`**: No se permite JS/CSS en línea.
- **Fuentes permitidas**: Solo Google Fonts.
- **Conexiones**: Solo a la API de GitHub.
- **Objetos**: `object-src 'none'` (bloquea Flash/plugins).
- **Base URI**: `base-uri 'self'` (evita secuestro de URLs relativas).

Si necesitas agregar scripts externos, debes listarlos explícitamente en el `<meta http-equiv="Content-Security-Policy">`.

---

[← Volver al README](../README.md) | **Vladimir Acuña** - Senior Software Engineer
