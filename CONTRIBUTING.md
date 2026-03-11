# GuÃ­a de ContribuciÃ³n

Â¡Gracias por considerar contribuir a este ecosistema! Al ser parte de un ecosistema diseÃ±ado bajo los estÃ¡ndares de **observabilidad**, **reproducibilidad**, **calidad local-first** e **idempotencia**, mantenemos expectativas altas sobre la integridad del cÃ³digo para mantener este portafolio como un reflejo de ingenierÃ­a moderna.

## Tipos de Contribuciones que Buscamos

- ðŸ› **CorrecciÃ³n de Bugs**: Resolver problemas identificados, preferiblemente sumando una prueba automatizada (`pytest`, etc.) que compruebe la soluciÃ³n.
- ðŸš€ **Nuevas Funcionalidades**: Mejoras arquitectÃ³nicas, nuevas integraciones (e.g. con n8n, Ollama o LangGraph).
- ðŸ“– **DocumentaciÃ³n**: Claridad, traducciones o diagramas de arquitectura explÃ­citos (Mermaid o draw.io).
- ðŸ—ï¸ **Infraestructura**: Mejoras a los flujos DevOps (K8s, CI/CD, Makefiles, PWA Configurations).

## Flujo de Trabajo (Git Flow)

Este proyecto usa un flujo estandarizado basado en ramas de caracterÃ­sticas:

1. **Haz Fork** del repositorio a tu cuenta.
2. **Crea una rama** para tu funcionalidad o correcciÃ³n partiendo del estado mÃ¡s reciente de la rama `main`:

    ```bash
    git checkout -b feature/nueva-magia-a-aws
    # o para fixes
    git checkout -b fix/auth-bypass
    ```

3. **Desarrolla** tu funcionalidad.
    - AsegÃºrate de seguir la filosofÃ­a del repositorio. Si estamos usando `uv` para Python de alto rendimiento, no uses otra cosa a menos que justifiques el cambio.
    - Comprueba los *guardsrails* existentes en el proyecto.
4. **Haz Commit** a tus cambios.
    Usamos **Conventional Commits** (`feat:`, `fix:`, `docs:`, `chore:`, etc.):

    ```bash
    git commit -m "feat: implementar circuit breaker global para llamadas fallidas"
    ```

5. **Haz Push** a tu rama:

    ```bash
    git push origin feature/nueva-magia-a-aws
    ```

6. **Abre un Pull Request (PR)** hacia la rama `main` de este repositorio.

## EstÃ¡ndares del CÃ³digo

- **Test-Driven Development (opcional pero recomendado)**: Incluye comandos para correr tus pruebas. Si el repositorio tiene Action de GitHub con `mypy` o `bandit`, asegÃºrate de que tus modificaciones pasen localmente (`make test`, `make lint` o scripts disponibles en el ecosistema).
- **Docker-first**: Cualquier dependencia requerida debe estar documentada y disponible mediante `docker-compose.yml` para levantar la arquitectura en menos de 60 segundos u obviar la fricciÃ³n del setup local.
- **DocumentaciÃ³n obligatoria**: Si es un cambio mayor, no olvides la documentaciÃ³n en el README y si es aplicable, un diagrama explicativo.

## Skills de IA del Repositorio

Si el cambio afecta varias superficies pÃºblicas, usa el skill adecuado antes de abrir el PR:

- `portfolio-consistency-audit`: detectar contradicciones entre sitio, API, docs, wiki y SEO.
- `portfolio-doc-sync`: alinear README, manuales y wiki con cambios tÃ©cnicos.
- `portfolio-seo-llm-maintainer`: actualizar `llm.txt`, `robots.txt`, `sitemap.xml` y metadatos pÃºblicos.
- `portfolio-mobile-wrapper-check`: revisar el wrapper Capacitor cuando cambien PWA, assets o manifest.
- `portfolio-release-guard`: validar lint, build e integridad antes de push/release.
- `portfolio-full-update`: usar cuando el cambio sea transversal y afecte CV, JSON API, sitio y documentaciÃ³n completa.
