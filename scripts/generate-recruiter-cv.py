#!/usr/bin/env python3
"""
Generate recruiter-oriented CVs (ES + EN) as PDF.
Two-column layout with dark blue header matching the original design.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# ── Colors ──────────────────────────────────────────
NAVY = HexColor("#1e3a5f")
DARK_NAVY = HexColor("#162d4a")
WHITE = white
BLACK = HexColor("#000000")
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#444444")
LIGHT_GRAY = HexColor("#f0f0f0")
ACCENT = HexColor("#2563eb")
SIDEBAR_BG = HexColor("#f5f7fa")
LINE_COLOR = HexColor("#cccccc")
SIDEBAR_HEADING = HexColor("#1e3a5f")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")

PAGE_W, PAGE_H = letter
SIDEBAR_W = 2.4 * inch
MAIN_W = PAGE_W - SIDEBAR_W
HEADER_H = 1.15 * inch
MARGIN = 0.35 * inch
SIDEBAR_PAD = 0.25 * inch


def make_styles():
    # ── Header styles (white on navy) ──
    name = ParagraphStyle(
        "Name", fontName="Helvetica-Bold", fontSize=22, leading=26,
        textColor=WHITE,
    )
    subtitle = ParagraphStyle(
        "Subtitle", fontName="Helvetica", fontSize=10, leading=13,
        textColor=HexColor("#c0d0e8"),
    )
    header_contact = ParagraphStyle(
        "HeaderContact", fontName="Helvetica", fontSize=8.5, leading=11,
        textColor=HexColor("#a0b8d0"),
    )

    # ── Sidebar styles ──
    side_heading = ParagraphStyle(
        "SideHeading", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
        textColor=SIDEBAR_HEADING, spaceBefore=8, spaceAfter=4,
    )
    side_body = ParagraphStyle(
        "SideBody", fontName="Helvetica", fontSize=8.5, leading=11.5,
        textColor=DARK, spaceAfter=1.5,
    )
    side_bold = ParagraphStyle(
        "SideBold", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5,
        textColor=DARK, spaceAfter=0.5,
    )
    side_muted = ParagraphStyle(
        "SideMuted", fontName="Helvetica", fontSize=8, leading=10.5,
        textColor=MUTED, spaceAfter=3,
    )
    side_link = ParagraphStyle(
        "SideLink", fontName="Helvetica", fontSize=8.5, leading=11.5,
        textColor=ACCENT, spaceAfter=1.5,
    )

    # ── Main column styles ──
    heading = ParagraphStyle(
        "Heading", fontName="Helvetica-Bold", fontSize=12, leading=15,
        textColor=NAVY, spaceBefore=8, spaceAfter=3,
    )
    subheading = ParagraphStyle(
        "SubHeading", fontName="Helvetica-Bold", fontSize=10, leading=13,
        textColor=DARK, spaceBefore=3, spaceAfter=1,
    )
    date_style = ParagraphStyle(
        "DateStyle", fontName="Helvetica", fontSize=9, leading=12,
        textColor=MUTED, spaceAfter=2,
    )
    body = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=9.2, leading=12.5,
        textColor=DARK, spaceAfter=2,
    )
    bullet = ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=9.2, leading=12.5,
        textColor=DARK, spaceAfter=2, leftIndent=10, bulletIndent=0,
    )
    tech = ParagraphStyle(
        "Tech", fontName="Helvetica", fontSize=8.5, leading=11,
        textColor=MUTED, spaceAfter=2,
    )
    note_heading = ParagraphStyle(
        "NoteHeading", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        textColor=NAVY, spaceBefore=6, spaceAfter=2,
    )
    note_body = ParagraphStyle(
        "NoteBody", fontName="Helvetica", fontSize=8.5, leading=11.5,
        textColor=DARK, spaceAfter=2, leftIndent=8, bulletIndent=0,
    )

    return dict(
        name=name, subtitle=subtitle, header_contact=header_contact,
        side_heading=side_heading, side_body=side_body, side_bold=side_bold,
        side_muted=side_muted, side_link=side_link,
        heading=heading, subheading=subheading, date=date_style,
        body=body, bullet=bullet, tech=tech,
        note_heading=note_heading, note_body=note_body,
    )


def bullet_p(style, text):
    return Paragraph(f"\u2022 {text}", style)


def side_hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR,
                       spaceBefore=4, spaceAfter=4)


def main_hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR,
                       spaceBefore=2, spaceAfter=4)


# ── Content ─────────────────────────────────────────

SIDEBAR_ES = dict(
    h_contact="CONTACTO",
    contact=[
        "Santiago, Chile",
        "+56 9 8121 8838",
        "vladimir.acuna.dev@gmail.com",
    ],
    contact_links=[
        ("Sitio web / portafolio", "https://vladimiracunadev-create.github.io/"),
        ("GitHub: vladimiracunadev-create", "https://github.com/vladimiracunadev-create"),
        ("GitLab: vladimir.acuna.dev-group", "https://gitlab.com/vladimir.acuna.dev-group"),
        ("LinkedIn: Vladimir Acu\u00f1a", "https://www.linkedin.com/in/vladimir-acuna-valdebenito"),
    ],
    h_skills="SKILLS",
    skills=[
        ("<b>Backend:</b> PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby",),
        ("<b>Frontend:</b> JavaScript, HTML, CSS",),
        ("<b>Datos:</b> SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB, modelado, ETL desde Excel",),
        ("<b>DevOps/Cloud:</b> Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform (b\u00e1sico)",),
        ("<b>Calidad/Seguridad:</b> hardening b\u00e1sico, secret scanning (Gitleaks, TruffleHog), control anti-inyecci\u00f3n, Trivy",),
        ("<b>Observabilidad:</b> Prometheus/Grafana (laboratorios y fundamentos)",),
        ("<b>IA/Agentes:</b> LangGraph, MCP, Ollama, n8n",),
    ],
    h_education="EDUCACI\u00d3N",
    degrees=[
        ("Ingenier\u00eda de Ejecuci\u00f3n en Computaci\u00f3n e Inform\u00e1tica", "Universidad de Tarapac\u00e1 (Arica)"),
        ("T\u00e9cnico de Administraci\u00f3n de Empresas (Menci\u00f3n Marketing)", "INACAP (Santiago)"),
    ],
    h_languages="IDIOMAS",
    languages="Ingl\u00e9s: intermedio en lectura; b\u00e1sico en escritura y conversaci\u00f3n.",
)

MAIN_ES = dict(
    h_summary="RESUMEN",
    summary=[
        "14 a\u00f1os de experiencia principal en Fundaci\u00f3n CEIS Maristas (2011-2025), desarrollando, manteniendo y modernizando una plataforma educativa/psicom\u00e9trica.",
        "Experiencia previa en desarrollo web y soporte de sistemas para instituciones p\u00fablicas y privadas, con foco en PHP, SQL Server/MySQL, reporter\u00eda PDF/Excel, migraci\u00f3n de datos e integraciones.",
        "Portafolio t\u00e9cnico actual con proyectos y laboratorios en Docker, AWS, CI/CD, observabilidad e IA aplicada a automatizaci\u00f3n, publicados en GitHub y GitLab.",
    ],
    h_experience="EXPERIENCIA DESTACADA",
    exp_title="Fundaci\u00f3n CEIS Maristas - Arquitecto de Software y Desarrollador Full-Stack Senior",
    exp_date="2011-2025",
    experience=[
        "Desarrollo, mantenci\u00f3n y evoluci\u00f3n de plataforma de evaluaci\u00f3n de alumnos, m\u00f3dulos institucionales y reporter\u00eda.",
        "Migraci\u00f3n tecnol\u00f3gica de PHP 5.4 a PHP 8.2+, actualizaci\u00f3n de servidores/librer\u00edas y mejoras de rendimiento.",
        "Reportes PDF/Excel con indicadores, percentiles y an\u00e1lisis por curso, nivel y establecimiento.",
        "Importaci\u00f3n y migraci\u00f3n de datos desde Excel con validaciones; automatizaci\u00f3n de comunicaciones y seguimientos.",
        "Soporte directo a usuarios clave (coordinadores, orientadores, directivos) y operaci\u00f3n en producci\u00f3n.",
    ],
    exp_tech="Tecnolog\u00edas: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
    h_previous="TRAYECTORIA PREVIA (S\u00cdNTESIS)",
    previous="CONACE / Gobierno de Chile (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 Centro Europeo para la Capacitaci\u00f3n (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 Amigos Defensores de los Animales (2001-2002)",
    h_projects="PROYECTOS DESTACADOS",
    projects=[
        "Cloud/AWS y FinOps \u2014 GitHub + GitLab (15 casos AWS, CI/CD 5 stages)",
        "Microsistemas \u2014 suite de 11 micro-apps, Hub CLI, MCP server",
        "Social Bot Scheduler \u2014 matriz 9 ejes, 9 motores DB, n8n, Prometheus/Grafana",
        "Docker Labs \u2014 12 labs, Control Center, instalador Windows",
        "LangGraph \u2014 25 casos reales, 4 operacionales/industriales, agentes con estado",
        "MCP + Ollama local \u2014 chat IA local, herramientas MCP, 100% privado",
    ],
    h_training="FORMACI\u00d3N Y ACTIVIDAD RECIENTE",
    training=[
        "Formaci\u00f3n continua en automatizaci\u00f3n pr\u00e1ctica, ML/NLP y herramientas de desarrollo.",
        "Consolidaci\u00f3n de portafolio t\u00e9cnico con laboratorios cloud, microsistemas y documentaci\u00f3n orientada a reclutadores.",
    ],
    h_notes="NOTAS",
    notes=[
        "Carta de recomendaci\u00f3n disponible.",
        'Si el proceso usa ATS, favor considerar el CV ATS de la p\u00e1gina web: <link href="https://vladimiracunadev-create.github.io/">vladimiracunadev-create.github.io</link>',
    ],
)

SIDEBAR_EN = dict(
    h_contact="CONTACT",
    contact=[
        "Santiago, Chile",
        "+56 9 8121 8838",
        "vladimir.acuna.dev@gmail.com",
    ],
    contact_links=[
        ("Website / portfolio", "https://vladimiracunadev-create.github.io/"),
        ("GitHub: vladimiracunadev-create", "https://github.com/vladimiracunadev-create"),
        ("GitLab: vladimir.acuna.dev-group", "https://gitlab.com/vladimir.acuna.dev-group"),
        ("LinkedIn: Vladimir Acu\u00f1a", "https://www.linkedin.com/in/vladimir-acuna-valdebenito"),
    ],
    h_skills="SKILLS",
    skills=[
        ("<b>Backend:</b> PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby",),
        ("<b>Frontend:</b> JavaScript, HTML, CSS",),
        ("<b>Data:</b> SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB, modeling, ETL from Excel",),
        ("<b>DevOps/Cloud:</b> Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform (basic)",),
        ("<b>Quality/Security:</b> basic hardening, secret scanning (Gitleaks, TruffleHog), anti-injection controls, Trivy",),
        ("<b>Observability:</b> Prometheus/Grafana (labs and fundamentals)",),
        ("<b>AI/Agents:</b> LangGraph, MCP, Ollama, n8n",),
    ],
    h_education="EDUCATION",
    degrees=[
        ("Computer Science and Informatics Engineering", "University of Tarapac\u00e1 (Arica)"),
        ("Business Administration Technician (Marketing specialization)", "INACAP (Santiago)"),
    ],
    h_languages="LANGUAGES",
    languages="English: intermediate reading; basic writing and conversation.",
)

MAIN_EN = dict(
    h_summary="SUMMARY",
    summary=[
        "14 years of core experience at Fundaci\u00f3n CEIS Maristas (2011-2025), developing, maintaining, and modernizing an educational/psychometric platform.",
        "Previous experience in web development and systems support for public and private institutions, focused on PHP, SQL Server/MySQL, PDF/Excel reporting, data migration, and integrations.",
        "Current technical portfolio with projects and labs in Docker, AWS, CI/CD, observability, and AI applied to automation, published on GitHub and GitLab.",
    ],
    h_experience="HIGHLIGHTED EXPERIENCE",
    exp_title="Fundaci\u00f3n CEIS Maristas - Software Architect and Senior Full-Stack Developer",
    exp_date="2011-2025",
    experience=[
        "Development, maintenance, and evolution of a student assessment platform, institutional modules, and reporting.",
        "Technology migration from PHP 5.4 to PHP 8.2+, plus server/library upgrades and performance improvements.",
        "PDF/Excel reports with indicators, percentiles, and analysis by class, grade level, and institution.",
        "Excel-based data import and migration with validations; automation of communications and follow-up processes.",
        "Direct support for key users (coordinators, counselors, school leaders) and production operations.",
    ],
    exp_tech="Technologies: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
    h_previous="PREVIOUS CAREER (SUMMARY)",
    previous="CONACE / Government of Chile (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 European Training Center (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 Friends Defenders of Animals (2001-2002)",
    h_projects="SELECTED PROJECTS",
    projects=[
        "Cloud/AWS and FinOps \u2014 GitHub + GitLab (15 AWS cases, 5-stage CI/CD)",
        "Microsystems \u2014 suite of 11 micro-apps, Hub CLI, MCP server",
        "Social Bot Scheduler \u2014 9-axis integration matrix, 9 DB engines, n8n, Prometheus/Grafana",
        "Docker Labs \u2014 12 labs, Control Center, Windows installer",
        "LangGraph \u2014 25 real-world cases, 4 operational/industrial, stateful agents",
        "MCP + local Ollama \u2014 local AI chat, MCP tools, 100% private",
    ],
    h_training="RECENT TRAINING AND PROJECTS",
    training=[
        "Continuous training in practical automation, ML/NLP, and development tools.",
        "Consolidation of a technical portfolio with cloud labs, microsystems, and recruiter-oriented documentation.",
    ],
    h_notes="NOTES",
    notes=[
        "Recommendation letter available.",
        'If the hiring process uses ATS, please consider the ATS CV available on the website: <link href="https://vladimiracunadev-create.github.io/">vladimiracunadev-create.github.io</link>',
    ],
)


# ── Header subtitle per language ────────────────────
HEADER_ES = dict(
    name="Vladimir Acu\u00f1a",
    subtitle="Arquitecto de Software | Full-Stack Senior (PHP/JS/SQL) | Modernizaci\u00f3n y DevOps",
    contact="Santiago, Chile  |  +56 9 8121 8838  |  vladimir.acuna.dev@gmail.com",
)
HEADER_EN = dict(
    name="Vladimir Acu\u00f1a",
    subtitle="Software Architect | Senior Full-Stack (PHP/JS/SQL) | Modernization & DevOps",
    contact="Santiago, Chile  |  +56 9 8121 8838  |  vladimir.acuna.dev@gmail.com",
)


class RecruiterCV(BaseDocTemplate):
    """Two-column CV with navy header."""

    def __init__(self, filename, header_data, **kw):
        self.header_data = header_data
        BaseDocTemplate.__init__(self, filename, pagesize=letter,
                                  leftMargin=0, rightMargin=0,
                                  topMargin=0, bottomMargin=0, **kw)

        # Frames below the header
        sidebar_frame = Frame(
            SIDEBAR_PAD,                       # x
            MARGIN,                            # y
            SIDEBAR_W - SIDEBAR_PAD * 2,       # width
            PAGE_H - HEADER_H - MARGIN - 0.1*inch,  # height
            id="sidebar",
            showBoundary=0,
        )
        main_frame = Frame(
            SIDEBAR_W + 0.15*inch,             # x
            MARGIN,                            # y
            MAIN_W - 0.5*inch,                 # width
            PAGE_H - HEADER_H - MARGIN - 0.1*inch,  # height
            id="main",
            showBoundary=0,
        )

        template = PageTemplate(
            id="recruiter",
            frames=[main_frame, sidebar_frame],
            onPage=self._draw_page,
        )
        self.addPageTemplates([template])

    def _draw_page(self, canvas, doc):
        """Draw the navy header and sidebar background."""
        canvas.saveState()

        # ── Navy header bar ──
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)

        # ── Header text ──
        s = make_styles()
        # Name
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 22)
        canvas.drawString(0.45*inch, PAGE_H - 0.45*inch, self.header_data["name"])
        # Subtitle
        canvas.setFillColor(HexColor("#c0d0e8"))
        canvas.setFont("Helvetica", 10)
        canvas.drawString(0.45*inch, PAGE_H - 0.65*inch, self.header_data["subtitle"])
        # Contact
        canvas.setFillColor(HexColor("#a0b8d0"))
        canvas.setFont("Helvetica", 8.5)
        canvas.drawString(0.45*inch, PAGE_H - 0.85*inch, self.header_data["contact"])

        # ── Sidebar background (light gray) ──
        canvas.setFillColor(SIDEBAR_BG)
        canvas.rect(0, 0, SIDEBAR_W, PAGE_H - HEADER_H, fill=1, stroke=0)

        # ── Thin accent line under header ──
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(2)
        canvas.line(0, PAGE_H - HEADER_H, PAGE_W, PAGE_H - HEADER_H)

        canvas.restoreState()


def build_sidebar(sidebar_data):
    """Build sidebar flowable list."""
    s = make_styles()
    items = []

    # Contact
    items.append(Paragraph(sidebar_data["h_contact"], s["side_heading"]))
    for line in sidebar_data["contact"]:
        items.append(Paragraph(line, s["side_body"]))
    for label, url in sidebar_data["contact_links"]:
        items.append(Paragraph(f'<link href="{url}">{label}</link>', s["side_link"]))

    items.append(side_hr())

    # Skills
    items.append(Paragraph(sidebar_data["h_skills"], s["side_heading"]))
    for (skill_line,) in sidebar_data["skills"]:
        items.append(Paragraph(skill_line, s["side_body"]))
        items.append(Spacer(1, 1))

    items.append(side_hr())

    # Education
    items.append(Paragraph(sidebar_data["h_education"], s["side_heading"]))
    for title, inst in sidebar_data["degrees"]:
        items.append(Paragraph(f"<b>{title}</b>", s["side_bold"]))
        items.append(Paragraph(inst, s["side_muted"]))

    items.append(side_hr())

    # Languages
    items.append(Paragraph(sidebar_data["h_languages"], s["side_heading"]))
    items.append(Paragraph(sidebar_data["languages"], s["side_body"]))

    return items


def build_main(main_data):
    """Build main column flowable list."""
    s = make_styles()
    items = []

    # Summary
    items.append(Paragraph(main_data["h_summary"], s["heading"]))
    for item in main_data["summary"]:
        items.append(bullet_p(s["bullet"], item))

    items.append(main_hr())

    # Experience
    items.append(Paragraph(main_data["h_experience"], s["heading"]))
    items.append(Paragraph(main_data["exp_title"], s["subheading"]))
    items.append(Paragraph(main_data["exp_date"], s["date"]))
    for item in main_data["experience"]:
        items.append(bullet_p(s["bullet"], item))
    items.append(Paragraph(main_data["exp_tech"], s["tech"]))

    items.append(main_hr())

    # Previous career
    items.append(Paragraph(main_data["h_previous"], s["heading"]))
    items.append(Paragraph(main_data["previous"], s["body"]))

    items.append(main_hr())

    # Projects (NEW section)
    items.append(Paragraph(main_data["h_projects"], s["heading"]))
    for proj in main_data["projects"]:
        items.append(bullet_p(s["bullet"], proj))

    items.append(main_hr())

    # Training
    items.append(Paragraph(main_data["h_training"], s["heading"]))
    for item in main_data["training"]:
        items.append(bullet_p(s["bullet"], item))

    items.append(main_hr())

    # Notes
    items.append(Paragraph(main_data["h_notes"], s["note_heading"]))
    for note in main_data["notes"]:
        items.append(bullet_p(s["note_body"], note))

    return items


def build_cv(header, sidebar_data, main_data, output_path):
    """Build the two-column recruiter CV."""
    doc = RecruiterCV(output_path, header)

    # Main column content goes first (first frame), sidebar second (second frame)
    main_items = build_main(main_data)
    sidebar_items = build_sidebar(sidebar_data)

    # FrameBreak to switch from main to sidebar
    from reportlab.platypus import FrameBreak
    story = main_items + [FrameBreak()] + sidebar_items

    doc.build(story)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  -> {output_path} ({size_kb:.1f} KB)")


def main():
    es_path = os.path.join(ASSETS_DIR, "cv-reclutador.pdf")
    en_path = os.path.join(ASSETS_DIR, "cv-reclutador-english.pdf")

    print("Generating recruiter CVs...")
    build_cv(HEADER_ES, SIDEBAR_ES, MAIN_ES, es_path)
    build_cv(HEADER_EN, SIDEBAR_EN, MAIN_EN, en_path)
    print("Done.")


if __name__ == "__main__":
    main()
