#!/usr/bin/env python3
"""Generate the 22-language web, API, documentation and PDF surface.

The six original portfolio locales keep their hand-authored SPA translations and
specialized PDF generators. The additional locales are sourced from the fully
translated GitHub profile READMEs committed under sources/profile-readme/.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "sources" / "profile-readme"
WEB_DIR = ROOT / "i18n"
DOCS_DIR = ROOT / "docs" / "i18n"
API_DIR = ROOT / "api" / "v1" / "i18n"
ASSETS_DIR = ROOT / "assets"
PDF_TMP_DIR = ROOT / "tmp" / "pdfs"
TODAY = date(2026, 10, 16).isoformat()
FULL_LANGUAGE_CODES = "ES · EN · PT · IT · FR · ZH · ZH-TW · JA · KO · TR · RU · VI · TH · DE · UK · PL · AR · FA · ID · NL · HI · EL"


@dataclass(frozen=True)
class Locale:
    code: str
    source: str
    suffix: str
    native_name: str
    english_name: str
    direction: str = "ltr"


LOCALES = (
    Locale("es", "README.md", "", "Español", "Spanish"),
    Locale("en", "README.en.md", "-english", "English", "English"),
    Locale("pt", "README.pt.md", "-portuguese", "Português", "Portuguese"),
    Locale("it", "README.it.md", "-italian", "Italiano", "Italian"),
    Locale("fr", "README.fr.md", "-french", "Français", "French"),
    Locale("zh", "README.zh.md", "-chinese", "简体中文", "Simplified Chinese"),
    Locale("zh-TW", "README.zh-TW.md", "-traditional-chinese", "繁體中文", "Traditional Chinese"),
    Locale("ja", "README.ja.md", "-japanese", "日本語", "Japanese"),
    Locale("ko", "README.ko.md", "-korean", "한국어", "Korean"),
    Locale("tr", "README.tr.md", "-turkish", "Türkçe", "Turkish"),
    Locale("ru", "README.ru.md", "-russian", "Русский", "Russian"),
    Locale("vi", "README.vi.md", "-vietnamese", "Tiếng Việt", "Vietnamese"),
    Locale("th", "README.th.md", "-thai", "ไทย", "Thai"),
    Locale("de", "README.de.md", "-german", "Deutsch", "German"),
    Locale("uk", "README.uk.md", "-ukrainian", "Українська", "Ukrainian"),
    Locale("pl", "README.pl.md", "-polish", "Polski", "Polish"),
    Locale("ar", "README.ar.md", "-arabic", "العربية", "Arabic", "rtl"),
    Locale("fa", "README.fa.md", "-persian", "فارسی", "Persian", "rtl"),
    Locale("id", "README.id.md", "-indonesian", "Bahasa Indonesia", "Indonesian"),
    Locale("nl", "README.nl.md", "-dutch", "Nederlands", "Dutch"),
    Locale("hi", "README.hi.md", "-hindi", "हिन्दी", "Hindi"),
    Locale("el", "README.el.md", "-greek", "Ελληνικά", "Greek"),
)

INLINE_CODES = {"es", "en", "pt", "it", "fr", "zh"}

DOCUMENTS = (
    ("portfolio", "portafolio", "Portfolio"),
    ("resume", "hoja-de-vida", "Professional resume"),
    ("recruiter", "cv-reclutador", "Recruiter CV"),
    ("ats", "cv-ats", "ATS CV"),
    ("achievements", "declaracion-logros-validacion", "Achievements and validation statement"),
    ("recommendation", "carta-recomendacion_sin_firma", "Recommendation letter context"),
    ("institutional", "nota-vigencia-contexto-institucional-ceis", "CEIS institutional context note"),
)

# Localized document names. Body content comes from the corresponding translated
# README, so the generator never fabricates professional claims.
TITLES = {
    "es": ["Portafolio", "Hoja de vida profesional", "CV para reclutamiento", "CV ATS", "Declaración de logros y validación", "Contexto de la carta de recomendación", "Nota de vigencia y contexto institucional CEIS"],
    "en": ["Portfolio", "Professional resume", "Recruiter CV", "ATS CV", "Achievements and validation statement", "Recommendation letter context", "CEIS institutional validity and context note"],
    "pt": ["Portfólio", "Currículo profissional", "CV para recrutamento", "CV ATS", "Declaração de realizações e validação", "Contexto da carta de recomendação", "Nota de vigência e contexto institucional CEIS"],
    "it": ["Portfolio", "Curriculum professionale", "CV per selezione", "CV ATS", "Dichiarazione dei risultati e convalida", "Contesto della lettera di raccomandazione", "Nota di validità e contesto istituzionale CEIS"],
    "fr": ["Portfolio", "Curriculum professionnel", "CV pour le recrutement", "CV ATS", "Déclaration de réalisations et validation", "Contexte de la lettre de recommandation", "Note de validité et de contexte institutionnel CEIS"],
    "zh": ["作品集", "专业简历", "招聘简历", "ATS 简历", "成果与验证声明", "推荐信背景说明", "CEIS 机构有效性与背景说明"],
    "zh-TW": ["作品集", "專業履歷", "招募履歷", "ATS 履歷", "成果與驗證聲明", "推薦信背景說明", "CEIS 機構有效性與背景說明"],
    "ja": ["ポートフォリオ", "職務経歴書", "採用担当者向けCV", "ATS向けCV", "実績および検証声明", "推薦状の背景説明", "CEIS機関の有効性および背景に関する注記"],
    "ko": ["포트폴리오", "전문 이력서", "채용 담당자용 CV", "ATS CV", "성과 및 검증 진술서", "추천서 배경 설명", "CEIS 기관 유효성 및 배경 설명"],
    "tr": ["Portföy", "Profesyonel özgeçmiş", "İşe alım CV'si", "ATS CV", "Başarılar ve doğrulama beyanı", "Tavsiye mektubu bağlamı", "CEIS kurumsal geçerlilik ve bağlam notu"],
    "ru": ["Портфолио", "Профессиональное резюме", "Резюме для рекрутера", "Резюме ATS", "Заявление о достижениях и проверке", "Контекст рекомендательного письма", "Примечание о действительности и контексте CEIS"],
    "vi": ["Hồ sơ năng lực", "Sơ yếu lý lịch chuyên nghiệp", "CV dành cho nhà tuyển dụng", "CV ATS", "Tuyên bố thành tích và xác minh", "Bối cảnh thư giới thiệu", "Ghi chú về hiệu lực và bối cảnh tổ chức CEIS"],
    "th": ["แฟ้มผลงาน", "ประวัติย่อระดับมืออาชีพ", "CV สำหรับผู้สรรหา", "CV สำหรับ ATS", "คำชี้แจงผลงานและการตรวจสอบ", "บริบทของจดหมายแนะนำ", "หมายเหตุความถูกต้องและบริบทสถาบัน CEIS"],
    "de": ["Portfolio", "Beruflicher Lebenslauf", "Recruiter-Lebenslauf", "ATS-Lebenslauf", "Erfolgs- und Validierungserklärung", "Kontext des Empfehlungsschreibens", "Hinweis zur Gültigkeit und zum institutionellen Kontext von CEIS"],
    "uk": ["Портфоліо", "Професійне резюме", "Резюме для рекрутера", "Резюме ATS", "Заява про досягнення та перевірку", "Контекст рекомендаційного листа", "Примітка про чинність та інституційний контекст CEIS"],
    "pl": ["Portfolio", "Życiorys zawodowy", "CV dla rekrutera", "CV ATS", "Oświadczenie o osiągnięciach i weryfikacji", "Kontekst listu polecającego", "Nota o ważności i kontekście instytucjonalnym CEIS"],
    "ar": ["ملف الأعمال", "السيرة المهنية", "سيرة ذاتية لمسؤول التوظيف", "سيرة ذاتية لنظام ATS", "بيان الإنجازات والتحقق", "سياق خطاب التوصية", "ملاحظة صلاحية وسياق مؤسسة CEIS"],
    "fa": ["نمونه‌کار", "رزومه حرفه‌ای", "رزومه ویژه استخدام", "رزومه ATS", "بیانیه دستاوردها و اعتبارسنجی", "زمینه نامه توصیه", "یادداشت اعتبار و زمینه سازمانی CEIS"],
    "id": ["Portofolio", "Riwayat hidup profesional", "CV untuk perekrut", "CV ATS", "Pernyataan pencapaian dan validasi", "Konteks surat rekomendasi", "Catatan validitas dan konteks institusi CEIS"],
    "nl": ["Portfolio", "Professioneel cv", "Cv voor recruiters", "ATS-cv", "Verklaring van prestaties en validatie", "Context van de aanbevelingsbrief", "Notitie over geldigheid en institutionele context van CEIS"],
    "hi": ["पोर्टफोलियो", "पेशेवर जीवनवृत्त", "भर्तीकर्ता के लिए CV", "ATS CV", "उपलब्धियों और सत्यापन का विवरण", "अनुशंसा पत्र का संदर्भ", "CEIS संस्थागत वैधता और संदर्भ नोट"],
    "el": ["Χαρτοφυλάκιο", "Επαγγελματικό βιογραφικό", "Βιογραφικό για υπεύθυνο προσλήψεων", "Βιογραφικό ATS", "Δήλωση επιτευγμάτων και επικύρωσης", "Πλαίσιο συστατικής επιστολής", "Σημείωση ισχύος και θεσμικού πλαισίου CEIS"],
}


def source_for(locale: Locale) -> str:
    path = SOURCE_DIR / locale.source
    if not path.exists():
        raise FileNotFoundError(f"Missing localized source: {path}")
    return path.read_text(encoding="utf-8")


def clean_source(text: str) -> str:
    text = re.sub(r"<div[^>]*>|</div>", "", text, flags=re.I)
    text = re.sub(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.strip()


def expanded_source(text: str) -> str:
    """Normalize the inherited six-language claim in translated profile sources."""
    replacements = {
        "6 idiomas": "22 idiomas",
        "6 languages": "22 languages",
        "6 langues": "22 langues",
        "6 lingue": "22 lingue",
        "6 Sprachen": "22 Sprachen",
        "6 языках": "22 языках",
        "6 языков": "22 языков",
        "6 мовах": "22 мовах",
        "6 мов": "22 мов",
        "6 językach": "22 językach",
        "6 języków": "22 języków",
        "6 لغات": "22 لغات",
        "6 زبان": "22 زبان",
        "۶ زبان": "۲۲ زبان",
        "6 bahasa": "22 bahasa",
        "6 talen": "22 talen",
        "6 भाषाओं": "22 भाषाओं",
        "6 भाषाएँ": "22 भाषाएँ",
        "6 γλώσσες": "22 γλώσσες",
        "6種語言": "22種語言",
        "6 個語言": "22 個語言",
        "6 种语言": "22 种语言",
        "6言語": "22言語",
        "6 の言語": "22 の言語",
        "6개 언어": "22개 언어",
        "6 개 언어": "22 개 언어",
        "6 dil": "22 dil",
        "6 ngôn ngữ": "22 ngôn ngữ",
        "6 ภาษา": "22 ภาษา",
        "36 PDFs": "154 PDFs",
        "36 PDF": "154 PDF",
        "PDF36": "PDF154",
        "36個PDF": "154個PDF",
        "42 PDFs": "154 PDFs",
        "ES · EN · PT · IT · FR · ZH": FULL_LANGUAGE_CODES,
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def plain(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_`>#]", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    return " ".join(text.split())


def parse_profile(text: str) -> dict:
    title_match = re.search(r"^#\s+(.+)$", text, re.M)
    h2 = list(re.finditer(r"^##\s+(.+)$", text, re.M))
    sections = []
    for i, match in enumerate(h2):
        end = h2[i + 1].start() if i + 1 < len(h2) else len(text)
        sections.append({"heading": plain(match.group(1)), "markdown": text[match.end():end].strip()})
    lead = text[:h2[0].start()] if h2 else text
    paragraphs = [plain(p) for p in re.split(r"\n\s*\n", lead) if plain(p)]
    summary = max((p for p in paragraphs if len(p) > 120), key=len, default="")
    if not summary and len(sections) > 1:
        section_paragraphs = [
            plain(p) for p in re.split(r"\n\s*\n", sections[1]["markdown"]) if plain(p)
        ]
        summary = max(section_paragraphs, key=len, default="")
    subtitle = sections[0]["heading"] if sections else ""
    return {
        "title": plain(title_match.group(1)) if title_match else "Vladimir Acuña",
        "subtitle": subtitle,
        "summary": summary,
        "sections": sections[1:] if sections else [],
    }


def pdf_name(base: str, locale: Locale) -> str:
    return f"{base}{locale.suffix}.pdf"


def artifact_map(locale: Locale) -> dict:
    return {
        key: f"/assets/{pdf_name(base, locale)}"
        for key, base, _ in DOCUMENTS
    }


def language_options(current: str) -> str:
    return "\n".join(
        f'<option value="{html.escape(loc.code)}"'
        f'{" selected" if loc.code == current else ""}>{html.escape(loc.native_name)}</option>'
        for loc in LOCALES
    )


def alternate_links() -> str:
    links = [
        '<link rel="alternate" hreflang="x-default" href="https://vladimiracunadev-create.github.io/">'
    ]
    links.extend(
        f'<link rel="alternate" hreflang="{html.escape(loc.code)}" '
        f'href="https://vladimiracunadev-create.github.io/i18n/{html.escape(loc.code)}/">'
        for loc in LOCALES
    )
    return "\n  ".join(links)


def document_links(locale: Locale) -> str:
    labels = TITLES[locale.code]
    return "\n".join(
        f'<a class="doc-link" href="../../assets/{html.escape(pdf_name(base, locale))}">{html.escape(labels[i])}</a>'
        for i, (_, base, _) in enumerate(DOCUMENTS)
    )


def accessible_table_markup(fragment: str) -> str:
    """Normalize Markdown table markup for the site's accessibility and CSP rules."""
    fragment = re.sub(r"<th\b(?![^>]*\bscope=)([^>]*)>", r'<th scope="col"\1>', fragment)
    fragment = re.sub(
        r' style="text-align:\s*(left|center|right);?"',
        lambda match: f' class="align-{match.group(1)}"',
        fragment,
    )
    return fragment


