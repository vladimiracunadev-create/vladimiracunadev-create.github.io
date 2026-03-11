---
name: portfolio-mobile-wrapper-check
description: >
  Revisa la salud del wrapper móvil del portafolio basado en Capacitor,
  verificando sincronía entre web root, assets, manifest, Android/iOS y la
  documentación mobile. Úsalo cuando cambie el sitio web, la PWA, los assets de
  app o el usuario pida validar la salida móvil sin tocar la lógica principal.
---

# Skill: Portfolio Mobile Wrapper Check

Validar que la capa móvil siga alineada con el núcleo web.

## Flujo

1. Revisar `apps/mobile/`, `capacitor.config.ts`, Android e iOS para detectar rutas o assets desactualizados.
2. Confirmar que la PWA y el sitio sigan exponiendo los recursos que el wrapper consume.
3. Verificar que iconos, splash, package metadata y documentación mobile sigan vigentes.
4. Reportar incompatibilidades antes de intentar builds nativos.

## Focos de revisión

- `apps/mobile/package.json`
- `apps/mobile/capacitor.config.ts`
- `apps/mobile/android/`
- `apps/mobile/ios/`
- `manifest.webmanifest`
- `assets/icons/`
- `docs/GUIA_MAESTRA_MOBILE.md`
- `docs/IOS_TROUBLESHOOTING.md`

## Entrega esperada

Entregar compatibilidad observada, riesgos de desalineación y pasos siguientes mínimos para Android/iOS.
