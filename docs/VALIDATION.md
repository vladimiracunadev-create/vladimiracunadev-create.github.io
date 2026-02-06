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
4. **SEO**: Metaetiquetas, títulos, robots.txt.

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
