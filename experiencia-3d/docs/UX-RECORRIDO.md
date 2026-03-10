# UX - Recorrido

## El Problema del WebGL en Portafolios

El problema de dejar al usuario "libre" con un OrbitControls o PointerLock Controls es que típicamente se pierden, se marean o no pueden leer la información en perspectivas sesgadas.

## Solución: Puntos Panorámicos Fijos y Overlays HTML

1. **Guiado, no sandbox**: Hemos limitado la cámara a 4 posiciones (`waypoints`).
2. **Html Text**: Al mezclar HTML normal sobre un canvas 3D evitamos problemas de aliasing, accesibilidad, y resolución típica de la textura SDF font para textos en 3D puro. Cualquier lector de pantallas sabrá qué texto hay en el portafolio inmersivo, y es 100% legible y responsivo en móviles.
3. **Flujo Causal**: Avanzas solo hacia el frente, simulando un avance metafórico por la carrera profesional.
