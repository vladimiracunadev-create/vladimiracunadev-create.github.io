# Experiencia 3D - Galería Inmersiva

Esta carpeta contiene una experiencia 3D complementaria e inmersiva para el portafolio de Vladimir Acuña. Se diseñó respetando rígidamente la filosofía estática, la modularidad y el rendimiento general del repositorio principal.

> [!NOTE]
> **Estado de Producción:** Este módulo se mantiene bajo control de versiones como una demostración viva de arquitectura WebGL, matemáticas 3D y rendimiento (Three.js puro sin dependencias de build). Sin embargo, el **botón de acceso público en la UI principal está actualmente desactivado**. Esta decisión intencional busca no agregar fricción ni tiempos de recorrido innecesarios al flujo de lectura rápido y optimizado esperado por los reclutadores de TI.

## ¿Qué es?

Es una "sala de exposición" tipo galería profesional o showroom, que usa **Three.js** para proyectar un entorno 3D navegable con cámara controlada (pasillo guiado), donde los paneles 3D muestran información clave extraída directamente o sintetizada del CV y portafolio principal.

## Estructura

Toda la lógica, estilos y vistas de la experiencia están aisladas dentro de esta carpeta (`/experiencia-3d/`).

- `index.html`: Punto de entrada único. Carga el `<canvas>` y los `#overlays` de UI.
- `css/`: Estilos propios de la UI inmersiva. No interfiere con el `styles.css` del home.
- `js/`: Lógica separada por responsabilidades (cámara, escena, interacciones).
- `docs/`: Documentación arquitectónica de la experiencia 3D.

## Ejecución Local

Al ser código estático puro basado en Import Maps (`<script type="importmap">`), se puede servir localmente junto con la raíz usando cualquier servidor HTTP:

```bash
cd ..
npx http-server .
```

Y luego acceder a `localhost:8080/experiencia-3d/`

## Restricciones

- No utilizar modelos pesados salvo que estén ultra optimizados (ej. GLTF draco).
- Mantener compatibilidad con *fallback* HTML en caso de que WebGL falle en el navegador del cliente.
