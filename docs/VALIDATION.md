# Guía de Validación Local

Este proyecto utiliza **Lighthouse CI** para asegurar calidad, accesibilidad y performance.

## Requisitos Previos

- Node.js instalado.
- Dependencias instaladas: `npm install`.

## Comandos de Validación

Para ejecutar la auditoría completa, usa:

```sh
npm run build
npm run lhci
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
