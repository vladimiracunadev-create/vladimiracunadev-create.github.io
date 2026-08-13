# Reporte de Sesión — 2026-08-13

**Commits generados:** 2
**Rango de commits:** `80c65b1` → (commit de correcciones manuales)
**Brecha sincronizada:** 27 días (último sync: 2026-07-17, commit `1a2ed1b`)

## Resumen ejecutivo

Sincronización completa del portafolio tras 27 días. Se integraron 13 repos nuevos y 7
descripciones cambiadas en web, API, scripts PDF y README de perfil. El `--apply` automático
dejó cuatro defectos de datos (cuadros negros en PDFs, enlaces apuntando al repo equivocado,
cards fuera del grid y entradas faltantes); se corrigieron **en la causa raíz** dentro de
`sync-portfolio.py` además de en la salida, porque uno de ellos era una recurrencia del bug ya
documentado el 2026-07-17. Los 30 PDFs se regeneraron dos veces: una por el apply y otra tras
las correcciones. Validación final limpia.

## Cambios por archivo — detalle estricto

### scripts/sync-portfolio.py

**Commit:** correcciones manuales

- `_EMOJI_RE`: añadidos rangos `FE00–FE0F` (variation selectors), `200D` (ZWJ), `20E3` (keycap)
  y `2B00–2BFF`. Antes quitaba el emoji y dejaba el selector huérfano → cuadro negro ■ en PDF.
- `strip_emojis()`: colapsa espacios dobles resultantes de la eliminación.
- `repo_key(name, taken=None)`: nuevo parámetro `taken`. Si la clave corta ya está ocupada por
  otro repo, extiende con más tokens. `rootcause-web-inspector` → `rootcause_web` (antes:
  `rootcause`, heredando la URL de `rootcause-windows-inspector`).
- `existing_url_keys(content)`: nueva función; lee las claves ya presentes en `PROJECTS_URLS`.
- `inject_into_all_languages()`: pasa `existing_url_keys(content)` a `repo_key`.
- `inject_into_all_languages()` / `projects_ats`: dedupe `if key in segment` →
  `if f'"{key}"),' in segment or title in segment`. Antes `multi` hacía match dentro de
  `multijugador` y saltaba la entrada de Multi-Cloud.
- `inject_into_portfolio()`: deriva `taken` desde `PROJECT_LINKS`.
- `_insert_card_in_grid()`: nueva función. Inserta la card antes del `</div>` que cierra el
  grid, no en `CARD_ANCHOR` (que está fuera del grid).
- `inject_html_cards()`: usa `_insert_card_in_grid()`.

### scripts/generate-all-languages.py

**Commit:** correcciones manuales

- Eliminados 35 U+FE0F huérfanos en las entradas de `blockchain-learning-path`, `sandbox-labs`
  y `multi-cloud-engineering-program` (las 3 únicas afectadas; el contenido previo estaba limpio).
- `PROJECTS_URLS`: + 4 claves — `rootcause_mobile`, `rootcause_web`, `modern_business`,
  `modern_cyber`.
- 15 entradas de `projects_ats` reapuntadas a la clave correcta.
- 8 entradas añadidas: `projects_ats` ES (Modern Business Creation, Rootcause Web Inspector,
  Multi Cloud Engineering) y `projects_rec` EN (3) y PT (2).

### scripts/generate-portfolio.py

**Commit:** correcciones manuales

- Eliminados 18 U+FE0F huérfanos en las mismas 3 entradas.

### index.html

**Commit:** correcciones manuales

- `buildDate`: `2026-07-17` → `2026-08-13`.
- Tag del hero (6 idiomas): `Jul 2026 / Jul 2026 / Jul 2026 / Lug 2026 / Juil 2026 / 2026年7月`
  → `Ago 2026 / Aug 2026 / Ago 2026 / Ago 2026 / Août 2026 / 2026年8月`.
- Cierre del grid reubicado: el `</div>` que cerraba `<div class="grid">` estaba antes de las
  13 cards nuevas; se movió después de la última (Polyglot Programming Labs). Verificado en
  navegador: 35/35 cards dentro del grid, ancho uniforme 533px, 2 columnas.
- 18 líneas limpiadas de U+FE0F (12 + 6 de `sandbox-labs`, cuya descripción no contiene el
  nombre del repo y se saltó en la primera pasada).
- 13 cards nuevas traducidas a EN/PT/IT/FR/ZH (65 spans).
- 24 reemplazos de datos desactualizados en 4 cards existentes × 6 idiomas.

### api/v1/projects.json

**Commit:** correcciones manuales

- `python-data-science-program`: `"version": "v3.8.0"` → `"version": "v3.11.0"`
  (release real verificado con `gh release view`). Único cambio: 1 línea.

### CLAUDE.md · .agents/skills/{sync-portfolio,build-deploy-zip,portfolio-release-guard}/SKILL.md

**Commit:** correcciones manuales

- 16 invocaciones `npm test` / `npm run …` / `npm.cmd run …` → `pnpm`.

## PDFs — estado final

| Documento | Variantes | Páginas | Estado |
|---|---|---|---|
| CV Reclutador | 6 | 6–7 | OK · multipágina intacta · 13/13 repos nuevos |
| CV ATS | 6 | 3–4 | OK · enlaces reapuntados |
| Portafolio | 6 | 4–5 | OK · 7 enlaces curados intactos |
| Declaración de Logros | 6 | 3 | OK |
| Carta de Recomendación | 6 | 1 | OK |

