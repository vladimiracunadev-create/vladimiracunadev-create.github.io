#!/usr/bin/env python3
"""
Generate the generic "Hoja de Vida" PDF for ALL 6 languages.

This document is deliberately GENERIC: it is not tailored to any job title.
It is the classic, formal, single-column CV (LatAm "hoja de vida") meant to be
attached to any application, whatever the role name in the posting.

Outputs:
  - hoja-de-vida.pdf           (ES)
  - hoja-de-vida-english.pdf   (EN)
  - hoja-de-vida-portuguese.pdf(PT)
  - hoja-de-vida-italian.pdf   (IT)
  - hoja-de-vida-french.pdf    (FR)
  - hoja-de-vida-chinese.pdf   (ZH)

Content is NOT duplicated here: the translated blocks (summary, experience,
skills, degrees, previous career, projects, training) are imported from
generate-all-languages.py so there is a single source of truth. Only the
labels specific to this document live in this file.
"""

import os
import sys
import importlib.util

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "assets"))


# ═══════════════════════════════════════════════════
# SHARED CONTENT (single source of truth)
# ═══════════════════════════════════════════════════

def _load_shared():
    """Import generate-all-languages.py (hyphenated name -> importlib)."""
    path = os.path.join(SCRIPT_DIR, "generate-all-languages.py")
    spec = importlib.util.spec_from_file_location("gen_all_languages", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["gen_all_languages"] = module
    spec.loader.exec_module(module)
    return module


G = _load_shared()

LANGS = ["es", "en", "pt", "it", "fr", "zh"]
LANG_SUFFIX = G.LANG_SUFFIX

# ── Colors (aligned with the rest of the PDF suite) ──
NAVY = HexColor("#1e3a5f")
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#444444")
SOFT = HexColor("#666666")
ACCENT = HexColor("#2563eb")
LINE_COLOR = HexColor("#cccccc")
BAND_BG = HexColor("#f5f7fa")

BASE_ASSETS_URL = "https://vladimiracunadev-create.github.io/assets"


# ═══════════════════════════════════════════════════
# DOCUMENT-SPECIFIC LABELS
# ═══════════════════════════════════════════════════

HDV = {
    "es": {
        "doc_title": "HOJA DE VIDA",
        "doc_note": "Documento genérico de presentación profesional. No está dirigido a un cargo específico: sirve para cualquier proceso de selección, con independencia del nombre del puesto.",
        "h_personal": "DATOS PERSONALES",
        "l_name": "Nombre completo", "l_location": "Ubicación", "l_phone": "Teléfono",
        "l_email": "Correo electrónico", "l_web": "Sitio web / portafolio",
        "l_linkedin": "LinkedIn", "l_github": "GitHub", "l_gitlab": "GitLab",
        "l_updated": "Actualizado", "updated": "agosto de 2026",
        "h_profile": "PERFIL PROFESIONAL",
        "h_experience": "EXPERIENCIA LABORAL",
        "exp_role": "Arquitecto de Software · Analista y Desarrollador Full-Stack",
        "exp_company": "Fundación CEIS Maristas — Santiago, Chile",
        "exp_period": "mayo 2011 — octubre 2025",
        "l_functions": "Funciones y responsabilidades",
        "l_achievements": "Logros verificados",
        "l_tech": "Tecnologías",
        "h_previous": "TRAYECTORIA PREVIA",
        "previous_note": "Desarrollo web, soporte de sistemas y reportería para instituciones públicas y privadas.",
        "h_education": "FORMACIÓN ACADÉMICA",
        "h_skills": "COMPETENCIAS TÉCNICAS",
        "h_projects": "PROYECTOS Y PORTAFOLIO",
        "projects_note": "El detalle técnico, las métricas y el código de cada proyecto están en el portafolio PDF y en el sitio web.",
        "h_training": "FORMACIÓN Y ACTIVIDAD RECIENTE",
        "h_languages": "IDIOMAS",
        "lang_native": "Español: nativo.",
        "h_refs": "REFERENCIAS Y DOCUMENTOS DE RESPALDO",
        "refs_available": "Referencias laborales disponibles a solicitud.",
        "ref_manager": "Último jefe directo: Jean Claude Dupry (Fundación CEIS Maristas) — contacto disponible a solicitud.",
        "footer_note": "Esta hoja de vida está publicada en 6 idiomas (ES · EN · PT · IT · FR · ZH) en",
        "page": "pág.",
    },
    "en": {
        "doc_title": "CURRICULUM VITAE",
        "doc_note": "General professional profile document. It is not tailored to a specific job title: it works for any selection process, whatever the position is called.",
        "h_personal": "PERSONAL DETAILS",
        "l_name": "Full name", "l_location": "Location", "l_phone": "Phone",
        "l_email": "Email", "l_web": "Website / portfolio",
        "l_linkedin": "LinkedIn", "l_github": "GitHub", "l_gitlab": "GitLab",
        "l_updated": "Last updated", "updated": "August 2026",
        "h_profile": "PROFESSIONAL PROFILE",
        "h_experience": "WORK EXPERIENCE",
        "exp_role": "Software Architect · Systems Analyst & Full-Stack Developer",
        "exp_company": "Fundación CEIS Maristas — Santiago, Chile",
        "exp_period": "May 2011 — October 2025",
        "l_functions": "Duties and responsibilities",
        "l_achievements": "Verified achievements",
        "l_tech": "Technologies",
        "h_previous": "PREVIOUS CAREER",
        "previous_note": "Web development, systems support and reporting for public and private institutions.",
        "h_education": "EDUCATION",
        "h_skills": "TECHNICAL SKILLS",
        "h_projects": "PROJECTS AND PORTFOLIO",
        "projects_note": "Technical detail, metrics and source code for each project are in the portfolio PDF and on the website.",
        "h_training": "RECENT TRAINING AND ACTIVITY",
        "h_languages": "LANGUAGES",
        "lang_native": "Spanish: native.",
        "h_refs": "REFERENCES AND SUPPORTING DOCUMENTS",
        "refs_available": "Work references available upon request.",
        "ref_manager": "Most recent direct manager: Jean Claude Dupry (Fundación CEIS Maristas) — contact available upon request.",
        "footer_note": "This CV is published in 6 languages (ES · EN · PT · IT · FR · ZH) at",
        "page": "p.",
    },
    "pt": {
        "doc_title": "CURRÍCULO",
        "doc_note": "Documento genérico de apresentação profissional. Não é direcionado a um cargo específico: serve para qualquer processo seletivo, independentemente do nome da vaga.",
        "h_personal": "DADOS PESSOAIS",
        "l_name": "Nome completo", "l_location": "Localização", "l_phone": "Telefone",
        "l_email": "E-mail", "l_web": "Site / portfólio",
        "l_linkedin": "LinkedIn", "l_github": "GitHub", "l_gitlab": "GitLab",
        "l_updated": "Atualizado em", "updated": "agosto de 2026",
        "h_profile": "PERFIL PROFISSIONAL",
        "h_experience": "EXPERIÊNCIA PROFISSIONAL",
        "exp_role": "Arquiteto de Software · Analista e Desenvolvedor Full-Stack",
        "exp_company": "Fundación CEIS Maristas — Santiago, Chile",
        "exp_period": "maio 2011 — outubro 2025",
        "l_functions": "Funções e responsabilidades",
        "l_achievements": "Resultados verificados",
        "l_tech": "Tecnologias",
        "h_previous": "TRAJETÓRIA ANTERIOR",
        "previous_note": "Desenvolvimento web, suporte de sistemas e relatórios para instituições públicas e privadas.",
        "h_education": "FORMAÇÃO ACADÊMICA",
        "h_skills": "COMPETÊNCIAS TÉCNICAS",
        "h_projects": "PROJETOS E PORTFÓLIO",
        "projects_note": "O detalhe técnico, as métricas e o código de cada projeto estão no portfólio em PDF e no site.",
        "h_training": "FORMAÇÃO E ATIVIDADE RECENTE",
        "h_languages": "IDIOMAS",
        "lang_native": "Espanhol: nativo.",
        "h_refs": "REFERÊNCIAS E DOCUMENTOS DE APOIO",
        "refs_available": "Referências profissionais disponíveis mediante solicitação.",
        "ref_manager": "Último gestor direto: Jean Claude Dupry (Fundación CEIS Maristas) — contato disponível mediante solicitação.",
        "footer_note": "Este currículo está publicado em 6 idiomas (ES · EN · PT · IT · FR · ZH) em",
        "page": "pág.",
    },
    "it": {
        "doc_title": "CURRICULUM VITAE",
        "doc_note": "Documento generico di presentazione professionale. Non è riferito a una posizione specifica: è valido per qualsiasi processo di selezione, indipendentemente dal nome del ruolo.",
        "h_personal": "DATI PERSONALI",
        "l_name": "Nome completo", "l_location": "Località", "l_phone": "Telefono",
        "l_email": "E-mail", "l_web": "Sito web / portfolio",
        "l_linkedin": "LinkedIn", "l_github": "GitHub", "l_gitlab": "GitLab",
        "l_updated": "Aggiornato", "updated": "agosto 2026",
        "h_profile": "PROFILO PROFESSIONALE",
        "h_experience": "ESPERIENZA LAVORATIVA",
        "exp_role": "Architetto Software · Analista e Sviluppatore Full-Stack",
        "exp_company": "Fundación CEIS Maristas — Santiago, Cile",
        "exp_period": "maggio 2011 — ottobre 2025",
        "l_functions": "Mansioni e responsabilità",
        "l_achievements": "Risultati verificati",
        "l_tech": "Tecnologie",
        "h_previous": "PERCORSO PRECEDENTE",
        "previous_note": "Sviluppo web, supporto sistemi e reportistica per istituzioni pubbliche e private.",
        "h_education": "FORMAZIONE ACCADEMICA",
        "h_skills": "COMPETENZE TECNICHE",
        "h_projects": "PROGETTI E PORTFOLIO",
        "projects_note": "Il dettaglio tecnico, le metriche e il codice di ogni progetto sono nel portfolio PDF e sul sito web.",
        "h_training": "FORMAZIONE E ATTIVITÀ RECENTE",
        "h_languages": "LINGUE",
        "lang_native": "Spagnolo: madrelingua.",
        "h_refs": "REFERENZE E DOCUMENTI DI SUPPORTO",
        "refs_available": "Referenze lavorative disponibili su richiesta.",
        "ref_manager": "Ultimo responsabile diretto: Jean Claude Dupry (Fundación CEIS Maristas) — contatto disponibile su richiesta.",
        "footer_note": "Questo curriculum è pubblicato in 6 lingue (ES · EN · PT · IT · FR · ZH) su",
        "page": "pag.",
    },
    "fr": {
        "doc_title": "CURRICULUM VITAE",
        "doc_note": "Document générique de présentation professionnelle. Il ne vise pas un poste précis : il convient à tout processus de recrutement, quel que soit l'intitulé du poste.",
        "h_personal": "DONNÉES PERSONNELLES",
        "l_name": "Nom complet", "l_location": "Localisation", "l_phone": "Téléphone",
        "l_email": "E-mail", "l_web": "Site web / portfolio",
        "l_linkedin": "LinkedIn", "l_github": "GitHub", "l_gitlab": "GitLab",
        "l_updated": "Mise à jour", "updated": "août 2026",
        "h_profile": "PROFIL PROFESSIONNEL",
        "h_experience": "EXPÉRIENCE PROFESSIONNELLE",
        "exp_role": "Architecte Logiciel · Analyste et Développeur Full-Stack",
        "exp_company": "Fundación CEIS Maristas — Santiago, Chili",
        "exp_period": "mai 2011 — octobre 2025",
        "l_functions": "Missions et responsabilités",
        "l_achievements": "Résultats vérifiés",
        "l_tech": "Technologies",
        "h_previous": "PARCOURS ANTÉRIEUR",
        "previous_note": "Développement web, support systèmes et reporting pour des institutions publiques et privées.",
        "h_education": "FORMATION ACADÉMIQUE",
        "h_skills": "COMPÉTENCES TECHNIQUES",
        "h_projects": "PROJETS ET PORTFOLIO",
        "projects_note": "Le détail technique, les métriques et le code de chaque projet figurent dans le portfolio PDF et sur le site web.",
        "h_training": "FORMATION ET ACTIVITÉ RÉCENTE",
        "h_languages": "LANGUES",
        "lang_native": "Espagnol : langue maternelle.",
        "h_refs": "RÉFÉRENCES ET DOCUMENTS JUSTIFICATIFS",
        "refs_available": "Références professionnelles disponibles sur demande.",
        "ref_manager": "Dernier responsable direct : Jean Claude Dupry (Fundación CEIS Maristas) — contact disponible sur demande.",
        "footer_note": "Ce curriculum vitae est publié en 6 langues (ES · EN · PT · IT · FR · ZH) sur",
        "page": "p.",
    },
    "zh": {
        "doc_title": "个人简历",
        "doc_note": "通用职业介绍文件。本文件未针对特定职位：无论招聘岗位名称为何，均适用于任何招聘流程。",
        "h_personal": "个人信息",
        "l_name": "姓名", "l_location": "所在地", "l_phone": "电话",
        "l_email": "电子邮箱", "l_web": "网站 / 作品集",
        "l_linkedin": "领英", "l_github": "GitHub", "l_gitlab": "GitLab",
        "l_updated": "更新日期", "updated": "2026年8月",
        "h_profile": "职业简介",
        "h_experience": "工作经历",
        "exp_role": "软件架构师 · 系统分析师兼全栈开发工程师",
        "exp_company": "Fundación CEIS Maristas — 智利圣地亚哥",
        "exp_period": "2011年5月 — 2025年10月",
        "l_functions": "职责与工作内容",
        "l_achievements": "已验证的成果",
        "l_tech": "技术栈",
        "h_previous": "此前职业经历",
        "previous_note": "为公共和私营机构提供网站开发、系统支持与报表服务。",
        "h_education": "教育背景",
        "h_skills": "专业技能",
        "h_projects": "项目与作品集",
        "projects_note": "各项目的技术细节、指标与源代码详见作品集PDF及网站。",
        "h_training": "近期培训与活动",
        "h_languages": "语言",
        "lang_native": "西班牙语：母语。",
        "h_refs": "推荐人与证明文件",
        "refs_available": "工作推荐人信息可应要求提供。",
        "ref_manager": "最近直属上级：Jean Claude Dupry（Fundación CEIS Maristas）——联系方式可应要求提供。",
        "footer_note": "本简历提供6种语言版本（ES · EN · PT · IT · FR · ZH），详见",
        "page": "第", "page_end": " 页",
    },
}


# ═══════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════

def make_styles(lang):
    s = dict(
        name=ParagraphStyle("HdvName", fontName="Helvetica-Bold", fontSize=21, leading=25,
                            textColor=NAVY, spaceAfter=2, alignment=TA_LEFT),
        title=ParagraphStyle("HdvTitle", fontName="Helvetica-Bold", fontSize=10, leading=13,
                             textColor=MUTED, spaceAfter=4, alignment=TA_LEFT),
        subtitle=ParagraphStyle("HdvSub", fontName="Helvetica", fontSize=9.5, leading=13,
                                textColor=DARK, spaceAfter=2, alignment=TA_LEFT),
        note=ParagraphStyle("HdvNote", fontName="Helvetica-Oblique", fontSize=8, leading=10.5,
                            textColor=SOFT, spaceAfter=2, alignment=TA_JUSTIFY),
        heading=ParagraphStyle("HdvHead", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                               textColor=NAVY, spaceBefore=8, spaceAfter=2),
        subheading=ParagraphStyle("HdvSHead", fontName="Helvetica-Bold", fontSize=10, leading=13,
                                  textColor=DARK, spaceBefore=2, spaceAfter=1),
        meta=ParagraphStyle("HdvMeta", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
                            textColor=SOFT, spaceAfter=3),
        label=ParagraphStyle("HdvLabel", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                             textColor=MUTED, spaceAfter=1),
        body=ParagraphStyle("HdvBody", fontName="Helvetica", fontSize=9, leading=12,
                            textColor=DARK, spaceAfter=2, alignment=TA_JUSTIFY),
        bullet=ParagraphStyle("HdvBullet", fontName="Helvetica", fontSize=9, leading=12,
                              textColor=DARK, spaceAfter=2, leftIndent=11, bulletIndent=0,
                              alignment=TA_JUSTIFY),
        small=ParagraphStyle("HdvSmall", fontName="Helvetica", fontSize=8.5, leading=11,
                             textColor=MUTED, spaceAfter=2),
        project=ParagraphStyle("HdvProject", fontName="Helvetica", fontSize=8, leading=10,
                               textColor=DARK, spaceAfter=1, leftIndent=8, bulletIndent=0),
        link=ParagraphStyle("HdvLink", fontName="Helvetica", fontSize=8.5, leading=11,
                            textColor=ACCENT, spaceAfter=2, leftIndent=11, bulletIndent=0),
    )
    if lang == "zh":
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
            for st in s.values():
                st.fontName = "STSong-Light"
        except Exception:
            pass
    return s


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=LINE_COLOR,
                      spaceBefore=1, spaceAfter=5)


