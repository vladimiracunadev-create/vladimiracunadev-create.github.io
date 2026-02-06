# Wiki Asíncrono & Patrones Técnicos

## Flujo de Trabajo (Wiki Async)

Este documento sirve como checklist manual antes de enviar un Pull Request.

### 1. Setup Inicial

Asegúrate de tener instaladas las dependencias:

```bash
npm install
```

### 2. Validación de Calidad (PR1)

Ejecuta los linters para HTML y Markdown:

```bash
npm run lint
```

- [ ] No debe haber errores de `html-validate`.
- [ ] No debe haber errores de `markdownlint`.

Validar enlaces rotos (requiere internet):

```bash
# Si corres Lychee localmente (requiere Docker o instalación binaria)
lychee ./**/*.html
```

### 3. SEO y Assets

Generar sitemap y robots.txt:

```bash
npm run sitemap
```

- [ ] Verificar que `sitemap.xml` incluya las URLs correctas.
- [ ] Verificar que `assets/` no tenga PDFs gigantes (>5MB).

```bash
node scripts/check-pdf.js
```

### 4. Performance y Build (PR2)

Generar versión de distribución para probar minificación:

```bash
npm run build
```

- [ ] Revisar carpeta `dist/`.
- [ ] Abrir `dist/index.html` en navegador y verificar que cargue todo.

Si tienes Lighthouse CI instalado globalmente:

```bash
lhci autorun
```

- [ ] Score de Performance > 90.
- [ ] Score de Accessibility > 90.

### 5. Deployment Checklist (PR3)

Antes de mezclar a `main`:

- [ ] ¿Los nombres de archivo PDF son correctos? (Sin doble extensión).
- [ ] ¿Se actualizaron las fechas en el footer/meta?

---

## Documentación Técnica: Patrones Asíncronos

### Frontend (app.js)

El portfolio utiliza JavaScript moderno con `async/await` para mejorar la experiencia de usuario sin bloquear el hilo principal.

- **Carga de Repositorios (`loadRecentRepos`)**:
  Consulta la API de GitHub (`https://api.github.com/users/...`) mediante `fetch` de forma asíncrona. Esto permite que la página cargue inmediatamente mientras los datos de los repositorios se obtienen en segundo plano. Muestra un estado de error si la promesa falla.

- **Portapapeles (`initCopyEmail`)**:
  Utiliza la API `navigator.clipboard.writeText`, que es una operación asíncrona, para copiar el email al portapapeles de manera segura.

### Scripts y CI/CD

Aunque scripts como `check-pdf.js` y `generate-seo.js` se ejecutan síncronamente para garantizar la consistencia, el flujo de Integración Continua (`ci.yml`) aprovecha la asincronía mediante trabajos paralelos:

- **Ejecución en Paralelo**: Los trabajos `quality`, `seo`, y `links` se inician simultáneamente.
- **Dependencias**: El trabajo `performance` espera asíncronamente a que `quality` termine exitosamente antes de iniciarse.

---

[🏠 Volver al Home](Home.md) | **Vladimir Acuña** - Senior Software Engineer
