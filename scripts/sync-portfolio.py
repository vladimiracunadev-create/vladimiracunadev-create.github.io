#!/usr/bin/env python3
"""
sync-portfolio.py — CLI de sincronización automática del portafolio

Uso:
    python scripts/sync-portfolio.py              # dry-run (solo reporte)
    python scripts/sync-portfolio.py --apply      # aplica todo + commit + push
    python scripts/sync-portfolio.py --apply --no-push     # aplica sin push
    python scripts/sync-portfolio.py --apply --skip-pdfs  # sin regenerar PDFs
    python scripts/sync-portfolio.py --apply --only-api   # solo api/v1/

Qué hace:
    1. Detecta repos públicos nuevos Y cambios de descripción en repos existentes
    2. Actualiza api/v1/*.json  (generated_at, profile label, proyectos nuevos y actualizados)
    3. Inyecta nuevos repos en generate-all-languages.py y generate-portfolio.py  [Gap 2]
    4. Agrega cards HTML en index.html (#proyectos, 6 idiomas)                    [Gap 1]
    5. Propaga cambios de identidad desde SUBTITLES a los scripts de PDFs          [Gap 4]
    6. Actualiza README del perfil GitHub
    7. Crea backup de PDFs + regenera 30 PDFs
    8. Actualiza CHANGELOG.md y hace commit + push
"""

import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

# ── UTF-8 en Windows ──────────────────────────────────────────────────────────
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT       = Path(__file__).parent.parent.resolve()
API_DIR    = ROOT / "api" / "v1"
ASSETS_DIR = ROOT / "assets"
SCRIPTS_DIR = ROOT / "scripts"
INDEX_HTML  = ROOT / "index.html"
TODAY       = date.today().isoformat()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN CENTRAL — editar aquí cuando cambia la identidad
# ═══════════════════════════════════════════════════════════════════════════════

PROFILE_LABEL = (
    "Arquitecto de Soluciones | Senior Full-Stack | "
    "Modernización Legacy, Automatización e Integración de IA Aplicada"
)

# Gap 4: subtítulos en los 6 idiomas para los scripts de generación de PDFs
SUBTITLES = {
    "es": "Arquitecto de Soluciones | Senior Full-Stack | Modernización, Automatización e IA Aplicada",
    "en": "Solutions Architect | Senior Full-Stack | Modernization, Automation & Applied AI",
    "pt": "Arquiteto de Soluções | Senior Full-Stack | Modernização, Automação e IA Aplicada",
    "it": "Architetto di Soluzioni | Senior Full-Stack | Modernizzazione, Automazione e IA Applicata",
    "fr": "Architecte de Solutions | Senior Full-Stack | Modernisation, Automatisation et IA Appliquée",
    "zh": "解决方案架构师 | 高级全栈开发 | 现代化、自动化与应用AI",
}

# Repos permanentemente ocultos
HIDDEN_REPOS = {"rootcause-windows-inspector", "rootcause-landing"}

# Repos que no se agregan como proyectos
SKIP_AS_PROJECT = {
    "vladimiracunadev-create",
    "vladimiracunadev-create.github.io",
    "portal-bienestar",
}

# Categoría por repo (agregar aquí repos nuevos conocidos)
REPO_CATEGORIES = {
    "proyectos-aws": "cloud",
    "social-bot-scheduler": "orchestration",
    "docker-labs": "platform",
    "microsistemas": "tooling",
    "langgraph-realworld": "ai",
    "mcp-ollama-local": "ai",
    "unikernel-labs": "platform",
    "chofyai-studio": "ai",
}

