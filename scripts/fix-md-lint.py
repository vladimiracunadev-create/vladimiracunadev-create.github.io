"""
fix-md-lint.py — Detecta, auto-corrige y reporta errores markdownlint
en archivos .md modificados antes de git push.

Errores que resuelve automaticamente:
  MD031 - Blank lines around fenced code blocks   (--fix)
  MD032 - Lists surrounded by blank lines         (--fix)
  MD034 - Bare URLs                               (--fix)
  MD028 - Blank line inside blockquote            (--fix)
  MD040 - Fenced code blocks without language     (logica propia)

Errores que reporta pero no toca:
  MD013 - Line length (desactivado en este proyecto)
  MD033 - Inline HTML (desactivado en este proyecto)
  Cualquier otro que requiera criterio humano

Uso:
  python scripts/fix-md-lint.py              # solo archivos modificados (git)
  python scripts/fix-md-lint.py --all        # todos los .md del repo
  python scripts/fix-md-lint.py --dry-run    # reporta sin modificar
"""

import subprocess
import sys
import re
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()

# Reglas que markdownlint-cli2 --fix puede resolver solo
AUTO_FIXABLE = {"MD031", "MD032", "MD034", "MD028", "MD027"}

# Patrones para inferir lenguaje en bloques MD040
LANG_PATTERNS = [
    (r"^\s*(git |npm |npx |yarn |cd |ls |cp |mv |mkdir |rm |cat |echo |grep )", "bash"),
    (r"^\s*(python |pip |pip3 |\.py)", "bash"),
    (r"^\s*(aws |terraform |kubectl |docker |make )", "bash"),
    (r"^\s*\$\s", "bash"),
    (r"^\s*(import |from |def |class |if __name__)", "python"),
    (r"^\s*(function|const |let |var |=>|module\.exports)", "javascript"),
    (r"^\s*(\{|\[)\s*$", "json"),
    (r"^\s*\"[^\"]+\"\s*:", "json"),
    (r"^\s*(on:|jobs:|steps:|uses:|run:)", "yaml"),
    (r"^\s*(<[a-zA-Z]|<!DOCTYPE)", "html"),
    (r"^\s*(SELECT |INSERT |UPDATE |DELETE |CREATE )", "sql"),
    (r"^\s*(FROM |COPY |RUN |ENV |ARG |WORKDIR )", "dockerfile"),
    (r"^\s*(resource |provider |variable |output |module )\s*\"", "hcl"),
]


