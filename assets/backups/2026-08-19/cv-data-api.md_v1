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
| [`/api/v1/meta.json`](https://vladimiracunadev-create.github.io/api/v1/meta.json) | Metadatos de la API, versión, capacidades multilingüe y endpoints |
| [`/api/v1/profile.json`](https://vladimiracunadev-create.github.io/api/v1/profile.json) | Perfil público |
| [`/api/v1/experience.json`](https://vladimiracunadev-create.github.io/api/v1/experience.json) | Experiencia laboral |
| [`/api/v1/projects.json`](https://vladimiracunadev-create.github.io/api/v1/projects.json) | Proyectos destacados |
| [`/api/v1/skills.json`](https://vladimiracunadev-create.github.io/api/v1/skills.json) | Skills, educación e idiomas |
| [`/api/v1/artifacts.json`](https://vladimiracunadev-create.github.io/api/v1/artifacts.json) | Inventario de PDFs públicos con 6 variantes de idioma c/u |

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

## PDFs directos — 6 idiomas (ES/EN/PT/IT/FR/ZH)

Los PDFs están disponibles en **6 idiomas**. En la interfaz web, el selector de idioma cambia automáticamente el enlace de descarga al documento equivalente vía atributos `data-pdf-{lang}`.

**Mapa de sufijos:** ES → `` | EN → `-english` | PT → `-portuguese` | IT → `-italian` | FR → `-french` | ZH → `-chinese`

### CV ATS

| Idioma | Enlace |
|---|---|
| Español | [`/assets/cv-ats.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf) |
| English | [`/assets/cv-ats-english.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats-english.pdf) |
| Português | [`/assets/cv-ats-portuguese.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats-portuguese.pdf) |
| Italiano | [`/assets/cv-ats-italian.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats-italian.pdf) |
| Français | [`/assets/cv-ats-french.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats-french.pdf) |
| 中文 | [`/assets/cv-ats-chinese.pdf`](https://vladimiracunadev-create.github.io/assets/cv-ats-chinese.pdf) |

### CV Reclutador

| Idioma | Enlace |
|---|---|
| Español | [`/assets/cv-reclutador.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador.pdf) |
| English | [`/assets/cv-reclutador-english.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador-english.pdf) |
| Português | [`/assets/cv-reclutador-portuguese.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador-portuguese.pdf) |
| Italiano | [`/assets/cv-reclutador-italian.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador-italian.pdf) |
| Français | [`/assets/cv-reclutador-french.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador-french.pdf) |
| 中文 | [`/assets/cv-reclutador-chinese.pdf`](https://vladimiracunadev-create.github.io/assets/cv-reclutador-chinese.pdf) |

### Portafolio

| Idioma | Enlace |
|---|---|
| Español | [`/assets/portafolio.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio.pdf) |
| English | [`/assets/portafolio-english.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio-english.pdf) |
| Português | [`/assets/portafolio-portuguese.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio-portuguese.pdf) |
| Italiano | [`/assets/portafolio-italian.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio-italian.pdf) |
| Français | [`/assets/portafolio-french.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio-french.pdf) |
| 中文 | [`/assets/portafolio-chinese.pdf`](https://vladimiracunadev-create.github.io/assets/portafolio-chinese.pdf) |

### Carta de Recomendación

| Idioma | Enlace |
|---|---|
| Español | [`/assets/carta-recomendacion_sin_firma.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma.pdf) |
| English | [`/assets/carta-recomendacion_sin_firma-english.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma-english.pdf) |
| Português | [`/assets/carta-recomendacion_sin_firma-portuguese.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma-portuguese.pdf) |
| Italiano | [`/assets/carta-recomendacion_sin_firma-italian.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma-italian.pdf) |
| Français | [`/assets/carta-recomendacion_sin_firma-french.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma-french.pdf) |
| 中文 | [`/assets/carta-recomendacion_sin_firma-chinese.pdf`](https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma-chinese.pdf) |

### Declaración de Logros y Validación

La **Declaración de Logros y Validación** se publica como artefacto separado: resume logros observables y provee referencia externa de contexto laboral, sin reemplazar el CV ni el portafolio.

| Idioma | Enlace |
|---|---|
| Español | [`/assets/declaracion-logros-validacion.pdf`](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion.pdf) |
| English | [`/assets/declaracion-logros-validacion-english.pdf`](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion-english.pdf) |
| Português | [`/assets/declaracion-logros-validacion-portuguese.pdf`](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion-portuguese.pdf) |
| Italiano | [`/assets/declaracion-logros-validacion-italian.pdf`](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion-italian.pdf) |
| Français | [`/assets/declaracion-logros-validacion-french.pdf`](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion-french.pdf) |
| 中文 | [`/assets/declaracion-logros-validacion-chinese.pdf`](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion-chinese.pdf) |

---

## Cómo actualizar

1. Editar o reemplazar los PDFs en `assets/` o los JSON en `api/v1/`.
2. Para regenerar todos los PDFs: `python scripts/generate-all-languages.py && python scripts/generate-portfolio.py && python scripts/generate-achievements-statement.py && python scripts/generate-recommendation-letter.py`
3. Ejecutar `git add -A && git commit -m "update: ..." && git push origin main`.
4. GitHub Pages publica automáticamente en alrededor de 1 minuto.

Para regenerar `robots.txt` y `sitemap.xml`, ejecutar `node scripts/generate-seo.js`.

---

## Privacidad

- Teléfono y email no se exponen en los endpoints públicos.
- Los PDFs en `assets/no_aplica/` y `assets/por_solicitud/` no se listan en la API.
- La referencia externa incluida en la declaración de logros sirve para validar contexto laboral general; no atribuye autoría automática del documento al contacto mencionado.

---

## Links rápidos

- [Portafolio](https://vladimiracunadev-create.github.io/)
- [CV ATS (PDF)](https://vladimiracunadev-create.github.io/assets/cv-ats.pdf)
- [Achievements Statement (PDF)](https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion-english.pdf)
- [artifacts.json](https://vladimiracunadev-create.github.io/api/v1/artifacts.json)
- [llm.txt](https://vladimiracunadev-create.github.io/llm.txt)
