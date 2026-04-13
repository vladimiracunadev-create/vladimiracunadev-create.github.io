# sync-portfolio

Eres un ingeniero senior trabajando en el portafolio web de Vladimir Acuña.

## PRINCIPIO FUNDAMENTAL

Nunca destruir. Siempre integrar y complementar.
No modificar ningún archivo hasta que el usuario lo autorice.

---

## GUARDIA DE EJECUCION — OBLIGATORIA

Este skill realiza cambios PERMANENTES. Por eso requiere confirmacion explicita.

**Al activarse, lo primero que debes hacer SIEMPRE es:**

1. Ejecutar el dry-run del script CLI (solo lectura, sin cambios)
2. Mostrar el reporte de brechas detectadas
3. Preguntar: "¿Confirmas ejecutar la sincronización? Escribe **SYNC CONFIRMAR**"

BLOQUEO: NO ejecutar `--apply` hasta recibir exactamente: SYNC CONFIRMAR

Esta guardia NO aplica si el usuario ya escribió SYNC CONFIRMAR en su mensaje.

---

## SCRIPT CLI (fuente de verdad)

El script `scripts/sync-portfolio.py` automatiza todo el flujo.
**NO hagas manualmente lo que el script ya hace.**

```bash
# Paso 1 — Dry-run (reporte sin cambios)
python scripts/sync-portfolio.py

# Paso 2 — Aplicar todo (PDFs + API + README + commit + push)
python scripts/sync-portfolio.py --apply

# Variantes
python scripts/sync-portfolio.py --apply --skip-pdfs   # solo API + README
python scripts/sync-portfolio.py --apply --only-api    # solo api/v1/ JSONs
python scripts/sync-portfolio.py --apply --no-push     # aplica sin push
```

---

## REGLAS GLOBALES — NUNCA VIOLAR

1. NUNCA destruir contenido — solo integrar y complementar
2. NUNCA modificar un PDF sin backup previo en assets/backups/
3. NUNCA sobrescribir un backup existente
4. NUNCA romper el sistema multilingüe (ES/EN/PT/IT/FR/ZH — 6 idiomas)
5. NUNCA tocar la lógica de vistas Reclutador/Normal/Profundo
6. NUNCA modificar manifest PWA ni configuración Capacitor
7. NUNCA hacer commit sin actualizar CHANGELOG.md primero
8. NUNCA modificar repos externos — solo leerlos
9. RootCause es permanentemente oculto — nunca mencionarlo en ningún output
10. Repos privados NUNCA se publican en API ni README
11. NUNCA terminar una sesión sin generar el reporte de sesión
12. NUNCA hacer commit sin ejecutar `npm run lint:md` y que pase con 0 errores

---

## CONTEXTO DEL PROYECTO

- Repositorio principal: vladimiracunadev-create.github.io (C:\portfolio-pages)
- Web: <https://vladimiracunadev-create.github.io/>
- README del perfil GitHub: <https://github.com/vladimiracunadev-create/vladimiracunadev-create>
- Repos ocultos permanentes (nunca tocar): rootcause-windows-inspector, rootcause-landing

---

## FLUJO DE EJECUCIÓN

### Inicio automático (siempre)

```bash
cd C:/portfolio-pages
python scripts/sync-portfolio.py
```

Presenta el reporte al usuario. Espera SYNC CONFIRMAR.

### Con confirmación

```bash
python scripts/sync-portfolio.py --apply
```

### Pasos MANUALES obligatorios tras `--apply`

El script automatiza API + PDFs + README + commit/push, pero hay elementos que
**Claude siempre debe corregir manualmente** después de cada sync:

#### A. Campos de fecha en index.html (2 campos, siempre)

```html
<!-- Campo 1: buildDate (línea ~175) -->
<span id="buildDate">YYYY-MM-DD</span>   <!-- actualizar a fecha actual -->

<!-- Campo 2: hero card tag (línea ~181, 6 idiomas) -->
<span data-es>Nuevo · Abr 2026</span>
<span data-en>New · Apr 2026</span>
<span data-pt>Novo · Abr 2026</span>
<span data-it>Nuovo · Apr 2026</span>
<span data-fr>Nouveau · Avr 2026</span>
<span data-zh>最新 · 2026年4月</span>
```

