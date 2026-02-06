# Vladimir Acuña - Portafolio

Este repositorio contiene el código fuente de mi portafolio profesional personal.
Es un sitio web estático diseñado para ser rápido, limpio y profesional, mostrando mi experiencia, proyectos y servicios.

## 🛠 Stack Tecnológico

El proyecto está construido con principios **KISS (Keep It Simple, Stupid)**, evitando frameworks pesados innecesarios para este caso de uso.

- **HTML5 Semántico**: Estructura clara y accesible.
- **CSS3 Vanilla**: Estilos personalizados, variables CSS, Flexbox y Grid. Sin preprocesadores complejos.
- **JavaScript (ES6+)**: Lógica ligera para interactividad (menú móvil, acordeones, cambio de vistas) sin dependencias externas.
- **PDF Assets**: CVs y documentos descargables optimizados.

## 📚 Documentación Especializada

He preparado guías específicas según quién revise este repositorio:

- **[🎯 Guía para Reclutadores](docs/RECRUITER.md)**: Valor de negocio, métricas técnicas (Lighthouse) y por qué elegir este stack.
- **[🧠 Racional Técnico](docs/TECHNICAL_RATIONAL.md)**: ¿Por qué Vanilla JS/CSS? Una explicación sobre simplicidad y rendimiento.
- **[🔰 Manual para Novatos](docs/BEGINNER_GUIDE.md)**: Cómo clonar, editar y subir tu propio portafolio si estás empezando.

---

## 💻 Desarrollo Local

Para visualizar y editar el sitio localmente:

1. **Clonar el repositorio** (o descargar el ZIP):

    ```bash
    git clone https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io.git
    cd vladimiracunadev-create.github.io
    ```

2. **Abrir Directamente**:
    Al ser un sitio puramente estático, simplemente haz doble clic en `index.html` para verlo en tu navegador.

    > **Nota**: No requieres instalar nada (ni Node, ni Python) a menos que quieras simular un entorno de servidor real.

3. **Servidor Local** (Opcional - solo si prefieres):
    Si deseas usar un servidor local por comodidad:
    - Node/NPM: `npx http-server .`
    - Python: `python -m http.server`

## 📂 Estructura

- `index.html`: Página principal (Single Page Portfolio).
- `styles.css`: Hoja de estilos principal.
- `app.js`: Scripts de interfaz (UI Logic).
- `*.pdf`: Recursos estáticos (Curriculum, Cartas).

---
© 2026 Vladimir Acuña
