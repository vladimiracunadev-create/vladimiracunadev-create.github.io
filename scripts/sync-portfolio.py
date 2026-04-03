#!/usr/bin/env python3
"""
sync-portfolio.py — CLI de sincronización automática del portafolio

Uso:
    python scripts/sync-portfolio.py              # dry-run (solo reporte)
    python scripts/sync-portfolio.py --apply      # aplica cambios + commit + push
    python scripts/sync-portfolio.py --apply --no-push   # aplica sin push
    python scripts/sync-portfolio.py --apply --skip-pdfs # sin regenerar PDFs
    python scripts/sync-portfolio.py --apply --only-api  # solo actualiza api/v1/

Qué hace:
    1. Detecta repos públicos nuevos en GitHub (no listados en api/v1/projects.json)
    2. Actualiza api/v1/*.json (generated_at, label en profile, nuevos proyectos)
    3. Actualiza README del perfil GitHub con repos nuevos
    4. Crea backup de PDFs en assets/backups/YYYY-MM-DD/
    5. Regenera los 30 PDFs (si no se usa --skip-pdfs)
    6. Actualiza CHANGELOG.md
    7. Commit + push (si se usa --apply y no --no-push)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

# Forzar UTF-8 en la salida de la consola (Windows)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent.resolve()
API_DIR = ROOT / "api" / "v1"
ASSETS_DIR = ROOT / "assets"
SCRIPTS_DIR = ROOT / "scripts"
TODAY = date.today().isoformat()

# ── Repos permanentemente ocultos (nunca publicar) ───────────────────────────
HIDDEN_REPOS = {"rootcause-windows-inspector", "rootcause-landing"}

# ── Identidad del perfil (actualizar aquí si cambia) ─────────────────────────
PROFILE_LABEL = (
    "Arquitecto de Soluciones | Senior Full-Stack | "
    "Modernización Legacy, Automatización e Integración de IA Aplicada"
)

# ── Mapa de categorías por repo ───────────────────────────────────────────────
REPO_CATEGORIES = {
    "proyectos-aws": "cloud",
    "social-bot-scheduler": "orchestration",
    "docker-labs": "platform",
    "microsistemas": "tooling",
    "langgraph-realworld": "ai",
    "mcp-ollama-local": "ai",
    "unikernel-labs": "platform",
    "chofyai-studio": "ai",
    "vladimiracunadev-create.github.io": "portfolio",
}

# ── Repos que NO se agregan como proyectos (perfil, portfolio web) ────────────
SKIP_AS_PROJECT = {
    "vladimiracunadev-create",
    "vladimiracunadev-create.github.io",
    "portal-bienestar",
}


def run(cmd, check=True, capture=False):
    """Ejecuta un comando shell."""
    result = subprocess.run(
        cmd, shell=True, check=check,
        capture_output=capture, text=True
    )
    return result


def run_capture(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def log(msg, level="INFO"):
    prefix = {"INFO": "  ", "OK": "[OK]  ", "WARN": "[!!]  ", "ERR": "[ERR] ", "HEAD": "\n>>>  "}
    print(f"{prefix.get(level, '  ')}{msg}")


# ─────────────────────────────────────────────────────────────────────────────
# 1. GITHUB — listar repos públicos
# ─────────────────────────────────────────────────────────────────────────────

def get_public_repos():
    """Devuelve lista de repos públicos de la organización."""
    log("Consultando repos GitHub...", "HEAD")
    out, code = run_capture(
        'gh repo list vladimiracunadev-create --limit 50 '
        '--json name,isPrivate,description,updatedAt,url'
    )
    if code != 0:
        log("No se pudo conectar a GitHub (¿gh auth login?)", "WARN")
        return []
    repos = json.loads(out)
    public = [r for r in repos if not r["isPrivate"] and r["name"] not in HIDDEN_REPOS]
    log(f"{len(public)} repos públicos encontrados (excluidos ocultos)", "OK")
    return public


# ─────────────────────────────────────────────────────────────────────────────
# 2. DETECTAR repos nuevos no en projects.json
# ─────────────────────────────────────────────────────────────────────────────

def get_known_repo_urls():
    """Devuelve set de URLs ya documentadas en projects.json."""
    projects_file = API_DIR / "projects.json"
    data = json.loads(projects_file.read_text(encoding="utf-8"))
    known = set()
    for p in data.get("projects", []):
        if p.get("url"):
            known.add(p["url"].rstrip("/"))
    return known


def detect_new_repos(public_repos, known_urls):
    """Encuentra repos públicos no documentados aún."""
    new = []
    for r in public_repos:
        if r["name"] in SKIP_AS_PROJECT:
            continue
        url = f"https://github.com/vladimiracunadev-create/{r['name']}"
        if url not in known_urls:
            new.append(r)
    return new


# ─────────────────────────────────────────────────────────────────────────────
# 3. ACTUALIZAR api/v1/*.json
# ─────────────────────────────────────────────────────────────────────────────

def update_api_json(new_repos, apply=False):
    """Actualiza generated_at, profile label y agrega repos nuevos."""
    log("Actualizando api/v1/...", "HEAD")
    changes = []

    # Todos los JSONs: actualizar generated_at
    for json_file in API_DIR.glob("*.json"):
        data = json.loads(json_file.read_text(encoding="utf-8"))
        meta = data.get("meta", {})
        if meta.get("generated_at") != TODAY:
            changes.append(f"  {json_file.name}: generated_at → {TODAY}")
            if apply:
                meta["generated_at"] = TODAY
                data["meta"] = meta
                json_file.write_text(
                    json.dumps(data, ensure_ascii=False, indent=4),
                    encoding="utf-8"
                )

    # profile.json: label
    profile_file = API_DIR / "profile.json"
    profile = json.loads(profile_file.read_text(encoding="utf-8"))
    if profile.get("label") != PROFILE_LABEL:
        changes.append(f"  profile.json: label actualizado")
        if apply:
            profile["label"] = PROFILE_LABEL
            profile_file.write_text(
                json.dumps(profile, ensure_ascii=False, indent=4),
                encoding="utf-8"
            )

    # projects.json: agregar repos nuevos
    if new_repos:
        projects_file = API_DIR / "projects.json"
        projects_data = json.loads(projects_file.read_text(encoding="utf-8"))
        for r in new_repos:
            entry = {
                "name": r["name"],
                "description": r.get("description") or "",
                "url": f"https://github.com/vladimiracunadev-create/{r['name']}",
                "tags": [],
                "category": REPO_CATEGORIES.get(r["name"], "other"),
            }
            changes.append(f"  projects.json: + {r['name']}")
            if apply:
                projects_data["projects"].append(entry)
        if apply:
            projects_file.write_text(
                json.dumps(projects_data, ensure_ascii=False, indent=4),
                encoding="utf-8"
            )

    if changes:
        for c in changes:
            log(c, "WARN" if not apply else "OK")
    else:
        log("api/v1/ ya está al día", "OK")
    return changes


# ─────────────────────────────────────────────────────────────────────────────
# 4. BACKUP de PDFs
# ─────────────────────────────────────────────────────────────────────────────

def backup_pdfs(apply=False):
    """Copia PDFs actuales a assets/backups/YYYY-MM-DD/ con sufijo _v1."""
    backup_dir = ASSETS_DIR / "backups" / TODAY
    pdfs = list(ASSETS_DIR.glob("*.pdf"))
    if not pdfs:
        log("No hay PDFs en assets/ para respaldar", "WARN")
        return

    if backup_dir.exists():
        log(f"Backup {TODAY} ya existe — omitiendo", "OK")
        return

    log(f"Creando backup en assets/backups/{TODAY}/", "HEAD")
    if apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        for pdf in pdfs:
            dest = backup_dir / f"{pdf.stem}_v1.pdf"
            shutil.copy2(pdf, dest)
        log(f"{len(pdfs)} PDFs respaldados", "OK")
    else:
        log(f"[dry-run] Se respaldarían {len(pdfs)} PDFs", "WARN")


# ─────────────────────────────────────────────────────────────────────────────
# 5. REGENERAR PDFs
# ─────────────────────────────────────────────────────────────────────────────

def regenerate_pdfs(apply=False):
    """Ejecuta los scripts de generación de PDFs."""
    log("Regenerando PDFs...", "HEAD")
    scripts = [
        "generate-all-languages.py",
        "generate-portfolio.py",
        "generate-achievements-statement.py",
        "generate-recommendation-letter.py",
    ]
    for script_name in scripts:
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            log(f"{script_name} no encontrado — omitido", "WARN")
            continue
        if apply:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(ROOT), capture_output=True, text=True
            )
            if result.returncode == 0:
                log(f"{script_name} ✓", "OK")
            else:
                log(f"{script_name} falló:\n{result.stderr}", "ERR")
        else:
            log(f"[dry-run] Ejecutaría: {script_name}", "WARN")


# ─────────────────────────────────────────────────────────────────────────────
# 6. README perfil GitHub
# ─────────────────────────────────────────────────────────────────────────────

def update_github_readme(new_repos, apply=False):
    """Agrega secciones para repos nuevos en el README del perfil GitHub."""
    if not new_repos:
        log("README GitHub: sin repos nuevos que agregar", "OK")
        return

    log("Actualizando README perfil GitHub...", "HEAD")

    # Leer README actual
    out, code = run_capture(
        "gh api repos/vladimiracunadev-create/vladimiracunadev-create"
        "/contents/README.md --jq '.content,.sha'"
    )
    if code != 0:
        log("No se pudo leer README de GitHub", "WARN")
        return

    lines = out.strip().split("\n")
    sha = lines[-1]
    import base64
    content_b64 = "\n".join(lines[:-1])
    readme = base64.b64decode(content_b64).decode("utf-8")

    # Insertar secciones nuevas antes del separador "---\n\n## ⚡"
    separator = "---\n\n## ⚡"
    new_sections = ""
    for r in new_repos:
        url = f"https://github.com/vladimiracunadev-create/{r['name']}"
        desc = r.get("description") or "Repositorio público."
        new_sections += (
            f"\n### 🔧 {r['name']}\n"
            f"**Repo:** {url}\n"
            f"**Qué demuestra:** {desc}\n"
        )

    updated_readme = readme.replace(separator, new_sections + separator, 1)

    if apply:
        encoded = base64.b64encode(updated_readme.encode("utf-8")).decode("ascii")
        result = subprocess.run(
            [
                "gh", "api", "--method", "PUT",
                "repos/vladimiracunadev-create/vladimiracunadev-create/contents/README.md",
                "--field", f"message=feat: add {', '.join(r['name'] for r in new_repos)} to profile README",
                "--field", f"content={encoded}",
                "--field", f"sha={sha}",
                "--jq", ".commit.sha"
            ],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            log(f"README actualizado → commit {result.stdout.strip()[:8]}", "OK")
        else:
            log(f"Error actualizando README: {result.stderr}", "ERR")
    else:
        for r in new_repos:
            log(f"[dry-run] Agregaría sección: {r['name']}", "WARN")


# ─────────────────────────────────────────────────────────────────────────────
# 7. CHANGELOG
# ─────────────────────────────────────────────────────────────────────────────

def update_changelog(new_repos, api_changes, skip_pdfs, apply=False):
    """Prepende entrada en CHANGELOG.md."""
    changelog = ROOT / "CHANGELOG.md"
    items = []
    if api_changes:
        items.append("- `api/v1/`: generated_at actualizado a " + TODAY)
    if new_repos:
        names = ", ".join(r["name"] for r in new_repos)
        items.append(f"- `api/v1/projects.json`: repos nuevos agregados: {names}")
    if not skip_pdfs:
        items.append("- 30 PDFs regenerados (5 tipos × 6 idiomas)")
        items.append(f"- Backup en `assets/backups/{TODAY}/`")

    if not items:
        log("CHANGELOG: sin cambios que registrar", "OK")
        return

    entry = f"## {TODAY}\n\n### sync-portfolio (automático)\n\n" + "\n".join(items) + "\n\n"
    log("Actualizando CHANGELOG.md...", "HEAD")
    if apply:
        original = changelog.read_text(encoding="utf-8")
        # Insertar después de la primera línea "# Changelog"
        updated = original.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
        changelog.write_text(updated, encoding="utf-8")
        log("CHANGELOG.md actualizado", "OK")
    else:
        log("[dry-run] Agregaría entrada en CHANGELOG.md", "WARN")


# ─────────────────────────────────────────────────────────────────────────────
# 8. COMMIT + PUSH
# ─────────────────────────────────────────────────────────────────────────────

def git_commit_push(new_repos, skip_pdfs, no_push, apply=False):
    """Staging selectivo, commit y push."""
    if not apply:
        log("[dry-run] Haría commit + push", "WARN")
        return

    log("Preparando commit...", "HEAD")

    # Stage api/v1/, CHANGELOG y backups
    run(f'git -C "{ROOT}" add api/v1/ CHANGELOG.md', check=False)
    if not skip_pdfs:
        run(f'git -C "{ROOT}" add assets/', check=False)

    # Construir mensaje
    parts = [f"chore(sync): auto-sync {TODAY}"]
    details = []
    if new_repos:
        details.append(f"repos nuevos: {', '.join(r['name'] for r in new_repos)}")
    if not skip_pdfs:
        details.append("30 PDFs regenerados")
    details.append("api/v1/ generated_at actualizado")
    if details:
        parts.append("\n\n" + "\n".join(f"- {d}" for d in details))
    parts.append("\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>")
    msg = "".join(parts)

    result = run(f'git -C "{ROOT}" commit -m "{msg}"', check=False, capture=True)
    if result.returncode == 0:
        log("Commit creado", "OK")
    elif "nothing to commit" in result.stdout + result.stderr:
        log("Nada que commitear — ya está al día", "OK")
        return
    else:
        log(f"Error en commit: {result.stderr}", "ERR")
        return

    if not no_push:
        result = run(f'git -C "{ROOT}" push', check=False, capture=True)
        if result.returncode == 0:
            log("Push exitoso", "OK")
        else:
            log(f"Error en push: {result.stderr}", "ERR")
    else:
        log("--no-push activo: push omitido", "WARN")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza automáticamente el portafolio (API, PDFs, README, GitHub)."
    )
    parser.add_argument("--apply", action="store_true",
                        help="Aplica cambios (sin --apply es dry-run)")
    parser.add_argument("--no-push", action="store_true",
                        help="Aplica cambios pero no hace push")
    parser.add_argument("--skip-pdfs", action="store_true",
                        help="Omite la regeneración de PDFs")
    parser.add_argument("--only-api", action="store_true",
                        help="Solo actualiza api/v1/ (implica --skip-pdfs)")
    args = parser.parse_args()

    skip_pdfs = args.skip_pdfs or args.only_api
    apply = args.apply

    if not apply:
        print("\n" + "="*60)
        print("  MODO DRY-RUN — ningún archivo será modificado")
        print("  Usa --apply para ejecutar los cambios")
        print("="*60)

    # 1. Repos públicos
    public_repos = get_public_repos()
    known_urls = get_known_repo_urls()
    new_repos = detect_new_repos(public_repos, known_urls)

    if new_repos:
        log(f"Repos nuevos detectados: {[r['name'] for r in new_repos]}", "WARN")
    else:
        log("No hay repos públicos nuevos", "OK")

    # 2. API JSONs
    api_changes = update_api_json(new_repos, apply=apply)

    # 3. GitHub README (solo si hay repos nuevos)
    if new_repos:
        update_github_readme(new_repos, apply=apply)

    # 4. Backup PDFs
    if not skip_pdfs:
        backup_pdfs(apply=apply)

    # 5. Regenerar PDFs
    if not skip_pdfs:
        regenerate_pdfs(apply=apply)

    # 6. CHANGELOG
    update_changelog(new_repos, api_changes, skip_pdfs, apply=apply)

    # 7. Commit + Push
    if not args.only_api:
        git_commit_push(new_repos, skip_pdfs, args.no_push, apply=apply)

    # Resumen final
    print("\n" + "="*60)
    if apply:
        print(f"  SYNC COMPLETADO — {TODAY}")
    else:
        print(f"  DRY-RUN completado. Ejecuta con --apply para aplicar.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
