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

---

## CONTEXTO DEL PROYECTO

- Repositorio principal: vladimiracunadev-create.github.io (C:\portfolio-pages)
- Web: <https://vladimiracunadev-create.github.io/>
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

### Si hay contenido nuevo en index.html o PDFs

El script NO edita HTML ni scripts de generación — eso requiere trabajo manual.
Solo interviene Claude cuando:

- Hay proyectos nuevos que necesitan card en index.html (sección #proyectos)
- Los scripts de generación necesitan nuevo contenido (descripciones, idiomas)
- Hay cambios de identidad/título profesional

### Si hay errores en el script

Reportar primero. Arreglar con autorización del usuario.

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
[resultado de npm run lint:md y git push]
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
[API]       — JSONs actualizados
[Scripts]   — cambios en generate-*.py (repos, subtítulos)
[HTML]      — cards nuevas / descripciones actualizadas
[Backups]   — PDFs respaldados en assets/backups/YYYY-MM-DD/
[PDFs]      — N PDFs regenerados
[README]    — perfil GitHub actualizado
[Lint]      — resultado npm run lint:md
[Commit]    — hash del commit
[Push]      — estado
[Reporte]   — assets/backups/YYYY-MM-DD/SESSION-REPORT-YYYY-MM-DD.md
[Manual]    — tareas que requieren intervención (si las hay)
```
