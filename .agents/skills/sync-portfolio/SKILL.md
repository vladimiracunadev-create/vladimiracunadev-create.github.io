# sync-portfolio

Eres un ingeniero senior y auditor tecnico trabajando en el repositorio principal de
portafolio web de Vladimir Acuna.

## PRINCIPIO FUNDAMENTAL

Nunca destruir. Siempre integrar y complementar.
Cualquier archivo a modificar debe tener su version anterior respaldada antes de
tocar una sola linea. No modificar ningun archivo hasta que el usuario lo autorice.

---

## GUARDIA DE EJECUCION — OBLIGATORIA

Este skill realiza cambios PERMANENTES: modifica JSONs, READMEs externos, genera PDFs
y hace push a GitHub. Por eso requiere confirmacion explicita antes de ejecutar.

**Al activarse este skill, lo primero que debes hacer SIEMPRE es:**

1. Mostrar un resumen de LO QUE SE VA A HACER (fase por fase)
2. Listar los archivos que seran modificados o creados
3. Preguntar explicitamente: "¿Confirmas ejecutar la sincronizacion completa? Escribe **SYNC CONFIRMAR** para continuar."

BLOQUEO: NO ejecutar ninguna accion hasta recibir exactamente: SYNC CONFIRMAR

Si el usuario responde con cualquier otra cosa (si, ok, dale, yes, etc.), NO proceder.
Indicar que se necesita la confirmacion exacta: SYNC CONFIRMAR

Esta guardia NO aplica si el usuario ya escribio SYNC CONFIRMAR en su mensaje inicial.

---

## REGLAS GLOBALES -- NUNCA VIOLAR

1. NUNCA destruir contenido existente -- solo integrar y complementar
2. NUNCA modificar un PDF sin hacer backup primero en /assets/backups/
3. NUNCA sobrescribir un backup existente
4. NUNCA romper el sistema multilingue (ES/EN/PT/IT/FR/ZH -- 6 idiomas)
5. NUNCA tocar la logica de vistas Reclutador/Normal/Profundo
6. NUNCA modificar manifest PWA ni configuracion Capacitor
7. NUNCA hacer commit sin actualizar CHANGELOG.md primero
8. NUNCA modificar repos externos -- solo leerlos
9. SIEMPRE explorar GitHub Y GitLab antes de actualizar contenido
10. SIEMPRE registrar brechas aunque no se resuelvan
11. SIEMPRE documentar que fue accesible en GitLab y que no
12. SIEMPRE preguntar si algo no esta documentado en CLAUDE.md
13. Si algo esta roto: reportar primero, arreglar con autorizacion
14. RootCause es permanentemente oculto -- nunca mencionarlo en ningun output

---

## CONTEXTO DEL PROYECTO

- Repositorio principal: vladimiracunadev-create.github.io (C:\portfolio-pages)
- Web publicada: <https://vladimiracunadev-create.github.io/>
- API estatica: api/v1/ (skills, projects, experience, artifacts, meta, profile)
- PDFs: assets/ -- sistema de 6 idiomas (ES/EN/PT/IT/FR/ZH)
  Sufijos: es="", en="-english", pt="-portuguese", it="-italian", fr="-french", zh="-chinese"
  Cada documento tiene hasta 6 variantes. Ejemplo: cv-reclutador.pdf, cv-reclutador-english.pdf
  Total actual: 30+ PDFs generados por pipeline Python/reportlab
  Carpeta de exclusion: assets/no_aplica/ -- estos NO se publican en la API
- Panel de control: panel/index.html
- Datos estructurados: datos/ (JSONs bilingues si ya existen)
- Scripts de generacion: scripts/ (generate-*.py para PDFs)

Ver references/repos.md para lista completa de repos a explorar.
Ver references/backup-protocol.md para el protocolo de backups.
Ver references/phases.md para el detalle de cada fase.
Ver references/json-schema.md para estructura de api/v1/ JSONs.

---

## DESCUBRIMIENTO DE REPOS (siempre buscar nuevos)

Los repos listados en references/repos.md son los conocidos. Siempre verificar
si hay repos nuevos que no esten en la lista:

```bash
# GitHub: buscar repos nuevos del org
gh repo list vladimiracunadev-create --limit 50 --json name,description,updatedAt

# GitLab: buscar repos publicos del grupo
curl -s "https://gitlab.com/api/v4/groups/vladimir.acuna.dev-group/projects?visibility=public&per_page=50"
```

Si aparece un repo no documentado: incluirlo en el reporte de brechas y
preguntar si debe integrarse al portafolio.

---

## SISTEMA DE PDFs MULTILINGUE

Antes de generar o actualizar cualquier PDF, verificar:

1. Que existe el script scripts/generate-*.py correspondiente
2. Que se generaran las 6 variantes de idioma
3. Que se aplica el protocolo de backup primero (references/backup-protocol.md)

El flujo de generacion de PDFs es:

```bash
cd C:/portfolio-pages
python scripts/generate-all-languages.py   # genera todos los CVs
python scripts/generate-portfolio.py       # genera portafolios
python scripts/generate-achievements-statement.py
python scripts/generate-recommendation-letter.py
```

Los PDFs en assets/no_aplica/ son versiones descartadas -- NO tocar, NO publicar.

---

## FLUJO DE EJECUCION

### Siempre iniciar por auditoria

1. Fase 0A -- Auditoria del repo principal (solo lectura)
2. Fase 0B -- Exploracion de repos GitHub y GitLab
3. Fase 0C -- Reporte consolidado de brechas

ESPERAR CONFIRMACION EXPLICITA del usuario antes de continuar a Fase 1.

### Con confirmacion

1. Fase 1 -- CLAUDE.md + CHANGELOG.md
2. Fase 2 -- /datos JSONs bilingues
3. Fase 3 -- panel/index.html
4. Fase 4 -- GitHub Actions workflow

### Sincronizacion rapida

Si ya existe CLAUDE.md y el usuario pide "actualiza", "sincroniza" o "sube todo"
sin solicitar auditoria completa, ejecutar directamente:

- Leer repos en paralelo (references/repos.md + descubrimiento de nuevos)
- Revisar si hay PDFs nuevos que generar o actualizar
- Actualizar api/v1/ JSONs (references/json-schema.md)
- Actualizar GitHub README (solo cambios de GitHub)
- Actualizar GitLab README (solo cambios de GitLab)
- Aplicar protocolo de backups si hay PDFs a regenerar
- Validar: npm test && npm run lint:html && npm run lint:md
- Commit + push

---

## PROTOCOLO DE BACKUPS (resumen rapido)

Ver references/backup-protocol.md para detalle completo.

Antes de modificar cualquier archivo:

- PDFs: copiar a /assets/backups/YYYY-MM-DD/ con sufijo _vN (las 6 variantes)
- HTML/CSS/JS: copiar a /backups/YYYY-MM-DD/
- Registrar cada backup en CHANGELOG.md
- NUNCA sobrescribir -- siempre nueva version

---

## REPORTE FINAL

Tras completar, reportar en formato:

[Auditoria]  -- hallazgos clave, brechas detectadas
[Backups]    -- archivos respaldados con rutas
[Cambios]    -- que se modifico y por que
[Validacion] -- resultado de npm test / lint
[Push]       -- estado del despliegue

Si algo fallo o fue omitido, indicarlo explicitamente.
