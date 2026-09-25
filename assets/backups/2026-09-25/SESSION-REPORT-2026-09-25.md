# Reporte de Sesión — 2026-09-25

**Commits generados:** 2
**Rango de commits:** `8172d36` → `HEAD` (incluye este reporte)

## Resumen ejecutivo

Se sincronizó el portafolio con el estado público vigente de GitHub: 62
repositorios propios detectados, 19 proyectos nuevos incorporados y 11
descripciones existentes actualizadas. Antes de regenerar documentos se
respaldaron los 36 PDFs públicos. La web, la API JSON y los seis portafolios
multilingües quedaron actualizados y validados sin errores bloqueantes.

## Cambios por archivo — detalle estricto

### `scripts/sync-portfolio.py`

**Commit:** `HEAD`

- La consulta de GitHub cambió de un máximo de 50 a 100 repositorios.
- Se agregó fallback de solo lectura a la API pública cuando `gh` no dispone
  de una credencial válida.
- Se excluyen forks para no presentar trabajo ajeno como proyecto propio.
- El saneamiento PDF ahora elimina banderas regionales y el símbolo de Bitcoin,
  además de los emojis ya contemplados.
- El conteo documental se corrigió de 30 PDFs/5 tipos a 36 PDFs/6 tipos.
- Se registraron categorías estables para Codex Skills Toolkit, AI Dataset
  Foundry y Pañuelo al Viento.

### `api/v1/*.json`

**Commit:** `8172d36`

- `generated_at`: fechas anteriores → `2026-09-25` en los seis endpoints.
- `projects.json`: 42 → 61 proyectos publicados.
- Se agregaron: Codex Skills Toolkit, RootCause QR Inspector, Chilean School
  Learning Path, Architecture Built Environment Learning Program, PDF Reader,
  Universal Payments Engineering Lab, Psychometrics and Assessment Program,
  RootCause Server, AWS Desktop Studio, AI Dataset Foundry, RootCause
  Blockchain Security, RootCause Bitcoin Defense, Decentraland Social Arcade,
  Commerce Operating System, Pañuelo al Viento, QEMU/KVM Labs, Database Systems
  Labs, Video Transcript Studio y Framework Ecosystems Labs.
- Se actualizaron descripciones de Modern Cybersecurity Program, Artificial
  Intelligence Evolution Program, Finance and Banking Evolution Program,
  Blockchain Learning Path, Empresa Operativa Chile, Executive Leadership
  Founder Program, Machine Operator Program, Neural Network Training Labs,
  Multi-Cloud Engineering Program, RootCause Web Inspector y Claude Skills
  Toolkit.

### `index.html`

**Commit:** `8172d36` + `HEAD`

- Se añadieron 19 cards dentro de los grupos de proyectos.
- `buildDate`: `2026-08-13` → `2026-09-25`.
- Hero: `Ago/Aug/Août/2026年8月` → `Sep/Set/2026年9月` en seis idiomas.
- Se sincronizaron versiones visibles: Blockchain `v0.9.0` → `v0.14.0`,
  Empresa Operativa Chile `v1.4.0` → `v1.5.0`, RootCause Web `v0.1.0` →
  `v0.2.0`, Multi-Cloud `v2.0.0` → `v2.2.0` y AI Evolution `v0.2.0` →
  `v0.17.0`.
- Modern Cybersecurity: 340 clases/19 partes → 360 clases/20 partes.
- Claude Skills Toolkit: 14 → 15 skills, preservando los seis idiomas.

### `scripts/generate-all-languages.py`

**Commit:** `8172d36`

- Se añadieron los 19 proyectos nuevos a los CV ATS y de reclutador en los seis
  idiomas, con URLs únicas y descripciones saneadas para ReportLab.

### `scripts/generate-portfolio.py`

**Commit:** `8172d36` + `HEAD`

- Se añadieron los 19 proyectos nuevos a las seis variantes del portafolio.
- Once proyectos variables toman ahora su descripción vigente desde
  `api/v1/projects.json`, evitando drift de versiones.
- Cada entrada de proyecto usa `KeepTogether`, eliminando la línea huérfana que
  dejaba `tests.` sola al inicio de una página.
- Se normalizó `≈` a `~` y se eliminaron símbolos sin glifo antes de renderizar.

### `assets/*.pdf`

**Commit:** `8172d36` + `HEAD`

- Los 36 PDFs originales se copiaron antes de cualquier regeneración a
  `assets/backups/2026-09-25/`; ningún respaldo existente fue sobrescrito.
- Se regeneraron los 36 PDFs mediante sus scripts oficiales.
- Los seis portafolios se regeneraron una segunda vez tras corregir paginación,
  descripciones variables y saneamiento Unicode.

### `CHANGELOG.md`

**Commit:** `8172d36` + `HEAD`

- Se documentó la sincronización del 25 de septiembre de 2026, el número real
  de PDFs, los proyectos incorporados y las correcciones de calidad.

## PDFs — estado final

| Documento | Variantes | Estado |
|---|---:|---|
| CV ATS | 6 | Regenerado; apertura y extracción correctas |
| CV Reclutador | 6 | Regenerado; apertura y extracción correctas |
| Hoja de Vida | 6 | Conservada y respaldada |
| Portafolio | 6 | Regenerado; revisión visual completa en español y muestras EN/ZH |
| Carta de Recomendación | 6 | Conservada y respaldada |
| Declaración de Logros | 6 | Conservada y respaldada |

## Errores encontrados y resueltos

| Error | Causa | Fix aplicado |
|---|---|---|
| Todos los repos aparecían como inexistentes | Token local de `gh` vencido | Fallback a API pública y exclusión de forks |
| `tests.` quedaba sola al cambiar de página | Un párrafo de proyecto podía dividirse | `KeepTogether` por entrada |
| Cuadrados negros en portafolios | Banderas y símbolo Bitcoin sin glifo ReportLab | Regex Unicode ampliada y regeneración |
| `pnpm` intentó acceder al registro | Wrapper del runtime quiso reinstalar dependencias | Gates ejecutados directamente con dependencias locales |

## Validación final

- Integridad: 57 PASSED · 1 warning informativo · 0 ERRORS.
- Markdown: 53 archivos · 0 errores.
- HTML Validate: 0 errores.
- PDFs: 36 archivos · 121 páginas · 0 glifos de reemplazo detectados.
- Revisión visual: CV ATS (2 páginas), CV reclutador (4 páginas), portafolio
  español completo (6 páginas) y muestras English/Chinese sin solapamientos ni
  texto recortado.
- Backup: 36 PDFs en `assets/backups/2026-09-25/`.
- Git push: pendiente al cierre de este reporte; la credencial `gh` local está
  vencida, pero se intentará el remoto Git configurado tras el commit final.
- GitHub Pages: pendiente de push y despliegue; usar Ctrl+F5 tras publicarse.
