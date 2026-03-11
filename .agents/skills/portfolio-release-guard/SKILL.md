---
name: portfolio-release-guard
description: >
  Ejecuta una verificación previa a publicación para el portafolio: lint,
  build, integridad de `dist/`, artefactos públicos clave y rutas críticas de
  PWA/API. Úsalo antes de hacer commit/push, preparar releases o cuando el
  usuario pida confirmar que nada se rompió.
---

# Skill: Portfolio Release Guard

Validar cambios de bajo riesgo antes de publicar.

## Flujo

1. Ejecutar `npm.cmd run lint` y `npm.cmd run build` en Windows; usar `npm run ...` en shells Unix.
2. Verificar que `dist/` contenga al menos `index.html`, `styles.css`, `app.js`, `assets/`, `api/v1/`, `llm.txt`, `manifest.webmanifest`, `service-worker.js` y `offline.html`.
3. Confirmar que el build no dependa de fallbacks silenciosos; si los hay, explicarlos.
4. Revisar `git diff --cached --stat` antes de commitear.
5. Confirmar push solo después de validación local exitosa.

## Casos que debe detectar

- Lint mal apuntado o que no cubre archivos reales.
- Build que pasa pero omite assets o endpoints públicos.
- Errores de rutas en PWA, APK, SEO o experiencia 3D.
- Diferencias entre lo validado y lo que realmente se va a subir.

## Entrega esperada

Cerrar con estado de validación, comandos ejecutados y cualquier excepción aceptada conscientemente.