Verificación sobre texto extraído de los 30 PDFs: **0 variation selectors, 0 emojis**.

## Errores encontrados y resueltos

| Error | Causa | Fix aplicado |
|---|---|---|
| Cuadros negros ■ en PDFs | `strip_emojis` no cubría U+FE0F | Rangos añadidos a `_EMOJI_RE` + limpieza de 53 líneas ya inyectadas |
| 4 enlaces al repo equivocado | `repo_key` colisionaba por primera palabra | `repo_key(name, taken)` + 4 claves nuevas + 15 entradas reapuntadas |
| 13 cards a ancho completo | `CARD_ANCHOR` fuera del grid | `_insert_card_in_grid()` + cierre del grid reubicado |
| Multi-Cloud ausente del ATS | dedupe `multi` ⊂ `multijugador` | Comparación por tupla exacta + 8 entradas añadidas |
| Cards nuevas en español en los 6 idiomas | el apply no traduce | 13 cards × 5 idiomas traducidas |
| Indentación destruida en 67 líneas | regex `\s+(")` propia mal acotada | Revert + recorte preservando indentado y CRLF |
| `projects.json` reformateado entero (538 líneas) | `json.dumps` propio | Revert a HEAD + reemplazo textual de 1 línea |

## Segunda ronda — los 3 pendientes + README del perfil

El usuario pidió ejecutar los tres pendientes y actualizar el README del perfil. Al abordarlos
apareció un defecto mayor y **preexistente** que explicaba el desbalance del ATS.

### Defecto raíz: entradas inyectadas en la lista equivocada

`inject_*` guardaba los offsets de los 6 bloques de idioma UNA vez y los reasignaba dentro del
bucle —lo cual no afecta a la iteración en curso—. Tras la primera inserción los offsets
restantes quedaban corridos:

| Destino correcto | Dónde cayeron | Cantidad | Efecto visible |
|---|---|---:|---|
| `projects_ats` | `projects_rec` | 101 | CV reclutador EN/IT/FR/ZH imprimía tuplas `('…', 'clave')` |
| portafolio `projects` | portafolio `vp` | 130 | 5 portafolios listaban repos bajo "Propuesta de Valor" |
| `projects_ats` | `ats_experience` / `experience` | 118 | CV ATS listaba proyectos dentro de la experiencia laboral |

Ya venía publicado: los backups `_v1` (estado previo al sync) tenían 7–11 tuplas por idioma.
El sync de hoy lo amplificó a 36–44. **Solo el CV en español estaba limpio.**

Corregido con una única función `_insert_per_language` que recalcula offsets en cada iteración,
usada por los 4 puntos de inserción.

### Normalización aplicada

| Lista | Antes (es/en/pt/it/fr/zh) | Después |
|---|---|---|
| `projects_ats` | 31 / 17 / 11 / 9 / 9 / 9 | **35 en los 6** |
| `projects_rec` | 34 / 27 / 30 / 30 / 29 / 26 | **34 en los 6** |
| `ats_experience` | 5 / 30 / 31 / 31 / 32 / 26 | **5 en los 6** |
| portafolio `vp` | 7 / 33 / 33 / 33 / 33 / 33 | **7 en los 6** |
| portafolio `projects` | 33 / 7 / 7 / 7 / 7 / 7 | **33 en los 6** |

Drift alineado en las entradas curadas: AWS 15 → 16 casos A–P (EN/IT/FR/ZH), Social Bot ZH
9 → 18+ motores DB, LangGraph FR/ZH → 25/25 backends v4.15.

### Los 3 pendientes

- **Detector de drift**: usa el tag de `gh release` como fuente primaria; el README pasa a
  fallback ampliado a badges shields.io. `social-bot-scheduler` deja de reportarse.
- **Scripts móviles**: migrados a `corepack pnpm`. Requirió `pnpm-workspace.yaml` con
  `nodeLinker: hoisted` (en pnpm ≥ 10 va ahí, no en `.npmrc`) porque el linker aislado hacía que
  `cap sync android` escribiera una ruta Gradle con la versión embebida. Verificado con
  `pnpm install` + `cap sync android`; el build Gradle del APK no se ejecutó (requiere Android SDK).
- **README del perfil**: el commit del sync `2827ec5` fue **vacío** (0 adiciones) pese a reportar
  éxito. Pasada completa: +5 repos, cifras contadas sobre las carpetas reales
  (GameDev 292 → 352, total 1.508 → 1.928), Blockchain 19 → 28 módulos, Multi-Cloud
  1.537 → 1.220 páginas, landings 18 → 24. Publicado en `5d802a6`, con el bloque
  `<!-- STATS -->` del workflow y el mermaid intactos.

### Pendiente que queda

- **Build Android real**: la migración a pnpm está verificada hasta `cap sync`; falta ejecutar
  `mobile-android-build.ps1` completo en una máquina con Android SDK para confirmar el APK.

## Pendientes reportados (primera ronda, ya resueltos en la segunda)

## Validación final

- `pnpm test`: **55 PASSED · 0 ERRORS** (1 warning preexistente: 110 links sin `rel="noopener"`)
- `pnpm run lint:md`: **0 error(s)** sobre 258 archivos
- Navegador: 35/35 cards en el grid · 2 columnas · los 6 idiomas conmutan con 1 span visible
- Dry-run posterior: **"Sin repos públicos nuevos"** · drift de `python-data-science-program` resuelto