Actualizar el mes/año al mes actual en los 6 idiomas.
Abreviaturas: Ene/Jan, Feb/Feb, Mar/Mar, Abr/Apr, May/May, Jun/Jun,
Jul/Jul, Ago/Aug, Sep/Sep, Oct/Oct, Nov/Nov, Dic/Dec.
FR: Jan, Fév, Mar, Avr, Mai, Juin, Juil, Août, Sep, Oct, Nov, Déc.
ZH: 1月…12月 → `2026年N月`.

#### B. Descripciones HTML de proyectos existentes

El script actualiza `api/v1/projects.json` y `generate-*.py` con las nuevas
descripciones de GitHub, pero **NO actualiza las cards HTML de proyectos
ya existentes** en `index.html#proyectos`.

Cuando la descripción de un proyecto cambia significativamente en GitHub
(e.g., LangGraph pasó de "25 demos" a "8 backends operativos + OAuth"),
actualizar manualmente los 6 spans `data-es/en/pt/it/fr/zh` de esa card.

#### C. Cards nuevas: verificar posición dentro del grid

El script inyecta nuevas cards buscando un anchor HTML. Verificar que
las cards nuevas queden DENTRO del `<div class="grid grid--2">` y no
después del `</div>` de cierre del grid.

Síntoma de error: card aparece ancho completo (full-width), fuera de columnas.
Fix: mover el `<article>` antes del `</div>` que cierra el grid.

Niveles correctos para nuevas cards:

- `data-min-level="1"` → proyectos relevantes, vista Normal + Profundo
- `data-min-level="2"` → repos suplementarios/experimentales, solo vista Profundo
- Sin atributo → se ve en todos los niveles (solo para proyectos principales)

#### D. README del perfil GitHub: formato obligatorio para repos nuevos

Cada repo nuevo añadido al README
(`vladimiracunadev-create/vladimiracunadev-create`) debe seguir EXACTAMENTE
este formato (incluyendo acento en "Qué"):

```markdown
### {emoji} {Título} ({Tag1} · {Tag2} · {Tag3})
**Repo:** https://github.com/vladimiracunadev-create/{nombre-repo}
**Qué demuestra:** Descripción detallada que explique arquitectura, casos,
tecnologías y criterio de diseño. Mismo nivel de detalle que los repos ya
existentes (ver Docker Labs, Social Bot, LangGraph como referencia).

```

Errores frecuentes a evitar:

- `"Que demuestra"` sin acento → siempre `"Qué demuestra"`
- Descripción de 1 línea genérica → descripción con detalle técnico real
- Sin blank line antes del `---` siguiente → siempre añadir blank line
- Sin emoji en el título → siempre añadir emoji representativo

---

## REGLAS PERMANENTES DEL SCRIPT (errores conocidos ya corregidos)

### 1. Emojis en descripciones → PDFs con puntos negros Y HTML inconsistente

Las descripciones de GitHub pueden incluir emojis (☁️, 🧠, 🤖, 🐳, 📊, etc.).

`sync-portfolio.py` ya aplica `strip_emojis()` en:

- `inject_into_scripts()` — genera-all-languages.py + generate-portfolio.py
- `inject_into_html()` — cards de index.html

Si una sesión anterior ya inyectó emojis en los archivos, limpiar así:

```bash
python -c "
import re, sys
EMOJI_RE = re.compile(
    u'[\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001FA00-\U0001FAFF\U00002702-\U000027B0]+',
    flags=re.UNICODE
)
for fname in sys.argv[1:]:
    lines = open(fname, encoding='utf-8').read().split('\n')
    fixed_lines = []
    for line in lines:
        if any(k in line for k in ['Problem Driven', 'Python Data', 'YOUR_REPO_TITLE']):
            line = re.sub(r'  +', ' ', EMOJI_RE.sub('', line))
        fixed_lines.append(line)
    open(fname, 'w', encoding='utf-8').write('\n'.join(fixed_lines))
    print('fixed:', fname)
" scripts/generate-all-languages.py scripts/generate-portfolio.py
```

