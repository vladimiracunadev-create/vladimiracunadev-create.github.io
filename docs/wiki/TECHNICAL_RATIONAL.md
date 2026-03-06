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

### CSS Custom Properties (Variables)

En lugar de usar SASS o Tailwind, usamos variables CSS nativas. Permiten temas dinámicos y un mantenimiento sencillo con una sintaxis que el navegador entiende nativamente.

### Lógica Asíncrona y DOM

Usamos `async/await` para cargar datos y manipulación directa del DOM para la interactividad. Esto mantiene el "payload" de JavaScript por debajo de los 100kb totales.

### Automatización vs. Runtime

Automatizamos el **Build** (minificación de CSS/JS, generación de Sitemap) usando Node.js, pero el **Runtime** (lo que corre en el navegador del usuario) es 100% puro. Esto combina lo mejor de ambos mundos: herramientas modernas de desarrollo con una ejecución ligera para el usuario.

### LLM Discoverability (llm.txt) y CV Data API

- **`llm.txt`** en raíz del sitio: estándar [llmstxt.org](https://llmstxt.org) para que los asistentes de IA indexen el sitio semánticamente.
- **CV Data API** (`/api/v1/`): 6 endpoints JSON estáticos extraídos desde PDFs con `pdfminer.six`. Currículum legible por máquinas sin servidor ni autenticación.

## 🚀 Conclusión

Este portafolio es un testimonio de que **menos es más**. La adición de `llm.txt` y la CV Data API extienden esta filosofía al ámbito de la IA: ser legíble, semántico y discoverable para agentes automáticos.

---
[🏠 Regresar al Inicio](Home)
