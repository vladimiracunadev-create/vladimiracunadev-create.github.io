# 🧠 Racional Técnico: ¿Por qué Vanilla?

En una era de frameworks masivos, este proyecto elige deliberadamente volver a las bases. Aquí explicamos el "porqué" detrás de nuestras decisiones de arquitectura.

## 🏗 La Filosofía KISS (Keep It Simple, Stupid)

### El Problema de la Sobre-Ingeniería

Muchos desarrolladores utilizan React, Vue o Next.js para sitios web que son esencialmente estáticos (como un portafolio). Esto introduce:

- **Dependencias masivas** (`node_modules` de cientos de MB).
- **Tiempos de compilación**.
- **JavaScript adicional** que el navegador debe procesar solo para mostrar texto e imágenes.

### Nuestra Solución: Vanilla Web Stack

Hemos elegido **HTML, CSS y JS puro** porque:

1. **Rendimiento Imbatible**: Carga instantánea. El navegador no necesita descargar una librería de 100KB antes de empezar a renderizar.
2. **Sostenibilidad**: El código escrito hoy funcionará en 10 años sin necesidad de actualizar 50 paquetes de `npm`.
3. **Control Total**: Cada píxel y cada línea de lógica están bajo nuestro control directo, sin abstracciones innecesarias.

## 🛠 Decisiones Técnicas Clave

### Internationalization (i18n) de Alto Rendimiento

A diferencia de librerías pesadas, implementamos una **Visibilidad Pasiva** mediante atributos `data-es` y `data-en`. El CSS solo oculta lo inactivo, permitiendo que el navegador renderice instantáneamente sin ejecuciones costosas de JS ni recargas de página.

### Temas Dinámicos Reales (Dark/Light)

Implementamos el sistema de temas usando variables CSS globales y atributos de data en el `body`. Esto garantiza que la transición de colores sea suave, respete la vista del usuario y tenga impacto cero en el rendimiento a largo plazo.

### Lógica Asíncrona Robusta

Usamos `async/await` con patrones de manejo de fallos para cargar datos de APIs externas (GitHub). El payload total de JS es inferior a 15kb, logrando una interactividad inmediata.

### Automatización vs. Runtime

Automatizamos el **Build** (minificación de CSS/JS, generación de Sitemap) usando Node.js, pero el **Runtime** (lo que corre en el navegador del usuario) es 100% puro. Esto combina lo mejor de ambos mundos: herramientas modernas de desarrollo con una ejecución ligera para el usuario.

### LLM Discoverability (llm.txt)

Con la adopción masiva de asistentes de IA que razonan sobre el contenido web, este proyecto implementa el estándar emergente **[llmstxt.org](https://llmstxt.org)**:

- **`llm.txt`** en la raíz del sitio: provee contexto semántico legible por máquinas (tecnología, propósito, permisos de indexación).
- **`robots.txt` actualizado**: referencia explícita a `llm.txt` para que los crawlers de IA lo descubran automáticamente.
- **Deploy garantizado**: los tres archivos SEO (`robots.txt`, `sitemap.xml`, `llm.txt`) son commiteados directamente en la raíz del repositorio, eliminando el riesgo de que el build los omita.

## 📱 Diseño Responsivo y Portabilidad

Este proyecto ha sido diseñado para funcionar en cualquier lugar:

1. **Mobile First / Fluid**: El CSS utiliza Flexbox y Grid con media queries estratégicas para asegurar que la experiencia sea fluida desde teléfonos móviles hasta monitores Ultra-Wide.
2. **Cross-Platform Build**: Los scripts de automatización (`scripts/`) utilizan APIs nativas de Node.js y `npx`, garantizando que el entorno de desarrollo sea idéntico en Windows, macOS y Linux.
3. **Browser Agnostic**: Al evitar dependencias específicas de proveedores o motores de renderizado modernos (como los que requieren algunos frameworks), el sitio es compatible con todos los navegadores compatibles con ES6 (97%+ del mercado global).

## 🚀 Conclusión

Este portafolio es un testimonio de que **menos es más**. La eficiencia técnica es una característica, no una limitación. La adición de `llm.txt` extiende esta filosofía al ámbito de la IA: ser legíble, semántico y discoverable para las próximas generaciones de agentes automáticos.

---
[← Volver al README](../README.md) | **Vladimir Acuña** - Senior Software Engineer