def page_html(locale: Locale, profile: dict, markdown_text: str) -> str:
    body = accessible_table_markup(
        markdown.markdown(
            clean_source(markdown_text),
            extensions=["extra", "tables", "fenced_code", "sane_lists"],
        )
    )
    return f"""<!DOCTYPE html>
<html lang="{html.escape(locale.code)}" dir="{locale.direction}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="{html.escape(profile['summary'][:260])}">
  <title>{html.escape(profile['title'])} · {html.escape(locale.native_name)}</title>
  <link rel="canonical" href="https://vladimiracunadev-create.github.io/i18n/{html.escape(locale.code)}/">
  {alternate_links()}
  <link rel="stylesheet" href="../localized.css">
</head>
<body>
  <header class="locale-bar">
    <a class="home-link" href="../../">← Interactive portfolio</a>
    <label>Language
      <select id="locale-select" aria-label="Language">{language_options(locale.code)}</select>
    </label>
    <span class="stamp">{TODAY} · America/Santiago</span>
  </header>
  <main>
    <section class="downloads" aria-label="PDF documents">
      <h2>PDF · {html.escape(locale.native_name)}</h2>
      <div class="doc-grid">{document_links(locale)}</div>
      <a class="api-link" href="../../api/v1/i18n/{html.escape(locale.code)}.json">JSON API</a>
    </section>
    <article class="profile-content">{body}</article>
  </main>
  <footer>Source synchronized from the public GitHub profile · {TODAY}</footer>
  <script src="../localized.js"></script>
</body>
</html>
"""


