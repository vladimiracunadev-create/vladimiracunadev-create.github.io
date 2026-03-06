---
name: portfolio-full-update
description: >
  Extrae información desde los PDFs del portafolio (CV, cartas, portafolio),
  consulta los repositorios GitHub y GitLab del usuario, y actualiza de forma
  integral el sitio (index.html), la CV Data API (api/v1/*.json), toda la
  documentación (docs/, wiki/, README) y los archivos SEO. Úsalo cuando el
  usuario indique que ha aprendido algo nuevo, cambió de trabajo, actualizó
  su CV, o quiere refrescar el portafolio.
---

# Skill: Portfolio Full Update

## Objetivo

Mantener el portafolio y su CV Data API **siempre sincronizados** con el
estado real del profesional: nuevos skills, proyectos, experiencia o
documentos actualizados.

---

## Cuándo usar este skill

- El usuario dice _"actualicé mi CV"_ o _"agregué un nuevo proyecto"_.
- El usuario dice _"aprendí algo nuevo"_ (lenguaje, herramienta, cloud, IA...).
- El usuario sube un PDF nuevo a `assets/`.
- El usuario quiere refrescar toda la documentación / sitio.

---

## Repositorios de referencia

| Plataforma | URL |
|---|---|
| GitHub | https://github.com/vladimiracunadev-create |
| GitLab | https://gitlab.com/vladimir.acuna.dev-group |

> **Nota**: Los repos públicos se pueden leer con `read_url_content` o
> `browser_subagent`. Usar para detectar proyectos nuevos, READMEs,
> tecnologías y fechas de actividad reciente.

---

## Pasos del workflow

### FASE 0 — Verificar qué cambió

```
1. git status  →  detectar PDFs nuevos / modificados
2. Listar assets/ para inventariar archivos actuales
3. (Opcional) Leer repos GitHub/GitLab para detectar proyectos nuevos
```

**Comandos clave:**

```powershell
git status
Get-ChildItem assets/ -Recurse -Filter *.pdf
```

---

### FASE 1 — Extraer texto de los PDFs

```
pip install pdfminer.six --quiet   (solo si no está instalado)
python C:/tmp/extract_pdfs.py       (script de extracción)
```

**Script de extracción reutilizable:**

```python
# Guardar como C:/tmp/extract_pdfs.py
import os
from datetime import datetime
from pdfminer.high_level import extract_text

PDFS = {
    "cv-ats":              "assets/cv-ats.pdf",
    "cv-reclutador":       "assets/cv-reclutador.pdf",
    "portafolio":          "assets/portafolio.pdf",
    "carta-recomendacion": "assets/carta-recomendacion_sin_firma.pdf",
}

os.makedirs("sources/extracted", exist_ok=True)

for name, path in PDFS.items():
    if not os.path.exists(path):
        print(f"MISSING: {path}")
        continue
    text = extract_text(path)
    out  = f"sources/extracted/{name}.extracted.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# SOURCE: {path}\n# DATE: {datetime.now().isoformat()}\n\n")
        f.write(text)
    print(f"OK [{len(text.strip())} chars] -> {out}")
```

**Reglas de calidad:**

- Si un PDF genera < 200 chars → es escaneado → crear `docs/NEEDS_OCR.md`.
- No inventar datos. Si un campo no aparece en el PDF → `null` o `"TODO"`.
- Nunca exponer teléfono ni email en JSON públicos.

---

### FASE 2 — Detectar proyectos nuevos en GitHub/GitLab

```
Usar read_url_content o browser_subagent para:
  https://github.com/vladimiracunadev-create
  https://gitlab.com/vladimir.acuna.dev-group

Buscar:
  - Repos nuevos no listados en api/v1/projects.json
  - READMEs con tecnologías nuevas
  - Commits recientes relevantes
```

---

### FASE 3 — Actualizar la CV Data API

Actualizar los 6 archivos JSON en `api/v1/` basándose en los textos extraídos
y proyectos detectados:

| Archivo | Qué actualizar |
|---|---|
| `api/v1/profile.json` | Título, resumen, años de experiencia |
| `api/v1/experience.json` | Cargo actual / nuevo, fechas, highlights |
| `api/v1/projects.json` | Proyectos nuevos desde GitHub/GitLab |
| `api/v1/skills.json` | Skills nuevos (lenguajes, herramientas, cloud, IA) |
| `api/v1/artifacts.json` | PDFs nuevos o renombrados con URLs correctas |
| `api/v1/meta.json` | Actualizar `generated_at` a fecha actual |

También actualizar `data/resume.json` (canónico JSON Resume).

---

### FASE 4 — Actualizar index.html

Secciones que pueden requerir cambio:

| Sección | Qué revisar |
|---|---|
| `#evolucion` (hero cards) | Nuevos pilares técnicos, fecha (Mar/Abr...) |
| `#proyectos` | Agregar artículos de proyectos nuevos |
| `#roles` | Nuevos roles profesionales |
| `#descargas` | Nuevos PDFs o renombramientos |
| `id="buildDate"` | Actualizar fecha de última actualización |

> **Regla**: Solo agregar `data-es` + `data-en` para cada texto bilingüe.
> No romper el sistema de vistas (`data-min-level="1"` para Normal+Deep,
> `data-min-level="2"` para Deep only).

---

### FASE 5 — Actualizar toda la documentación

Archivos que siempre deben reflejar el estado actual:

```
README.md                     → arquitectura, hitos, API, fechas
docs/RECRUITER.md             → tabla de habilidades, CV Data API
docs/TECHNICAL_RATIONAL.md   → nuevas decisiones técnicas
docs/BUILD_GUIDE.md           → si cambian scripts o PDFs del bundle
docs/VALIDATION.md            → si se agrega nuevo eje de calidad
docs/SECURITY_HEADERS.md      → si cambian endpoints o PDFs
docs/wiki/Home.md             → sección CV Data API, benchmarks
docs/wiki/_Sidebar.md         → si hay secciones nuevas
docs/wiki/RECRUITER.md        → mirror de docs/RECRUITER.md
docs/wiki/TECHNICAL_RATIONAL.md → mirror de docs/TECHNICAL_RATIONAL.md
docs/wiki/VALIDATION.md       → mirror de docs/VALIDATION.md
cv-data-api.md                → si cambian endpoints o PDFs públicos
llm.txt                       → si cambia el stack o propósito del sitio
```

> **Regla Markdown lint (MD040)**: Todo bloque de código con triple backtick
> debe tener lenguaje especificado (` ```text `, ` ```bash `, ` ```json `, etc.)

---

### FASE 6 — SEO y discoverability

Revisar si corresponde actualizar:

- `sitemap.xml` → agregar nuevas URLs relevantes / actualizar `<lastmod>`
- `robots.txt` → sin cambios usuales
- `llm.txt` → actualizar stack, proyectos, fecha de última actualización

---

### FASE 7 — Lint, commit y push

```powershell
# Verificar markdown (en CI, no localmente en PowerShell restringido)
git add -A
git status --short   # revisar qué se va a subir
git commit -m "feat: update portfolio — [descripción del cambio]"
git push origin main
```

**Convención de commit messages:**

| Tipo | Cuándo usar |
|---|---|
| `feat:` | Nuevo proyecto, nueva sección, nueva API |
| `fix:` | Link roto, dato incorrecto, lint error |
| `chore(assets):` | PDF nuevo, renombrado, actualizado |
| `docs:` | Solo cambios en documentación |
| `refactor:` | Reorganización sin cambio funcional |

---

## Checklist de aceptación

- [ ] `sources/extracted/*.extracted.txt` actualizados
- [ ] `api/v1/*.json` actualizados (especialmente `meta.json` con fecha)
- [ ] `data/resume.json` actualizado
- [ ] `index.html` — `buildDate` y secciones actualizadas
- [ ] `llm.txt` — fecha y stack actualizados
- [ ] `sitemap.xml` — `<lastmod>` actualizadas
- [ ] Lint markdown: 0 errores
- [ ] `git push` exitoso
- [ ] Verificar URLs en producción (GitHub Pages demora ~1 min)

---

## Notas importantes

- **No mover ni borrar** archivos en `assets/no_aplica/` ni `assets/por_solicitud/`
  — existen con propósito. Solo actualizar si el usuario lo pide explícitamente.
- **PDFs privados** nunca van en `api/v1/artifacts.json` ni en `index.html`.
- El sitio se despliega **desde la raíz de `main`** — no hay carpeta `/docs` ni
  rama `gh-pages`. Todo lo que está en raíz es público en GitHub Pages.
- `dist/` está en `.gitignore` — es solo para Lighthouse CI local.
