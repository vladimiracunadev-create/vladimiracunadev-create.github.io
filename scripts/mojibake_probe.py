#!/usr/bin/env python3
"""Detect and optionally repair UTF-8 text decoded as Windows-1252.

The repair is conservative: a line changes only when the reverse Windows-1252
round trip produces valid UTF-8 and reduces common mojibake markers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".md", ".mjs", ".py", ".ps1",
    ".sh", ".txt", ".webmanifest", ".xml", ".yaml", ".yml",
}
SKIP_DIRS = {
    ".git", ".gradle-user-home", "dist", "dist-release", "node_modules",
    "assets", "sources",
}
MARKERS = ("Ã", "Â", "â", "ð", "ï")


def _sloppy_cp1252_bytes(text: str) -> bytes:
    result = bytearray()
    for char in text:
        try:
            result.extend(char.encode("cp1252"))
        except UnicodeEncodeError:
            codepoint = ord(char)
            if codepoint <= 0xFF:
                result.append(codepoint)
            else:
                raise
    return bytes(result)


def _marker_score(text: str) -> int:
    return sum(text.count(marker) for marker in MARKERS)


def repair_line(line: str) -> str:
    current = line
    for _ in range(3):
        if _marker_score(current) == 0:
            break
        try:
            candidate = _sloppy_cp1252_bytes(current).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            break
        if _marker_score(candidate) >= _marker_score(current):
            break
        current = candidate
    return current


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS or part.startswith(".gradle-user-home-") for part in path.parts):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    findings = []
    for path in iter_text_files(root):
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        repaired = "".join(repair_line(line) for line in original.splitlines(keepends=True))
        if repaired == original:
            continue
        findings.append(str(path.relative_to(root)))
        if args.fix:
            path.write_text(repaired, encoding="utf-8", newline="")

    print(json.dumps({"changed" if args.fix else "candidates": findings}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
