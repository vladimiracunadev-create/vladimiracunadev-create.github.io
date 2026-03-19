#!/usr/bin/env python3
"""
Generate unified recruiter CVs (ES + EN).
Page 1: Recruiter format (two-column, blue header) — for human reviewers.
Transition page: Brief explanation of why an ATS version follows.
Page 2+: ATS-optimized format (single column, plain) — for automated systems.
Output: cv-reclutador.pdf / cv-reclutador-english.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, Frame, PageTemplate,
    BaseDocTemplate, FrameBreak, NextPageTemplate, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Colors ──────────────────────────────────────────
NAVY = HexColor("#1e3a5f")
WHITE = white
BLACK = HexColor("#000000")
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#444444")
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


# ═══════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════

def recruiter_styles():
    """Styles for the recruiter (page 1) layout."""
    return dict(
        side_heading=ParagraphStyle(
            "SideHeading", fontName="Helvetica-Bold", fontSize=10.5, leading=14,
            textColor=SIDEBAR_HEADING, spaceBefore=8, spaceAfter=4,
        ),
        side_body=ParagraphStyle(
            "SideBody", fontName="Helvetica", fontSize=8.5, leading=11.5,
            textColor=DARK, spaceAfter=1.5,
        ),
        side_bold=ParagraphStyle(
            "SideBold", fontName="Helvetica-Bold", fontSize=8.5, leading=11.5,
            textColor=DARK, spaceAfter=0.5,
        ),
        side_muted=ParagraphStyle(
            "SideMuted", fontName="Helvetica", fontSize=8, leading=10.5,
            textColor=MUTED, spaceAfter=3,
        ),
        side_link=ParagraphStyle(
            "SideLink", fontName="Helvetica", fontSize=8.5, leading=11.5,
            textColor=ACCENT, spaceAfter=1.5,
        ),
        heading=ParagraphStyle(
            "RHeading", fontName="Helvetica-Bold", fontSize=12, leading=15,
            textColor=NAVY, spaceBefore=8, spaceAfter=3,
        ),
        subheading=ParagraphStyle(
            "RSubHeading", fontName="Helvetica-Bold", fontSize=10, leading=13,
            textColor=DARK, spaceBefore=3, spaceAfter=1,
        ),
        date=ParagraphStyle(
            "RDate", fontName="Helvetica", fontSize=9, leading=12,
            textColor=MUTED, spaceAfter=2,
        ),
        body=ParagraphStyle(
            "RBody", fontName="Helvetica", fontSize=9.2, leading=12.5,
            textColor=DARK, spaceAfter=2,
        ),
        bullet=ParagraphStyle(
            "RBullet", fontName="Helvetica", fontSize=9.2, leading=12.5,
            textColor=DARK, spaceAfter=2, leftIndent=10, bulletIndent=0,
        ),
        tech=ParagraphStyle(
            "RTech", fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=MUTED, spaceAfter=2,
        ),
        link=ParagraphStyle(
            "RLink", fontName="Helvetica", fontSize=9, leading=12,
            textColor=ACCENT, spaceAfter=2, leftIndent=10, bulletIndent=0,
        ),
        note_heading=ParagraphStyle(
            "RNoteH", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
            textColor=NAVY, spaceBefore=6, spaceAfter=2,
        ),
        note_body=ParagraphStyle(
            "RNoteB", fontName="Helvetica", fontSize=8.5, leading=11.5,
            textColor=DARK, spaceAfter=2, leftIndent=8, bulletIndent=0,
        ),
    )


def ats_styles():
    """Styles for the ATS (page 2+) layout."""
    return dict(
        name=ParagraphStyle(
            "AName", fontName="Helvetica-Bold", fontSize=22, leading=26,
            textColor=BLACK, spaceAfter=2,
        ),
        subtitle=ParagraphStyle(
            "ASubtitle", fontName="Helvetica", fontSize=10, leading=13,
            textColor=DARK, spaceAfter=1,
        ),
        contact=ParagraphStyle(
            "AContact", fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=MUTED, spaceAfter=8,
        ),
        heading=ParagraphStyle(
            "AHeading", fontName="Helvetica-Bold", fontSize=12, leading=15,
            textColor=BLACK, spaceBefore=10, spaceAfter=4,
        ),
        subheading=ParagraphStyle(
            "ASubHeading", fontName="Helvetica-Bold", fontSize=10, leading=13,
            textColor=DARK, spaceBefore=4, spaceAfter=2,
        ),
        body=ParagraphStyle(
            "ABody", fontName="Helvetica", fontSize=9.5, leading=12.5,
            textColor=DARK, spaceAfter=2,
        ),
        bullet=ParagraphStyle(
            "ABullet", fontName="Helvetica", fontSize=9.5, leading=12.5,
            textColor=DARK, spaceAfter=2, leftIndent=12, bulletIndent=0,
        ),
        tech=ParagraphStyle(
            "ATech", fontName="Helvetica", fontSize=9, leading=12,
            textColor=MUTED, spaceAfter=1,
        ),
        link=ParagraphStyle(
            "ALink", fontName="Helvetica", fontSize=9, leading=12,
            textColor=ACCENT, spaceAfter=2, leftIndent=12, bulletIndent=0,
        ),
    )


def transition_styles():
    """Styles for the transition note between recruiter and ATS sections."""
    return dict(
        title=ParagraphStyle(
            "TTitle", fontName="Helvetica-Bold", fontSize=14, leading=18,
            textColor=NAVY, spaceAfter=12, alignment=TA_CENTER,
        ),
        body=ParagraphStyle(
            "TBody", fontName="Helvetica", fontSize=10, leading=14,
            textColor=DARK, spaceAfter=8, alignment=TA_CENTER,
        ),
        note=ParagraphStyle(
            "TNote", fontName="Helvetica", fontSize=9, leading=13,
            textColor=MUTED, spaceAfter=4, alignment=TA_CENTER,
        ),
    )


# ═══════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════

def bp(style, text):
    return Paragraph(f"\u2022 {text}", style)


def hr(color=LINE_COLOR):
    return HRFlowable(width="100%", thickness=0.5, color=color,
                       spaceBefore=2, spaceAfter=4)


def side_hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR,
                       spaceBefore=4, spaceAfter=4)


# ═══════════════════════════════════════════════════
# CONTENT DATA
# ═══════════════════════════════════════════════════

# ── Recruiter sidebar ───────────────────────────────

SIDEBAR_ES = dict(
    h_contact="CONTACTO",
    contact=["Santiago, Chile", "+56 9 8121 8838", "vladimir.acuna.dev@gmail.com"],
    contact_links=[
        ("Sitio web / portafolio", "https://vladimiracunadev-create.github.io/"),
        ("GitHub: vladimiracunadev-create", "https://github.com/vladimiracunadev-create"),
        ("GitLab: vladimir.acuna.dev-group", "https://gitlab.com/vladimir.acuna.dev-group"),
        ("LinkedIn: Vladimir Acu\u00f1a", "https://www.linkedin.com/in/vladimir-acuna-valdebenito"),
    ],
    h_skills="SKILLS",
    skills=[
        "<b>Backend:</b> PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby",
        "<b>Frontend:</b> JavaScript, HTML, CSS",
        "<b>Datos:</b> SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB, modelado, ETL desde Excel",
        "<b>DevOps/Cloud:</b> Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform (b\u00e1sico)",
        "<b>Calidad/Seguridad:</b> hardening b\u00e1sico, secret scanning (Gitleaks, TruffleHog), control anti-inyecci\u00f3n, Trivy",
        "<b>Observabilidad:</b> Prometheus/Grafana (laboratorios y fundamentos)",
        "<b>IA/Agentes:</b> LangGraph, MCP, Ollama, n8n",
    ],
    h_education="EDUCACI\u00d3N",
    degrees=[
        ("Ingenier\u00eda de Ejecuci\u00f3n en Computaci\u00f3n e Inform\u00e1tica", "Universidad de Tarapac\u00e1 (Arica)"),
        ("T\u00e9cnico de Administraci\u00f3n de Empresas (Menci\u00f3n Marketing)", "INACAP (Santiago)"),
    ],
    h_languages="IDIOMAS",
    languages="Ingl\u00e9s: intermedio en lectura; b\u00e1sico en escritura y conversaci\u00f3n.",
)

SIDEBAR_EN = dict(
    h_contact="CONTACT",
    contact=["Santiago, Chile", "+56 9 8121 8838", "vladimir.acuna.dev@gmail.com"],
    contact_links=[
        ("Website / portfolio", "https://vladimiracunadev-create.github.io/"),
        ("GitHub: vladimiracunadev-create", "https://github.com/vladimiracunadev-create"),
        ("GitLab: vladimir.acuna.dev-group", "https://gitlab.com/vladimir.acuna.dev-group"),
        ("LinkedIn: Vladimir Acu\u00f1a", "https://www.linkedin.com/in/vladimir-acuna-valdebenito"),
    ],
    h_skills="SKILLS",
    skills=[
        "<b>Backend:</b> PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby",
        "<b>Frontend:</b> JavaScript, HTML, CSS",
        "<b>Data:</b> SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB, modeling, ETL from Excel",
        "<b>DevOps/Cloud:</b> Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform (basic)",
        "<b>Quality/Security:</b> basic hardening, secret scanning (Gitleaks, TruffleHog), anti-injection controls, Trivy",
        "<b>Observability:</b> Prometheus/Grafana (labs and fundamentals)",
        "<b>AI/Agents:</b> LangGraph, MCP, Ollama, n8n",
    ],
    h_education="EDUCATION",
    degrees=[
        ("Computer Science and Informatics Engineering", "University of Tarapac\u00e1 (Arica)"),
        ("Business Administration Technician (Marketing specialization)", "INACAP (Santiago)"),
    ],
    h_languages="LANGUAGES",
    languages="English: intermediate reading; basic writing and conversation.",
)

# ── Recruiter main column ───────────────────────────

RMAIN_ES = dict(
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
    doc_links=[
        ("Ver declaración de logros profesionales", "https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion.pdf"),
        ("Ver carta de recomendación", "https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma.pdf"),
    ],
    h_training="FORMACI\u00d3N Y ACTIVIDAD RECIENTE",
    training=[
        "Formaci\u00f3n continua en automatizaci\u00f3n pr\u00e1ctica, ML/NLP y herramientas de desarrollo.",
        "Consolidaci\u00f3n de portafolio t\u00e9cnico con laboratorios cloud, microsistemas y documentaci\u00f3n orientada a reclutadores.",
    ],
)

RMAIN_EN = dict(
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
    doc_links=[
        ("View professional achievements statement", "https://vladimiracunadev-create.github.io/assets/declaracion-logros-validacion-english.pdf"),
        ("View recommendation letter", "https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma-english.pdf"),
    ],
    h_training="RECENT TRAINING AND PROJECTS",
    training=[
        "Continuous training in practical automation, ML/NLP, and development tools.",
        "Consolidation of a technical portfolio with cloud labs, microsystems, and recruiter-oriented documentation.",
    ],
)

# ── ATS content ─────────────────────────────────────

ATS_ES = dict(
    subtitle="Arquitecto de Software | Full-Stack Senior (PHP/JS/SQL) | Modernizaci\u00f3n & DevOps",
    contact_line1="Santiago, Chile | +56 9 8121 8838 | vladimir.acuna.dev@gmail.com",
    contact_line2=(
        'Web: <link href="https://vladimiracunadev-create.github.io/">vladimiracunadev-create.github.io</link> | '
        'GitHub: <link href="https://github.com/vladimiracunadev-create">github.com/vladimiracunadev-create</link> | '
        'GitLab: <link href="https://gitlab.com/vladimir.acuna.dev-group">gitlab.com/vladimir.acuna.dev-group</link>'
    ),
    contact_line3='LinkedIn: <link href="https://www.linkedin.com/in/vladimir-acuna-valdebenito">linkedin.com/in/vladimir-acuna-valdebenito</link>',
    h_summary="RESUMEN",
    summary=[
        "14 a\u00f1os liderando el dise\u00f1o, evoluci\u00f3n y operaci\u00f3n de una plataforma educativa/psicom\u00e9trica (2011-2025), con foco en continuidad operacional.",
        "Modernizaci\u00f3n progresiva (PHP 5.4 \u2192 PHP 8.2+), optimizaci\u00f3n de rendimiento y automatizaci\u00f3n de reportes (PDF/Excel) y procesos de datos.",
        "Experiencia en bases de datos (SQL Server, MySQL/MariaDB) y despliegues/entornos reproducibles con Docker y CI/CD.",
        "Portafolio t\u00e9cnico con casos pr\u00e1cticos (Cloud/AWS, microsistemas, agentes IA y observabilidad), documentaci\u00f3n y demos verificables en GitHub y GitLab.",
    ],
    h_skills="SKILLS",
    skills=[
        ("<b>Backend:</b>", "PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"),
        ("<b>Frontend:</b>", "JavaScript, HTML, CSS"),
        ("<b>Datos:</b>", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB, modelado, ETL desde Excel"),
        ("<b>DevOps/Cloud:</b>", "Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform (b\u00e1sico)"),
        ("<b>Calidad/Seguridad:</b>", "hardening b\u00e1sico, secret scanning (Gitleaks, TruffleHog), control anti-inyecci\u00f3n, Trivy, pip-audit"),
        ("<b>Observabilidad:</b>", "Prometheus/Grafana (laboratorios y fundamentos)"),
        ("<b>IA/Agentes:</b>", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"),
    ],
    h_experience="EXPERIENCIA",
    exp_title="Fundaci\u00f3n CEIS Maristas \u2014 Arquitecto de Software y Desarrollador Full-Stack (2011-2025)",
    experience=[
        "Dise\u00f1o, desarrollo y mantenci\u00f3n de plataforma de evaluaci\u00f3n de alumnos (bater\u00edas de test), m\u00f3dulos institucionales y reportes.",
        "Migraci\u00f3n tecnol\u00f3gica (PHP 5.4 \u2192 PHP 8.2+), actualizaci\u00f3n de servidores/librer\u00edas y mejoras de rendimiento con JavaScript y pruebas de carga.",
        "Desarrollo de reportes avanzados PDF/Excel con indicadores, percentiles y an\u00e1lisis por curso/nivel/establecimiento.",
        "Importaci\u00f3n y migraci\u00f3n de datos masivos desde Excel con validaciones; automatizaci\u00f3n de comunicaciones (env\u00edos, segmentaci\u00f3n, seguimiento).",
        "Soporte directo a usuarios clave (coordinadores, orientadores, directivos) y operaci\u00f3n en producci\u00f3n.",
    ],
    exp_tech="Tecnolog\u00edas: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
    h_projects="PROYECTOS DESTACADOS",
    projects=[
        ("Cloud/AWS y FinOps \u2014 GitHub (demos y documentaci\u00f3n):", "https://github.com/vladimiracunadev-create/proyectos-aws"),
        ("Cloud/AWS \u2014 GitLab (15 casos, CI/CD 5 stages, ~80% SAA-C03):", "https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab"),
        ("Microsistemas (suite de 11 micro-apps, Hub CLI, MCP server):", "https://github.com/vladimiracunadev-create/microsistemas"),
        ("Social Bot Scheduler (matriz 9 ejes de integraci\u00f3n, 9 motores DB, n8n, Prometheus/Grafana):", "https://github.com/vladimiracunadev-create/social-bot-scheduler"),
        ("Docker Labs (12 labs, Control Center, instalador Windows):", "https://github.com/vladimiracunadev-create/docker-labs"),
        ("LangGraph casos reales (25 casos, 4 operacionales/industriales, agentes con estado):", "https://github.com/vladimiracunadev-create/langgraph-realworld"),
        ("MCP + Ollama local (chat IA local, herramientas MCP, 100% privado):", "https://github.com/vladimiracunadev-create/mcp-ollama-local"),
    ],
    h_education="FORMACI\u00d3N Y ACTIVIDAD RECIENTE",
    education_activity=[
        "Formaci\u00f3n continua (cursos online): bases de ML/NLP y automatizaci\u00f3n pr\u00e1ctica aplicada a proyectos.",
        "Consolidaci\u00f3n de portafolio t\u00e9cnico (Cloud/AWS, Docker labs, agentes) y documentaci\u00f3n orientada a reclutadores.",
    ],
    h_degrees="EDUCACI\u00d3N",
    degrees=[
        ("Ingenier\u00eda de Ejecuci\u00f3n en Computaci\u00f3n e Inform\u00e1tica", "Universidad de Tarapac\u00e1 (Arica)"),
        ("T\u00e9cnico de Administraci\u00f3n de Empresas (Menci\u00f3n Marketing)", "INACAP (Santiago)"),
    ],
    h_languages="IDIOMAS",
    languages="Ingl\u00e9s: intermedio en lectura; b\u00e1sico en escritura y conversaci\u00f3n.",
)

ATS_EN = dict(
    subtitle="Software Architect | Senior Full-Stack (PHP/JS/SQL) | Modernization & DevOps",
    contact_line1="Santiago, Chile | +56 9 8121 8838 | vladimir.acuna.dev@gmail.com",
    contact_line2=(
        'Web: <link href="https://vladimiracunadev-create.github.io/">vladimiracunadev-create.github.io</link> | '
        'GitHub: <link href="https://github.com/vladimiracunadev-create">github.com/vladimiracunadev-create</link> | '
        'GitLab: <link href="https://gitlab.com/vladimir.acuna.dev-group">gitlab.com/vladimir.acuna.dev-group</link>'
    ),
    contact_line3='LinkedIn: <link href="https://www.linkedin.com/in/vladimir-acuna-valdebenito">linkedin.com/in/vladimir-acuna-valdebenito</link>',
    h_summary="SUMMARY",
    summary=[
        "14 years leading the design, evolution, and operation of an educational/psychometric platform (2011-2025), with a strong focus on operational continuity.",
        "Progressive modernization (PHP 5.4 \u2192 PHP 8.2+), performance optimization, and automation of PDF/Excel reports and data processes.",
        "Experience with databases (SQL Server, MySQL/MariaDB) and reproducible deployments/environments using Docker and CI/CD.",
        "Technical portfolio with practical cases (Cloud/AWS, microsystems, AI agents, and observability), documentation, and verifiable demos on GitHub and GitLab.",
    ],
    h_skills="SKILLS",
    skills=[
        ("<b>Backend:</b>", "PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"),
        ("<b>Frontend:</b>", "JavaScript, HTML, CSS"),
        ("<b>Data:</b>", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB, data modeling, ETL from Excel"),
        ("<b>DevOps/Cloud:</b>", "Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform (basic)"),
        ("<b>Quality/Security:</b>", "basic hardening, secret scanning (Gitleaks, TruffleHog), anti-injection controls, Trivy, pip-audit"),
        ("<b>Observability:</b>", "Prometheus/Grafana (labs and fundamentals)"),
        ("<b>AI/Agents:</b>", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"),
    ],
    h_experience="EXPERIENCE",
    exp_title="Fundaci\u00f3n CEIS Maristas \u2014 Software Architect and Full-Stack Developer (2011-2025)",
    experience=[
        "Design, development, and maintenance of a student assessment platform (test batteries), institutional modules, and reports.",
        "Technology migration (PHP 5.4 \u2192 PHP 8.2+), server/library upgrades, and performance improvements with JavaScript and load testing.",
        "Development of advanced PDF/Excel reports with indicators, percentiles, and analysis by class, level, and school.",
        "Import and migration of high-volume data from Excel with validations; automation of communications (sending, segmentation, follow-up).",
        "Direct support for key users (coordinators, counselors, school leaders) and production operations.",
    ],
    exp_tech="Technologies: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
    h_projects="SELECTED PROJECTS",
    projects=[
        ("Cloud/AWS and FinOps \u2014 GitHub (demos and documentation):", "https://github.com/vladimiracunadev-create/proyectos-aws"),
        ("Cloud/AWS \u2014 GitLab (15 cases, 5-stage CI/CD, ~80% SAA-C03):", "https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab"),
        ("Microsystems (suite of 11 micro-apps, Hub CLI, MCP server):", "https://github.com/vladimiracunadev-create/microsistemas"),
        ("Social Bot Scheduler (9-axis integration matrix, 9 DB engines, n8n, Prometheus/Grafana):", "https://github.com/vladimiracunadev-create/social-bot-scheduler"),
        ("Docker Labs (12 labs, Control Center, Windows installer):", "https://github.com/vladimiracunadev-create/docker-labs"),
        ("LangGraph real-world cases (25 cases, 4 operational/industrial, stateful agents):", "https://github.com/vladimiracunadev-create/langgraph-realworld"),
        ("MCP + local Ollama (local AI chat, MCP tools, 100% private):", "https://github.com/vladimiracunadev-create/mcp-ollama-local"),
    ],
    h_education="EDUCATION & RECENT ACTIVITY",
    education_activity=[
        "Continuous learning (online courses): ML/NLP fundamentals and practical automation applied to projects.",
        "Consolidation of a technical portfolio (Cloud/AWS, Docker labs, agents) and recruiter-oriented documentation.",
    ],
    h_degrees="EDUCATION",
    degrees=[
        ("Computer and Informatics Engineering", "Universidad de Tarapac\u00e1 (Arica)"),
        ("Business Administration Technician (Marketing concentration)", "INACAP (Santiago)"),
    ],
    h_languages="LANGUAGES",
    languages="English: intermediate reading; basic writing and conversation.",
)

# ── Transition text ─────────────────────────────────

TRANSITION_ES = dict(
    title="Versi\u00f3n optimizada para ATS",
    body=(
        "A continuaci\u00f3n se incluye una versi\u00f3n del curr\u00edculum optimizada para "
        "sistemas de seguimiento de candidatos (ATS)."
    ),
    reasons=[
        "Los procesos de selecci\u00f3n actuales frecuentemente utilizan inteligencia artificial y filtros autom\u00e1ticos para evaluar curr\u00edculums antes de que lleguen a un reclutador humano.",
        "El formato de columna \u00fanica y texto plano de la siguiente p\u00e1gina est\u00e1 dise\u00f1ado para ser le\u00eddo correctamente por estos sistemas, maximizando la compatibilidad con parsers ATS.",
        "El contenido es el mismo \u2014 solo cambia la presentaci\u00f3n para garantizar que ninguna informaci\u00f3n se pierda en el procesamiento autom\u00e1tico.",
    ],
    footer="La p\u00e1gina anterior es para lectura humana. Las siguientes son para procesamiento autom\u00e1tico.",
)

TRANSITION_EN = dict(
    title="ATS-Optimized Version",
    body=(
        "The following pages contain an ATS-optimized version of this resume."
    ),
    reasons=[
        "Modern hiring processes frequently use artificial intelligence and automated filters to evaluate resumes before they reach a human recruiter.",
        "The single-column, plain-text format on the following pages is designed to be correctly parsed by these systems, maximizing ATS compatibility.",
        "The content is the same \u2014 only the presentation changes to ensure no information is lost during automated processing.",
    ],
    footer="The previous page is for human review. The following pages are for automated processing.",
)

# ── Header data ─────────────────────────────────────

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


# ═══════════════════════════════════════════════════
# DOCUMENT CLASS
# ═══════════════════════════════════════════════════

class UnifiedCV(BaseDocTemplate):
    """Multi-template document: recruiter page, transition, then ATS pages."""

    def __init__(self, filename, header_data, **kw):
        self.header_data = header_data
        BaseDocTemplate.__init__(self, filename, pagesize=letter,
                                  leftMargin=0, rightMargin=0,
                                  topMargin=0, bottomMargin=0, **kw)

        # ── Template 1: Recruiter (two-column with header) ──
        main_frame = Frame(
            SIDEBAR_W + 0.15*inch, MARGIN,
            MAIN_W - 0.5*inch, PAGE_H - HEADER_H - MARGIN - 0.1*inch,
            id="main", showBoundary=0,
        )
        sidebar_frame = Frame(
            SIDEBAR_PAD, MARGIN,
            SIDEBAR_W - SIDEBAR_PAD*2, PAGE_H - HEADER_H - MARGIN - 0.1*inch,
            id="sidebar", showBoundary=0,
        )
        recruiter_tmpl = PageTemplate(
            id="recruiter",
            frames=[main_frame, sidebar_frame],
            onPage=self._draw_recruiter_page,
        )

        # ── Template 2: Transition page ──
        transition_frame = Frame(
            1.2*inch, 1.5*inch,
            PAGE_W - 2.4*inch, PAGE_H - 3*inch,
            id="transition", showBoundary=0,
        )
        transition_tmpl = PageTemplate(
            id="transition",
            frames=[transition_frame],
            onPage=self._draw_transition_page,
        )

        # ── Template 3: ATS (single column, no decoration) ──
        ats_frame = Frame(
            0.7*inch, 0.5*inch,
            PAGE_W - 1.4*inch, PAGE_H - 1*inch,
            id="ats", showBoundary=0,
        )
        ats_tmpl = PageTemplate(
            id="ats",
            frames=[ats_frame],
            onPage=self._draw_ats_page,
        )

        self.addPageTemplates([recruiter_tmpl, transition_tmpl, ats_tmpl])

    def _draw_recruiter_page(self, canvas, doc):
        canvas.saveState()
        # Navy header
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)
        # Header text
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 22)
        canvas.drawString(0.45*inch, PAGE_H - 0.45*inch, self.header_data["name"])
        canvas.setFillColor(HexColor("#c0d0e8"))
        canvas.setFont("Helvetica", 10)
        canvas.drawString(0.45*inch, PAGE_H - 0.65*inch, self.header_data["subtitle"])
        canvas.setFillColor(HexColor("#a0b8d0"))
        canvas.setFont("Helvetica", 8.5)
        canvas.drawString(0.45*inch, PAGE_H - 0.85*inch, self.header_data["contact"])
        # Sidebar background
        canvas.setFillColor(SIDEBAR_BG)
        canvas.rect(0, 0, SIDEBAR_W, PAGE_H - HEADER_H, fill=1, stroke=0)
        # Accent line
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(2)
        canvas.line(0, PAGE_H - HEADER_H, PAGE_W, PAGE_H - HEADER_H)
        canvas.restoreState()

    def _draw_transition_page(self, canvas, doc):
        canvas.saveState()
        # Subtle navy top bar
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_H - 0.15*inch, PAGE_W, 0.15*inch, fill=1, stroke=0)
        # Accent line bottom
        canvas.setStrokeColor(LINE_COLOR)
        canvas.setLineWidth(0.5)
        canvas.line(1.2*inch, 1.3*inch, PAGE_W - 1.2*inch, 1.3*inch)
        canvas.restoreState()

    def _draw_ats_page(self, canvas, doc):
        """ATS pages: clean, no decoration."""
        pass


# ═══════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════

def build_recruiter_section(sidebar_data, main_data):
    """Build recruiter page flowables (main + sidebar)."""
    s = recruiter_styles()
    items = []

    # ── Main column ──
    items.append(Paragraph(main_data["h_summary"], s["heading"]))
    for t in main_data["summary"]:
        items.append(bp(s["bullet"], t))
    items.append(hr())

    items.append(Paragraph(main_data["h_experience"], s["heading"]))
    items.append(Paragraph(main_data["exp_title"], s["subheading"]))
    items.append(Paragraph(main_data["exp_date"], s["date"]))
    for t in main_data["experience"]:
        items.append(bp(s["bullet"], t))
    items.append(Paragraph(main_data["exp_tech"], s["tech"]))
    items.append(hr())

    items.append(Paragraph(main_data["h_previous"], s["heading"]))
    items.append(Paragraph(main_data["previous"], s["body"]))
    items.append(hr())

    items.append(Paragraph(main_data["h_projects"], s["heading"]))
    for proj in main_data["projects"]:
        items.append(bp(s["bullet"], proj))

    # ── Document links (achievements, recommendation) ──
    if main_data.get("doc_links"):
        items.append(hr())
        for label, url in main_data["doc_links"]:
            items.append(Paragraph(f'\u2022 <link href="{url}">{label}</link>', s["link"]))

    items.append(hr())

    items.append(Paragraph(main_data["h_training"], s["heading"]))
    for t in main_data["training"]:
        items.append(bp(s["bullet"], t))

    # ── Switch to sidebar frame ──
    items.append(FrameBreak())

    # ── Sidebar ──
    items.append(Paragraph(sidebar_data["h_contact"], s["side_heading"]))
    for line in sidebar_data["contact"]:
        items.append(Paragraph(line, s["side_body"]))
    for label, url in sidebar_data["contact_links"]:
        items.append(Paragraph(f'<link href="{url}">{label}</link>', s["side_link"]))
    items.append(side_hr())

    items.append(Paragraph(sidebar_data["h_skills"], s["side_heading"]))
    for skill_line in sidebar_data["skills"]:
        items.append(Paragraph(skill_line, s["side_body"]))
        items.append(Spacer(1, 1))
    items.append(side_hr())

    items.append(Paragraph(sidebar_data["h_education"], s["side_heading"]))
    for title, inst in sidebar_data["degrees"]:
        items.append(Paragraph(f"<b>{title}</b>", s["side_bold"]))
        items.append(Paragraph(inst, s["side_muted"]))
    items.append(side_hr())

    items.append(Paragraph(sidebar_data["h_languages"], s["side_heading"]))
    items.append(Paragraph(sidebar_data["languages"], s["side_body"]))

    return items


def build_transition_section(trans_data):
    """Build transition page flowables."""
    ts = transition_styles()
    s = recruiter_styles()
    items = []

    items.append(Spacer(1, 1.5*inch))
    items.append(Paragraph(trans_data["title"], ts["title"]))
    items.append(Spacer(1, 0.15*inch))
    items.append(Paragraph(trans_data["body"], ts["body"]))
    items.append(Spacer(1, 0.25*inch))

    reason_style = ParagraphStyle(
        "Reason", fontName="Helvetica", fontSize=9.5, leading=13,
        textColor=DARK, spaceAfter=6, leftIndent=20, bulletIndent=8,
    )
    for reason in trans_data["reasons"]:
        items.append(bp(reason_style, reason))

    items.append(Spacer(1, 0.4*inch))
    items.append(Paragraph(trans_data["footer"], ts["note"]))

    return items


def build_ats_section(ats_data):
    """Build ATS page flowables."""
    s = ats_styles()
    items = []

    # Header
    items.append(Paragraph("Vladimir Acu\u00f1a", s["name"]))
    items.append(Paragraph(ats_data["subtitle"], s["subtitle"]))
    items.append(Paragraph(ats_data["contact_line1"], s["contact"]))
    items.append(Paragraph(ats_data["contact_line2"], s["contact"]))
    items.append(Paragraph(ats_data["contact_line3"], s["contact"]))

    # Summary
    items.append(hr())
    items.append(Paragraph(ats_data["h_summary"], s["heading"]))
    for t in ats_data["summary"]:
        items.append(bp(s["bullet"], t))

    # Skills
    items.append(hr())
    items.append(Paragraph(ats_data["h_skills"], s["heading"]))
    for label, value in ats_data["skills"]:
        items.append(Paragraph(f"{label} {value}", s["tech"]))

    # Experience
    items.append(hr())
    items.append(Paragraph(ats_data["h_experience"], s["heading"]))
    items.append(Paragraph(ats_data["exp_title"], s["subheading"]))
    for t in ats_data["experience"]:
        items.append(bp(s["bullet"], t))
    items.append(Paragraph(ats_data["exp_tech"], s["tech"]))

    # Projects
    items.append(hr())
    items.append(Paragraph(ats_data["h_projects"], s["heading"]))
    for desc, url in ats_data["projects"]:
        items.append(bp(s["link"], f'{desc} <link href="{url}">{url}</link>'))

    # Education & Activity
    items.append(hr())
    items.append(Paragraph(ats_data["h_education"], s["heading"]))
    for t in ats_data["education_activity"]:
        items.append(bp(s["bullet"], t))

    # Degrees
    for title, inst in ats_data["degrees"]:
        items.append(Paragraph(f"<b>{title}</b>", s["body"]))
        items.append(Paragraph(inst, s["tech"]))
        items.append(Spacer(1, 3))

    # Languages
    items.append(hr())
    items.append(Paragraph(ats_data["h_languages"], s["heading"]))
    items.append(bp(s["bullet"], ats_data["languages"]))

    return items


def build_unified(header, sidebar, rmain, transition, ats, output_path):
    """Build the complete unified CV."""
    doc = UnifiedCV(output_path, header)

    story = []

    # Page 1: Recruiter
    story.extend(build_recruiter_section(sidebar, rmain))

    # Page 2: Transition
    story.append(NextPageTemplate("transition"))
    story.append(PageBreak())
    story.extend(build_transition_section(transition))

    # Page 3+: ATS
    story.append(NextPageTemplate("ats"))
    story.append(PageBreak())
    story.extend(build_ats_section(ats))

    doc.build(story)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  -> {output_path} ({size_kb:.1f} KB)")


def main():
    es_path = os.path.normpath(os.path.join(ASSETS_DIR, "cv-reclutador.pdf"))
    en_path = os.path.normpath(os.path.join(ASSETS_DIR, "cv-reclutador-english.pdf"))

    print("Generating unified CVs (recruiter + ATS)...")
    build_unified(HEADER_ES, SIDEBAR_ES, RMAIN_ES, TRANSITION_ES, ATS_ES, es_path)
    build_unified(HEADER_EN, SIDEBAR_EN, RMAIN_EN, TRANSITION_EN, ATS_EN, en_path)
    print("Done.")


if __name__ == "__main__":
    main()
