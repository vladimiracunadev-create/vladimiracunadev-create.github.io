# CV Data API Manual

**Vladimir Acuña** | Arquitecto de Software y Full-Stack Senior

> Currículum publicado como API JSON estática y PDFs descargables, servido desde **GitHub Pages** sin servidor ni autenticación.

---

## Qué es

Un conjunto de endpoints JSON de solo lectura que reflejan la información profesional del portafolio. Sirve para integraciones, bots, herramientas de RRHH o cualquier sistema que necesite consumir datos estructurados del CV.

---

## Base URL

```text
https://vladimiracunadev-create.github.io
```

---

## Endpoints v1

| Endpoint | Descripción |
|---|---|
| [`/api/v1/meta.json`](https://vladimiracunadev-create.github.io/api/v1/meta.json) | Metadatos de la API, versión y endpoints |
| [`/api/v1/profile.json`](https://vladimiracunadev-create.github.io/api/v1/profile.json) | Perfil público |
| [`/api/v1/experience.json`](https://vladimiracunadev-create.github.io/api/v1/experience.json) | Experiencia laboral |
| [`/api/v1/projects.json`](https://vladimiracunadev-create.github.io/api/v1/projects.json) | Proyectos destacados |
| [`/api/v1/skills.json`](https://vladimiracunadev-create.github.io/api/v1/skills.json) | Skills, educación e idiomas |
| [`/api/v1/artifacts.json`](https://vladimiracunadev-create.github.io/api/v1/artifacts.json) | Inventario de PDFs públicos |

---

## Ejemplos de uso

### curl

```bash
curl https://vladimiracunadev-create.github.io/api/v1/profile.json
curl https://vladimiracunadev-create.github.io/api/v1/artifacts.json
curl https://vladimiracunadev-create.github.io/api/v1/skills.json
```

### JavaScript

```js
const BASE = "https://vladimiracunadev-create.github.io";
const profile = await fetch(`${BASE}/api/v1/profile.json`).then(r => r.json());
const artifacts = await fetch(`${BASE}/api/v1/artifacts.json`).then(r => r.json());
console.log(profile, artifacts);
```

---

## PDFs directos

| Documento | URL |
|---|---|
| CV ATS | [`/assets/cv-ats.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf) |
| CV Reclutador | [`/assets/cv-reclutador.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador.pdf) |
| Portafolio | [`/assets/portafolio.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio.pdf) |
| Carta de Recomendación | [`/assets/carta-recomendacion_sin_firma.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma.pdf) |

---

## Cómo actualizar

1. Editar o reemplazar los PDFs en `assets/` o los JSON en `api/v1/`.
2. Ejecutar `git add -A && git commit -m "update: ..." && git push origin main`.
3. GitHub Pages publica automáticamente en alrededor de 1 minuto.

Para regenerar `robots.txt` y `sitemap.xml`, ejecutar `node scripts/generate-seo.js`.

---

## Privacidad

- Teléfono y email no se exponen en los endpoints públicos.
- Los PDFs en `assets/no_aplica/` y `assets/por_solicitud/` no se listan en la API.

---

## Links rápidos

- [Portafolio](https://vladimiracunadev-create.github.io/)
- [CV ATS (PDF)](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf)
- [artifacts.json](https://vladimiracunadev-create.github.io/api/v1/artifacts.json)
- [llm.txt](https://vladimiracunadev-create.github.io/llm.txt)