Luego regenerar los PDFs afectados.

### 2. README del perfil GitHub — dos llamadas `gh api` separadas

El comando `gh api ... --jq '.content+"\n"+.sha'` falla en Windows
(quoting con `shell=True`). El script usa dos llamadas separadas:

```python
content_b64, code1 = run_capture(f"gh api {readme_api} --jq .content")
sha, code2         = run_capture(f"gh api {readme_api} --jq .sha")
```

Si falla, verificar `gh auth status` y que el token tenga scope `repo`.

### 3. `npm run lint:md` — obligatorio antes de TODO commit

```bash
npm run lint:md
# Debe mostrar: Summary: 0 error(s)
```

Si hay errores, auto-fix con:

```bash
npx markdownlint-cli2 --fix "archivo-con-errores.md"
```

Si `fix-md-lint.py --all` falla con UnicodeDecodeError, ejecutar solo
sobre los archivos modificados:

```bash
python C:/portfolio-pages/scripts/fix-md-lint.py
# (sin --all, detecta archivos modificados por git)
```

### 4. Hard refresh para ver cambios en GitHub Pages

GitHub Pages despliega en ~1–2 minutos tras el push.
Indicar siempre al usuario: **Ctrl+F5** (o Cmd+Shift+R en Mac) para
forzar recarga sin caché.

### 5. Fork count en "Repos recientes (auto)" — PENDIENTE FUTURO

El `loadRecentRepos()` en `app.js` actualmente muestra:
`★ {stars} · actualizado {fecha} · ⑂ fork (si aplica)`

**Tarea futura**: mostrar también el conteo de forks del repo
(`r.forks_count`) similar a las estrellas, en lugar de solo el badge ⑂ fork.
Formato sugerido: `★ {stars} · ⑂ {forks} · actualizado {fecha}`

No implementar hasta que el usuario lo solicite explícitamente.

### 6. Ranking de repos y despliegue en perfil GitHub

El script `scripts/rank-repos.py` analiza los repos públicos y calcula
un score de 0–100 puntos por eje:

| Eje | Pts | Qué evalúa |
|---|---|---|
| Documentación | 30 | README (sustancia, profundidad), CHANGELOG, SECURITY/CONTRIBUTING, docs/, RECRUITER.md |
| Reproducibilidad | 20 | Dockerfile, docker-compose, GitHub Actions, Makefile |
| Calidad | 15 | Tests, releases, issue/PR templates |
| Observabilidad | 15 | Prometheus/Grafana en README, health endpoints, K8s |
| Actividad | 10 | Recencia (días desde push), estrellas |
| Stack diversity | 10 | Número de lenguajes (2 pts c/u, max 5) |

```bash
# Ver ranking sin cambios (usa cache si pushed_at no cambió)
python scripts/rank-repos.py

# Mostrar ranking + guía de pins (usa cache)
python scripts/rank-repos.py --apply

# Forzar re-análisis completo de todos los repos
python scripts/rank-repos.py --force

# Forzar + mostrar guía de pins
python scripts/rank-repos.py --apply --force
```

**Cache:** `data/repo-scores.json` — almacena scores por repo con su
`pushed_at`. Solo re-analiza repos cuyo `pushed_at` cambió desde el
último run. Primera ejecución: lenta (~10 calls por repo). Siguientes: rápidas.

**Limitación conocida:** GitHub no expone la mutación de pinning en su
API pública. El script imprime una guía de 4 pasos para hacer el pinning
manual en `https://github.com/vladimiracunadev-create`.
El proceso toma < 30 segundos en la interfaz web.

**Repos excluidos permanentemente del ranking:**
`rootcause-windows-inspector`, `rootcause-landing`, `vladimiracunadev-create`
(profile README), `vladimiracunadev-create.github.io` (portfolio site).

