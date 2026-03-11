# Guia de Instalacion y Despliegue

Este proyecto puede ejecutarse como sitio estatico, PWA y contenedor movil via Capacitor.

## Requisitos

- Node.js 20 o compatible
- Dependencias instaladas con `npm install`

## Desarrollo local

```bash
npm install
npm run build
```

Para probar la PWA o el Service Worker, sirve la carpeta raiz con un servidor estatico local.

## Validaciones

```bash
npm run lint
npm run build
```

## Despliegue web

- GitHub Pages publica el contenido commiteado en la rama principal.
- Los artefactos publicos clave viven en la raiz, `assets/`, `api/v1/` y `experiencia-3d/`.
- El directorio `dist/` queda disponible para validaciones o previews locales.

## Mobile

La base movil esta en [`apps/mobile/`](./apps/mobile/) y la guia detallada esta en [`docs/GUIA_MAESTRA_MOBILE.md`](./docs/GUIA_MAESTRA_MOBILE.md).
