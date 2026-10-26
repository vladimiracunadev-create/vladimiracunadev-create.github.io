#!/usr/bin/env python3
"""Generate the runtime portfolio translation catalog.

The canonical professional content remains ``index.html``. Existing inline
translations are reused whenever their DOM structure matches Spanish; only
missing units are translated. The Argos provider runs entirely on the local
machine and uses the completed English catalog as its pivot.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import requests

from bs4 import BeautifulSoup, Comment, NavigableString


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"
CONTRACT_PATH = ROOT / "data" / "portfolio-i18n.json"
CATALOG_PATH = Path(os.environ.get(
    "PORTFOLIO_TRANSLATION_CATALOG",
    ROOT / "data" / "portfolio-translations.json",
))
JS_PATH = Path(os.environ.get(
    "PORTFOLIO_TRANSLATION_JS",
    ROOT / "i18n" / "translations.js",
))
PROGRESS_PATH = Path(os.environ.get(
    "PORTFOLIO_TRANSLATION_PROGRESS",
    ROOT / "tmp" / "portfolio-translations-progress-v2.json",
))
ARGOS_VENDOR_PATH = ROOT / ".vendor" / "argos"
OPENCC_VENDOR_PATH = ROOT / ".vendor" / "opencc"
_OPENCC_TW = None
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
GOOGLE_URL = "https://translate.googleapis.com/translate_a/single"
SKIP_TEXT_PARENTS = {"code", "pre", "kbd", "samp", "script", "style", "option", "title"}
TRANSLATABLE_ATTRIBUTES = ("title", "aria-label", "placeholder", "alt")

RUNTIME_SOURCES = {
    "copied": "Copiado ✔",
    "copy_email": "Copia el email:",
    "repos_error": "No se pudo cargar la lista.",
    "activity_error": "No se pudo cargar la actividad.",
    "ago_days": "hace {count}d",
    "ago_hours": "hace {count}h",
    "ago_minutes": "hace {count}m",
    "commits": "commits",
    "releases": "releases",
    "repos": "repos",
    "detected_platform": "Plataforma detectada: {platform}",
    "unknown_platform": "Plataforma no identificada",
    "download_apk": "Descargar APK",
    "download_apk_emulator": "Descargar APK (Emulador)",
    "install_pwa": "Instalar PWA",
    "install_pwa_desktop": "Instalar PWA (Desktop)",
    "install_pwa_app": "Instalar como App (PWA)",
    "document_title": "Vladimir Acuña — Arquitecto de Soluciones · Senior Full-Stack",
}

CODE_OVERRIDES = {"zh": "zh-Hans", "zh-TW": "zh-Hant"}
GOOGLE_CODE_OVERRIDES = {"zh": "zh-CN", "zh-TW": "zh-TW"}
BING_CODE_OVERRIDES = {"zh": "zh-Hans", "zh-TW": "zh-Hant"}
_BING_CLIENT = None


def text_nodes(element):
    return [
        node for node in element.descendants
        if isinstance(node, NavigableString)
        and not isinstance(node, Comment)
        and str(node).strip()
        and node.parent.name not in SKIP_TEXT_PARENTS
    ]


def language_attribute(element, inline_codes: set[str]) -> str | None:
    for ancestor in (element, *element.parents):
        for code in inline_codes:
            if ancestor.has_attr(f"data-{code}"):
                return code
    return None


def canonical_text_nodes(soup: BeautifulSoup, inline_codes: set[str]):
    nodes = []
    for node in soup.body.descendants:
        if (
            not isinstance(node, NavigableString)
            or isinstance(node, Comment)
            or not str(node).strip()
            or node.parent.name in SKIP_TEXT_PARENTS
        ):
            continue
        localized = language_attribute(node.parent, inline_codes)
        if localized is not None and localized != "es":
            continue
        if any(character.isalpha() for character in str(node)):
            nodes.append(node)
    return nodes


def extract_units(soup: BeautifulSoup, inline_codes: set[str]) -> list[dict]:
    units = []
    for index, node in enumerate(canonical_text_nodes(soup, inline_codes)):
        units.append({"key": f"u{index:04d}", "node": node, "source": str(node).strip()})
    return units


def extract_attributes(soup: BeautifulSoup) -> list[dict]:
    attributes = []
    for element in soup.find_all(True):
        for attribute in TRANSLATABLE_ATTRIBUTES:
            value = element.get(attribute)
            if value and any(character.isalpha() for character in value):
                attributes.append({
                    "key": f"a{len(attributes):04d}_{attribute}",
                    "attribute": attribute,
                    "source": value,
                })
    return attributes


def seed_inline_locale(soup: BeautifulSoup, locale: str, units: list[dict]) -> dict[str, str]:
    seeded = {}
    keys_by_node = {id(unit["node"]): unit["key"] for unit in units}
    for element_index, spanish in enumerate(soup.select("[data-es]")):
        spanish_nodes = text_nodes(spanish)
        sibling = next((
            candidate for candidate in spanish.parent.find_all(recursive=False)
            if candidate.name == spanish.name and candidate.has_attr(f"data-{locale}")
        ), None)
        if sibling is None:
            continue
        localized_nodes = text_nodes(sibling)
        if len(spanish_nodes) != len(localized_nodes):
            continue
        for spanish_node, localized in zip(spanish_nodes, localized_nodes):
            key = keys_by_node.get(id(spanish_node))
            if key:
                seeded[key] = str(localized).strip()
    return seeded


def read_progress() -> dict:
    if not PROGRESS_PATH.exists():
        return {"locales": {}}
    return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))


def write_progress(progress: dict) -> None:
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def prompt(source_text: str, target_name: str, target_code: str) -> str:
    return (
        f"You are a professional Spanish (es) to {target_name} ({target_code}) translator. "
        f"Your goal is to accurately convey the meaning and nuances of the original Spanish "
        f"text while adhering to {target_name} grammar, vocabulary, and cultural sensitivities.\n"
        f"Produce only the {target_name} translation, without any additional explanations or "
        f"commentary. Preserve every marker of the form [[[U0000]]], all placeholders inside "
        f"curly braces, URLs, product names and line order. Please translate the following "
        f"Spanish text into {target_name}:\n\n\n{source_text}"
    )


def ollama_translate(model: str, source_text: str, target_name: str, target_code: str) -> str:
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt(source_text, target_name, target_code)}],
        "stream": False,
        "keep_alive": "30m",
        "options": {"temperature": 0, "num_predict": 8192},
    }).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=900) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(f"Local Ollama request failed: {error}") from error
    return result["message"]["content"].strip()


def google_translate(source_text: str, target_code: str) -> str:
    payload = urllib.parse.urlencode({
        "client": "gtx",
        "sl": "es",
        "tl": GOOGLE_CODE_OVERRIDES.get(target_code, target_code),
        "dt": "t",
        "q": source_text,
    }).encode("utf-8")
    request = urllib.request.Request(
        GOOGLE_URL,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "portfolio-i18n-generator/1.0",
        },
        method="POST",
    )
    last_error = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
            return "".join(segment[0] for segment in result[0] if segment and segment[0]).strip()
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
            is_rate_limit = isinstance(error, urllib.error.HTTPError) and error.code == 429
            time.sleep((30 * (attempt + 1)) if is_rate_limit else (2 ** attempt))
    raise RuntimeError(f"Google Translate request failed: {last_error}")


class BingClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/141.0 Safari/537.36",
            "Referer": "https://www.bing.com/translator",
        })
        self.sequence = 0
        self.refresh()

    def refresh(self):
        html = self.session.get("https://www.bing.com/translator", timeout=30).text
        self.ig = re.search(r'IG:"([^"]+)', html).group(1)
        token_match = re.search(
            r'params_AbusePreventionHelper\s*=\s*\[(\d+),"([^"]+)",(\d+)\]',
            html,
        )
        self.key, self.token = token_match.group(1), token_match.group(2)
        iid_match = re.search(r'data-iid="([^"]+)', html)
        self.iid = iid_match.group(1) if iid_match else "translator.5023"
        self.sequence = 0

    def translate(self, source_text: str, target_code: str) -> str:
        last_error = None
        for attempt in range(4):
            self.sequence += 1
            response = self.session.post(
                f"https://www.bing.com/ttranslatev3?isVertical=1&IG={self.ig}"
                f"&IID={self.iid}.{self.sequence}",
                data={
                    "fromLang": "es",
                    "to": BING_CODE_OVERRIDES.get(target_code, target_code),
                    "text": source_text,
                    "token": self.token,
                    "key": self.key,
                },
                timeout=60,
            )
            if response.ok:
                payload = response.json()
                if isinstance(payload, list) and payload and payload[0].get("translations"):
                    return payload[0]["translations"][0]["text"].strip()
                last_error = f"Unexpected response: {str(payload)[:200]}"
                self.refresh()
                continue
            last_error = f"HTTP {response.status_code}: {response.text[:200]}"
            self.refresh()
            time.sleep(2 ** attempt)
        raise RuntimeError(f"Bing Translate request failed: {last_error}")


def bing_translate(source_text: str, target_code: str) -> str:
    global _BING_CLIENT
    if _BING_CLIENT is None:
        _BING_CLIENT = BingClient()
    return _BING_CLIENT.translate(source_text, target_code)


def chunks(items: list[str], max_chars: int = 9000, max_items: int = 100):
    current = []
    size = 0
    for item in items:
        item_size = len(item) + 20
        if current and (len(current) >= max_items or size + item_size > max_chars):
            yield current
            current = []
            size = 0
        current.append(item)
        size += item_size
    if current:
        yield current


def parse_marked(output: str, expected: int) -> dict[int, str]:
    pattern = re.compile(r"\[\[\[U(\d{4})\]\]\]\s*(.*?)(?=\n\s*\[\[\[U\d{4}\]\]\]|\Z)", re.S)
    parsed = {int(match.group(1)): match.group(2).strip() for match in pattern.finditer(output)}
    return {index: value for index, value in parsed.items() if index < expected and value}


def translate_sources(
    sources: list[str], target_name: str, target_code: str, model: str,
    provider: str, cached: dict[str, str], checkpoint=None
) -> dict[str, str]:
    pending = [source for source in dict.fromkeys(sources) if source not in cached]
    batches = list(chunks(
        pending,
        max_chars=900 if provider == "bing" else 9000,
        max_items=25 if provider == "bing" else 100,
    ))
    for batch_number, batch in enumerate(batches, start=1):
        marked = "\n".join(f"[[[U{index:04d}]]] {source}" for index, source in enumerate(batch))
        if provider == "google":
            output = google_translate(marked, target_code)
        elif provider == "bing":
            output = bing_translate(marked, target_code)
        else:
            output = ollama_translate(model, marked, target_name, CODE_OVERRIDES.get(target_code, target_code))
        parsed = parse_marked(output, len(batch))
        for index, source in enumerate(batch):
            translated = parsed.get(index)
            if translated is None:
                translated = (
                    google_translate(source, target_code)
                    if provider == "google"
                    else bing_translate(source, target_code)
                    if provider == "bing"
                    else ollama_translate(model, source, target_name, CODE_OVERRIDES.get(target_code, target_code))
                )
            cached[source] = translated
        if checkpoint:
            checkpoint()
        print(f"  batch {batch_number}/{len(batches)} ({len(batch)} units)", flush=True)
        if provider == "google":
            time.sleep(1.5)
        elif provider == "bing":
            time.sleep(0.15)
    return cached


def argos_translation(source_code: str, target_code: str):
    """Return one installed local translation package and fast batch engine."""
    if ARGOS_VENDOR_PATH.exists():
        sys.path.insert(0, str(ARGOS_VENDOR_PATH))
    try:
        import ctranslate2
        from argostranslate import package as argos_package
    except ImportError as error:
        raise RuntimeError(
            "Argos Translate is not installed under .vendor/argos. "
            "Install it before using --provider argos."
        ) from error

    package = next((
        item for item in argos_package.get_installed_packages()
        if item.from_code == source_code and item.to_code == target_code and item.type == "translate"
    ), None)
    if package is None:
        raise RuntimeError(f"Missing installed Argos model {source_code} -> {target_code}")
    engine = ctranslate2.Translator(
        str(package.package_path / "model"),
        device="cpu",
        inter_threads=2,
        intra_threads=4,
        compute_type="default",
    )
    return package, engine


def protect_placeholders(value: str) -> tuple[str, dict[str, str]]:
    placeholders = {}

    def replace(match):
        token = f"ZXQPLACEHOLDER{len(placeholders)}QXZ"
        placeholders[token] = match.group(0)
        return token

    return re.sub(r"\{[^{}]+\}", replace, value), placeholders


def restore_placeholders(value: str, placeholders: dict[str, str]) -> str:
    for token, placeholder in placeholders.items():
        value = value.replace(token, placeholder)
        value = value.replace(token.lower(), placeholder)
    return value


def split_visual_prefix(value: str) -> tuple[str, str]:
    """Keep leading emoji and decorative punctuation outside the MT model."""
    for index, character in enumerate(value):
        if character.isalpha() or character.isdigit() or character == "{":
            return value[:index], value[index:]
    return "", value


def collapse_degenerate_repetition(value: str) -> str:
    """Collapse rare model loops where a one-word label repeats endlessly."""
    words = value.split()
    if len(words) > 1 and len({word.casefold() for word in words}) == 1:
        return words[0]
    for width in range(1, min(8, len(words) // 3) + 1):
        pattern = words[:width]
        if all(words[index] == pattern[index % width] for index in range(len(words))):
            return " ".join(pattern)
    return value


def has_repeated_ngram(value: str) -> bool:
    """Detect adjacent MT loops, including loops embedded in a longer sentence."""
    words = [re.sub(r"^\W+|\W+$", "", word, flags=re.UNICODE).casefold() for word in value.split()]
    words = [word for word in words if word and word not in {"quot", "amp", "nbsp"}]
    for width in range(1, min(12, len(words) // 2) + 1):
        minimum_repeats = 3 if width == 1 else 2
        span = width * minimum_repeats
        for start in range(0, len(words) - span + 1):
            pattern = words[start:start + width]
            if all(
                words[start + offset:start + offset + width] == pattern
                for offset in range(width, span, width)
            ):
                return True
    if len(words) >= 12:
        most_common = max((words.count(word) for word in set(words)), default=0)
        if most_common >= 5 and most_common / len(words) > 0.25:
            return True
    return False


def is_suspicious_translation(value: str, source: str) -> bool:
    """Reject unusable MT output so the documented Spanish key fallback is used."""
    mojibake = ("Ã", "Â", "ðŸ", "рї", "�")
    return (
        not value.strip()
        or len(value) >= 2500
        or (len(source) >= 40 and len(value) > len(source) * 5)
        or any(marker in value for marker in mojibake)
        or re.search(r"(?:[/\\-]\s*){6,}", value) is not None
        or re.search(r"(.{8,})\1{2,}", value, re.S) is not None
        or has_repeated_ngram(value)
    )


def apply_spanish_fallbacks(catalog: dict, units: list[dict], attributes: list[dict]) -> dict[str, int]:
    """Replace visibly corrupt generated values with the canonical Spanish source."""
    sources = {
        "translations": {item["key"]: item["source"] for item in units},
        "attributes": {item["key"]: item["source"] for item in attributes},
        "runtime": RUNTIME_SOURCES,
    }
    fallback_counts = {}
    for code, locale in catalog.get("locales", {}).items():
        count = 0
        for section, source_map in sources.items():
            for key, source in source_map.items():
                value = locale.get(section, {}).get(key, "")
                if is_suspicious_translation(value, source):
                    locale[section][key] = source
                    count += 1
        fallback_counts[code] = count
    return fallback_counts


def to_traditional_chinese(value: str) -> str:
    """Convert simplified output to the Traditional Chinese (Taiwan) variant."""
    global _OPENCC_TW
    if OPENCC_VENDOR_PATH.exists():
        sys.path.insert(0, str(OPENCC_VENDOR_PATH))
    try:
        from opencc import OpenCC
    except ImportError as error:
        raise RuntimeError(
            "OpenCC is required to generate zh-TW without simplified characters"
        ) from error
    if _OPENCC_TW is None:
        _OPENCC_TW = OpenCC("s2twp")
    return _OPENCC_TW.convert(value)


def translate_argos_sources(
    sources: list[str], source_code: str, target_code: str,
    cached: dict[str, str], checkpoint=None
) -> dict[str, str]:
    """Translate unique strings locally in efficient batches."""
    package, engine = argos_translation(source_code, target_code)
    pending = [source for source in dict.fromkeys(sources) if source not in cached]
    total = len(pending)
    for start in range(0, total, 100):
        batch = pending[start:start + 100]
        prepared = []
        for source in batch:
            protected, placeholders = protect_placeholders(source)
            prefix, translatable = split_visual_prefix(protected)
            prepared.append((translatable, placeholders, prefix))
        tokenized = [package.tokenizer.encode(value) for value, _, _ in prepared]
        target_prefix = None
        if package.target_prefix:
            target_prefix = [[package.target_prefix]] * len(tokenized)
        results = engine.translate_batch(
            tokenized,
            target_prefix=target_prefix,
            replace_unknowns=True,
            max_batch_size=100,
            batch_type="tokens",
            beam_size=1,
            num_hypotheses=1,
            length_penalty=0.2,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,
            return_scores=True,
        )
        for source, (_, placeholders, prefix), result in zip(batch, prepared, results):
            translated = package.tokenizer.decode(result.hypotheses[0]).strip()
            if package.target_prefix and translated.startswith(package.target_prefix):
                translated = translated[len(package.target_prefix):].strip()
            translated = collapse_degenerate_repetition(
                prefix + restore_placeholders(translated, placeholders)
            )
            if not translated:
                raise RuntimeError(f"Argos returned an empty translation for {target_code}: {source!r}")
            cached[source] = translated
        if checkpoint:
            checkpoint()
        print(f"  local units {min(start + len(batch), total)}/{total}", flush=True)
    return cached


def translation_chunks(value: str, max_chars: int = 150) -> list[str]:
    """Split long copy at natural boundaries before local neural translation."""
    parts = re.split(r"(?<=[.!?;:,])\s+", value)
    chunks_to_translate = []
    current = ""
    for part in parts:
        if len(part) > max_chars:
            words = part.split()
            subpart = ""
            for word in words:
                candidate = f"{subpart} {word}".strip()
                if subpart and len(candidate) > max_chars:
                    chunks_to_translate.append(subpart)
                    subpart = word
                else:
                    subpart = candidate
            if subpart:
                if current:
                    chunks_to_translate.append(current)
                    current = ""
                chunks_to_translate.append(subpart)
            continue
        candidate = f"{current} {part}".strip()
        if current and len(candidate) > max_chars:
            chunks_to_translate.append(current)
            current = part
        else:
            current = candidate
    if current:
        chunks_to_translate.append(current)
    return chunks_to_translate or [value]


def translate_argos_repairs(
    sources: list[str], source_code: str, target_code: str
) -> dict[str, str]:
    """Translate suspect values with segmentation and conservative decoding."""
    package, engine = argos_translation(source_code, target_code)
    unique_sources = list(dict.fromkeys(sources))
    prepared = []
    flat_chunks = []
    for source in unique_sources:
        protected, placeholders = protect_placeholders(source)
        prefix, translatable = split_visual_prefix(protected)
        parts = translation_chunks(translatable)
        prepared.append((source, placeholders, prefix, len(parts)))
        flat_chunks.extend(parts)
    results = engine.translate_batch(
        [package.tokenizer.encode(value) for value in flat_chunks],
        replace_unknowns=True,
        max_batch_size=100,
        batch_type="tokens",
        beam_size=4,
        num_hypotheses=1,
        length_penalty=0.2,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3,
        max_decoding_length=192,
    )
    decoded = [package.tokenizer.decode(result.hypotheses[0]).strip() for result in results]
    translated = {}
    offset = 0
    for source, placeholders, prefix, part_count in prepared:
        value = " ".join(decoded[offset:offset + part_count]).strip()
        offset += part_count
        if package.target_prefix and value.startswith(package.target_prefix):
            value = value[len(package.target_prefix):].strip()
        value = collapse_degenerate_repetition(prefix + restore_placeholders(value, placeholders))
        translated[source] = value
    return translated


def write_catalog(catalog: dict) -> None:
    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    JS_PATH.write_text(
        "/* Generated from data/portfolio-translations.json. */\n"
        "window.PORTFOLIO_TRANSLATIONS = "
        + json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )


def is_degenerate(value: str) -> bool:
    """Detect empty, runaway or visibly looping model output."""
    return (
        not value.strip()
        or len(value) >= 2500
        or re.search(r"(.{8,})\1{4,}", value, re.S) is not None
    )
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="translategemma:4b")
    parser.add_argument("--provider", choices=("ollama", "google", "bing", "argos"), default="ollama")
    parser.add_argument("--no-seed", action="store_true", help="Do not reuse legacy inline translations")
    parser.add_argument("--locales", nargs="*", help="Optional locale subset")
    parser.add_argument(
        "--repair-degenerate",
        action="store_true",
        help="Retranslate only empty, runaway or repeated catalog values",
    )
    parser.add_argument(
        "--sanitize-existing",
        action="store_true",
        help="Replace corrupt generated values with the canonical Spanish fallback",
    )
    args = parser.parse_args()

    index_text = INDEX_PATH.read_text(encoding="utf-8")
    soup = BeautifulSoup(index_text, "html.parser")
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    inline_codes = set(contract["inline_locales"])
    units = extract_units(soup, inline_codes)
    attributes = extract_attributes(soup)
    source_fingerprint = json.dumps(
        {
            "units": [unit["source"] for unit in units],
            "attributes": [item["source"] for item in attributes],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    locale_contracts = [item for item in contract["locales"] if item["code"] != "es"]
    if args.locales:
        requested = set(args.locales)
        locale_contracts = [item for item in locale_contracts if item["code"] in requested]

    progress = read_progress()
    existing_catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {"locales": {}}
    catalog = {
        "schema_version": 1,
        "source": "index.html",
        "source_sha256": hashlib.sha256(source_fingerprint.encode("utf-8")).hexdigest(),
        "unit_count": len(units),
        "attribute_count": len(attributes),
        "fallback_locale": "es",
        "locales": dict(existing_catalog.get("locales", {})),
    }

    if args.sanitize_existing:
        counts = apply_spanish_fallbacks(catalog, units, attributes)
        write_catalog(catalog)
        print(
            "Spanish fallbacks applied: "
            + ", ".join(f"{code}={count}" for code, count in counts.items()),
            flush=True,
        )
        return

    if args.repair_degenerate:
        unit_sources = {unit["key"]: unit["source"] for unit in units}
        attribute_sources = {item["key"]: item["source"] for item in attributes}
        for locale in locale_contracts:
            code = locale["code"]
            current = catalog["locales"].get(code)
            if not current:
                continue
            repair_progress = progress.setdefault("repairs", {}).setdefault(code, {})
            bad = {
                "translations": [key for key, value in current["translations"].items() if is_degenerate(value)],
                "attributes": [key for key, value in current["attributes"].items() if is_degenerate(value)],
                "runtime": [key for key, value in current["runtime"].items() if is_degenerate(value)],
            }
            if args.provider == "argos" and code != "en":
                pivot = catalog["locales"]["en"]
                selected_unit_sources = pivot["translations"]
                selected_attribute_sources = pivot["attributes"]
                selected_runtime_sources = pivot["runtime"]
                source_code = "en"
                target_code = "zh" if code == "zh-TW" else code
            else:
                selected_unit_sources = unit_sources
                selected_attribute_sources = attribute_sources
                selected_runtime_sources = RUNTIME_SOURCES
                source_code = "es"
                target_code = "en" if code == "en" else code
            sources = (
                [selected_unit_sources[key] for key in bad["translations"]]
                + [selected_attribute_sources[key] for key in bad["attributes"]]
                + [selected_runtime_sources[key] for key in bad["runtime"]]
            )
            if not sources:
                continue
            print(f"Repairing {code}: {sum(map(len, bad.values()))} values", flush=True)
            if args.provider == "argos":
                repaired = translate_argos_repairs(sources, source_code, target_code)
                if code == "zh-TW":
                    repaired = {key: to_traditional_chinese(value) for key, value in repaired.items()}
                repair_progress.update(repaired)
            else:
                translate_sources(
                    sources,
                    locale["english_name"],
                    code,
                    args.model,
                    args.provider,
                    repair_progress,
                    lambda: write_progress(progress),
                )
            for key in bad["translations"]:
                current["translations"][key] = repair_progress[selected_unit_sources[key]]
            for key in bad["attributes"]:
                current["attributes"][key] = repair_progress[selected_attribute_sources[key]]
            for key in bad["runtime"]:
                current["runtime"][key] = repair_progress[selected_runtime_sources[key]]
            write_progress(progress)
            write_catalog(catalog)
        remaining = sum(
            is_degenerate(value)
            for locale in catalog["locales"].values()
            for section in ("translations", "attributes", "runtime")
            for value in locale[section].values()
        )
        if remaining:
            raise RuntimeError(f"Catalog still contains {remaining} degenerate values")
        print("Targeted catalog repair complete", flush=True)
        return

    for locale in locale_contracts:
        code = locale["code"]
        print(f"Translating {code} ({locale['english_name']})", flush=True)
        if args.provider == "argos":
            english = catalog["locales"].get("en")
            if code != "en" and not english:
                raise RuntimeError("The complete English catalog is required as the Argos pivot")
            locale_progress = progress.setdefault("argos_locales", {}).setdefault(code, {})
            if code == "en":
                source_code = "es"
                target_code = "en"
                source_translations = {unit["key"]: unit["source"] for unit in units}
                source_attributes = {item["key"]: item["source"] for item in attributes}
                source_runtime = RUNTIME_SOURCES
            else:
                source_code = "en"
                target_code = "zh" if code == "zh-TW" else code
                source_translations = english["translations"]
                source_attributes = english["attributes"]
                source_runtime = english["runtime"]
            pivot_sources = (
                list(source_translations.values())
                + list(source_attributes.values())
                + list(source_runtime.values())
            )
            translate_argos_sources(
                pivot_sources,
                source_code,
                target_code,
                locale_progress,
                lambda: write_progress(progress),
            )
            catalog["locales"][code] = {
                "direction": locale["direction"],
                "translations": {
                    key: locale_progress[value]
                    for key, value in source_translations.items()
                },
                "attributes": {
                    key: locale_progress[value]
                    for key, value in source_attributes.items()
                },
                "runtime": {
                    key: locale_progress[value]
                    for key, value in source_runtime.items()
                },
            }
            if code == "zh-TW":
                for section in ("translations", "attributes", "runtime"):
                    catalog["locales"][code][section] = {
                        key: to_traditional_chinese(value)
                        for key, value in catalog["locales"][code][section].items()
                    }
            apply_spanish_fallbacks(catalog, units, attributes)
            write_progress(progress)
            write_catalog(catalog)
            print(
                f"  wrote {len(source_translations)} text units and "
                f"{len(source_attributes)} attributes",
                flush=True,
            )
            continue

        seeded = seed_inline_locale(soup, code, units) if code in contract["inline_locales"] and not args.no_seed else {}
        progress_group = "bing_locales" if args.provider == "bing" else "locales"
        locale_progress = progress.setdefault(progress_group, {}).setdefault(code, {})
        missing_unit_sources = [unit["source"] for unit in units if unit["key"] not in seeded]
        required_sources = missing_unit_sources + [item["source"] for item in attributes] + list(RUNTIME_SOURCES.values())
        translate_sources(
            required_sources,
            locale["english_name"],
            code,
            args.model,
            args.provider,
            locale_progress,
            lambda: write_progress(progress),
        )
        write_progress(progress)

        translations = {
            unit["key"]: (
                seeded[unit["key"]]
                if unit["key"] in seeded
                else locale_progress[unit["source"]]
            )
            for unit in units
        }
        attribute_translations = {
            item["key"]: locale_progress[item["source"]]
            for item in attributes
        }
        runtime = {key: locale_progress[source] for key, source in RUNTIME_SOURCES.items()}
        catalog["locales"][code] = {
            "direction": locale["direction"],
            "translations": translations,
            "attributes": attribute_translations,
            "runtime": runtime,
        }
        apply_spanish_fallbacks(catalog, units, attributes)
        write_catalog(catalog)
        print(f"  wrote {len(translations)} text units and {len(attribute_translations)} attributes", flush=True)

    missing = [item["code"] for item in contract["locales"] if item["code"] != "es" and item["code"] not in catalog["locales"]]
    if missing:
        print(f"Catalog remains incomplete: {', '.join(missing)}", flush=True)
    else:
        print(
            f"Complete catalog written: {len(catalog['locales'])} locales × "
            f"{len(units)} text units + {len(attributes)} attributes",
            flush=True,
        )


if __name__ == "__main__":
    main()
