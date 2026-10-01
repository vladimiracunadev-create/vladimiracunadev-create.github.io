#!/usr/bin/env python3
"""Refresh the tracked text extractions for the public ES/EN PDF set."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "sources" / "extracted"

PDFS = {
    "cv-ats": "cv-ats.pdf",
    "cv-ats-english": "cv-ats-english.pdf",
    "cv-reclutador": "cv-reclutador.pdf",
    "cv-reclutador-english": "cv-reclutador-english.pdf",
    "portafolio": "portafolio.pdf",
    "portafolio-english": "portafolio-english.pdf",
    "carta-recomendacion": "carta-recomendacion_sin_firma.pdf",
    "carta-recomendacion-english": "carta-recomendacion_sin_firma-english.pdf",
    "declaracion-logros-validacion": "declaracion-logros-validacion.pdf",
    "declaracion-logros-validacion-english": "declaracion-logros-validacion-english.pdf",
}


def extract(path: Path) -> str:
    reader = PdfReader(path)
    return "\n\n".join((page.extract_text() or "").strip() for page in reader.pages).strip()


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().isoformat()
    too_short = []
    for name, filename in PDFS.items():
        source = ASSETS / filename
        text = extract(source)
        if len(text) < 200:
            too_short.append(filename)
        destination = OUTPUT / f"{name}.extracted.txt"
        destination.write_text(
            f"# SOURCE: assets/{filename}\n# DATE: {stamp}\n\n{text}\n",
            encoding="utf-8",
            newline="\n",
        )
        print(f"OK [{len(text)} chars] -> {destination.relative_to(ROOT)}")
    if too_short:
        raise RuntimeError("PDFs que requieren OCR: " + ", ".join(too_short))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
