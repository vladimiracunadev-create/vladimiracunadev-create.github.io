# 📡 CV Data API — Manual

**Vladimir Acuña** · Arquitecto de Software & Full-Stack Senior

> Currículum publicado como API JSON estática + PDFs descargables, servido desde **GitHub Pages** sin servidor ni autenticación.

---

## ¿Qué es?

Un conjunto de endpoints JSON de solo lectura que reflejan la información profesional de este portafolio, extraída desde los PDFs del repositorio. Ideal para integraciones, bots, herramientas de RRHH o cualquier sistema que necesite consumir datos estructurados de un CV.

---

## Base URL

```text
https://vladimiracunadev-create.github.io
```

---

## Endpoints v1

| Endpoint | Descripción |
|---|---|
| [`/api/v1/meta.json`](https://vladimiracunadev-create.github.io/api/v1/meta.json) | Metadatos de la API, versión, endpoints |
| [`/api/v1/profile.json`](https://vladimiracunadev-create.github.io/api/v1/profile.json) | Perfil público (nombre, título, redes) |
| [`/api/v1/experience.json`](https://vladimiracunadev-create.github.io/api/v1/experience.json) | Experiencia laboral |
| [`/api/v1/projects.json`](https://vladimiracunadev-create.github.io/api/v1/projects.json) | Proyectos destacados |
| [`/api/v1/skills.json`](https://vladimiracunadev-create.github.io/api/v1/skills.json) | Skills, educación, idiomas |
| [`/api/v1/artifacts.json`](https://vladimiracunadev-create.github.io/api/v1/artifacts.json) | Inventario de PDFs con URLs directas |

---

## Ejemplos de uso

### curl

```bash
# Perfil
curl https://vladimiracunadev-create.github.io/api/v1/profile.json

# Todos los artefactos (PDFs)
curl https://vladimiracunadev-create.github.io/api/v1/artifacts.json

# Skills
curl https://vladimiracunadev-create.github.io/api/v1/skills.json
```

### JavaScript (fetch)

```js
const BASE = "https://vladimiracunadev-create.github.io";

// Perfil
const profile = await fetch(`${BASE}/api/v1/profile.json`).then(r => r.json());

// Listado de PDFs
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
| Carta de Recomendación | [`/assets/carta-recomendacion_sin_firma.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma.pdf) |

---

## Cómo actualizar

1. Editar/reemplazar los PDFs en `assets/` o los JSON en `api/v1/`.
2. `git add -A && git commit -m "update: ..." && git push origin main`
3. GitHub Pages publica automáticamente en ~1 minuto.

Para regenerar los JSON desde los PDFs: ejecutar `python scripts/generate-seo.js` (o el script de extracción si se agrega).

---

## Versionado

- **v1** es estable. No cambiará su contrato.
- Si se requiere cambio de estructura, se creará `/api/v2/` manteniendo v1 activo.

---

## Privacidad

- Teléfono y email **no** están expuestos en los endpoints públicos.
- PDFs en `assets/no_aplica/` y `assets/por_solicitud/` **no** están listados en la API.

---

## Links rápidos

- 🏠 [Portafolio](https://vladimiracunadev-create.github.io/)
- 📄 [CV ATS (PDF)](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf)
- 📦 [artifacts.json](https://vladimiracunadev-create.github.io/api/v1/artifacts.json)
- 🤖 [llm.txt](https://vladimiracunadev-create.github.io/llm.txt)