def get_modified_md_files() -> list[Path]:
    """Archivos .md modificados segun git (staged + unstaged + untracked)."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        capture_output=True, text=True, cwd=ROOT
    )
    staged = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True, cwd=ROOT
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        capture_output=True, text=True, cwd=ROOT
    )

    files = set()
    for output in [result.stdout, staged.stdout, untracked.stdout]:
        for line in output.strip().splitlines():
            if line.endswith(".md"):
                p = ROOT / line
                if p.exists():
                    files.add(p)
    return sorted(files)


def get_all_md_files() -> list[Path]:
    """Todos los .md del repo (respetando .markdownlintignore)."""
    result = subprocess.run(
        ["git", "ls-files", "*.md", "**/*.md"],
        capture_output=True, text=True, cwd=ROOT
    )
    files = []
    for line in result.stdout.strip().splitlines():
        p = ROOT / line
        if p.exists():
            files.append(p)
    return sorted(files)


def infer_language(block_lines: list[str]) -> str:
    """Infiere el lenguaje de un bloque de codigo por su contenido."""
    text = "\n".join(block_lines)
    for pattern, lang in LANG_PATTERNS:
        if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
            return lang
    return "text"


def fix_md040(path: Path, dry_run: bool = False) -> int:
    """Agrega especificador de lenguaje a bloques de codigo sin lenguaje."""
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    fixed = 0
    result = []
    i = 0
    in_block = False
    block_lang = None
    block_lines = []
    block_start = -1

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not in_block:
            # Bloque sin lenguaje: ``` o ~~~ solos
            if re.match(r"^(`{3,}|~{3,})\s*$", stripped):
                in_block = True
                block_lang = None
                block_lines = []
                block_start = len(result)
                result.append(line)
            # Bloque con lenguaje: ```python etc — no tocar
            elif re.match(r"^(`{3,}|~{3,})\w", stripped):
                in_block = True
                block_lang = "has_lang"
                result.append(line)
            else:
                result.append(line)
        else:
            # Cierre del bloque
            if re.match(r"^(`{3,}|~{3,})\s*$", stripped):
                in_block = False
                if block_lang is None:
                    # Inferir lenguaje y parchear la linea de apertura
                    lang = infer_language(block_lines)
                    fence_char = result[block_start].lstrip()[0]
                    fence_len = len(result[block_start].lstrip()) - len(result[block_start].lstrip().lstrip(fence_char))
                    indent = result[block_start][: len(result[block_start]) - len(result[block_start].lstrip())]
                    result[block_start] = f"{indent}{fence_char * fence_len}{lang}\n"
                    fixed += 1
                block_lang = None
                block_lines = []
                result.append(line)
            else:
                if block_lang is None:
                    block_lines.append(line.rstrip())
                result.append(line)

        i += 1

    if fixed > 0 and not dry_run:
        path.write_text("".join(result), encoding="utf-8")

    return fixed


def run_markdownlint(files: list[Path], fix: bool = False) -> tuple[int, str]:
    """Ejecuta markdownlint-cli2 sobre los archivos dados."""
    rel_paths = [str(f.relative_to(ROOT)).replace("\\", "/") for f in files]
    # En Windows npx necesita la extension .cmd
    npx = "npx.cmd" if sys.platform == "win32" else "npx"
    cmd = [npx, "markdownlint-cli2"] + (["--fix"] if fix else []) + rel_paths
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    output = result.stdout + result.stderr
    return result.returncode, output


def parse_error_count(output: str) -> int:
    m = re.search(r"Summary:\s*(\d+)\s*error", output)
    return int(m.group(1)) if m else 0


def main():
    parser = argparse.ArgumentParser(description="Detecta y corrige errores markdownlint.")
    parser.add_argument("--all", action="store_true", help="Procesar todos los .md del repo")
    parser.add_argument("--dry-run", action="store_true", help="Reportar sin modificar archivos")
    args = parser.parse_args()

    # Seleccionar archivos
    if args.all:
        files = get_all_md_files()
        scope = "todos los .md del repo"
    else:
        files = get_modified_md_files()
        scope = "archivos .md modificados (git)"

    if not files:
        print(f"[OK] No hay archivos .md en scope ({scope}). Nada que revisar.")
        sys.exit(0)

    print(f"\n[MD-LINT-FIX] Scope: {scope}")
    print(f"  Archivos a revisar: {len(files)}")
    for f in files:
        print(f"    - {f.relative_to(ROOT)}")

    # Paso 1: Escaneo inicial
    print("\n[1/3] Escaneando errores iniciales...")
    rc_before, out_before = run_markdownlint(files, fix=False)
    errors_before = parse_error_count(out_before)

    if errors_before == 0:
        print("      Sin errores. Nada que hacer.")
        sys.exit(0)

    print(f"      Errores encontrados: {errors_before}")

    # Paso 2: Fix MD040 (no auto-corregible por markdownlint)
    print("\n[2/3] Corrigiendo MD040 (bloques sin lenguaje)...")
    md040_fixed = 0
    for f in files:
        n = fix_md040(f, dry_run=args.dry_run)
        if n > 0:
            print(f"      {f.relative_to(ROOT)}: {n} bloque(s) corregido(s)")
            md040_fixed += n
    if md040_fixed == 0:
        print("      Sin MD040 pendientes.")

    # Paso 3: Auto-fix con markdownlint --fix (MD031, MD032, MD034, MD028...)
    print("\n[3/3] Aplicando auto-fix markdownlint (MD031/MD032/MD034/MD028)...")
    if not args.dry_run:
        run_markdownlint(files, fix=True)

    # Verificacion final
    rc_after, out_after = run_markdownlint(files, fix=False)
    errors_after = parse_error_count(out_after)

    print(f"\n[RESULTADO]")
    print(f"  Errores antes : {errors_before}")
    print(f"  MD040 fijados : {md040_fixed}")
    print(f"  Errores ahora : {errors_after}")

    if errors_after == 0:
        print("  Estado        : LIMPIO - listo para git push")
        sys.exit(0)
    else:
        print("  Estado        : REQUIERE ATENCION MANUAL")
        print("\n  Errores restantes:")
        for line in out_after.splitlines():
            if "MD" in line and "error" not in line.lower():
                print(f"    {line}")
        sys.exit(1)


if __name__ == "__main__":
    main()