def api_payload(locale: Locale, profile: dict) -> dict:
    return {
        "meta": {
            "generated_at": TODAY,
            "language": locale.code,
            "language_name": locale.english_name,
            "native_name": locale.native_name,
            "direction": locale.direction,
            "source": f"https://github.com/vladimiracunadev-create/vladimiracunadev-create/blob/main/{locale.source}",
        },
        "profile": {
            "name": "Vladimir Acuña",
            "title": profile["subtitle"],
            "summary": profile["summary"],
            "website": f"https://vladimiracunadev-create.github.io/i18n/{locale.code}/",
            "github": "https://github.com/vladimiracunadev-create",
            "gitlab": "https://gitlab.com/vladimir.acuna.dev-group",
        },
        "sections": [item["heading"] for item in profile["sections"]],
        "artifacts": artifact_map(locale),
    }


def selected_sections(profile: dict, kind: str) -> list[dict]:
    sections = profile["sections"]
    if kind == "portfolio":
        return sections
    indexes = {
        "resume": [0, 1, 3, 4, 5, 6, 10, 11, 13],
        "recruiter": [0, 1, 3, 6, 10, 11, 13],
        "ats": [0, 1, 10, 13],
        "achievements": [1, 9, 10],
        "recommendation": [1, 10, 11, 13],
        "institutional": [0, 1, 9, 10],
    }.get(kind, [])
    return [sections[i] for i in indexes if i < len(sections)]


