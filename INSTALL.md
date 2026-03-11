# Guía de Instalación y Despliegue

Este proyecto puede ejecutarse como sitio estático, PWA y contenedor móvil vía Capacitor.

## Requisitos

- Node.js 20 o compatible
- Dependencias instaladas con `npm install`

## Desarrollo local

```bash
npm install
npm run build
```

Para probar la PWA o el Service Worker, sirve la carpeta raíz con un servidor estático local.

## Validaciones

```bash
npm run lint
npm run build
```

## Despliegue web

- GitHub Pages publica el contenido commiteado en la rama principal.
- Los artefactos públicos clave viven en la raíz, `assets/`, `api/v1/` y `experiencia-3d/`.
- El directorio `dist/` queda disponible para validaciones o previews locales.

## Mobile

La base móvil está en [`apps/mobile/`](./apps/mobile/) y la guía detallada está en [`docs/GUIA_MAESTRA_MOBILE.md`](./docs/GUIA_MAESTRA_MOBILE.md).