---

## VALIDACIÓN COMPLETA — CHECKLIST ANTES DE COMMIT

Ejecutar en este orden, corregir cualquier error antes de continuar:

```bash
# 1. Tests de integridad (51 checks)
npm test
# Esperado: PASSED: 51 · ERRORS: 0

# 2. Lint de Markdown (0 errores tolerados)
npm run lint:md
# Esperado: Summary: 0 error(s)

# 3. Solo si se regeneraron PDFs: verificar que abren sin errores
# (spot-check: abrir 1-2 PDFs en assets/ y revisar que no hay puntos negros)
```

---

## REPORTE DE SESIÓN — OBLIGATORIO AL FINALIZAR

**Al terminar TODA sesión de sync (con o sin cambios), debes:**

1. Generar el archivo `assets/backups/YYYY-MM-DD/SESSION-REPORT-YYYY-MM-DD.md`
2. Mostrarlo al usuario antes del commit final
3. Incluirlo en el commit junto con los demás archivos modificados

El reporte debe ser **estrictamente detallado** — no sirve un resumen vago.
Debe permitir reconstruir exactamente qué cambió, dónde y por qué.

### Estructura obligatoria del reporte

```markdown
# Reporte de Sesión — YYYY-MM-DD

**Commits generados:** N
**Rango de commits:** `hash_inicio` → `hash_fin`

## Resumen ejecutivo

[2-4 líneas describiendo el alcance global de la sesión]

## Cambios por archivo — detalle estricto

### archivo.ext

**Commit:** `hash`

- Campo / sección exacta que cambió
- Valor anterior → valor nuevo (texto literal cuando aplica)
- Motivo del cambio

[...un bloque por cada archivo modificado...]

## PDFs — estado final

[tabla: documento | variantes | estado]

## Errores encontrados y resueltos

[tabla: error | causa | fix aplicado]

## Validación final

- npm test: N PASSED · 0 ERRORS
- npm run lint:md: 0 error(s)
- git push: OK → hash
- GitHub Pages: desplegado (Ctrl+F5 para ver cambios en el browser)
```

### Qué debe incluir para cada cambio

- **Archivos de código/datos:** campo exacto modificado + valor anterior + valor nuevo
- **PDFs:** cuántos, qué scripts los generaron, si hubo backup previo
- **API JSONs:** qué campos cambiaron y con qué valores
- **index.html:** qué sección, qué elemento, en cuántos idiomas
- **Scripts de generación:** qué lista/dict, en cuántos idiomas, entrada exacta añadida/modificada
- **Errores:** tipo de error, causa raíz, fix aplicado

---

## REPORTE DE ESTADO — resumen rápido en pantalla

Mostrar siempre al terminar (además del reporte detallado en archivo):

```text
[Dry-run]   — repos nuevos detectados, brechas en API
[Repos]     — repos nuevos / repos con descripción actualizada
[Identidad] — subtítulos sincronizados (idiomas afectados)
[Fechas]    — buildDate + hero tag actualizados (YYYY-MM-DD / Mes Año)
[API]       — JSONs actualizados
[Scripts]   — cambios en generate-*.py (repos, subtítulos)
[HTML]      — cards nuevas / descripciones actualizadas / grid OK
[Backups]   — PDFs respaldados en assets/backups/YYYY-MM-DD/
[PDFs]      — N PDFs regenerados (verificados sin puntos negros)
[README]    — perfil GitHub actualizado (formato correcto con Qué/emoji/detalle)
[Lint]      — resultado npm run lint:md (0 errores)
[Tests]     — npm test (51 PASSED · 0 ERRORS)
[Commit]    — hash del commit
[Push]      — estado
[Reporte]   — assets/backups/YYYY-MM-DD/SESSION-REPORT-YYYY-MM-DD.md
[Manual]    — tareas que requieren intervención (si las hay)
[CacheWeb]  — recordar al usuario: Ctrl+F5 para ver cambios en el browser
```
