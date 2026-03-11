# CV Data API Manual

**Vladimir Acuna** | Arquitecto de Software y Full-Stack Senior

> Curriculum publicado como API JSON estatica + PDFs descargables, servido desde **GitHub Pages** sin servidor ni autenticacion.

---

## Que es

Un conjunto de endpoints JSON de solo lectura que reflejan la informacion profesional de este portafolio, extraida desde los PDFs del repositorio. Ideal para integraciones, bots, herramientas de RRHH o cualquier sistema que necesite consumir datos estructurados de un CV.

---

## Base URL

```text
https://vladimiracunadev-create.github.io
```

---

## Endpoints v1

| Endpoint | Descripcion |
|---|---|
| [`/api/v1/meta.json`](https://vladimiracunadev-create.github.io/api/v1/meta.json) | Metadatos de la API, version, endpoints |
| [`/api/v1/profile.json`](https://vladimiracunadev-create.github.io/api/v1/profile.json) | Perfil publico (nombre, titulo, redes) |
| [`/api/v1/experience.json`](https://vladimiracunadev-create.github.io/api/v1/experience.json) | Experiencia laboral |
| [`/api/v1/projects.json`](https://vladimiracunadev-create.github.io/api/v1/projects.json) | Proyectos destacados |
| [`/api/v1/skills.json`](https://vladimiracunadev-create.github.io/api/v1/skills.json) | Skills, educacion, idiomas |
| [`/api/v1/artifacts.json`](https://vladimiracunadev-create.github.io/api/v1/artifacts.json) | Inventario de PDFs con URLs directas |

---

## Ejemplos de uso

### curl

```bash
curl https://vladimiracunadev-create.github.io/api/v1/profile.json
curl https://vladimiracunadev-create.github.io/api/v1/artifacts.json
curl https://vladimiracunadev-create.github.io/api/v1/skills.json
```

### JavaScript (fetch)

```js
const BASE = "https://vladimiracunadev-create.github.io";
const profile = await fetch(`${BASE}/api/v1/profile.json`).then(r => r.json());
const artifacts = await fetch(`${BASE}/api/v1/artifacts.json`).then(r => r.json());
console.log(artifacts.artifacts.map(a => a.url));
```

---

## PDFs directos

| Documento | URL |
|---|---|
| CV ATS | [`/assets/cv-ats.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf) |
| CV Reclutador | [`/assets/cv-reclutador.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador.pdf) |
| Portafolio | [`/assets/portafolio.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio.pdf) |
| Carta de Recomendacion | [`/assets/carta-recomendacion_sin_firma.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma.pdf) |

---

## Como actualizar

1. Editar o reemplazar los PDFs en `assets/` o los JSON en `api/v1/`.
2. `git add -A && git commit -m "update: ..." && git push origin main`
3. GitHub Pages publica automaticamente en alrededor de 1 minuto.

Para regenerar `robots.txt` y `sitemap.xml`: ejecutar `node scripts/generate-seo.js`.

La API JSON actual se mantiene como artefacto estatico versionado en `api/v1/`. Si luego se agrega un extractor dedicado desde PDFs, conviene documentarlo aqui por separado.

---

## Versionado

- **v1** es estable. No cambiara su contrato.
- Si se requiere cambio de estructura, se creara `/api/v2/` manteniendo v1 activo.

---

## Privacidad

- Telefono y email **no** estan expuestos en los endpoints publicos.
- PDFs en `assets/no_aplica/` y `assets/por_solicitud/` **no** estan listados en la API.

---

## Links rapidos

- [Portafolio](https://vladimiracunadev-create.github.io/)
- [CV ATS (PDF)](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf)
- [artifacts.json](https://vladimiracunadev-create.github.io/api/v1/artifacts.json)
- [llm.txt](https://vladimiracunadev-create.github.io/llm.txt)
