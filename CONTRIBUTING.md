# GuÃƒÂ­a de ContribuciÃƒÂ³n

Ã‚Â¡Gracias por considerar contribuir a este ecosistema! Al ser parte de un ecosistema diseÃƒÂ±ado bajo los estÃƒÂ¡ndares de **observabilidad**, **reproducibilidad**, **calidad local-first** e **idempotencia**, mantenemos expectativas altas sobre la integridad del cÃƒÂ³digo para mantener este portafolio como un reflejo de ingenierÃƒÂ­a moderna.

## Tipos de Contribuciones que Buscamos

- Ã°Å¸Ââ€º **CorrecciÃƒÂ³n de Bugs**: Resolver problemas identificados, preferiblemente sumando una prueba automatizada (`pytest`, etc.) que compruebe la soluciÃƒÂ³n.
- Ã°Å¸Å¡â‚¬ **Nuevas Funcionalidades**: Mejoras arquitectÃƒÂ³nicas, nuevas integraciones (e.g. con n8n, Ollama o LangGraph).
- Ã°Å¸â€œâ€“ **DocumentaciÃƒÂ³n**: Claridad, traducciones o diagramas de arquitectura explÃƒÂ­citos (Mermaid o draw.io).
- Ã°Å¸Ââ€”Ã¯Â¸Â **Infraestructura**: Mejoras a los flujos DevOps (K8s, CI/CD, Makefiles, PWA Configurations).

## Flujo de Trabajo (Git Flow)

Este proyecto usa un flujo estandarizado basado en ramas de caracterÃƒÂ­sticas:

1. **Haz Fork** del repositorio a tu cuenta.
2. **Crea una rama** para tu funcionalidad o correcciÃƒÂ³n partiendo del estado mÃƒÂ¡s reciente de la rama `main`:

    ```bash
    git checkout -b feature/nueva-magia-a-aws
    # o para fixes
    git checkout -b fix/auth-bypass
    ```

3. **Desarrolla** tu funcionalidad.
    - AsegÃƒÂºrate de seguir la filosofÃƒÂ­a del repositorio. Si estamos usando `uv` para Python de alto rendimiento, no uses otra cosa a menos que justifiques el cambio.
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

## EstÃƒÂ¡ndares del CÃƒÂ³digo

- **Test-Driven Development (opcional pero recomendado)**: Incluye comandos para correr tus pruebas. Si el repositorio tiene Action de GitHub con `mypy` o `bandit`, asegÃƒÂºrate de que tus modificaciones pasen localmente (`make test`, `make lint` o scripts disponibles en el ecosistema).
- **Docker-first**: Cualquier dependencia requerida debe estar documentada y disponible mediante `docker-compose.yml` para levantar la arquitectura en menos de 60 segundos u obviar la fricciÃƒÂ³n del setup local.
- **DocumentaciÃƒÂ³n obligatoria**: Si es un cambio mayor, no olvides la documentaciÃƒÂ³n en el README y si es aplicable, un diagrama explicativo.

## Skills de IA del Repositorio

Si el cambio afecta varias superficies publicas, usa el skill adecuado antes de abrir el PR:

- `portfolio-consistency-audit`: revisar contradicciones entre sitio, API, docs, wiki y SEO.
- `portfolio-doc-sync`: alinear README, manuales y wiki con cambios tecnicos.
- `portfolio-seo-llm-maintainer`: actualizar `llm.txt`, `robots.txt`, `sitemap.xml` y metadatos publicos.
- `portfolio-mobile-wrapper-check`: revisar el wrapper Capacitor cuando cambien PWA, assets o manifest.
- `portfolio-release-guard`: validar lint, build e integridad antes de push o release.
- `portfolio-full-update`: usar cuando el cambio sea transversal y afecte CV, JSON API, sitio y documentacion completa.