def bullet(style, text):
    return Paragraph(f"• {text}", style)


def clean(text, lang):
    """CID fonts have no bold face: drop inline bold markup for Chinese."""
    if lang == "zh":
        return text.replace("<b>", "").replace("</b>", "")
    return text


# ═══════════════════════════════════════════════════
# BUILDER
# ═══════════════════════════════════════════════════

def build_hoja_de_vida(lang, output_path):
    T = G.get_content(lang)
    H = HDV[lang]
    s = make_styles(lang)
    suffix = LANG_SUFFIX[lang]

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.6 * inch, bottomMargin=0.75 * inch,
        title=f"{H['doc_title']} — Vladimir Acuña",
        author="Vladimir Acuña Valdebenito",
        subject=H["doc_title"],
    )
    content_w = letter[0] - 1.5 * inch

    def page_furniture(canvas, doc_):
        canvas.saveState()
        font = "STSong-Light" if lang == "zh" else "Helvetica"
        canvas.setFont(font, 7.5)
        canvas.setFillColor(SOFT)
        canvas.drawString(0.75 * inch, 0.45 * inch,
                          f"Vladimir Acuña — {H['doc_title']}")
        canvas.drawRightString(letter[0] - 0.75 * inch, 0.45 * inch,
                               f"{H['page']} {doc_.page}{H.get('page_end', '')}")
        canvas.setStrokeColor(LINE_COLOR)
        canvas.setLineWidth(0.4)
        canvas.line(0.75 * inch, 0.6 * inch, letter[0] - 0.75 * inch, 0.6 * inch)
        canvas.restoreState()

    story = []

    # ── Header band ──────────────────────────────────
    head_cell = [
        Paragraph("Vladimir Acuña", s["name"]),
        Paragraph(H["doc_title"], s["title"]),
        Paragraph(T["subtitle_rec"], s["subtitle"]),
    ]
    band = Table([[head_cell]], colWidths=[content_w])
    band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BAND_BG),
        ("LINEBELOW", (0, 0), (-1, -1), 1.4, NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(band)
    story.append(Spacer(1, 6))
    story.append(Paragraph(H["doc_note"], s["note"]))
    story.append(Spacer(1, 2))

    # ── Datos personales ─────────────────────────────
    story.append(Paragraph(H["h_personal"], s["heading"]))
    story.append(hr())
    rows = [
        (H["l_name"], "Vladimir Bernardo Acuña Valdebenito"),
        (H["l_location"], G.CONTACT_LINES[0]),
        (H["l_phone"], G.CONTACT_LINES[1]),
        (H["l_email"], G.CONTACT_LINES[2]),
        (H["l_web"], f'<link href="{G.WEB_URL}">{G.WEB_URL}</link>'),
        (H["l_linkedin"], f'<link href="{G.LINKEDIN_URL}">{G.LINKEDIN_URL}</link>'),
        (H["l_github"], f'<link href="{G.GITHUB_URL}">{G.GITHUB_URL}</link>'),
        (H["l_gitlab"], f'<link href="{G.GITLAB_URL}">{G.GITLAB_URL}</link>'),
        (H["l_updated"], H["updated"]),
    ]
    data = [[Paragraph(f"{k}:", s["label"]), Paragraph(v, s["small"])] for k, v in rows]
    tbl = Table(data, colWidths=[1.45 * inch, content_w - 1.45 * inch])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    story.append(tbl)

    # ── Perfil profesional ───────────────────────────
    story.append(Paragraph(H["h_profile"], s["heading"]))
    story.append(hr())
    for item in T["summary"]:
        story.append(bullet(s["bullet"], clean(item, lang)))

    # ── Experiencia laboral ──────────────────────────
    story.append(Paragraph(H["h_experience"], s["heading"]))
    story.append(hr())
    story.append(Paragraph(H["exp_role"], s["subheading"]))
    story.append(Paragraph(f"{H['exp_company']} · {H['exp_period']}", s["meta"]))
    story.append(Paragraph(f"{H['l_functions']}:", s["label"]))
    for item in T["ats_experience"]:
        story.append(bullet(s["bullet"], clean(item, lang)))
    story.append(Spacer(1, 3))
    story.append(Paragraph(f"{H['l_achievements']}:", s["label"]))
    for item in (T["experience"][1], T["experience"][2]):
        story.append(bullet(s["bullet"], clean(item, lang)))
    story.append(bullet(
        s["link"],
        f'{T["exp_logros_label"]}: '
        f'<link href="{BASE_ASSETS_URL}/declaracion-logros-validacion{suffix}.pdf">'
        f'{BASE_ASSETS_URL}/declaracion-logros-validacion{suffix}.pdf</link>',
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph(clean(T["exp_tech"], lang), s["small"]))

    # ── Trayectoria previa ───────────────────────────
    story.append(Paragraph(H["h_previous"], s["heading"]))
    story.append(hr())
    story.append(Paragraph(H["previous_note"], s["body"]))
    story.append(Paragraph(G.PREVIOUS_CAREER[lang], s["small"]))

    # ── Formación académica ──────────────────────────
    edu = [Paragraph(H["h_education"], s["heading"]), hr()]
    for title, institution in T["degrees"]:
        edu.append(Paragraph(f"<b>{clean(title, lang)}</b>" if lang != "zh" else title,
                             s["subheading"]))
        edu.append(Paragraph(institution, s["small"]))
    story.append(KeepTogether(edu))

    # ── Competencias técnicas ────────────────────────
    story.append(Paragraph(H["h_skills"], s["heading"]))
    story.append(hr())
    for i in range(7):
        label = clean(T["skills_labels"][i], lang)
        story.append(Paragraph(f"{label} {G.SKILLS_VALUES[i]}", s["small"]))

    # ── Idiomas ──────────────────────────────────────
    langs_block = [Paragraph(H["h_languages"], s["heading"]), hr(),
                   bullet(s["bullet"], H["lang_native"]),
                   bullet(s["bullet"], T["language_skill"])]
    story.append(KeepTogether(langs_block))

    # ── Proyectos y portafolio ───────────────────────
    story.append(Paragraph(H["h_projects"], s["heading"]))
    story.append(hr())
    story.append(Paragraph(H["projects_note"], s["small"]))
    story.append(Spacer(1, 2))
    names = [p.split(" — ")[0].strip() for p in T["projects_rec"]]
    half = (len(names) + 1) // 2
    col_a, col_b = names[:half], names[half:]
    col_b += [""] * (len(col_a) - len(col_b))
    grid = [
        [Paragraph(f"• {a}" if a else "", s["project"]),
         Paragraph(f"• {b}" if b else "", s["project"])]
        for a, b in zip(col_a, col_b)
    ]
    ptbl = Table(grid, colWidths=[content_w / 2, content_w / 2])
    ptbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    story.append(ptbl)
    story.append(Spacer(1, 3))
    story.append(bullet(
        s["link"],
        f'{G.CONTACT_LINKS_LABELS[lang]}: <link href="{G.WEB_URL}">{G.WEB_URL}</link>',
    ))
    story.append(bullet(
        s["link"],
        f'GitHub: <link href="{G.GITHUB_URL}">{G.GITHUB_URL}</link> · '
        f'GitLab: <link href="{G.GITLAB_URL}">{G.GITLAB_URL}</link>',
    ))

    # ── Formación y actividad reciente ───────────────
    story.append(Paragraph(H["h_training"], s["heading"]))
    story.append(hr())
    for item in T["training"]:
        story.append(bullet(s["bullet"], clean(item, lang)))

    # ── Referencias y respaldos ──────────────────────
    refs = [Paragraph(H["h_refs"], s["heading"]), hr()]
    labels = G.DOC_LINK_LABELS[lang]
    refs.append(bullet(
        s["link"],
        f'{labels["recommendation"]}: '
        f'<link href="{BASE_ASSETS_URL}/carta-recomendacion_sin_firma{suffix}.pdf">'
        f'{BASE_ASSETS_URL}/carta-recomendacion_sin_firma{suffix}.pdf</link>',
    ))
    refs.append(bullet(
        s["link"],
        f'{labels["achievements"]}: '
        f'<link href="{BASE_ASSETS_URL}/declaracion-logros-validacion{suffix}.pdf">'
        f'{BASE_ASSETS_URL}/declaracion-logros-validacion{suffix}.pdf</link>',
    ))
    refs.append(bullet(s["bullet"], H["ref_manager"]))
    refs.append(bullet(s["bullet"], H["refs_available"]))
    story.append(KeepTogether(refs))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f'{H["footer_note"]} <link href="{G.WEB_URL}">{G.WEB_URL}</link>',
        s["note"],
    ))

    doc.build(story, onFirstPage=page_furniture, onLaterPages=page_furniture)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  -> {output_path} ({size_kb:.1f} KB)")


def main():
    print("Generating hoja de vida (generic CV) in 6 languages...")
    print("=" * 55)
    for lang in LANGS:
        path = os.path.normpath(
            os.path.join(ASSETS_DIR, f"hoja-de-vida{LANG_SUFFIX[lang]}.pdf"))
        build_hoja_de_vida(lang, path)
    print("=" * 55)
    print("Done. 6 hoja-de-vida PDFs generated.")


if __name__ == "__main__":
    main()
