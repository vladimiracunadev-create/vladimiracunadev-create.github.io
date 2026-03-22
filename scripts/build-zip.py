"""
build-zip.py — Genera el ZIP de despliegue para AWS y otros ambientes.

Incluye solo los archivos web públicos. Excluye todo lo que no es
necesario en producción: scripts de generación, node_modules, backups,
archivos de dev, docs internos, etc.

Uso:
    python scripts/build-zip.py
    python scripts/build-zip.py --output mi-nombre.zip

Salida:
    portfolio-bundle-YYYY-MM-DD.zip en la raíz del proyecto
"""

import os
import zipfile
import argparse
from datetime import date
from pathlib import Path

# ── Raíz del proyecto (un nivel arriba de scripts/)
ROOT = Path(__file__).parent.parent.resolve()

# ── Archivos individuales a incluir en la raíz
ROOT_FILES = [
    "index.html",
    "app.js",
    "styles.css",
    "pwa.js",
    "service-worker.js",
    "manifest.webmanifest",
    "offline.html",
    "robots.txt",
    "sitemap.xml",
    "llm.txt",
]

# ── Directorios a incluir completos (con filtros de exclusión)
DIRS_INCLUDE = [
    "api",
    "experiencia-3d",
]

# ── assets/ se incluye con exclusiones específicas
ASSETS_EXCLUDE_DIRS = {"backups", "no_aplica", "por_solicitud"}
ASSETS_EXCLUDE_EXT  = {".docx", ".doc", ".xlsx"}
ASSETS_EXCLUDE_FILES = {"LEEME_PDFS.txt"}


def should_include_asset(rel_path: str) -> bool:
    parts = Path(rel_path).parts
    # excluir subdirectorios específicos
    if len(parts) > 1 and parts[0] in ASSETS_EXCLUDE_DIRS:
        return False
    # excluir extensiones no web
    if Path(rel_path).suffix.lower() in ASSETS_EXCLUDE_EXT:
        return False
    # excluir archivos txt de aviso interno
    if Path(rel_path).name in ASSETS_EXCLUDE_FILES:
        return False
    return True


def build_zip(output_name: str | None = None) -> Path:
    today = date.today().isoformat()
    zip_name = output_name or f"portfolio-bundle-{today}.zip"
    zip_path = ROOT / zip_name

    added = []
    skipped = []

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:

        # 1. Archivos raíz individuales
        for fname in ROOT_FILES:
            src = ROOT / fname
            if src.exists():
                zf.write(src, fname)
                added.append(fname)
            else:
                skipped.append(f"MISSING: {fname}")

        # 2. Directorios completos (api/, experiencia-3d/)
        for dirname in DIRS_INCLUDE:
            dir_path = ROOT / dirname
            if not dir_path.exists():
                skipped.append(f"MISSING DIR: {dirname}/")
                continue
            for file in dir_path.rglob("*"):
                if file.is_file():
                    rel = file.relative_to(ROOT)
                    zf.write(file, str(rel).replace("\\", "/"))
                    added.append(str(rel))

        # 3. assets/ con filtros
        assets_dir = ROOT / "assets"
        if assets_dir.exists():
            for file in assets_dir.rglob("*"):
                if file.is_file():
                    rel = file.relative_to(assets_dir)
                    rel_str = str(rel).replace("\\", "/")
                    if should_include_asset(rel_str):
                        arc_name = f"assets/{rel_str}"
                        zf.write(file, arc_name)
                        added.append(arc_name)
                    else:
                        skipped.append(f"excluded: assets/{rel_str}")
        else:
            skipped.append("MISSING DIR: assets/")

    # ── Reporte
    size_mb = zip_path.stat().st_size / 1_048_576
    print(f"\n[OK] ZIP generado: {zip_name}")
    print(f"   Tamano     : {size_mb:.1f} MB")
    print(f"   Archivos   : {len(added)} incluidos, {len(skipped)} excluidos/omitidos")
    print(f"   Ruta       : {zip_path}\n")

    # Mostrar excluidos importantes (solo MISSING)
    missing = [s for s in skipped if s.startswith("MISSING")]
    if missing:
        print("[!] Archivos faltantes:")
        for m in missing:
            print(f"   {m}")

    return zip_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera el ZIP de despliegue del portafolio.")
    parser.add_argument("--output", help="Nombre del archivo ZIP (default: portfolio-bundle-YYYY-MM-DD.zip)")
    args = parser.parse_args()
    build_zip(args.output)
