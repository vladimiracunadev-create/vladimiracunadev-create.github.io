# Rendimiento y Optimización WebGL

## Sin modelos glb/gltf pesados

La escena es 100% **procedural** utilizando BoxGeometry, PlaneGeometry y PointsMaterial de primitivas Three.js construidas en buffer (Float32Array).

- Al no hacer requests `.glb` gigantes ahorramos MB de carga de assets.
- Las texturas de los materiales son colores puros combinados con propiedades PBR (StandardMaterial) computadas por luz local sin mapeos HDR inmensos (EnvMaps).

## Limitación del Device Pixel Ratio

Restringimos la resolución para que en displays Retina o QHD no sature la tarjeta de video renderizando más allá del doble nativo para un frame: `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))`. Emplea un render pass a resolución controlable.

## Animación Eficiente

No hay simulaciones físicas (Cannon.js / Ammo.js) requiriendo updates de ticks fijos.

## Lazy Load o Dependencia del CDN Módulo

`import * as THREE from 'unpkg/three@.../three.module.js'` se encarga del cache de navegador nativamente a través de las cabeceras del CDN.
