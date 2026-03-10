# Arquitectura de la Experiencia 3D

## Filosofía

La arquitectura sigue el mismo principio **KISS (Keep It Simple, Stupid)** del portafolio raíz:

1. **Sin Build Tool Invasiva**: No hay Vite, Webpack ni dependencias NPM complejas, para que pueda servirse 100% como un sistema de archivos `file://` o en GitHub Pages puro.
2. **Modulos ES**: Se usa `<script type="importmap">` para resolver Three.js directamente desde un CDN robusto (`unpkg`), lo que permite el uso de `import` y `export` del ES6 limpio y moderno.

## Estructura de Módulos (Separación de Responsabilidades)

- `main.js`: Setup general, inyección del Canvas DOM y Resize handler.
- `scene.js`: Manejo puramente visual. Solo contiene geometría paramétrica, parámetros de luz y texturas generadas proceduralmente (nada de texturas jpg/png externas que suban el payload).
- `camera-path.js`: Control de la cámara. Expone lógica de interpolación suave (LERP) entre waypoints. Se restringe el movimiento libre para evitar que el usuario se pierda o colisione contra mallas (Problema común de experiencia de usuario en webs WebGL no orientativas).
- `ui-navigation.js`: Lógica del DOM normal (overlay). Engancha eventos click de botones HTML convencionales a la cámara.

## Fallback Graceful

El sistema valida la existencia de WebGL. Si el driver WebGL del cliente falla o está desactivado, el preloader de capa negra jamás se borra y muta a un mensaje de error explícito con un botón de retorno al portafolio estático normal.