def pdf_html(locale: Locale, profile: dict, kind: str, title: str) -> str:
    blocks = []
    for section in selected_sections(profile, kind):
        blocks.append(f"## {section['heading']}\n\n{section['markdown']}")
    content = markdown.markdown(
        clean_source("\n\n".join(blocks)),
        extensions=["extra", "tables", "fenced_code", "sane_lists"],
    )
    source_note = (
        "This localized edition is derived from the corresponding complete public GitHub profile translation. "
        "Historical recommendation and institutional records remain linked to their source editions."
    )
    return f"""<!DOCTYPE html>
<html lang="{html.escape(locale.code)}" dir="{locale.direction}">
<head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 18mm 16mm 18mm; @bottom-center {{ content: "Vladimir Acuña · {TODAY} · " counter(page); font-size: 8pt; color: #526071; }} }}
* {{ box-sizing: border-box; }}
body {{ font-family: "Segoe UI", "Nirmala UI", "Yu Gothic", "Malgun Gothic", Arial, sans-serif; color: #162033; font-size: 9.2pt; line-height: 1.38; }}
header {{ border-bottom: 3px solid #2563eb; margin-bottom: 12mm; padding: 0 0 7mm; }}
h1 {{ color: #15375b; font-size: 23pt; margin: 0 0 3mm; }}
.role {{ color: #334155; font-size: 11pt; margin: 0 0 4mm; }}
.summary {{ background: #eff6ff; border-inline-start: 4px solid #2563eb; padding: 4mm; margin: 0; }}
h2 {{ color: #174a7e; font-size: 14pt; border-bottom: 1px solid #cbd5e1; padding-bottom: 1.5mm; margin: 8mm 0 3mm; break-after: avoid; }}
h3 {{ color: #263d57; font-size: 11pt; break-after: avoid; }}
p, li {{ orphans: 3; widows: 3; }}
table {{ width: 100%; border-collapse: collapse; font-size: 8pt; margin: 3mm 0; }}
th, td {{ border: 1px solid #cbd5e1; padding: 2mm; vertical-align: top; }}
th {{ background: #eaf2fb; }}
a {{ color: #1d4ed8; text-decoration: none; }}
pre, code {{ font-family: Consolas, monospace; font-size: 7.5pt; white-space: pre-wrap; }}
.source-note {{ margin-top: 10mm; padding-top: 4mm; border-top: 1px solid #94a3b8; color: #526071; font-size: 8pt; }}
</style></head>
<body>
<header><h1>{html.escape(title)}</h1><p class="role">{html.escape(profile['subtitle'])}</p><p class="summary">{html.escape(profile['summary'])}</p></header>
<main>{content}</main>
<p class="source-note">{html.escape(source_note)}<br>https://vladimiracunadev-create.github.io/i18n/{html.escape(locale.code)}/</p>
</body></html>"""


