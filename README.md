# Vladimir Acuña - Portafolio

Este repositorio contiene el código fuente de mi portafolio profesional personal.
Es un sitio web estático diseñado para ser rápido, limpio y profesional, mostrando mi experiencia, proyectos y servicios.

## 🛠 Stack Tecnológico

El proyecto está construido con principios **KISS (Keep It Simple, Stupid)**, evitando frameworks pesados innecesarios para este caso de uso.

- **HTML5 Semántico**: Estructura clara y accesible.
- **CSS3 Vanilla**: Estilos personalizados, variables CSS, Flexbox y Grid. Sin preprocesadores complejos.
- **JavaScript (ES6+)**: Lógica ligera para interactividad (menú móvil, acordeones, cambio de vistas) sin dependencias externas.
- **PDF Assets**: CVs y documentos descargables optimizados.

## 🚀 Despliegue (CD)

El sitio utiliza **AWS Amplify** configurado para **Continuous Deployment**.

- **Repositorio**: GitHub
- **Trigger**: Push a la rama `main`
- **URL de Producción**: https://main.d1uybq9oui7h8c.amplifyapp.com/

## 💻 Desarrollo Local

Para visualizar y editar el sitio localmente:

1.  **Clonar el repositorio**:
    ```bash
    git clone https://github.com/vladimiracunadev-create/vladimiracunadev-create.github.io.git
    cd vladimiracunadev-create.github.io
    ```

2.  **Servidor Local** (Recomendado):
    Puedes usar cualquier servidor estático. Por ejemplo, con `http-server` (Node.js):
    ```bash
    npx http-server . -p 8080
    ```
    O con Python:
    ```bash
    python -m http.server 8080
    ```

3.  Abrir `http://localhost:8080` en tu navegador.

## 📂 Estructura

- `index.html`: Página principal (Single Page Portfolio).
- `styles.css`: Hoja de estilos principal.
- `app.js`: Scripts de interfaz (UI Logic).
- `*.pdf`: Recursos estáticos (Curriculum, Cartas).

---
© 2026 Vladimir Acuña
