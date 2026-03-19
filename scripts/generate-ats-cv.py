#!/usr/bin/env python3
"""
Generate ATS-optimized CVs (ES + EN) as PDF.
Keeps the same clean, single-column format.
Integrates all current repo information.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Colors ──────────────────────────────────────────
BLACK = HexColor("#000000")
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#444444")
ACCENT = HexColor("#2563eb")
LINE_COLOR = HexColor("#cccccc")

# ── Paths ───────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "assets")


def make_styles():
    """Create paragraph styles matching the original CV format."""
    name = ParagraphStyle(
        "Name", fontName="Helvetica-Bold", fontSize=22, leading=26,
        textColor=BLACK, spaceAfter=2, alignment=TA_LEFT,
    )
    subtitle = ParagraphStyle(
        "Subtitle", fontName="Helvetica", fontSize=10, leading=13,
        textColor=DARK, spaceAfter=1,
    )
    contact = ParagraphStyle(
        "Contact", fontName="Helvetica", fontSize=8.5, leading=11,
        textColor=MUTED, spaceAfter=8,
    )
    heading = ParagraphStyle(
        "Heading", fontName="Helvetica-Bold", fontSize=12, leading=15,
        textColor=BLACK, spaceBefore=10, spaceAfter=4,
    )
    subheading = ParagraphStyle(
        "SubHeading", fontName="Helvetica-Bold", fontSize=10, leading=13,
        textColor=DARK, spaceBefore=4, spaceAfter=2,
    )
    body = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=9.5, leading=12.5,
        textColor=DARK, spaceAfter=2,
    )
    bullet = ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=9.5, leading=12.5,
        textColor=DARK, spaceAfter=2, leftIndent=12, bulletIndent=0,
    )
    tech_line = ParagraphStyle(
        "TechLine", fontName="Helvetica", fontSize=9, leading=12,
        textColor=MUTED, spaceAfter=1,
    )
    link_style = ParagraphStyle(
        "Link", fontName="Helvetica", fontSize=9, leading=12,
        textColor=ACCENT, spaceAfter=2, leftIndent=12, bulletIndent=0,
    )
    return dict(
        name=name, subtitle=subtitle, contact=contact, heading=heading,
        subheading=subheading, body=body, bullet=bullet, tech=tech_line,
        link=link_style,
    )


def hr():
    return HRFlowable(
        width="100%", thickness=0.5, color=LINE_COLOR,
        spaceBefore=2, spaceAfter=6,
    )


def bullet_p(style, text):
    return Paragraph(f"\u2022 {text}", style)


# ── Content (ES) ────────────────────────────────────
ES = dict(
    subtitle="Arquitecto de Software | Full-Stack Senior (PHP/JS/SQL) | Modernización & DevOps",
    contact_line1="Santiago, Chile | +56 9 8121 8838 | vladimir.acuna.dev@gmail.com",
    contact_line2=(
        'Web: <link href="https://vladimiracunadev-create.github.io/">vladimiracunadev-create.github.io</link> | '
        'GitHub: <link href="https://github.com/vladimiracunadev-create">github.com/vladimiracunadev-create</link> | '
        'GitLab: <link href="https://gitlab.com/vladimir.acuna.dev-group">gitlab.com/vladimir.acuna.dev-group</link>'
    ),
    contact_line3='LinkedIn: <link href="https://www.linkedin.com/in/vladimir-acuna-valdebenito">linkedin.com/in/vladimir-acuna-valdebenito</link>',
    h_summary="RESUMEN",
    summary=[
        "14 años liderando el diseño, evolución y operación de una plataforma educativa/psicométrica (2011-2025), con foco en continuidad operacional.",
        "Modernización progresiva (PHP 5.4 → PHP 8.2+), optimización de rendimiento y automatización de reportes (PDF/Excel) y procesos de datos.",
        "Experiencia en bases de datos (SQL Server, MySQL/MariaDB) y despliegues/entornos reproducibles con Docker y CI/CD.",
        "Portafolio técnico con casos prácticos (Cloud/AWS, microsistemas, agentes IA y observabilidad), documentación y demos verificables en GitHub y GitLab.",
    ],
    h_skills="SKILLS",
    skills=[
        ("<b>Backend:</b>", "PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"),
        ("<b>Frontend:</b>", "JavaScript, HTML, CSS"),
        ("<b>Datos:</b>", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB, modelado, ETL desde Excel"),
        ("<b>DevOps/Cloud:</b>", "Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform (básico)"),
        ("<b>Calidad/Seguridad:</b>", "hardening básico, secret scanning (Gitleaks, TruffleHog), control anti-inyección, Trivy, pip-audit"),
        ("<b>Observabilidad:</b>", "Prometheus/Grafana (laboratorios y fundamentos)"),
        ("<b>IA/Agentes:</b>", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"),
    ],
    h_experience="EXPERIENCIA",
    exp_title="Fundación CEIS Maristas — Arquitecto de Software y Desarrollador Full-Stack (2011-2025)",
    experience=[
        "Diseño, desarrollo y mantención de plataforma de evaluación de alumnos (baterías de test), módulos institucionales y reportes.",
        "Migración tecnológica (PHP 5.4 → PHP 8.2+), actualización de servidores/librerías y mejoras de rendimiento con JavaScript y pruebas de carga.",
        "Desarrollo de reportes avanzados PDF/Excel con indicadores, percentiles y análisis por curso/nivel/establecimiento.",
        "Importación y migración de datos masivos desde Excel con validaciones; automatización de comunicaciones (envíos, segmentación, seguimiento).",
        "Soporte directo a usuarios clave (coordinadores, orientadores, directivos) y operación en producción.",
    ],
    exp_tech="Tecnologías: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
    h_projects="PROYECTOS DESTACADOS",
    projects=[
        ("Cloud/AWS y FinOps — GitHub (demos y documentación):", "https://github.com/vladimiracunadev-create/proyectos-aws"),
        ("Cloud/AWS — GitLab (15 casos, CI/CD 5 stages, ~80% SAA-C03):", "https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab"),
        ("Microsistemas (suite de 11 micro-apps, Hub CLI, MCP server):", "https://github.com/vladimiracunadev-create/microsistemas"),
        ("Social Bot Scheduler (matriz 9 ejes de integración, 9 motores DB, n8n, Prometheus/Grafana):", "https://github.com/vladimiracunadev-create/social-bot-scheduler"),
        ("Docker Labs (12 labs, Control Center, instalador Windows):", "https://github.com/vladimiracunadev-create/docker-labs"),
        ("LangGraph casos reales (25 casos, 4 operacionales/industriales, agentes con estado):", "https://github.com/vladimiracunadev-create/langgraph-realworld"),
        ("MCP + Ollama local (chat IA local, herramientas MCP, 100% privado):", "https://github.com/vladimiracunadev-create/mcp-ollama-local"),
    ],
    h_education="FORMACIÓN Y ACTIVIDAD RECIENTE",
    education_activity=[
        "Formación continua (cursos online): bases de ML/NLP y automatización práctica aplicada a proyectos.",
        "Consolidación de portafolio técnico (Cloud/AWS, Docker labs, agentes) y documentación orientada a reclutadores.",
    ],
    h_degrees="EDUCACIÓN",
    degrees=[
        ("Ingeniería de Ejecución en Computación e Informática", "Universidad de Tarapacá (Arica)"),
        ("Técnico de Administración de Empresas (Mención Marketing)", "INACAP (Santiago)"),
    ],
    h_languages="IDIOMAS",
    languages="Inglés: intermedio en lectura; básico en escritura y conversación.",
)


# ── Content (EN) ────────────────────────────────────
EN = dict(
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
        "Progressive modernization (PHP 5.4 → PHP 8.2+), performance optimization, and automation of PDF/Excel reports and data processes.",
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
    exp_title="Fundaci\u00f3n CEIS Maristas - Software Architect and Full-Stack Developer (2011-2025)",
    experience=[
        "Design, development, and maintenance of a student assessment platform (test batteries), institutional modules, and reports.",
        "Technology migration (PHP 5.4 → PHP 8.2+), server/library upgrades, and performance improvements with JavaScript and load testing.",
        "Development of advanced PDF/Excel reports with indicators, percentiles, and analysis by class, level, and school.",
        "Import and migration of high-volume data from Excel with validations; automation of communications (sending, segmentation, follow-up).",
        "Direct support for key users (coordinators, counselors, school leaders) and production operations.",
    ],
    exp_tech="Technologies: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
    h_projects="SELECTED PROJECTS",
    projects=[
        ("Cloud/AWS and FinOps — GitHub (demos and documentation):", "https://github.com/vladimiracunadev-create/proyectos-aws"),
        ("Cloud/AWS — GitLab (15 cases, 5-stage CI/CD, ~80% SAA-C03):", "https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab"),
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


def build_cv(data, output_path):
    """Build a single ATS CV PDF from the given content dict."""
    s = make_styles()

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.5 * inch, bottomMargin=0.5 * inch,
    )

    story = []

    # ── Header ──
    story.append(Paragraph("Vladimir Acu\u00f1a", s["name"]))
    story.append(Paragraph(data["subtitle"], s["subtitle"]))
    story.append(Paragraph(data["contact_line1"], s["contact"]))
    story.append(Paragraph(data["contact_line2"], s["contact"]))
    story.append(Paragraph(data["contact_line3"], s["contact"]))

    # ── Summary ──
    story.append(hr())
    story.append(Paragraph(data["h_summary"], s["heading"]))
    for item in data["summary"]:
        story.append(bullet_p(s["bullet"], item))

    # ── Skills ──
    story.append(hr())
    story.append(Paragraph(data["h_skills"], s["heading"]))
    for label, value in data["skills"]:
        story.append(Paragraph(f"{label} {value}", s["tech"]))

    # ── Experience ──
    story.append(hr())
    story.append(Paragraph(data["h_experience"], s["heading"]))
    story.append(Paragraph(data["exp_title"], s["subheading"]))
    for item in data["experience"]:
        story.append(bullet_p(s["bullet"], item))
    story.append(Paragraph(data["exp_tech"], s["tech"]))

    # ── Projects ──
    story.append(hr())
    story.append(Paragraph(data["h_projects"], s["heading"]))
    for desc, url in data["projects"]:
        story.append(
            bullet_p(s["link"], f'{desc} <link href="{url}">{url}</link>')
        )

    # ── Education & Activity ──
    story.append(hr())
    story.append(Paragraph(data["h_education"], s["heading"]))
    for item in data["education_activity"]:
        story.append(bullet_p(s["bullet"], item))

    # ── Degrees ──
    for title, institution in data["degrees"]:
        story.append(Paragraph(f"<b>{title}</b>", s["body"]))
        story.append(Paragraph(institution, s["tech"]))
        story.append(Spacer(1, 3))

    # ── Languages ──
    story.append(hr())
    story.append(Paragraph(data["h_languages"], s["heading"]))
    story.append(bullet_p(s["bullet"], data["languages"]))

    doc.build(story)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  -> {output_path} ({size_kb:.1f} KB)")


def main():
    es_path = os.path.join(ASSETS_DIR, "cv-ats.pdf")
    en_path = os.path.join(ASSETS_DIR, "cv-ats-english.pdf")

    print("Generating ATS CVs...")
    build_cv(ES, es_path)
    build_cv(EN, en_path)
    print("Done.")


if __name__ == "__main__":
    main()
