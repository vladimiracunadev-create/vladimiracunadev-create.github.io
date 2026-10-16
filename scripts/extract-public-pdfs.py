#!/usr/bin/env python3
"""Refresh tracked text extractions for every public root-level PDF."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import time

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "sources" / "extracted"

def extract(path: Path) -> str:
    reader = PdfReader(path)
    return "\n\n".join((page.extract_text() or "").strip() for page in reader.pages).strip()


def write_with_retry(destination: Path, content: str) -> None:
    """Tolerate brief Windows scanner/indexer locks on tracked extraction files."""
    for attempt in range(5):
        try:
            destination.write_text(content, encoding="utf-8", newline="\n")
            return
        except OSError:
            if attempt == 4:
                raise
            time.sleep(0.25 * (attempt + 1))


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().isoformat()
    too_short = []
    pdfs = sorted(ASSETS.glob("*.pdf"), key=lambda path: path.name)
    if len(pdfs) != 154:
        raise RuntimeError(f"Se esperaban 154 PDFs públicos y se encontraron {len(pdfs)}")
    expected_outputs = {
        f"{source.stem.replace('_', '-')}.extracted.txt" for source in pdfs
    }
    for stale in OUTPUT.glob("*.extracted.txt"):
        if stale.name not in expected_outputs:
            stale.unlink()

    for source in pdfs:
        name = source.stem.replace("_", "-")
        filename = source.name
        text = "\n".join(line.rstrip() for line in extract(source).splitlines()).strip()
        if len(text) < 200:
            too_short.append(filename)
        destination = OUTPUT / f"{name}.extracted.txt"
        write_with_retry(
            destination,
            f"# SOURCE: assets/{filename}\n# DATE: {stamp}\n\n{text}\n",
        )
        print(f"OK [{len(text)} chars] -> {destination.relative_to(ROOT)}")
    if too_short:
        raise RuntimeError("PDFs que requieren OCR: " + ", ".join(too_short))
    print(f"OK: {len(pdfs)} PDFs extraídos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
