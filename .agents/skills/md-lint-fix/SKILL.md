# md-lint-fix

Detecta, auto-corrige y reporta errores markdownlint en archivos `.md`
modificados — antes de cualquier `git commit` o `git push`.

## Cuándo usar este skill

- El usuario menciona errores MD031, MD034, MD040, MD032, MD028
- Antes de hacer commit/push y hay archivos .md modificados
- Después de crear o editar skills, docs o cualquier archivo markdown
- El usuario dice "arregla el lint", "corrige los markdown", "limpia los MD"

---

## Errores que resuelve este skill

| Código | Descripción | Solución |
|--------|-------------|----------|
| MD031 | Blank lines around fenced code blocks | Auto-fix (`--fix`) |
| MD032 | Lists surrounded by blank lines | Auto-fix (`--fix`) |
| MD034 | Bare URL used | Auto-fix (`--fix`) — envuelve en `<>` |
| MD028 | Blank line inside blockquote | Auto-fix (`--fix`) |
| MD040 | Fenced code block without language | Script propio — infiere lenguaje por contexto |
| MD027 | Multiple spaces after blockquote | Auto-fix (`--fix`) |

**No resuelve automáticamente** (requieren criterio humano):

- MD013 (line length) — desactivado en este proyecto
- MD033 (inline HTML) — desactivado en este proyecto
- MD001/MD003 (heading style) — structural, requiere revisión

---

## Flujo de ejecución

### Caso normal — solo archivos modificados (pre-push)

```bash
cd C:/portfolio-pages
python scripts/fix-md-lint.py
```

El script detecta automáticamente los `.md` modificados según `git status`.

### Caso completo — todos los .md del repo

```bash
python scripts/fix-md-lint.py --all
```

### Modo diagnóstico sin modificar nada

```bash
python scripts/fix-md-lint.py --dry-run
python scripts/fix-md-lint.py --all --dry-run
```

---

## Qué hace el script internamente

1. **Detecta** los `.md` en scope (modificados o todos según flag)
2. **Escanea** con `markdownlint-cli2` y cuenta errores iniciales
3. **Corrige MD040**: recorre cada bloque sin lenguaje e infiere el correcto:
   - `git`, `npm`, `cd`, `aws`, `docker`, `make` → `bash`
   - `import`, `def`, `class` → `python`
   - `function`, `const`, `=>` → `javascript`
   - `{` / `"key":` → `json`
   - `on:`, `jobs:`, `steps:` → `yaml`
   - `resource "`, `provider "` → `hcl`
   - Sin patrón claro → `text`
4. **Auto-fix** con `markdownlint-cli2 --fix` (MD031/MD032/MD034/MD028)
5. **Verifica** de nuevo y reporta resultado final

---

## Integración con el flujo de commit

Antes de `git add` + `git commit` + `git push`, ejecutar:

```bash
python scripts/fix-md-lint.py
```

Si el resultado es `LIMPIO`, continuar con el commit normalmente.
Si quedan errores manuales, resolverlos antes de hacer push.

---

## Referencia de reglas MDxxx completa

Las reglas están documentadas en:
<https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md>

Reglas desactivadas en este proyecto (`.markdownlint.json`):

- MD013 — line length (textos largos son aceptables)
- MD033 — inline HTML (necesario para la web)
- MD041 — first line heading (no todos los docs empiezan con H1)