def browser_executable() -> Path:
    candidates = (
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Chrome or Microsoft Edge is required for multilingual PDF rendering")


def render_pdf(target: Path, markup: str, locale: Locale, kind: str) -> None:
    PDF_TMP_DIR.mkdir(parents=True, exist_ok=True)
    html_path = PDF_TMP_DIR / f"{kind}-{locale.code}.html"
    profile_dir = PDF_TMP_DIR / "edge-profile"
    html_path.write_text(markup, encoding="utf-8")
    target.unlink(missing_ok=True)
    command = [
        str(browser_executable()),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile_dir}",
        f"--print-to-pdf={target.resolve()}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=90)
    deadline = time.monotonic() + 90
    previous_size = -1
    stable_checks = 0
    while time.monotonic() < deadline:
        size = target.stat().st_size if target.exists() else 0
        if size > 1000 and size == previous_size:
            stable_checks += 1
            if stable_checks >= 2:
                break
        else:
            stable_checks = 0
        previous_size = size
        time.sleep(0.5)
    if result.returncode != 0 or not target.exists() or target.stat().st_size < 1000:
        raise RuntimeError(
            f"Edge PDF render failed for {target.name}: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    html_path.unlink(missing_ok=True)


def write_common_css() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    css = """\
:root { color-scheme: dark light; --bg:#08111f; --panel:#101d31; --text:#edf4ff; --muted:#a8b7ca; --accent:#6eb6ff; --line:#2c405b; }
* { box-sizing:border-box; }
html { scroll-behavior:smooth; }
body { margin:0; background:var(--bg); color:var(--text); font:16px/1.65 system-ui,"Segoe UI","Nirmala UI","Yu Gothic","Malgun Gothic",sans-serif; }
a { color:var(--accent); }
.locale-bar { position:sticky; top:0; z-index:2; display:flex; gap:1rem; align-items:center; flex-wrap:wrap; padding:.8rem max(1rem,calc((100% - 1120px)/2)); background:rgba(8,17,31,.96); border-bottom:1px solid var(--line); }
.locale-bar label { display:flex; align-items:center; gap:.5rem; }
.locale-bar select { max-width:16rem; padding:.45rem; border-radius:.5rem; }
.home-link { font-weight:700; }
.stamp { margin-inline-start:auto; color:var(--muted); font-size:.85rem; }
main { max-width:1120px; margin:auto; padding:1.5rem; }
.downloads { background:var(--panel); border:1px solid var(--line); border-radius:1rem; padding:1rem 1.2rem; margin-bottom:2rem; }
.doc-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:.6rem; }
.doc-link,.api-link { display:block; padding:.65rem .8rem; border:1px solid var(--line); border-radius:.65rem; text-decoration:none; }
.api-link { margin-top:.8rem; width:max-content; }
.profile-content { overflow-wrap:anywhere; }
.profile-content h1 { font-size:clamp(2rem,5vw,3.5rem); line-height:1.1; }
.profile-content h2 { margin-top:2.3rem; color:#a9d5ff; border-bottom:1px solid var(--line); padding-bottom:.35rem; }
.profile-content table { display:block; overflow-x:auto; border-collapse:collapse; width:100%; }
.profile-content th,.profile-content td { border:1px solid var(--line); padding:.55rem; vertical-align:top; }
.align-left { text-align:left; }
.align-center { text-align:center; }
.align-right { text-align:right; }
.profile-content pre { overflow:auto; background:#06101c; padding:1rem; border-radius:.7rem; }
.profile-content img { max-width:100%; }
footer { max-width:1120px; margin:2rem auto; padding:1.5rem; color:var(--muted); border-top:1px solid var(--line); }
@media (prefers-color-scheme:light) { :root { --bg:#f7fafc; --panel:#fff; --text:#132238; --muted:#53657b; --accent:#075eb5; --line:#cad5e2; } .locale-bar { background:rgba(247,250,252,.96); } .profile-content h2 { color:#164f82; } .profile-content pre { background:#eef3f8; } }
"""
    (WEB_DIR / "localized.css").write_text(css, encoding="utf-8")
    (WEB_DIR / "localized.js").write_text(
        "\"use strict\";\n"
        "document.getElementById(\"locale-select\").addEventListener(\"change\", function () {\n"
        "  window.location.href = \"../\" + encodeURIComponent(this.value) + \"/\";\n"
        "});\n",
        encoding="utf-8",
    )


def generate_locale(locale: Locale, generate_pdf: bool) -> None:
    raw = expanded_source(source_for(locale))
    profile = parse_profile(raw)

    web_path = WEB_DIR / locale.code / "index.html"
    web_path.parent.mkdir(parents=True, exist_ok=True)
    web_path.write_text(page_html(locale, profile, raw), encoding="utf-8")

    docs_path = DOCS_DIR / locale.code / "README.md"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    docs_path.write_text(
        f"<!-- Synced from the public GitHub profile on {TODAY}. -->\n\n{raw.rstrip()}\n",
        encoding="utf-8",
    )

    API_DIR.mkdir(parents=True, exist_ok=True)
    (API_DIR / f"{locale.code}.json").write_text(
        json.dumps(api_payload(locale, profile), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if generate_pdf:
        for i, (kind, base, _) in enumerate(DOCUMENTS):
            target = ASSETS_DIR / pdf_name(base, locale)
            render_pdf(target, pdf_html(locale, profile, kind, TITLES[locale.code][i]), locale, kind)
            print(f"PDF {locale.code}: {target.name}")


def write_indexes() -> None:
    languages = [
        {
            "code": loc.code,
            "name": loc.english_name,
            "native_name": loc.native_name,
            "direction": loc.direction,
            "web": f"/i18n/{loc.code}/",
            "api": f"/api/v1/i18n/{loc.code}.json",
            "artifacts": artifact_map(loc),
        }
        for loc in LOCALES
    ]
    payload = {
        "meta": {"generated_at": TODAY, "count": len(LOCALES), "default": "es"},
        "languages": languages,
    }
    (API_DIR / "index.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Documentación internacional",
        "",
        f"**Sincronizada:** {TODAY}. Las 22 versiones proceden del README público principal.",
        "",
        "| Código | Idioma | Documento | Web | API |",
        "|---|---|---|---|---|",
    ]
    for loc in LOCALES:
        lines.append(
            f"| `{loc.code}` | {loc.native_name} | [{loc.source}]({loc.code}/README.md) | "
            f"[/i18n/{loc.code}/](../../i18n/{loc.code}/) | "
            f"[`{loc.code}.json`](../../api/v1/i18n/{loc.code}.json) |"
        )
    (DOCS_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_canonical_contracts() -> None:
    locale_codes = [loc.code for loc in LOCALES]
    suffix_map = {loc.code: loc.suffix for loc in LOCALES}
    base_url = "https://vladimiracunadev-create.github.io"
    artifact_config = {
        "cv_ats": (3, "cv-ats"),
        "cv_recruiter": (2, "cv-reclutador"),
        "hoja_de_vida": (1, "hoja-de-vida"),
        "portfolio": (0, "portafolio"),
        "recommendation_letter": (5, "carta-recomendacion_sin_firma"),
        "achievements_statement": (4, "declaracion-logros-validacion"),
        "ceis_institutional_context_note": (6, "nota-vigencia-contexto-institucional-ceis"),
    }

    artifacts_path = ROOT / "api" / "v1" / "artifacts.json"
    artifacts = json.loads(artifacts_path.read_text(encoding="utf-8"))
    artifacts["meta"]["generated_at"] = TODAY
    artifacts["artifact_languages"] = locale_codes
    artifacts["language_suffix_map"] = suffix_map
    for item in artifacts["artifacts"]:
        title_index, base = artifact_config[item["id"]]
        item["updated_at"] = TODAY
        item["variants"] = {
            loc.code: {
                "label": TITLES[loc.code][title_index],
                "file": f"assets/{pdf_name(base, loc)}",
                "url": f"{base_url}/assets/{pdf_name(base, loc)}",
            }
            for loc in LOCALES
        }
    artifacts_path.write_text(json.dumps(artifacts, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")

    meta_path = ROOT / "api" / "v1" / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["meta"]["generated_at"] = TODAY
    meta["endpoints"]["i18n"] = "/api/v1/i18n/index.json"
    meta["site_pages"]["localized"] = "/i18n/{locale}/"
    meta["capabilities"]["artifact_languages"] = locale_codes
    meta["capabilities"]["artifact_switching"] = (
        "The six inline SPA languages switch in place; 16 additional languages use complete localized pages. "
        "Every locale links to seven matching PDF artifacts."
    )
    meta["capabilities"]["language_suffix_map"] = suffix_map
    meta["data_source"]["extraction_date"] = TODAY
    meta["data_source"]["pdf_generation"] = (
        "Python reportlab + Chromium print pipeline (154 PDFs: 7 document families across 22 languages)"
    )
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")

    for name in ("profile.json", "experience.json", "projects.json", "skills.json"):
        path = ROOT / "api" / "v1" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        if "meta" in data:
            data["meta"]["generated_at"] = TODAY
        if name == "projects.json":
            data["projects"] = [
                project for project in data["projects"]
                if not project.get("url", "").endswith("/software-engineering-learning-suite")
            ]
            for project in data["projects"]:
                if project.get("name") in {"lifelong-learning-ecosystem", "modern-software-engineering-program"}:
                    project["category"] = "curriculum"
        serialized = json.dumps(data, ensure_ascii=False, indent=4)
        serialized = serialized.replace("42 PDFs", "154 PDFs").replace("6 idiomas", "22 idiomas")
        serialized = serialized.replace("(ES/EN/PT/IT/FR/ZH)", f"({FULL_LANGUAGE_CODES.replace(' · ', '/')})")
        path.write_text(serialized + "\n", encoding="utf-8")

    resume_path = ROOT / "data" / "resume.json"
    resume = json.loads(resume_path.read_text(encoding="utf-8"))
    resume["meta"]["generated_at"] = TODAY
    resume["meta"]["available_locales"] = locale_codes
    resume["summary"] = [
        item.replace("42 PDFs en 6 idiomas", "154 PDFs en 22 idiomas")
        for item in resume.get("summary", [])
    ]
    resume["projects"] = [
        project for project in resume.get("projects", [])
        if not project.get("url", "").endswith("/software-engineering-learning-suite")
    ]
    known_urls = {project.get("url") for project in resume["projects"]}
    for name, description, url in (
        (
            "Lifelong Learning Ecosystem",
            "Brújula curricular federada con 30 recorridos en 6 áreas, mapas visuales y portal offline accesible.",
            "https://github.com/vladimiracunadev-create/lifelong-learning-ecosystem",
        ),
        (
            "Modern Software Engineering Program",
            "Programa de 480 clases, 40 partes y 8 etapas: fundamentos, producto, arquitectura, DevOps e IA.",
            "https://github.com/vladimiracunadev-create/modern-software-engineering-program",
        ),
    ):
        if url not in known_urls:
            resume["projects"].append({"name": name, "description": description, "url": url})
    resume_path.write_text(json.dumps(resume, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")


def update_current_documentation() -> None:
    targets = (
        ROOT / "README.md",
        ROOT / "CLAUDE.md",
        ROOT / "cv-data-api.md",
        ROOT / "llm.txt",
        ROOT / "docs" / "AI_CODE_ASSURANCE.md",
        ROOT / "docs" / "BEGINNER_GUIDE.md",
        ROOT / "docs" / "BUILD_GUIDE.md",
        ROOT / "docs" / "RECRUITER.md",
        ROOT / "docs" / "TECHNICAL_RATIONAL.md",
        ROOT / "docs" / "VALIDATION.md",
        ROOT / "docs" / "wiki" / "BUILD_GUIDE.md",
        ROOT / "docs" / "wiki" / "Home.md",
        ROOT / "docs" / "wiki" / "RECRUITER.md",
        ROOT / "docs" / "wiki" / "TECHNICAL_RATIONAL.md",
        ROOT / "docs" / "wiki" / "VALIDATION.md",
    )
    replacements = (
        ("2026-10-01", TODAY),
        ("42 PDFs", "154 PDFs"),
        ("42 pdf", "154 pdf"),
        ("6 idiomas", "22 idiomas"),
        ("seis idiomas", "22 idiomas"),
        ("6 languages", "22 languages"),
        ("six languages", "22 languages"),
        ("ES/EN/PT/IT/FR/ZH", FULL_LANGUAGE_CODES.replace(" · ", "/")),
        ("ES · EN · PT · IT · FR · ZH", FULL_LANGUAGE_CODES),
        ("7 familias por 6 idiomas", "7 familias por 22 idiomas"),
        ("7 document families across 6 languages", "7 document families across 22 languages"),
        ("7 tipos × 6 idiomas", "7 tipos × 22 idiomas"),
        ("30 archivos, 6 idiomas", "154 archivos, 22 idiomas"),
        ("los seis generadores Python producen 154 PDFs", "los generadores producen 154 PDFs"),
    )
    for path in targets:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def write_backup_manifest() -> None:
    """Record the immutable pre-update PDF backup created for this refresh."""
    backup_dir = ASSETS_DIR / "backups" / TODAY
    pdfs = sorted(backup_dir.glob("*.pdf"), key=lambda path: path.name.casefold())
    if not pdfs:
        return

    checksums = []
    for path in pdfs:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checksums.append(f"{digest}  {path.name}")
    (backup_dir / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")

    report = f"""# Respaldo previo a la actualización — {TODAY}

- PDF públicos respaldados antes de regenerar: **{len(pdfs)}**.
- Ubicación original: `assets/*.pdf`.
- Integridad: SHA-256 registrado en `SHA256SUMS.txt`.
- Alcance posterior: 7 familias documentales en 22 idiomas, **154 PDF públicos**.
- Fuentes lingüísticas: README principal y sus 21 traducciones del perfil público de GitHub.

Los directorios privados `assets/no_aplica/` y `assets/por_solicitud/` no fueron modificados ni publicados.
"""
    (backup_dir / f"SESSION-REPORT-{TODAY}.md").write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdfs", action="store_true", help="Generate the 16 additional locale PDF sets")
    parser.add_argument("--all-pdfs", action="store_true", help="Also replace the six specialized legacy PDF sets")
    parser.add_argument("--locale", action="append", choices=[loc.code for loc in LOCALES], help="Limit generation to one or more locales")
    args = parser.parse_args()

    write_common_css()
    selected_locales = [loc for loc in LOCALES if not args.locale or loc.code in args.locale]
    for locale in selected_locales:
        generate_pdf = args.all_pdfs or (args.pdfs and locale.code not in INLINE_CODES)
        generate_locale(locale, generate_pdf)
    write_indexes()
    update_canonical_contracts()
    update_current_documentation()
    write_backup_manifest()
    print(f"Generated {len(selected_locales)} localized web pages, docs and API documents.")
    if args.pdfs:
        pdf_locale_count = sum(loc.code not in INLINE_CODES for loc in selected_locales)
        print(f"Generated {pdf_locale_count * len(DOCUMENTS)} additional PDFs.")
        shutil.rmtree(PDF_TMP_DIR, ignore_errors=True)


if __name__ == "__main__":
    main()