# Etiquetas de categoría en los 6 idiomas (para cards HTML y tags PDF)
CATEGORY_TAGS = {
    "cloud":        {"es": "Cloud",         "en": "Cloud",        "pt": "Cloud",          "it": "Cloud",         "fr": "Cloud",       "zh": "云"},
    "orchestration":{"es": "Orquestación",  "en": "Orchestration","pt": "Orquestração",   "it": "Orchestrazione","fr": "Orchestration","zh": "编排"},
    "platform":     {"es": "Plataforma",    "en": "Platform",     "pt": "Plataforma",     "it": "Piattaforma",   "fr": "Plateforme",  "zh": "平台"},
    "tooling":      {"es": "Herramientas",  "en": "Tooling",      "pt": "Ferramentas",    "it": "Strumenti",     "fr": "Outils",      "zh": "工具"},
    "ai":           {"es": "IA local",      "en": "Local AI",     "pt": "IA local",       "it": "IA locale",     "fr": "IA locale",   "zh": "本地AI"},
    "other":        {"es": "Proyecto",      "en": "Project",      "pt": "Projeto",        "it": "Progetto",      "fr": "Projet",      "zh": "项目"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════════════════════

def log(msg, level="INFO"):
    prefix = {"INFO": "  ", "OK": "[OK]  ", "WARN": "[!!]  ", "ERR": "[ERR] ", "HEAD": "\n>>>  "}
    print(f"{prefix.get(level, '  ')}{msg}")


def run_capture(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout.strip(), r.returncode


# Emojis y símbolos gráficos renderizan como puntos negros en PDFs (reportlab).
# strip_emojis() elimina cualquier carácter fuera del rango Latin/puntuación antes
# de inyectar descripciones en los scripts de generación de PDFs.
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F9FF"   # símbolos & pictogramas / emoticons / objetos
    "\U00002600-\U000027BF"   # miscelánea simbólica
    "\U0001FA00-\U0001FA6F"   # símbolos extendidos A
    "\U0001FA70-\U0001FAFF"   # símbolos extendidos B
    "\U00002702-\U000027B0"   # Dingbats
    "]+",
    flags=re.UNICODE,
)

def strip_emojis(text: str) -> str:
    """Elimina emojis/símbolos gráficos Unicode para uso seguro en PDFs."""
    return _EMOJI_RE.sub("", text).strip()


def repo_key(name):
    """Deriva clave corta de un nombre de repo. ej: 'unikernel-labs' → 'unikernel'"""
    return name.split("-")[0]


def repo_display(name):
    """Nombre para mostrar. ej: 'chofyai-studio' → 'ChofyAI Studio'"""
    parts = name.replace("-", " ").split()
    return " ".join(p.capitalize() for p in parts)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. GITHUB — repos públicos y detección de nuevos
# ═══════════════════════════════════════════════════════════════════════════════

def get_public_repos():
    log("Consultando repos GitHub...", "HEAD")
    out, code = run_capture(
        "gh repo list vladimiracunadev-create --limit 50 "
        "--json name,isPrivate,description,updatedAt,url"
    )
    if code != 0:
        log("No se pudo conectar a GitHub (gh auth login?)", "WARN")
        return []
    repos = json.loads(out)
    public = [r for r in repos if not r["isPrivate"] and r["name"] not in HIDDEN_REPOS]
    log(f"{len(public)} repos públicos (excluidos ocultos)", "OK")
    return public


def get_known_projects():
    data = json.loads((API_DIR / "projects.json").read_text(encoding="utf-8"))
    return {p["url"].rstrip("/"): p for p in data.get("projects", []) if p.get("url")}


def detect_new_repos(public_repos, known_projects):
    new = []
    for r in public_repos:
        if r["name"] in SKIP_AS_PROJECT:
            continue
        url = f"https://github.com/vladimiracunadev-create/{r['name']}"
        if url not in known_projects:
            new.append(r)
    return new


def detect_updated_repos(public_repos, known_projects):
    """Detecta repos existentes cuya descripción cambió en GitHub."""
    updated = []
    for r in public_repos:
        if r["name"] in SKIP_AS_PROJECT:
            continue
        url = f"https://github.com/vladimiracunadev-create/{r['name']}"
        if url not in known_projects:
            continue  # es nuevo, lo maneja detect_new_repos
        gh_desc = (r.get("description") or "").strip()
        stored_desc = (known_projects[url].get("description") or "").strip()
        if gh_desc and gh_desc != stored_desc:
            updated.append({"repo": r, "old_desc": stored_desc, "new_desc": gh_desc})
    return updated


# ═══════════════════════════════════════════════════════════════════════════════
# 2. API v1 — generated_at, profile label, nuevos proyectos
# ═══════════════════════════════════════════════════════════════════════════════

def update_api_json(new_repos, updated_repos, apply=False):
    log("Actualizando api/v1/...", "HEAD")
    changes = []

    for json_file in API_DIR.glob("*.json"):
        data = json.loads(json_file.read_text(encoding="utf-8"))
        meta = data.get("meta", {})
        if meta.get("generated_at") != TODAY:
            changes.append(f"{json_file.name}: generated_at → {TODAY}")
            if apply:
                meta["generated_at"] = TODAY
                data["meta"] = meta
                json_file.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")

    profile_file = API_DIR / "profile.json"
    profile = json.loads(profile_file.read_text(encoding="utf-8"))
    if profile.get("label") != PROFILE_LABEL:
        changes.append("profile.json: label actualizado")
        if apply:
            profile["label"] = PROFILE_LABEL
            profile_file.write_text(json.dumps(profile, ensure_ascii=False, indent=4), encoding="utf-8")

    projects_file = API_DIR / "projects.json"
    projects_data = json.loads(projects_file.read_text(encoding="utf-8"))
    projects_modified = False

    if new_repos:
        for r in new_repos:
            entry = {
                "name": r["name"],
                "description": r.get("description") or "",
                "url": f"https://github.com/vladimiracunadev-create/{r['name']}",
                "tags": [],
                "category": REPO_CATEGORIES.get(r["name"], "other"),
            }
            changes.append(f"projects.json: + {r['name']}")
            if apply:
                projects_data["projects"].append(entry)
                projects_modified = True

    if updated_repos:
        for u in updated_repos:
            name = u["repo"]["name"]
            url  = f"https://github.com/vladimiracunadev-create/{name}"
            changes.append(f"projects.json: descripcion '{name}' actualizada")
            if apply:
                for p in projects_data["projects"]:
                    if p.get("url", "").rstrip("/") == url:
                        p["description"] = u["new_desc"]
                        projects_modified = True
                        break

    if projects_modified:
        projects_file.write_text(json.dumps(projects_data, ensure_ascii=False, indent=4), encoding="utf-8")

    if changes:
        for c in changes:
            log(c, "OK" if apply else "WARN")
    else:
        log("api/v1/ ya está al día", "OK")
    return changes


# ═══════════════════════════════════════════════════════════════════════════════
# 3. GAP 4 — Propagar identidad (subtítulos) a scripts de generación de PDFs
# ═══════════════════════════════════════════════════════════════════════════════

# Patrones de subtítulo en los scripts (para detectar y reemplazar)
# generate-all-languages.py usa subtitle_rec y subtitle_ats
SUBTITLE_PATTERNS_ALL = {
    "es": (r'"subtitle_rec": ".+?"', r'"subtitle_ats": ".+?"'),
    "en": (r'"subtitle_rec": ".+?"', r'"subtitle_ats": ".+?"'),
    "pt": (r'"subtitle_rec": ".+?"', r'"subtitle_ats": ".+?"'),
    "it": (r'"subtitle_rec": ".+?"', r'"subtitle_ats": ".+?"'),
    "fr": (r'"subtitle_rec": ".+?"', r'"subtitle_ats": ".+?"'),
    "zh": (r'"subtitle_rec": ".+?"', r'"subtitle_ats": ".+?"'),
}

# Índice de aparición de subtitle_rec por idioma en generate-all-languages.py (orden: es, en, pt, it, fr, zh)
LANG_ORDER = ["es", "en", "pt", "it", "fr", "zh"]


def sync_identity_all_languages(apply=False):
    """Actualiza subtitle_rec y subtitle_ats en generate-all-languages.py."""
    script = SCRIPTS_DIR / "generate-all-languages.py"
    content = script.read_text(encoding="utf-8")
    original = content
    changes = []

    # Reemplaza la n-ésima ocurrencia de subtitle_rec y subtitle_ats
    for idx, lang in enumerate(LANG_ORDER):
        subtitle = SUBTITLES[lang]
        rec_new = f'"subtitle_rec": "{subtitle}"'
        ats_new = f'"subtitle_ats": "{subtitle}"'

        # Encontrar la (idx+1)-ésima ocurrencia de "subtitle_rec"
        for field_old, field_new in [
            (r'"subtitle_rec": "[^"]*"', rec_new),
            (r'"subtitle_ats": "[^"]*"', ats_new),
        ]:
            matches = list(re.finditer(field_old, content))
            if idx < len(matches):
                m = matches[idx]
                if m.group() != field_new:
                    changes.append(f"generate-all-languages.py [{lang}] subtitle → actualizado")
                    content = content[:m.start()] + field_new + content[m.end():]
                    # Re-calcular después de cada reemplazo
                    matches = list(re.finditer(field_old, content))

    if content != original:
        if apply:
            script.write_text(content, encoding="utf-8")
        for c in set(changes):
            log(c, "OK" if apply else "WARN")
    else:
        log("generate-all-languages.py: subtítulos al día", "OK")


def sync_identity_portfolio(apply=False):
    """Actualiza subtitle en generate-portfolio.py."""
    script = SCRIPTS_DIR / "generate-portfolio.py"
    content = script.read_text(encoding="utf-8")
    original = content

    matches = list(re.finditer(r'"subtitle": "[^"]*"', content))
    if len(matches) < len(LANG_ORDER):
        log("generate-portfolio.py: no se encontraron todos los subtítulos", "WARN")
        return

    for idx, lang in enumerate(LANG_ORDER):
        subtitle = SUBTITLES[lang]
        field_new = f'"subtitle": "{subtitle}"'
        matches = list(re.finditer(r'"subtitle": "[^"]*"', content))
        if idx < len(matches):
            m = matches[idx]
            if m.group() != field_new:
                content = content[:m.start()] + field_new + content[m.end():]

    if content != original:
        log("generate-portfolio.py: subtítulos actualizados", "OK" if apply else "WARN")
        if apply:
            script.write_text(content, encoding="utf-8")
    else:
        log("generate-portfolio.py: subtítulos al día", "OK")


def sync_identity(apply=False):
    log("Sincronizando identidad (subtítulos en scripts PDF)...", "HEAD")
    sync_identity_all_languages(apply=apply)
    sync_identity_portfolio(apply=apply)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. GAP 2 — Inyectar nuevos repos en scripts de generación de PDFs
# ═══════════════════════════════════════════════════════════════════════════════

def _inject_before_last(content, pattern_open, entry_str, close_char):
    """
    Encuentra el último bloque que abre con pattern_open y cierra con close_char,
    e inserta entry_str antes del cierre. Devuelve (new_content, changed).
    """
    # Busca todas las posiciones del cierre dentro de bloques que empiecen con pattern_open
    positions = [m.start() for m in re.finditer(re.escape(close_char), content)]
    opens = [m.end() for m in re.finditer(pattern_open, content)]
    if not opens or not positions:
        return content, False
    # Tomar el último bloque abierto y su cierre más próximo después
    last_open = opens[-1]
    close_pos = next((p for p in positions if p > last_open), None)
    if close_pos is None:
        return content, False
    new_content = content[:close_pos] + entry_str + content[close_pos:]
    return new_content, True


def inject_into_all_languages(new_repos, apply=False):
    """Inyecta entries de nuevos repos en generate-all-languages.py."""
    if not new_repos:
        return
    script = SCRIPTS_DIR / "generate-all-languages.py"
    content = script.read_text(encoding="utf-8")
    original = content
    changes = []

    for r in new_repos:
        key   = repo_key(r["name"])
        title = repo_display(r["name"])
        url   = f"https://github.com/vladimiracunadev-create/{r['name']}"
        # strip_emojis: los PDFs (reportlab) no soportan emojis → puntos negros
        desc  = strip_emojis((r.get("description") or title)).rstrip(".")

        # 1. PROJECTS_URLS
        url_entry = f'    "{key}": "{url}",\n'
        if f'"{key}":' not in content:
            content, ok = _inject_before_last(content, r'PROJECTS_URLS\s*=\s*\{', url_entry, "}")
            if ok:
                changes.append(f"PROJECTS_URLS: + {key}")

        # 2. projects_rec (una entrada por idioma — 6 ocurrencias)
        rec_entries = {
            "es": f'                "{title} \u2014 {desc}",\n',
            "en": f'                "{title} \u2014 {desc}",\n',
            "pt": f'                "{title} \u2014 {desc}",\n',
            "it": f'                "{title} \u2014 {desc}",\n',
            "fr": f'                "{title} \u2014 {desc}",\n',
            "zh": f'                "{title} \u2014 {desc}",\n',
        }
        # Buscar todas las posiciones de "projects_rec": [
        rec_positions = [m.start() for m in re.finditer(r'"projects_rec":\s*\[', content)]
        for idx, pos in enumerate(rec_positions):
            lang = LANG_ORDER[idx] if idx < len(LANG_ORDER) else "es"
            entry = rec_entries[lang]
            # Verificar que la entrada no exista ya
            segment_end = content.find('],', pos)
            if segment_end == -1:
                continue
            segment = content[pos:segment_end]
            if title in segment:
                continue
            content = content[:segment_end] + entry + content[segment_end:]
            # Recalcular posiciones después de modificar
            rec_positions = [m.start() for m in re.finditer(r'"projects_rec":\s*\[', content)]
        changes.append(f"projects_rec (6 langs): + {title}")

        # 3. projects_ats (una tupla por idioma — 6 ocurrencias)
        ats_entries = {
            "es": f'                ("{title} \u2014 {desc}:", "{key}"),\n',
            "en": f'                ("{title} \u2014 {desc}:", "{key}"),\n',
            "pt": f'                ("{title} \u2014 {desc}:", "{key}"),\n',
            "it": f'                ("{title} \u2014 {desc}:", "{key}"),\n',
            "fr": f'                ("{title} \u2014 {desc} :", "{key}"),\n',
            "zh": f'                ("{title} \u2014 {desc}\uff1a", "{key}"),\n',
        }
        ats_positions = [m.start() for m in re.finditer(r'"projects_ats":\s*\[', content)]
        for idx, pos in enumerate(ats_positions):
            lang = LANG_ORDER[idx] if idx < len(LANG_ORDER) else "es"
            entry = ats_entries[lang]
            segment_end = content.find('],', pos)
            if segment_end == -1:
                continue
            segment = content[pos:segment_end]
            if key in segment:
                continue
            content = content[:segment_end] + entry + content[segment_end:]
            ats_positions = [m.start() for m in re.finditer(r'"projects_ats":\s*\[', content)]
        changes.append(f"projects_ats (6 langs): + {title}")

    if content != original:
        if apply:
            script.write_text(content, encoding="utf-8")
        for c in changes:
            log(c, "OK" if apply else "WARN")
    else:
        log("generate-all-languages.py: sin cambios de proyectos", "OK")


def inject_into_portfolio(new_repos, apply=False):
    """Inyecta entries de nuevos repos en generate-portfolio.py."""
    if not new_repos:
        return
    script = SCRIPTS_DIR / "generate-portfolio.py"
    content = script.read_text(encoding="utf-8")
    original = content
    changes = []

    for r in new_repos:
        key   = repo_key(r["name"])
        title = repo_display(r["name"])
        # strip_emojis: los PDFs (reportlab) no soportan emojis → puntos negros
        desc  = strip_emojis((r.get("description") or title)).rstrip(".")

        # 1. projects list (6 ocurrencias, una por idioma)
        proj_entries = {
            "es": f'            "<b>{title}:</b> {desc}",\n',
            "en": f'            "<b>{title}:</b> {desc}",\n',
            "pt": f'            "<b>{title}:</b> {desc}",\n',
            "it": f'            "<b>{title}:</b> {desc}",\n',
            "fr": f'            "<b>{title} :</b> {desc}",\n',
            "zh": f'            "<b>{title}\uff1a</b> {desc}",\n',
        }
        proj_positions = [m.start() for m in re.finditer(r'"projects":\s*\[', content)]
        for idx, pos in enumerate(proj_positions):
            lang = LANG_ORDER[idx] if idx < len(LANG_ORDER) else "es"
            entry = proj_entries[lang]
            segment_end = content.find('],', pos)
            if segment_end == -1:
                continue
            segment = content[pos:segment_end]
            if title in segment:
                continue
            content = content[:segment_end] + entry + content[segment_end:]
            proj_positions = [m.start() for m in re.finditer(r'"projects":\s*\[', content)]
        changes.append(f"portfolio projects (6 langs): + {title}")

        # 2. project_link_labels (6 ocurrencias)
        label_entry = f'            "{key}": "{title}",\n'
        label_positions = [m.start() for m in re.finditer(r'"project_link_labels":\s*\{', content)]
        for pos in label_positions:
            segment_end = content.find('},', pos)
            if segment_end == -1:
                continue
            segment = content[pos:segment_end]
            if f'"{key}":' in segment:
                continue
            content = content[:segment_end] + label_entry + content[segment_end:]
            label_positions = [m.start() for m in re.finditer(r'"project_link_labels":\s*\{', content)]
        changes.append(f"project_link_labels (6 langs): + {key}")

    if content != original:
        if apply:
            script.write_text(content, encoding="utf-8")
        for c in changes:
            log(c, "OK" if apply else "WARN")
    else:
        log("generate-portfolio.py: sin cambios de proyectos", "OK")


def inject_into_pdf_scripts(new_repos, apply=False):
    log("Actualizando scripts de generación de PDFs...", "HEAD")
    inject_into_all_languages(new_repos, apply=apply)
    inject_into_portfolio(new_repos, apply=apply)


# ═══════════════════════════════════════════════════════════════════════════════
# 5. GAP 1 — Agregar cards HTML en index.html (#proyectos)
# ═══════════════════════════════════════════════════════════════════════════════

CARD_TEMPLATE = """\

          <article class="card project" data-min-level="1">
            <div class="project__head">
              <h3 data-es>{title} · {tag_es}</h3>
              <h3 data-en>{title} · {tag_en}</h3>
              <h3 data-pt>{title} · {tag_pt}</h3>
              <h3 data-it>{title} · {tag_it}</h3>
              <h3 data-fr>{title} · {tag_fr}</h3>
              <h3 data-zh>{title} · {tag_zh}</h3>
              <span class="tag" data-es>{tag_es}</span><span class="tag" data-en>{tag_en}</span><span class="tag" data-pt>{tag_pt}</span><span class="tag" data-it>{tag_it}</span><span class="tag" data-fr>{tag_fr}</span><span class="tag" data-zh>{tag_zh}</span>
            </div>
            <p>
              <span data-es>{desc}</span>
              <span data-en>{desc}</span>
              <span data-pt>{desc}</span>
              <span data-it>{desc}</span>
              <span data-fr>{desc}</span>
              <span data-zh>{desc}</span>
            </p>
            <div class="actions">
              <a class="btn primary" href="{url}" target="_blank" rel="noreferrer"><span data-es>Repo (GitHub)</span><span data-en>Repo (GitHub)</span><span data-pt>Repo (GitHub)</span><span data-it>Repo (GitHub)</span><span data-fr>Repo (GitHub)</span><span data-zh>Repo (GitHub)</span></a>
            </div>
          </article>
"""

# Marcador de inserción: justo antes del footer de nota de IA en #proyectos
CARD_ANCHOR = '<p class="small muted text-center-pad" data-es>'


def inject_html_cards(new_repos, apply=False):
    """Agrega project cards en index.html para repos nuevos."""
    if not new_repos:
        return
    log("Actualizando index.html (#proyectos)...", "HEAD")

    content = INDEX_HTML.read_text(encoding="utf-8")
    original = content
    changes = []

    for r in new_repos:
        title = repo_display(r["name"])
        url   = f"https://github.com/vladimiracunadev-create/{r['name']}"
        # strip_emojis: emojis en descripciones rompen la semántica visual del HTML
        desc  = strip_emojis((r.get("description") or title)).rstrip(".")
        cat   = REPO_CATEGORIES.get(r["name"], "other")
        tags  = CATEGORY_TAGS.get(cat, CATEGORY_TAGS["other"])

        # Verificar si ya existe un card para este repo
        if url in content:
            log(f"index.html: card '{title}' ya existe — omitido", "OK")
            continue

        card = CARD_TEMPLATE.format(
            title=title, url=url, desc=desc,
            tag_es=tags["es"], tag_en=tags["en"], tag_pt=tags["pt"],
            tag_it=tags["it"], tag_fr=tags["fr"], tag_zh=tags["zh"],
        )

        # Insertar antes del anchor (nota de IA)
        if CARD_ANCHOR in content:
            content = content.replace(CARD_ANCHOR, card + "          " + CARD_ANCHOR, 1)
            changes.append(f"index.html: card + {title}")
        else:
            log(f"index.html: no se encontró anchor de inserción para '{title}'", "WARN")

    if content != original:
        if apply:
            INDEX_HTML.write_text(content, encoding="utf-8")
        for c in changes:
            log(c, "OK" if apply else "WARN")
        log("[!!] Traduce PT/IT/FR/ZH en las cards nuevas cuando sea posible", "WARN")
    else:
        log("index.html: sin cards nuevas que agregar", "OK")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. README perfil GitHub
# ═══════════════════════════════════════════════════════════════════════════════

def update_github_readme(new_repos, apply=False):
    if not new_repos:
        log("README GitHub: sin repos nuevos", "OK")
        return
    log("Actualizando README perfil GitHub...", "HEAD")

    # Dos llamadas separadas para evitar problemas de quoting en Windows (shell=True)
    readme_api = "repos/vladimiracunadev-create/vladimiracunadev-create/contents/README.md"
    content_b64, code1 = run_capture(f"gh api {readme_api} --jq .content")
    sha, code2         = run_capture(f"gh api {readme_api} --jq .sha")
    if code1 != 0 or code2 != 0:
        log("No se pudo leer README de GitHub", "WARN")
        return

    readme = base64.b64decode(content_b64).decode("utf-8")

    separator = "---\n\n## ⚡"
    new_sections = ""
    for r in new_repos:
        if r["name"] in readme:
            continue
        url  = f"https://github.com/vladimiracunadev-create/{r['name']}"
        desc = r.get("description") or "Repositorio público."
        new_sections += (
            f"\n### {repo_display(r['name'])}\n"
            f"**Repo:** {url}\n"
            f"**Qué demuestra:** {desc}\n"
        )

    if not new_sections:
        log("README GitHub: ya está al día", "OK")
        return

    updated = readme.replace(separator, new_sections + separator, 1)
    if apply:
        encoded = base64.b64encode(updated.encode("utf-8")).decode("ascii")
        r2 = subprocess.run(
            ["gh", "api", "--method", "PUT",
             "repos/vladimiracunadev-create/vladimiracunadev-create/contents/README.md",
             "--field", f"message=feat: add {', '.join(r['name'] for r in new_repos)} to profile README",
             "--field", f"content={encoded}",
             "--field", f"sha={sha}",
             "--jq", ".commit.sha"],
            capture_output=True, text=True
        )
        if r2.returncode == 0:
            log(f"README actualizado → {r2.stdout.strip()[:8]}", "OK")
        else:
            log(f"Error en README: {r2.stderr[:100]}", "ERR")
    else:
        log(f"[dry-run] Agregaría {len(new_repos)} sección(es) al README", "WARN")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. BACKUP + REGENERAR PDFs
# ═══════════════════════════════════════════════════════════════════════════════

def backup_pdfs(apply=False):
    backup_dir = ASSETS_DIR / "backups" / TODAY
    pdfs = list(ASSETS_DIR.glob("*.pdf"))
    if not pdfs:
        log("No hay PDFs para respaldar", "WARN")
        return
    if backup_dir.exists():
        log(f"Backup {TODAY} ya existe — omitiendo", "OK")
        return
    log(f"Creando backup en assets/backups/{TODAY}/...", "HEAD")
    if apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        for pdf in pdfs:
            shutil.copy2(pdf, backup_dir / f"{pdf.stem}_v1.pdf")
        log(f"{len(pdfs)} PDFs respaldados", "OK")
    else:
        log(f"[dry-run] Se respaldarían {len(pdfs)} PDFs", "WARN")


def regenerate_pdfs(apply=False):
    log("Regenerando PDFs...", "HEAD")
    scripts = [
        "generate-all-languages.py",
        "generate-portfolio.py",
        "generate-achievements-statement.py",
        "generate-recommendation-letter.py",
    ]
    for name in scripts:
        path = SCRIPTS_DIR / name
        if not path.exists():
            log(f"{name} no encontrado — omitido", "WARN")
            continue
        if apply:
            r = subprocess.run([sys.executable, str(path)], cwd=str(ROOT),
                               capture_output=True, text=True)
            log(f"{name}", "OK" if r.returncode == 0 else "ERR")
            if r.returncode != 0:
                log(r.stderr[:200], "ERR")
        else:
            log(f"[dry-run] {name}", "WARN")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. CHANGELOG
# ═══════════════════════════════════════════════════════════════════════════════

def update_changelog(new_repos, api_changes, identity_changed, skip_pdfs, apply=False):
    changelog = ROOT / "CHANGELOG.md"
    items = []
    if api_changes:
        items.append(f"- `api/v1/`: generated_at → {TODAY}")
    if new_repos:
        names = ", ".join(r["name"] for r in new_repos)
        items.append(f"- Repos nuevos integrados: {names}")
        items.append("- Cards HTML agregados en `#proyectos` (index.html)")
        items.append("- Scripts PDF y api/v1/projects.json actualizados")
    if identity_changed:
        items.append("- Subtítulos de identidad propagados a scripts de PDFs")
    if not skip_pdfs:
        items.append("- 30 PDFs regenerados (5 tipos × 6 idiomas)")
        items.append(f"- Backup en `assets/backups/{TODAY}/`")

    if not items:
        log("CHANGELOG: sin cambios", "OK")
        return

    entry = f"## {TODAY}\n\n### sync-portfolio (automático)\n\n" + "\n".join(items) + "\n\n"
    log("Actualizando CHANGELOG.md...", "HEAD")
    if apply:
        original = changelog.read_text(encoding="utf-8")
        updated = original.replace("# Changelog\n\n", "# Changelog\n\n" + entry, 1)
        changelog.write_text(updated, encoding="utf-8")
        log("CHANGELOG.md actualizado", "OK")
    else:
        log("[dry-run] Agregaría entrada en CHANGELOG.md", "WARN")


# ═══════════════════════════════════════════════════════════════════════════════
# 9. COMMIT + PUSH
# ═══════════════════════════════════════════════════════════════════════════════

def git_commit_push(new_repos, skip_pdfs, no_push, apply=False):
    if not apply:
        log("[dry-run] Haría commit + push", "WARN")
        return
    log("Preparando commit...", "HEAD")

    files = ["api/v1/", "CHANGELOG.md", "index.html",
             "scripts/generate-all-languages.py", "scripts/generate-portfolio.py"]
    if not skip_pdfs:
        files.append("assets/")

    for f in files:
        subprocess.run(f'git -C "{ROOT}" add {f}', shell=True, capture_output=True)

    details = []
    if new_repos:
        details.append(f"repos nuevos: {', '.join(r['name'] for r in new_repos)}")
    if not skip_pdfs:
        details.append("30 PDFs regenerados")
    details.append(f"api/v1/ → {TODAY}")

    body = "\n".join(f"- {d}" for d in details)
    msg = (
        f"chore(sync): auto-sync {TODAY}\n\n"
        f"{body}\n\n"
        "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    )

    r = subprocess.run(
        ["git", "-C", str(ROOT), "commit", "-m", msg],
        capture_output=True, text=True
    )
    if r.returncode == 0:
        log("Commit creado", "OK")
    elif "nothing to commit" in r.stdout + r.stderr:
        log("Nada que commitear — ya está al día", "OK")
        return
    else:
        log(f"Error en commit: {r.stderr[:100]}", "ERR")
        return

    if not no_push:
        r2 = subprocess.run(["git", "-C", str(ROOT), "push"], capture_output=True, text=True)
        log("Push exitoso" if r2.returncode == 0 else f"Error push: {r2.stderr[:80]}",
            "OK" if r2.returncode == 0 else "ERR")
    else:
        log("--no-push activo", "WARN")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Sincroniza el portafolio completo (API, HTML, PDFs, README, GitHub)."
    )
    parser.add_argument("--apply",      action="store_true", help="Aplica cambios")
    parser.add_argument("--no-push",    action="store_true", help="Aplica sin push")
    parser.add_argument("--skip-pdfs",  action="store_true", help="Omite regenerar PDFs")
    parser.add_argument("--only-api",   action="store_true", help="Solo api/v1/")
    args = parser.parse_args()

    skip_pdfs = args.skip_pdfs or args.only_api
    apply     = args.apply

    if not apply:
        print("\n" + "="*60)
        print("  DRY-RUN — ningún archivo será modificado")
        print("  Usa --apply para ejecutar los cambios")
        print("="*60)

    # Repos
    public_repos    = get_public_repos()
    known_projects  = get_known_projects()
    new_repos       = detect_new_repos(public_repos, known_projects)
    updated_repos   = detect_updated_repos(public_repos, known_projects)

    if new_repos:
        log(f"Repos nuevos: {[r['name'] for r in new_repos]}", "WARN")
    else:
        log("Sin repos públicos nuevos", "OK")

    if updated_repos:
        for u in updated_repos:
            log(f"Descripcion cambiada — {u['repo']['name']}:", "WARN")
            log(f"  antes: {u['old_desc'][:80]}", "INFO")
            log(f"  ahora: {u['new_desc'][:80]}", "INFO")
    else:
        log("Sin cambios de descripcion en repos existentes", "OK")

    # Gap 4: identidad
    identity_changed = False
    if not args.only_api:
        sync_identity(apply=apply)

    # API JSONs
    api_changes = update_api_json(new_repos, updated_repos, apply=apply)

    # Gap 2: scripts PDF
    if new_repos and not args.only_api:
        inject_into_pdf_scripts(new_repos, apply=apply)

    # Gap 1: cards HTML
    if new_repos and not args.only_api:
        inject_html_cards(new_repos, apply=apply)

    # README GitHub
    if new_repos:
        update_github_readme(new_repos, apply=apply)

    # PDFs
    if not skip_pdfs:
        backup_pdfs(apply=apply)
        regenerate_pdfs(apply=apply)

    # CHANGELOG
    update_changelog(new_repos, api_changes, identity_changed, skip_pdfs, apply=apply)

    # Commit + Push
    if not args.only_api:
        git_commit_push(new_repos, skip_pdfs, args.no_push, apply=apply)

    print("\n" + "="*60)
    print(f"  {'SYNC COMPLETADO' if apply else 'DRY-RUN completado'} — {TODAY}")
    if not apply:
        print("  Ejecuta con --apply para aplicar los cambios.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
