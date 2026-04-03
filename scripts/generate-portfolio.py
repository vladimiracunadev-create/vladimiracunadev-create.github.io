#!/usr/bin/env python3
"""
Generate professional portfolio PDFs for all 6 languages (ES, EN, PT, IT, FR, ZH).
Output: assets/portafolio.pdf, assets/portafolio-english.pdf, etc.
Run:    python scripts/generate-portfolio.py
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle,
    KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# ── Register CJK font for Chinese ────────────────────
pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))

# ── Paths ────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "assets"))

# ── Colors ───────────────────────────────────────────
NAVY = HexColor("#2c5282")
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#444444")
ACCENT = HexColor("#2563eb")
LINE_COLOR = HexColor("#cccccc")
TABLE_HEADER_BG = HexColor("#2c5282")
TABLE_ALT_BG = HexColor("#f0f4f8")
WHITE = HexColor("#ffffff")

PAGE_W, PAGE_H = letter
MARGIN = 0.7 * inch

# ── Font helpers for CJK ─────────────────────────────
def _font(lang, bold=False):
    if lang == "zh":
        return "STSong-Light"
    return "Helvetica-Bold" if bold else "Helvetica"

def _font_oblique(lang):
    if lang == "zh":
        return "STSong-Light"
    return "Helvetica-Oblique"


# ═══════════════════════════════════════════════════════
# STYLES
# ═══════════════════════════════════════════════════════

def make_styles(lang="es"):
    fn = _font(lang, False)
    fb = _font(lang, True)
    fo = _font_oblique(lang)

    return dict(
        name=ParagraphStyle(
            "Name", fontName=fb, fontSize=18, leading=22,
            textColor=NAVY, spaceAfter=2,
        ),
        subtitle=ParagraphStyle(
            "Subtitle", fontName=fn, fontSize=10, leading=13,
            textColor=DARK, spaceAfter=6,
        ),
        contact=ParagraphStyle(
            "Contact", fontName=fn, fontSize=8.5, leading=11.5,
            textColor=MUTED, spaceAfter=1.5,
        ),
        heading=ParagraphStyle(
            "Heading", fontName=fb, fontSize=12, leading=15,
            textColor=NAVY, spaceBefore=10, spaceAfter=4,
        ),
        subheading=ParagraphStyle(
            "SubHeading", fontName=fb, fontSize=10, leading=13,
            textColor=DARK, spaceBefore=4, spaceAfter=2,
        ),
        body=ParagraphStyle(
            "Body", fontName=fn, fontSize=9.2, leading=12.5,
            textColor=DARK, spaceAfter=3,
        ),
        bullet=ParagraphStyle(
            "Bullet", fontName=fn, fontSize=9.2, leading=12.5,
            textColor=DARK, spaceAfter=2, leftIndent=12, bulletIndent=0,
        ),
        link=ParagraphStyle(
            "Link", fontName=fn, fontSize=8.5, leading=11,
            textColor=ACCENT, spaceAfter=1.5, leftIndent=12, bulletIndent=0,
        ),
        table_header=ParagraphStyle(
            "TH", fontName=fb, fontSize=8.5, leading=11,
            textColor=WHITE,
        ),
        table_cell_bold=ParagraphStyle(
            "TCB", fontName=fb, fontSize=8.5, leading=11,
            textColor=DARK,
        ),
        table_cell=ParagraphStyle(
            "TC", fontName=fn, fontSize=8.5, leading=11,
            textColor=DARK,
        ),
        muted=ParagraphStyle(
            "Muted", fontName=fo, fontSize=8.5, leading=11,
            textColor=MUTED, spaceAfter=2,
        ),
    )


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR,
                      spaceBefore=2, spaceAfter=6)


def bullet_p(style, text):
    return Paragraph(f"\u2022  {text}", style)


def link_p(style, url, label=None):
    label = label or url
    return Paragraph(f'<link href="{url}">{label}</link>', style)


# ═══════════════════════════════════════════════════════
# CONTACT INFO (shared)
# ═══════════════════════════════════════════════════════

CONTACT = {
    "email": "vladimir.acuna.dev@gmail.com",
    "linkedin": "linkedin.com/in/vladimir-acuna-valdebenito",
    "web": "https://vladimiracunadev-create.github.io/",
    "github": "https://github.com/vladimiracunadev-create",
    "gitlab": "https://gitlab.com/vladimir.acuna.dev-group",
    "country": "Chile",
}

PROJECT_LINKS = {
    "cloud_gh": "https://github.com/vladimiracunadev-create/proyectos-aws",
    "cloud_gl": "https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab",
    "micro": "https://github.com/vladimiracunadev-create/microsistemas",
    "social": "https://github.com/vladimiracunadev-create/social-bot-scheduler",
    "docker": "https://github.com/vladimiracunadev-create/docker-labs",
    "langgraph": "https://github.com/vladimiracunadev-create/langgraph-realworld",
    "mcp": "https://github.com/vladimiracunadev-create/mcp-ollama-local",
}


# ═══════════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════════

def get_content(lang):
    T = {}

    # ──────────────────── SPANISH ────────────────────
    T["es"] = {
        "subtitle": "Arquitecto de Soluciones | Senior Full-Stack | Modernización, Automatización e IA Aplicada",
        "contact_labels": {
            "email": "Email", "linkedin": "LinkedIn", "web": "Portafolio Web",
            "github": "GitHub", "gitlab": "GitLab", "country": "Pa\u00eds",
        },
        "intro_title": "Introducci\u00f3n Profesional",
        "intro": [
            "Profesional titulado en Ingenier\u00eda en Inform\u00e1tica, con m\u00e1s de 16 a\u00f1os de experiencia desarrollando, manteniendo y modernizando soluciones web para organizaciones p\u00fablicas y privadas. Especializado en sistemas de misi\u00f3n cr\u00edtica, plataformas complejas, continuidad operacional, calidad de datos y rendimiento.",
            "\u00daltimos 14 a\u00f1os especializados en el dise\u00f1o, desarrollo y evoluci\u00f3n de una plataforma educativa/psicom\u00e9trica. Combinando backend, frontend, bases de datos, reportes avanzados, y recientemente automatizaci\u00f3n e IA Ag\u00e9ntica, con foco en resiliencia y observabilidad.",
            "Sello profesional: Modernizaci\u00f3n Progresiva \u2014 tomar sistemas legacy complejos, comprenderlos en profundidad y evolucionarlos hacia un estado moderno, estable y escalable utilizando observabilidad avanzada, resiliencia industrial, arquitectura cloud-native (DevOps/FinOps), asegurando siempre la continuidad operacional.",
        ],
        "vp_title": "Propuesta de Valor",
        "vp": [
            "Modernizaci\u00f3n de sistemas legacy (PHP 5.x \u2192 PHP 8.x, arquitecturas desacopladas)",
            "Dise\u00f1o/mantenci\u00f3n de plataformas web complejas (m\u00faltiples m\u00f3dulos, grandes vol\u00famenes de datos, integraciones con banca/pagos/gobierno)",
            "Optimizaci\u00f3n, Observabilidad, Escalabilidad (SQL tuning, dashboards Prometheus/Grafana)",
            "Automatizaci\u00f3n, Analytics, IA (reportes PDF/Excel, indicadores, prototipos de IA Ag\u00e9ntica)",
            "Cloud y Gobernanza/FinOps (Terraform, OIDC, AWS Budgets)",
            "Developer Experience/DX (Docker Labs, Hub CLI, doctor/smoke tests)",
            "Perspectiva hol\u00edstica de negocio (estudios en marketing, administraci\u00f3n, finanzas)",
        ],
        "projects_title": "Proyectos Actuales y Foco (Portafolio P\u00fablico)",
        "projects_intro": "Repositorios p\u00fablicos demostrando capacidades actuales:",
        "projects": [
            "<b>Arquitectura Resiliente &amp; Infraestructura Inmutable:</b> CI/CD con GitHub Actions/OIDC, Terraform, FinOps/AWS Budgets",
            "<b>Observabilidad &amp; DX:</b> Docker Labs con Prometheus/Grafana, Microsistemas (Hub CLI), doctor/smoke tests",
            "<b>IA Ag\u00e9ntica:</b> LangGraph + Ollama (IA local), agentes stateful, rutas condicionales",
            "<b>Social Bot Scheduler:</b> Matriz de integraci\u00f3n 9 ejes, 9 motores de BD, orquestaci\u00f3n n8n, Prometheus/Grafana",
            "<b>MCP + Ollama local:</b> Chat IA local, herramientas MCP, 100% privado",
            "<b>Unikernel Labs:</b> Control Center Windows — WSL2 + Node.js + WinForms, servicios Unikraft",
            "<b>ChofyAI Studio:</b> Lanzador IA local macOS — Tauri + Rust + React, Apple Silicon",
        ],
        "project_links_title": "Enlaces de Proyectos",
        "project_link_labels": {
            "cloud_gh": "Cloud/AWS (GitHub)", "cloud_gl": "Cloud/AWS (GitLab)",
            "micro": "Microsistemas", "social": "Social Bot Scheduler",
            "docker": "Docker Labs", "langgraph": "LangGraph",
            "mcp": "MCP + Ollama",
            "unikernel": "Unikernel Labs",
            "chofyai": "ChofyAI Studio",
        },
        "exp_title": "Experiencia Relevante",
        "exp_main_org": "Plataforma educativa/psicom\u00e9trica (2011\u20132025)",
        "exp_main": [
            "<b>Rol:</b> Desarrollador Senior / Arquitecto de Software (de facto)",
            "<b>Alcance:</b> Fundaci\u00f3n educativa; soluciones para colegios y equipos de orientaci\u00f3n",
            "Dise\u00f1o, desarrollo y mantenci\u00f3n de plataforma web de evaluaci\u00f3n de alumnos",
            "Migraci\u00f3n tecnol\u00f3gica: PHP 5.4 \u2192 PHP 8.2+, migraci\u00f3n JS para rendimiento",
            "M\u00f3dulos de reportes avanzados: PDFs, gr\u00e1ficos, Excel con indicadores psicom\u00e9tricos",
            "Importaci\u00f3n/migraci\u00f3n de datos desde Excel con validaciones",
            "Automatizaci\u00f3n de comunicaciones: mailing masivo (SMTP, Constant Contact), segmentaci\u00f3n",
            "Soporte de alto nivel a usuarios",
            "<b>Tecnolog\u00edas:</b> PHP 5/8, JavaScript, jQuery, HTML, CSS, SQL Server, MySQL, Apache, Linux, LimeSurvey, JMeter",
        ],
        "exp_prev_title": "Experiencia Previa",
        "exp_prev": [
            "<b>Gobierno (CONACE):</b> Sistemas RRHH, adquisiciones, inventarios, reportes PDF/Excel, m\u00f3dulos de seguridad",
            "<b>Financiero/Pagos (Transbank, PointPay, Corpvida):</b> Sistemas GSET, facturaci\u00f3n, SQL Server/Oracle, VB6 COM, Crystal Reports",
            "<b>Desarrollo web para diversas organizaciones (Giro Ingenier\u00eda, hoteles, colegios):</b> Sitios din\u00e1micos/est\u00e1ticos, intranets, encuestas, ambientes educativos",
        ],
        "edu_title": "Educaci\u00f3n",
        "edu": [
            "Ingenier\u00eda en Inform\u00e1tica, Universidad de Tarapac\u00e1, Arica",
            "T\u00e9cnico en Administraci\u00f3n de Empresas (Marketing), INACAP (Certificaci\u00f3n SAP User)",
            "Cursos varios: J2EE, web m\u00f3vil, ciberseguridad",
        ],
        "tech_title": "Competencias T\u00e9cnicas",
        "tech_header": ["Categor\u00eda", "Tecnolog\u00edas / Herramientas"],
        "tech_rows": [
            ["Backend", "PHP (4/5/8.x), JavaScript/Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"],
            ["Frontend", "HTML, CSS, JavaScript"],
            ["Bases de Datos", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB"],
            ["Servidores/Entornos", "Docker, Kubernetes, Linux, Windows Server, Apache"],
            ["Cloud/Infraestructura", "Terraform, AWS (S3, Amplify, CloudFront), OIDC, FinOps/Budgets, CI/CD (GitHub Actions/GitLab CI)"],
            ["Observabilidad", "Prometheus, Grafana"],
            ["Calidad/Seguridad", "Hardening, secret scanning (Gitleaks, TruffleHog), anti-inyecci\u00f3n, Trivy, pip-audit"],
            ["Resiliencia", "Circuit breakers, Idempotency"],
            ["IA/Automatizaci\u00f3n", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"],
            ["DX", "Hub CLI, doctor/smoke tests"],
        ],
        "style_title": "Estilo de Trabajo",
        "style": [
            "Orientado a soluciones y al detalle",
            "Responsable y comprometido",
            "Buena comunicaci\u00f3n con equipos no t\u00e9cnicos",
            "Aprendizaje continuo",
        ],
        "obj_title": "Objetivo Actual",
        "obj": "Integrar un equipo donde pueda aportar mi experiencia en modernizaci\u00f3n de sistemas, desarrollo full-stack y operaci\u00f3n de plataformas, contribuyendo a proyectos de alto impacto con foco en calidad, resiliencia y mejora continua.",
        "ref_title": "Referencias Profesionales",
        "ref_name": "Jean Claude Dupry",
        "ref_role": "Ex jefe directo",
        "ref_mobile": "M\u00f3vil: +56 9 9415 6984",
        "footer": "Portafolio Profesional \u2014 P\u00e1g.",
    }

    # ──────────────────── ENGLISH ────────────────────
    T["en"] = {
        "subtitle": "Solutions Architect | Senior Full-Stack | Modernization, Automation & Applied AI",
        "contact_labels": {
            "email": "Email", "linkedin": "LinkedIn", "web": "Web Portfolio",
            "github": "GitHub", "gitlab": "GitLab", "country": "Country",
        },
        "intro_title": "Professional Introduction",
        "intro": [
            "Professional with a degree in Computer Science Engineering, 16+ years of experience developing, maintaining, and modernizing web solutions for public and private organizations. Specialized in mission-critical systems, complex platforms, operational continuity, data quality, and performance.",
            "Last 14 years specialized in the design, development, and evolution of an educational/psychometric platform. Combining backend, frontend, databases, advanced reports, and recently automation and Agentic AI, with a focus on resilience and observability.",
            "Professional hallmark: Progressive Modernization \u2014 taking complex legacy systems, understanding them deeply, and evolving them toward a modern, stable, and scalable state using advanced observability, industrial resilience, cloud-native architecture (DevOps/FinOps), while always ensuring operational continuity.",
        ],
        "vp_title": "Value Proposition",
        "vp": [
            "Legacy system modernization (PHP 5.x \u2192 PHP 8.x, decoupled architectures)",
            "Design/maintenance of complex web platforms (multiple modules, large datasets, integrations with banking/payment/government)",
            "Optimization, Observability, Scalability (SQL tuning, Prometheus/Grafana dashboards)",
            "Automation, Analytics, AI (PDF/Excel reports, indicators, Agentic AI prototypes)",
            "Cloud and Governance/FinOps (Terraform, OIDC, AWS Budgets)",
            "Developer Experience/DX (Docker Labs, Hub CLI, doctor/smoke tests)",
            "Holistic business perspective (marketing, administration, finance studies)",
        ],
        "projects_title": "Current Projects and Focus (Public Portfolio)",
        "projects_intro": "Public repositories demonstrating current capabilities:",
        "projects": [
            "<b>Resilient Architecture &amp; Immutable Infrastructure:</b> CI/CD with GitHub Actions/OIDC, Terraform, FinOps/AWS Budgets",
            "<b>Observability &amp; DX:</b> Docker Labs with Prometheus/Grafana, Microsystems (Hub CLI), doctor/smoke tests",
            "<b>Agentic AI:</b> LangGraph + Ollama (local AI), stateful agents, conditional routes",
            "<b>Social Bot Scheduler:</b> 9-axis integration matrix, 9 DB engines, n8n orchestration, Prometheus/Grafana",
            "<b>MCP + Ollama local:</b> Local AI chat, MCP tools, 100% private",
            "<b>Unikernel Labs:</b> Windows Control Center \u2014 WSL2 + Node.js + WinForms, Unikraft services",
            "<b>ChofyAI Studio:</b> macOS local AI launcher \u2014 Tauri + Rust + React, Apple Silicon",
        ],
        "project_links_title": "Project Links",
        "project_link_labels": {
            "cloud_gh": "Cloud/AWS (GitHub)", "cloud_gl": "Cloud/AWS (GitLab)",
            "micro": "Microsystems", "social": "Social Bot Scheduler",
            "docker": "Docker Labs", "langgraph": "LangGraph",
            "mcp": "MCP + Ollama",
            "unikernel": "Unikernel Labs",
            "chofyai": "ChofyAI Studio",
        },
        "exp_title": "Relevant Experience",
        "exp_main_org": "Educational/psychometric platform (2011\u20132025)",
        "exp_main": [
            "<b>Role:</b> Senior Developer / Software Architect (de facto)",
            "<b>Scope:</b> Educational foundation; solutions for schools and guidance teams",
            "Design, development, and maintenance of student assessment web platform",
            "Tech migration: PHP 5.4 \u2192 PHP 8.2+, JS migration for performance",
            "Advanced reporting modules: PDFs, charts, Excel with psychometric indicators",
            "Data import/migration from Excel with validation",
            "Communication automation: mass email (SMTP, Constant Contact), segmentation",
            "High-level user support",
            "<b>Technologies:</b> PHP 5/8, JavaScript, jQuery, HTML, CSS, SQL Server, MySQL, Apache, Linux, LimeSurvey, JMeter",
        ],
        "exp_prev_title": "Previous Experience",
        "exp_prev": [
            "<b>Government (CONACE):</b> HR systems, procurement, inventories, PDF/Excel reports, security modules",
            "<b>Financial/Payment (Transbank, PointPay, Corpvida):</b> GSET systems, billing, SQL Server/Oracle, VB6 COM, Crystal Reports",
            "<b>Web development for diverse organizations (Giro Ingenier\u00eda, hotels, schools):</b> Dynamic/static sites, intranets, surveys, educational environments",
        ],
        "edu_title": "Education",
        "edu": [
            "Computer Science Engineering, Universidad de Tarapac\u00e1, Arica",
            "Business Administration Technician (Marketing), INACAP (SAP User certification)",
            "Various courses: J2EE, mobile web, cybersecurity",
        ],
        "tech_title": "Technical Competencies",
        "tech_header": ["Category", "Technologies / Tools"],
        "tech_rows": [
            ["Backend", "PHP (4/5/8.x), JavaScript/Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"],
            ["Frontend", "HTML, CSS, JavaScript"],
            ["Databases", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB"],
            ["Servers/Environments", "Docker, Kubernetes, Linux, Windows Server, Apache"],
            ["Cloud/Infrastructure", "Terraform, AWS (S3, Amplify, CloudFront), OIDC, FinOps/Budgets, CI/CD (GitHub Actions/GitLab CI)"],
            ["Observability", "Prometheus, Grafana"],
            ["Quality/Security", "Hardening, secret scanning (Gitleaks, TruffleHog), anti-injection, Trivy, pip-audit"],
            ["Resilience", "Circuit breakers, Idempotency"],
            ["AI/Automation", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"],
            ["DX", "Hub CLI, doctor/smoke tests"],
        ],
        "style_title": "Work Style",
        "style": [
            "Solution and detail-oriented",
            "Responsible and committed",
            "Good communication with non-technical teams",
            "Continuous learning",
        ],
        "obj_title": "Current Objective",
        "obj": "Join a team where I can contribute my experience in system modernization, full-stack development, and platform operations, contributing to high-impact projects with a focus on quality, resilience, and continuous improvement.",
        "ref_title": "Professional References",
        "ref_name": "Jean Claude Dupry",
        "ref_role": "Former direct manager",
        "ref_mobile": "Mobile: +56 9 9415 6984",
        "footer": "Professional Portfolio \u2014 Page",
    }

    # ──────────────────── PORTUGUESE ─────────────────
    T["pt"] = {
        "subtitle": "Arquiteto de Soluções | Senior Full-Stack | Modernização, Automação e IA Aplicada",
        "contact_labels": {
            "email": "Email", "linkedin": "LinkedIn", "web": "Portf\u00f3lio Web",
            "github": "GitHub", "gitlab": "GitLab", "country": "Pa\u00eds",
        },
        "intro_title": "Introdu\u00e7\u00e3o Profissional",
        "intro": [
            "Profissional formado em Engenharia da Computa\u00e7\u00e3o, com mais de 16 anos de experi\u00eancia desenvolvendo, mantendo e modernizando solu\u00e7\u00f5es web para organiza\u00e7\u00f5es p\u00fablicas e privadas. Especializado em sistemas de miss\u00e3o cr\u00edtica, plataformas complexas, continuidade operacional, qualidade de dados e desempenho.",
            "\u00daltimos 14 anos especializados no design, desenvolvimento e evolu\u00e7\u00e3o de uma plataforma educacional/psicom\u00e9trica. Combinando backend, frontend, bancos de dados, relat\u00f3rios avan\u00e7ados, e recentemente automa\u00e7\u00e3o e IA Ag\u00eantica, com foco em resili\u00eancia e observabilidade.",
            "Marca profissional: Moderniza\u00e7\u00e3o Progressiva \u2014 pegar sistemas legados complexos, compreend\u00ea-los profundamente e evolu\u00ed-los para um estado moderno, est\u00e1vel e escal\u00e1vel usando observabilidade avan\u00e7ada, resili\u00eancia industrial, arquitetura cloud-native (DevOps/FinOps), sempre garantindo a continuidade operacional.",
        ],
        "vp_title": "Proposta de Valor",
        "vp": [
            "Moderniza\u00e7\u00e3o de sistemas legados (PHP 5.x \u2192 PHP 8.x, arquiteturas desacopladas)",
            "Design/manuten\u00e7\u00e3o de plataformas web complexas (m\u00faltiplos m\u00f3dulos, grandes volumes de dados, integra\u00e7\u00f5es com bancos/pagamentos/governo)",
            "Otimiza\u00e7\u00e3o, Observabilidade, Escalabilidade (SQL tuning, dashboards Prometheus/Grafana)",
            "Automa\u00e7\u00e3o, Analytics, IA (relat\u00f3rios PDF/Excel, indicadores, prot\u00f3tipos de IA Ag\u00eantica)",
            "Cloud e Governan\u00e7a/FinOps (Terraform, OIDC, AWS Budgets)",
            "Developer Experience/DX (Docker Labs, Hub CLI, doctor/smoke tests)",
            "Perspectiva hol\u00edstica de neg\u00f3cios (estudos em marketing, administra\u00e7\u00e3o, finan\u00e7as)",
        ],
        "projects_title": "Projetos Atuais e Foco (Portf\u00f3lio P\u00fablico)",
        "projects_intro": "Reposit\u00f3rios p\u00fablicos demonstrando capacidades atuais:",
        "projects": [
            "<b>Arquitetura Resiliente &amp; Infraestrutura Imut\u00e1vel:</b> CI/CD com GitHub Actions/OIDC, Terraform, FinOps/AWS Budgets",
            "<b>Observabilidade &amp; DX:</b> Docker Labs com Prometheus/Grafana, Microssistemas (Hub CLI), doctor/smoke tests",
            "<b>IA Ag\u00eantica:</b> LangGraph + Ollama (IA local), agentes stateful, rotas condicionais",
            "<b>Social Bot Scheduler:</b> Matriz de integra\u00e7\u00e3o 9 eixos, 9 motores de BD, orquestra\u00e7\u00e3o n8n, Prometheus/Grafana",
            "<b>MCP + Ollama local:</b> Chat IA local, ferramentas MCP, 100% privado",
            "<b>Unikernel Labs:</b> Control Center Windows \u2014 WSL2 + Node.js + WinForms, servi\u00e7os Unikraft",
            "<b>ChofyAI Studio:</b> Launcher IA local macOS \u2014 Tauri + Rust + React, Apple Silicon",
        ],
        "project_links_title": "Links dos Projetos",
        "project_link_labels": {
            "cloud_gh": "Cloud/AWS (GitHub)", "cloud_gl": "Cloud/AWS (GitLab)",
            "micro": "Microssistemas", "social": "Social Bot Scheduler",
            "docker": "Docker Labs", "langgraph": "LangGraph",
            "mcp": "MCP + Ollama",
            "unikernel": "Unikernel Labs",
            "chofyai": "ChofyAI Studio",
        },
        "exp_title": "Experi\u00eancia Relevante",
        "exp_main_org": "Plataforma educacional/psicom\u00e9trica (2011\u20132025)",
        "exp_main": [
            "<b>Cargo:</b> Desenvolvedor S\u00eanior / Arquiteto de Software (de facto)",
            "<b>Escopo:</b> Funda\u00e7\u00e3o educacional; solu\u00e7\u00f5es para escolas e equipes de orienta\u00e7\u00e3o",
            "Design, desenvolvimento e manuten\u00e7\u00e3o de plataforma web de avalia\u00e7\u00e3o de alunos",
            "Migra\u00e7\u00e3o tecnol\u00f3gica: PHP 5.4 \u2192 PHP 8.2+, migra\u00e7\u00e3o JS para desempenho",
            "M\u00f3dulos de relat\u00f3rios avan\u00e7ados: PDFs, gr\u00e1ficos, Excel com indicadores psicom\u00e9tricos",
            "Importa\u00e7\u00e3o/migra\u00e7\u00e3o de dados a partir de Excel com valida\u00e7\u00f5es",
            "Automa\u00e7\u00e3o de comunica\u00e7\u00f5es: email em massa (SMTP, Constant Contact), segmenta\u00e7\u00e3o",
            "Suporte de alto n\u00edvel a usu\u00e1rios",
            "<b>Tecnologias:</b> PHP 5/8, JavaScript, jQuery, HTML, CSS, SQL Server, MySQL, Apache, Linux, LimeSurvey, JMeter",
        ],
        "exp_prev_title": "Experi\u00eancia Anterior",
        "exp_prev": [
            "<b>Governo (CONACE):</b> Sistemas de RH, compras, invent\u00e1rios, relat\u00f3rios PDF/Excel, m\u00f3dulos de seguran\u00e7a",
            "<b>Financeiro/Pagamentos (Transbank, PointPay, Corpvida):</b> Sistemas GSET, faturamento, SQL Server/Oracle, VB6 COM, Crystal Reports",
            "<b>Desenvolvimento web para diversas organiza\u00e7\u00f5es (Giro Ingenier\u00eda, hot\u00e9is, escolas):</b> Sites din\u00e2micos/est\u00e1ticos, intranets, pesquisas, ambientes educacionais",
        ],
        "edu_title": "Educa\u00e7\u00e3o",
        "edu": [
            "Engenharia da Computa\u00e7\u00e3o, Universidad de Tarapac\u00e1, Arica",
            "T\u00e9cnico em Administra\u00e7\u00e3o de Empresas (Marketing), INACAP (Certifica\u00e7\u00e3o SAP User)",
            "Diversos cursos: J2EE, web m\u00f3vel, ciberseguran\u00e7a",
        ],
        "tech_title": "Compet\u00eancias T\u00e9cnicas",
        "tech_header": ["Categoria", "Tecnologias / Ferramentas"],
        "tech_rows": [
            ["Backend", "PHP (4/5/8.x), JavaScript/Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"],
            ["Frontend", "HTML, CSS, JavaScript"],
            ["Bancos de Dados", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB"],
            ["Servidores/Ambientes", "Docker, Kubernetes, Linux, Windows Server, Apache"],
            ["Cloud/Infraestrutura", "Terraform, AWS (S3, Amplify, CloudFront), OIDC, FinOps/Budgets, CI/CD (GitHub Actions/GitLab CI)"],
            ["Observabilidade", "Prometheus, Grafana"],
            ["Qualidade/Seguran\u00e7a", "Hardening, secret scanning (Gitleaks, TruffleHog), anti-inje\u00e7\u00e3o, Trivy, pip-audit"],
            ["Resili\u00eancia", "Circuit breakers, Idempotency"],
            ["IA/Automa\u00e7\u00e3o", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"],
            ["DX", "Hub CLI, doctor/smoke tests"],
        ],
        "style_title": "Estilo de Trabalho",
        "style": [
            "Orientado a solu\u00e7\u00f5es e ao detalhe",
            "Respons\u00e1vel e comprometido",
            "Boa comunica\u00e7\u00e3o com equipes n\u00e3o t\u00e9cnicas",
            "Aprendizado cont\u00ednuo",
        ],
        "obj_title": "Objetivo Atual",
        "obj": "Integrar uma equipe onde possa contribuir com minha experi\u00eancia em moderniza\u00e7\u00e3o de sistemas, desenvolvimento full-stack e opera\u00e7\u00e3o de plataformas, contribuindo para projetos de alto impacto com foco em qualidade, resili\u00eancia e melhoria cont\u00ednua.",
        "ref_title": "Refer\u00eancias Profissionais",
        "ref_name": "Jean Claude Dupry",
        "ref_role": "Ex-gerente direto",
        "ref_mobile": "Celular: +56 9 9415 6984",
        "footer": "Portf\u00f3lio Profissional \u2014 P\u00e1g.",
    }

    # ──────────────────── ITALIAN ────────────────────
    T["it"] = {
        "subtitle": "Architetto di Soluzioni | Senior Full-Stack | Modernizzazione, Automazione e IA Applicata",
        "contact_labels": {
            "email": "Email", "linkedin": "LinkedIn", "web": "Portfolio Web",
            "github": "GitHub", "gitlab": "GitLab", "country": "Paese",
        },
        "intro_title": "Introduzione Professionale",
        "intro": [
            "Professionista laureato in Ingegneria Informatica, con oltre 16 anni di esperienza nello sviluppo, manutenzione e modernizzazione di soluzioni web per organizzazioni pubbliche e private. Specializzato in sistemi mission-critical, piattaforme complesse, continuit\u00e0 operativa, qualit\u00e0 dei dati e prestazioni.",
            "Ultimi 14 anni specializzati nella progettazione, sviluppo ed evoluzione di una piattaforma educativa/psicometrica. Combinando backend, frontend, database, report avanzati, e recentemente automazione e IA Agentica, con focus su resilienza e osservabilit\u00e0.",
            "Marchio professionale: Modernizzazione Progressiva \u2014 prendere sistemi legacy complessi, comprenderli a fondo ed evolverli verso uno stato moderno, stabile e scalabile utilizzando osservabilit\u00e0 avanzata, resilienza industriale, architettura cloud-native (DevOps/FinOps), garantendo sempre la continuit\u00e0 operativa.",
        ],
        "vp_title": "Proposta di Valore",
        "vp": [
            "Modernizzazione di sistemi legacy (PHP 5.x \u2192 PHP 8.x, architetture disaccoppiate)",
            "Progettazione/manutenzione di piattaforme web complesse (moduli multipli, grandi volumi di dati, integrazioni con banche/pagamenti/governo)",
            "Ottimizzazione, Osservabilit\u00e0, Scalabilit\u00e0 (SQL tuning, dashboard Prometheus/Grafana)",
            "Automazione, Analytics, IA (report PDF/Excel, indicatori, prototipi di IA Agentica)",
            "Cloud e Governance/FinOps (Terraform, OIDC, AWS Budgets)",
            "Developer Experience/DX (Docker Labs, Hub CLI, doctor/smoke tests)",
            "Prospettiva olistica del business (studi in marketing, amministrazione, finanza)",
        ],
        "projects_title": "Progetti Attuali e Focus (Portfolio Pubblico)",
        "projects_intro": "Repository pubblici che dimostrano le capacit\u00e0 attuali:",
        "projects": [
            "<b>Architettura Resiliente &amp; Infrastruttura Immutabile:</b> CI/CD con GitHub Actions/OIDC, Terraform, FinOps/AWS Budgets",
            "<b>Osservabilit\u00e0 &amp; DX:</b> Docker Labs con Prometheus/Grafana, Microsistemi (Hub CLI), doctor/smoke tests",
            "<b>IA Agentica:</b> LangGraph + Ollama (IA locale), agenti stateful, rotte condizionali",
            "<b>Social Bot Scheduler:</b> Matrice di integrazione 9 assi, 9 motori DB, orchestrazione n8n, Prometheus/Grafana",
            "<b>MCP + Ollama locale:</b> Chat IA locale, strumenti MCP, 100% privato",
            "<b>Unikernel Labs:</b> Control Center Windows \u2014 WSL2 + Node.js + WinForms, servizi Unikraft",
            "<b>ChofyAI Studio:</b> Launcher IA locale macOS \u2014 Tauri + Rust + React, Apple Silicon",
        ],
        "project_links_title": "Link dei Progetti",
        "project_link_labels": {
            "cloud_gh": "Cloud/AWS (GitHub)", "cloud_gl": "Cloud/AWS (GitLab)",
            "micro": "Microsistemi", "social": "Social Bot Scheduler",
            "docker": "Docker Labs", "langgraph": "LangGraph",
            "mcp": "MCP + Ollama",
            "unikernel": "Unikernel Labs",
            "chofyai": "ChofyAI Studio",
        },
        "exp_title": "Esperienza Rilevante",
        "exp_main_org": "Piattaforma educativa/psicometrica (2011\u20132025)",
        "exp_main": [
            "<b>Ruolo:</b> Sviluppatore Senior / Architetto Software (de facto)",
            "<b>Ambito:</b> Fondazione educativa; soluzioni per scuole e team di orientamento",
            "Progettazione, sviluppo e manutenzione di piattaforma web di valutazione studenti",
            "Migrazione tecnologica: PHP 5.4 \u2192 PHP 8.2+, migrazione JS per le prestazioni",
            "Moduli di reportistica avanzata: PDF, grafici, Excel con indicatori psicometrici",
            "Importazione/migrazione dati da Excel con validazioni",
            "Automazione comunicazioni: email di massa (SMTP, Constant Contact), segmentazione",
            "Supporto di alto livello agli utenti",
            "<b>Tecnologie:</b> PHP 5/8, JavaScript, jQuery, HTML, CSS, SQL Server, MySQL, Apache, Linux, LimeSurvey, JMeter",
        ],
        "exp_prev_title": "Esperienza Precedente",
        "exp_prev": [
            "<b>Governo (CONACE):</b> Sistemi HR, approvvigionamento, inventari, report PDF/Excel, moduli di sicurezza",
            "<b>Finanziario/Pagamenti (Transbank, PointPay, Corpvida):</b> Sistemi GSET, fatturazione, SQL Server/Oracle, VB6 COM, Crystal Reports",
            "<b>Sviluppo web per diverse organizzazioni (Giro Ingenier\u00eda, hotel, scuole):</b> Siti dinamici/statici, intranet, sondaggi, ambienti educativi",
        ],
        "edu_title": "Istruzione",
        "edu": [
            "Ingegneria Informatica, Universidad de Tarapac\u00e1, Arica",
            "Tecnico in Amministrazione Aziendale (Marketing), INACAP (Certificazione SAP User)",
            "Vari corsi: J2EE, web mobile, cybersecurity",
        ],
        "tech_title": "Competenze Tecniche",
        "tech_header": ["Categoria", "Tecnologie / Strumenti"],
        "tech_rows": [
            ["Backend", "PHP (4/5/8.x), JavaScript/Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"],
            ["Frontend", "HTML, CSS, JavaScript"],
            ["Database", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB"],
            ["Server/Ambienti", "Docker, Kubernetes, Linux, Windows Server, Apache"],
            ["Cloud/Infrastruttura", "Terraform, AWS (S3, Amplify, CloudFront), OIDC, FinOps/Budgets, CI/CD (GitHub Actions/GitLab CI)"],
            ["Osservabilit\u00e0", "Prometheus, Grafana"],
            ["Qualit\u00e0/Sicurezza", "Hardening, secret scanning (Gitleaks, TruffleHog), anti-injection, Trivy, pip-audit"],
            ["Resilienza", "Circuit breakers, Idempotency"],
            ["IA/Automazione", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"],
            ["DX", "Hub CLI, doctor/smoke tests"],
        ],
        "style_title": "Stile di Lavoro",
        "style": [
            "Orientato alle soluzioni e ai dettagli",
            "Responsabile e impegnato",
            "Buona comunicazione con team non tecnici",
            "Apprendimento continuo",
        ],
        "obj_title": "Obiettivo Attuale",
        "obj": "Unirmi a un team dove possa contribuire con la mia esperienza nella modernizzazione dei sistemi, sviluppo full-stack e gestione delle piattaforme, contribuendo a progetti ad alto impatto con focus su qualit\u00e0, resilienza e miglioramento continuo.",
        "ref_title": "Referenze Professionali",
        "ref_name": "Jean Claude Dupry",
        "ref_role": "Ex responsabile diretto",
        "ref_mobile": "Cellulare: +56 9 9415 6984",
        "footer": "Portfolio Professionale \u2014 Pag.",
    }

    # ──────────────────── FRENCH ─────────────────────
    T["fr"] = {
        "subtitle": "Architecte de Solutions | Senior Full-Stack | Modernisation, Automatisation et IA Appliquée",
        "contact_labels": {
            "email": "Email", "linkedin": "LinkedIn", "web": "Portfolio Web",
            "github": "GitHub", "gitlab": "GitLab", "country": "Pays",
        },
        "intro_title": "Introduction Professionnelle",
        "intro": [
            "Professionnel dipl\u00f4m\u00e9 en Ing\u00e9nierie Informatique, avec plus de 16 ans d\u2019exp\u00e9rience dans le d\u00e9veloppement, la maintenance et la modernisation de solutions web pour des organisations publiques et priv\u00e9es. Sp\u00e9cialis\u00e9 dans les syst\u00e8mes critiques, les plateformes complexes, la continuit\u00e9 op\u00e9rationnelle, la qualit\u00e9 des donn\u00e9es et la performance.",
            "Derni\u00e8res 14 ann\u00e9es sp\u00e9cialis\u00e9es dans la conception, le d\u00e9veloppement et l\u2019\u00e9volution d\u2019une plateforme \u00e9ducative/psychom\u00e9trique. Combinant backend, frontend, bases de donn\u00e9es, rapports avanc\u00e9s, et r\u00e9cemment automatisation et IA Agentique, avec un focus sur la r\u00e9silience et l\u2019observabilit\u00e9.",
            "Marque professionnelle : Modernisation Progressive \u2014 prendre des syst\u00e8mes legacy complexes, les comprendre en profondeur et les faire \u00e9voluer vers un \u00e9tat moderne, stable et \u00e9volutif en utilisant l\u2019observabilit\u00e9 avanc\u00e9e, la r\u00e9silience industrielle, l\u2019architecture cloud-native (DevOps/FinOps), tout en assurant la continuit\u00e9 op\u00e9rationnelle.",
        ],
        "vp_title": "Proposition de Valeur",
        "vp": [
            "Modernisation de syst\u00e8mes legacy (PHP 5.x \u2192 PHP 8.x, architectures d\u00e9coupl\u00e9es)",
            "Conception/maintenance de plateformes web complexes (modules multiples, grands volumes de donn\u00e9es, int\u00e9grations banques/paiements/gouvernement)",
            "Optimisation, Observabilit\u00e9, Scalabilit\u00e9 (SQL tuning, tableaux de bord Prometheus/Grafana)",
            "Automatisation, Analytics, IA (rapports PDF/Excel, indicateurs, prototypes d\u2019IA Agentique)",
            "Cloud et Gouvernance/FinOps (Terraform, OIDC, AWS Budgets)",
            "Developer Experience/DX (Docker Labs, Hub CLI, doctor/smoke tests)",
            "Perspective holistique des affaires (\u00e9tudes en marketing, administration, finance)",
        ],
        "projects_title": "Projets Actuels et Focus (Portfolio Public)",
        "projects_intro": "D\u00e9p\u00f4ts publics d\u00e9montrant les capacit\u00e9s actuelles :",
        "projects": [
            "<b>Architecture R\u00e9siliente &amp; Infrastructure Immuable :</b> CI/CD avec GitHub Actions/OIDC, Terraform, FinOps/AWS Budgets",
            "<b>Observabilit\u00e9 &amp; DX :</b> Docker Labs avec Prometheus/Grafana, Microsyst\u00e8mes (Hub CLI), doctor/smoke tests",
            "<b>IA Agentique :</b> LangGraph + Ollama (IA locale), agents stateful, routes conditionnelles",
            "<b>Social Bot Scheduler :</b> Matrice d\u2019int\u00e9gration 9 axes, 9 moteurs BD, orchestration n8n, Prometheus/Grafana",
            "<b>MCP + Ollama local :</b> Chat IA local, outils MCP, 100% priv\u00e9",
            "<b>Unikernel Labs :</b> Control Center Windows \u2014 WSL2 + Node.js + WinForms, services Unikraft",
            "<b>ChofyAI Studio :</b> Lanceur IA locale macOS \u2014 Tauri + Rust + React, Apple Silicon",
        ],
        "project_links_title": "Liens des Projets",
        "project_link_labels": {
            "cloud_gh": "Cloud/AWS (GitHub)", "cloud_gl": "Cloud/AWS (GitLab)",
            "micro": "Microsyst\u00e8mes", "social": "Social Bot Scheduler",
            "docker": "Docker Labs", "langgraph": "LangGraph",
            "mcp": "MCP + Ollama",
            "unikernel": "Unikernel Labs",
            "chofyai": "ChofyAI Studio",
        },
        "exp_title": "Exp\u00e9rience Pertinente",
        "exp_main_org": "Plateforme \u00e9ducative/psychom\u00e9trique (2011\u20132025)",
        "exp_main": [
            "<b>R\u00f4le :</b> D\u00e9veloppeur Senior / Architecte Logiciel (de facto)",
            "<b>Port\u00e9e :</b> Fondation \u00e9ducative ; solutions pour \u00e9coles et \u00e9quipes d\u2019orientation",
            "Conception, d\u00e9veloppement et maintenance de plateforme web d\u2019\u00e9valuation des \u00e9l\u00e8ves",
            "Migration technologique : PHP 5.4 \u2192 PHP 8.2+, migration JS pour la performance",
            "Modules de rapports avanc\u00e9s : PDF, graphiques, Excel avec indicateurs psychom\u00e9triques",
            "Importation/migration de donn\u00e9es depuis Excel avec validations",
            "Automatisation des communications : envoi massif (SMTP, Constant Contact), segmentation",
            "Support de haut niveau aux utilisateurs",
            "<b>Technologies :</b> PHP 5/8, JavaScript, jQuery, HTML, CSS, SQL Server, MySQL, Apache, Linux, LimeSurvey, JMeter",
        ],
        "exp_prev_title": "Exp\u00e9rience Pr\u00e9c\u00e9dente",
        "exp_prev": [
            "<b>Gouvernement (CONACE) :</b> Syst\u00e8mes RH, approvisionnement, inventaires, rapports PDF/Excel, modules de s\u00e9curit\u00e9",
            "<b>Financier/Paiements (Transbank, PointPay, Corpvida) :</b> Syst\u00e8mes GSET, facturation, SQL Server/Oracle, VB6 COM, Crystal Reports",
            "<b>D\u00e9veloppement web pour diverses organisations (Giro Ingenier\u00eda, h\u00f4tels, \u00e9coles) :</b> Sites dynamiques/statiques, intranets, enqu\u00eates, environnements \u00e9ducatifs",
        ],
        "edu_title": "\u00c9ducation",
        "edu": [
            "Ing\u00e9nierie Informatique, Universidad de Tarapac\u00e1, Arica",
            "Technicien en Administration des Entreprises (Marketing), INACAP (Certification SAP User)",
            "Divers cours : J2EE, web mobile, cybers\u00e9curit\u00e9",
        ],
        "tech_title": "Comp\u00e9tences Techniques",
        "tech_header": ["Cat\u00e9gorie", "Technologies / Outils"],
        "tech_rows": [
            ["Backend", "PHP (4/5/8.x), JavaScript/Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"],
            ["Frontend", "HTML, CSS, JavaScript"],
            ["Bases de Donn\u00e9es", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB"],
            ["Serveurs/Environnements", "Docker, Kubernetes, Linux, Windows Server, Apache"],
            ["Cloud/Infrastructure", "Terraform, AWS (S3, Amplify, CloudFront), OIDC, FinOps/Budgets, CI/CD (GitHub Actions/GitLab CI)"],
            ["Observabilit\u00e9", "Prometheus, Grafana"],
            ["Qualit\u00e9/S\u00e9curit\u00e9", "Hardening, secret scanning (Gitleaks, TruffleHog), anti-injection, Trivy, pip-audit"],
            ["R\u00e9silience", "Circuit breakers, Idempotency"],
            ["IA/Automatisation", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"],
            ["DX", "Hub CLI, doctor/smoke tests"],
        ],
        "style_title": "Style de Travail",
        "style": [
            "Orient\u00e9 solutions et d\u00e9tails",
            "Responsable et engag\u00e9",
            "Bonne communication avec les \u00e9quipes non techniques",
            "Apprentissage continu",
        ],
        "obj_title": "Objectif Actuel",
        "obj": "Int\u00e9grer une \u00e9quipe o\u00f9 je puisse apporter mon exp\u00e9rience en modernisation de syst\u00e8mes, d\u00e9veloppement full-stack et gestion de plateformes, en contribuant \u00e0 des projets \u00e0 fort impact ax\u00e9s sur la qualit\u00e9, la r\u00e9silience et l\u2019am\u00e9lioration continue.",
        "ref_title": "R\u00e9f\u00e9rences Professionnelles",
        "ref_name": "Jean Claude Dupry",
        "ref_role": "Ancien responsable direct",
        "ref_mobile": "T\u00e9l\u00e9phone : +56 9 9415 6984",
        "footer": "Portfolio Professionnel \u2014 Page",
    }

    # ──────────────────── CHINESE (Simplified) ───────
    T["zh"] = {
        "subtitle": "解决方案架构师 | 高级全栈开发 | 现代化、自动化与应用AI",
        "contact_labels": {
            "email": "\u7535\u5b50\u90ae\u4ef6", "linkedin": "LinkedIn", "web": "\u4f5c\u54c1\u96c6\u7f51\u7ad9",
            "github": "GitHub", "gitlab": "GitLab", "country": "\u56fd\u5bb6",
        },
        "intro_title": "\u4e13\u4e1a\u4ecb\u7ecd",
        "intro": [
            "\u8ba1\u7b97\u673a\u79d1\u5b66\u5de5\u7a0b\u4e13\u4e1a\u6bd5\u4e1a\uff0c\u62e5\u6709\u8d85\u8fc716\u5e74\u4e3a\u516c\u5171\u548c\u79c1\u8425\u7ec4\u7ec7\u5f00\u53d1\u3001\u7ef4\u62a4\u548c\u73b0\u4ee3\u5316Web\u89e3\u51b3\u65b9\u6848\u7684\u7ecf\u9a8c\u3002\u4e13\u6ce8\u4e8e\u5173\u952e\u4efb\u52a1\u7cfb\u7edf\u3001\u590d\u6742\u5e73\u53f0\u3001\u8fd0\u8425\u8fde\u7eed\u6027\u3001\u6570\u636e\u8d28\u91cf\u548c\u6027\u80fd\u3002",
            "\u8fc7\u53bb14\u5e74\u4e13\u6ce8\u4e8e\u6559\u80b2/\u5fc3\u7406\u6d4b\u91cf\u5e73\u53f0\u7684\u8bbe\u8ba1\u3001\u5f00\u53d1\u548c\u6f14\u8fdb\u3002\u7ed3\u5408\u540e\u7aef\u3001\u524d\u7aef\u3001\u6570\u636e\u5e93\u3001\u9ad8\u7ea7\u62a5\u544a\uff0c\u4ee5\u53ca\u6700\u8fd1\u7684\u81ea\u52a8\u5316\u548c\u667a\u80fdAI\uff0c\u4e13\u6ce8\u4e8e\u97e7\u6027\u548c\u53ef\u89c2\u6d4b\u6027\u3002",
            "\u4e13\u4e1a\u6807\u5fd7\uff1a\u6e10\u8fdb\u5f0f\u73b0\u4ee3\u5316\u2014\u2014\u63a5\u7ba1\u590d\u6742\u7684\u9057\u7559\u7cfb\u7edf\uff0c\u6df1\u5165\u7406\u89e3\u5b83\u4eec\uff0c\u5e76\u5229\u7528\u9ad8\u7ea7\u53ef\u89c2\u6d4b\u6027\u3001\u5de5\u4e1a\u7ea7\u97e7\u6027\u3001\u4e91\u539f\u751f\u67b6\u6784\uff08DevOps/FinOps\uff09\u5c06\u5176\u6f14\u8fdb\u5230\u73b0\u4ee3\u3001\u7a33\u5b9a\u3001\u53ef\u6269\u5c55\u7684\u72b6\u6001\uff0c\u59cb\u7ec8\u786e\u4fdd\u8fd0\u8425\u8fde\u7eed\u6027\u3002",
        ],
        "vp_title": "\u4ef7\u503c\u4e3b\u5f20",
        "vp": [
            "\u9057\u7559\u7cfb\u7edf\u73b0\u4ee3\u5316\uff08PHP 5.x \u2192 PHP 8.x\uff0c\u89e3\u8026\u67b6\u6784\uff09",
            "\u590d\u6742Web\u5e73\u53f0\u7684\u8bbe\u8ba1/\u7ef4\u62a4\uff08\u591a\u6a21\u5757\u3001\u5927\u6570\u636e\u91cf\u3001\u4e0e\u94f6\u884c/\u652f\u4ed8/\u653f\u5e9c\u7684\u96c6\u6210\uff09",
            "\u4f18\u5316\u3001\u53ef\u89c2\u6d4b\u6027\u3001\u53ef\u6269\u5c55\u6027\uff08SQL\u8c03\u4f18\u3001Prometheus/Grafana\u4eea\u8868\u677f\uff09",
            "\u81ea\u52a8\u5316\u3001\u5206\u6790\u3001AI\uff08PDF/Excel\u62a5\u544a\u3001\u6307\u6807\u3001\u667a\u80fdAI\u539f\u578b\uff09",
            "\u4e91\u548c\u6cbb\u7406/FinOps\uff08Terraform\u3001OIDC\u3001AWS Budgets\uff09",
            "\u5f00\u53d1\u8005\u4f53\u9a8c/DX\uff08Docker Labs\u3001Hub CLI\u3001doctor/smoke tests\uff09",
            "\u5168\u5c40\u4e1a\u52a1\u89c6\u89d2\uff08\u8425\u9500\u3001\u7ba1\u7406\u3001\u8d22\u52a1\u7814\u7a76\uff09",
        ],
        "projects_title": "\u5f53\u524d\u9879\u76ee\u548c\u5173\u6ce8\u70b9\uff08\u516c\u5f00\u4f5c\u54c1\u96c6\uff09",
        "projects_intro": "\u5c55\u793a\u5f53\u524d\u80fd\u529b\u7684\u516c\u5f00\u4ed3\u5e93\uff1a",
        "projects": [
            "<b>\u5f39\u6027\u67b6\u6784\u548c\u4e0d\u53ef\u53d8\u57fa\u7840\u8bbe\u65bd\uff1a</b>CI/CD\u4e0eGitHub Actions/OIDC\u3001Terraform\u3001FinOps/AWS Budgets",
            "<b>\u53ef\u89c2\u6d4b\u6027\u548cDX\uff1a</b>Docker Labs\u4e0ePrometheus/Grafana\u3001\u5fae\u7cfb\u7edf\uff08Hub CLI\uff09\u3001doctor/smoke tests",
            "<b>\u667a\u80fdAI\uff1a</b>LangGraph + Ollama\uff08\u672c\u5730AI\uff09\u3001\u6709\u72b6\u6001\u4ee3\u7406\u3001\u6761\u4ef6\u8def\u7531",
            "<b>Social Bot Scheduler\uff1a</b>9\u8f74\u96c6\u6210\u77e9\u9635\u30019\u4e2a\u6570\u636e\u5e93\u5f15\u64ce\u3001n8n\u7f16\u6392\u3001Prometheus/Grafana",
            "<b>MCP + Ollama\u672c\u5730\uff1a</b>\u672c\u5730AI\u804a\u5929\u3001MCP\u5de5\u5177\u3001100%\u79c1\u5bc6",
            "<b>Unikernel Labs\uff1a</b>Windows\u63a7\u5236\u4e2d\u5fc3 \u2014 WSL2 + Node.js + WinForms\uff0cUnikraft\u670d\u52a1",
            "<b>ChofyAI Studio\uff1a</b>macOS\u672c\u5730AI\u542f\u52a8\u5668 \u2014 Tauri + Rust + React\uff0cApple Silicon",
        ],
        "project_links_title": "\u9879\u76ee\u94fe\u63a5",
        "project_link_labels": {
            "cloud_gh": "Cloud/AWS (GitHub)", "cloud_gl": "Cloud/AWS (GitLab)",
            "micro": "\u5fae\u7cfb\u7edf", "social": "Social Bot Scheduler",
            "docker": "Docker Labs", "langgraph": "LangGraph",
            "mcp": "MCP + Ollama",
            "unikernel": "Unikernel Labs",
            "chofyai": "ChofyAI Studio",
        },
        "exp_title": "\u76f8\u5173\u7ecf\u9a8c",
        "exp_main_org": "\u6559\u80b2/\u5fc3\u7406\u6d4b\u91cf\u5e73\u53f0 (2011\u20132025)",
        "exp_main": [
            "<b>\u89d2\u8272\uff1a</b>\u9ad8\u7ea7\u5f00\u53d1\u4eba\u5458 / \u8f6f\u4ef6\u67b6\u6784\u5e08\uff08\u5b9e\u9645\uff09",
            "<b>\u8303\u56f4\uff1a</b>\u6559\u80b2\u57fa\u91d1\u4f1a\uff1b\u4e3a\u5b66\u6821\u548c\u6307\u5bfc\u56e2\u961f\u63d0\u4f9b\u89e3\u51b3\u65b9\u6848",
            "\u8bbe\u8ba1\u3001\u5f00\u53d1\u548c\u7ef4\u62a4\u5b66\u751f\u8bc4\u4f30Web\u5e73\u53f0",
            "\u6280\u672f\u8fc1\u79fb\uff1aPHP 5.4 \u2192 PHP 8.2+\uff0cJS\u8fc1\u79fb\u4ee5\u63d0\u9ad8\u6027\u80fd",
            "\u9ad8\u7ea7\u62a5\u544a\u6a21\u5757\uff1aPDF\u3001\u56fe\u8868\u3001\u5e26\u5fc3\u7406\u6d4b\u91cf\u6307\u6807\u7684Excel",
            "\u4eceExcel\u5bfc\u5165/\u8fc1\u79fb\u6570\u636e\u5e76\u8fdb\u884c\u9a8c\u8bc1",
            "\u901a\u4fe1\u81ea\u52a8\u5316\uff1a\u5927\u89c4\u6a21\u90ae\u4ef6\uff08SMTP\u3001Constant Contact\uff09\u3001\u7ec6\u5206",
            "\u9ad8\u7ea7\u7528\u6237\u652f\u6301",
            "<b>\u6280\u672f\uff1a</b>PHP 5/8\u3001JavaScript\u3001jQuery\u3001HTML\u3001CSS\u3001SQL Server\u3001MySQL\u3001Apache\u3001Linux\u3001LimeSurvey\u3001JMeter",
        ],
        "exp_prev_title": "\u4ee5\u5f80\u7ecf\u9a8c",
        "exp_prev": [
            "<b>\u653f\u5e9c (CONACE)\uff1a</b>\u4eba\u529b\u8d44\u6e90\u7cfb\u7edf\u3001\u91c7\u8d2d\u3001\u5e93\u5b58\u3001PDF/Excel\u62a5\u544a\u3001\u5b89\u5168\u6a21\u5757",
            "<b>\u91d1\u878d/\u652f\u4ed8 (Transbank, PointPay, Corpvida)\uff1a</b>GSET\u7cfb\u7edf\u3001\u8ba1\u8d39\u3001SQL Server/Oracle\u3001VB6 COM\u3001Crystal Reports",
            "<b>\u4e3a\u5404\u79cd\u7ec4\u7ec7\u8fdb\u884cWeb\u5f00\u53d1 (Giro Ingenier\u00eda, \u9152\u5e97, \u5b66\u6821)\uff1a</b>\u52a8\u6001/\u9759\u6001\u7f51\u7ad9\u3001\u5185\u8054\u7f51\u3001\u8c03\u67e5\u3001\u6559\u80b2\u73af\u5883",
        ],
        "edu_title": "\u6559\u80b2\u80cc\u666f",
        "edu": [
            "\u8ba1\u7b97\u673a\u79d1\u5b66\u5de5\u7a0b\uff0cUniversidad de Tarapac\u00e1\uff0cArica",
            "\u4f01\u4e1a\u7ba1\u7406\u6280\u672f\u5458\uff08\u8425\u9500\uff09\uff0cINACAP\uff08SAP\u7528\u6237\u8ba4\u8bc1\uff09",
            "\u5404\u79cd\u8bfe\u7a0b\uff1aJ2EE\u3001\u79fb\u52a8Web\u3001\u7f51\u7edc\u5b89\u5168",
        ],
        "tech_title": "\u6280\u672f\u80fd\u529b",
        "tech_header": ["\u7c7b\u522b", "\u6280\u672f / \u5de5\u5177"],
        "tech_rows": [
            ["\u540e\u7aef", "PHP (4/5/8.x), JavaScript/Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby"],
            ["\u524d\u7aef", "HTML, CSS, JavaScript"],
            ["\u6570\u636e\u5e93", "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB"],
            ["\u670d\u52a1\u5668/\u73af\u5883", "Docker, Kubernetes, Linux, Windows Server, Apache"],
            ["\u4e91/\u57fa\u7840\u8bbe\u65bd", "Terraform, AWS (S3, Amplify, CloudFront), OIDC, FinOps/Budgets, CI/CD (GitHub Actions/GitLab CI)"],
            ["\u53ef\u89c2\u6d4b\u6027", "Prometheus, Grafana"],
            ["\u8d28\u91cf/\u5b89\u5168", "Hardening, secret scanning (Gitleaks, TruffleHog), \u53cd\u6ce8\u5165, Trivy, pip-audit"],
            ["\u97e7\u6027", "Circuit breakers, Idempotency"],
            ["AI/\u81ea\u52a8\u5316", "LangGraph, MCP (Model Context Protocol), Ollama, n8n"],
            ["DX", "Hub CLI, doctor/smoke tests"],
        ],
        "style_title": "\u5de5\u4f5c\u98ce\u683c",
        "style": [
            "\u4ee5\u89e3\u51b3\u65b9\u6848\u548c\u7ec6\u8282\u4e3a\u5bfc\u5411",
            "\u8d1f\u8d23\u4e14\u6295\u5165",
            "\u4e0e\u975e\u6280\u672f\u56e2\u961f\u826f\u597d\u6c9f\u901a",
            "\u6301\u7eed\u5b66\u4e60",
        ],
        "obj_title": "\u5f53\u524d\u76ee\u6807",
        "obj": "\u52a0\u5165\u4e00\u4e2a\u56e2\u961f\uff0c\u8d21\u732e\u6211\u5728\u7cfb\u7edf\u73b0\u4ee3\u5316\u3001\u5168\u6808\u5f00\u53d1\u548c\u5e73\u53f0\u8fd0\u8425\u65b9\u9762\u7684\u7ecf\u9a8c\uff0c\u4e3a\u4ee5\u8d28\u91cf\u3001\u97e7\u6027\u548c\u6301\u7eed\u6539\u8fdb\u4e3a\u91cd\u70b9\u7684\u9ad8\u5f71\u54cd\u529b\u9879\u76ee\u505a\u51fa\u8d21\u732e\u3002",
        "ref_title": "\u4e13\u4e1a\u53c2\u8003",
        "ref_name": "Jean Claude Dupry",
        "ref_role": "\u524d\u76f4\u5c5e\u7ecf\u7406",
        "ref_mobile": "\u624b\u673a\uff1a+56 9 9415 6984",
        "footer": "\u4e13\u4e1a\u4f5c\u54c1\u96c6 \u2014 \u7b2c",
    }

    return T[lang]


# ═══════════════════════════════════════════════════════
# PDF BUILDER
# ═══════════════════════════════════════════════════════

LANG_SUFFIX = {
    "es": "", "en": "-english", "pt": "-portuguese",
    "it": "-italian", "fr": "-french", "zh": "-chinese",
}


class PortfolioDoc(SimpleDocTemplate):
    """Custom doc with page footer."""
    def __init__(self, *args, footer_label="", lang="es", **kwargs):
        self._footer_label = footer_label
        self._lang = lang
        super().__init__(*args, **kwargs)

    def afterPage(self):
        c = self.canv
        page_num = c.getPageNumber()
        c.saveState()
        font = _font(self._lang, False)
        c.setFont(font, 8.5)
        c.setFillColor(MUTED)
        c.drawRightString(
            PAGE_W - MARGIN, 0.45 * inch,
            f"{self._footer_label} {page_num}"
        )
        c.restoreState()


def build_portfolio(lang):
    T = get_content(lang)
    s = make_styles(lang)
    suffix = LANG_SUFFIX[lang]
    filename = f"portafolio{suffix}.pdf"
    output_path = os.path.join(ASSETS_DIR, filename)

    doc = PortfolioDoc(
        output_path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=0.6 * inch, bottomMargin=0.7 * inch,
        footer_label=T["footer"],
        lang=lang,
    )

    story = []
    usable_w = PAGE_W - 2 * MARGIN

    # ════════════════ PAGE 1 ════════════════

    # ── Name & subtitle ──
    story.append(Paragraph("Vladimir Bernardo Acu\u00f1a Valdebenito", s["name"]))
    story.append(Paragraph(T["subtitle"], s["subtitle"]))
    story.append(hr())

    # ── Contact ──
    cl = T["contact_labels"]
    contact_items = [
        f'{cl["email"]}: {CONTACT["email"]}',
        f'{cl["linkedin"]}: <link href="https://www.{CONTACT["linkedin"]}">{CONTACT["linkedin"]}</link>',
        f'{cl["web"]}: <link href="{CONTACT["web"]}">{CONTACT["web"]}</link>',
        f'{cl["github"]}: <link href="{CONTACT["github"]}">{CONTACT["github"]}</link>',
        f'{cl["gitlab"]}: <link href="{CONTACT["gitlab"]}">{CONTACT["gitlab"]}</link>',
        f'{cl["country"]}: {CONTACT["country"]}',
    ]
    for ci in contact_items:
        story.append(Paragraph(f"\u2022  {ci}", s["contact"]))
    story.append(Spacer(1, 4))

    # ── Introduction ──
    story.append(Paragraph(f"<b>{T['intro_title']}</b>", s["heading"]))
    story.append(hr())
    for p in T["intro"]:
        story.append(Paragraph(p, s["body"]))
    story.append(Spacer(1, 4))

    # ── Value Proposition ──
    story.append(Paragraph(f"<b>{T['vp_title']}</b>", s["heading"]))
    story.append(hr())
    for v in T["vp"]:
        story.append(bullet_p(s["bullet"], v))

    # ════════════════ PAGE 2 ════════════════

    # ── Current Projects ──
    story.append(Paragraph(f"<b>{T['projects_title']}</b>", s["heading"]))
    story.append(hr())
    story.append(Paragraph(T["projects_intro"], s["body"]))
    for p in T["projects"]:
        story.append(bullet_p(s["bullet"], p))
    story.append(Spacer(1, 4))

    # ── Project Links ──
    story.append(Paragraph(f"<b>{T['project_links_title']}</b>", s["subheading"]))
    pll = T["project_link_labels"]
    for key in ["cloud_gh", "cloud_gl", "micro", "social", "docker", "langgraph", "mcp"]:
        url = PROJECT_LINKS[key]
        label = pll[key]
        story.append(Paragraph(
            f'\u2022  {label}: <link href="{url}">{url}</link>', s["link"]
        ))
    story.append(Spacer(1, 6))

    # ── Relevant Experience ──
    story.append(Paragraph(f"<b>{T['exp_title']}</b>", s["heading"]))
    story.append(hr())
    story.append(Paragraph(f"<b>{T['exp_main_org']}</b>", s["subheading"]))
    for item in T["exp_main"]:
        story.append(bullet_p(s["bullet"], item))

    # ════════════════ PAGE 3 ════════════════

    # ── Previous Experience ──
    story.append(Paragraph(f"<b>{T['exp_prev_title']}</b>", s["heading"]))
    story.append(hr())
    for item in T["exp_prev"]:
        story.append(bullet_p(s["bullet"], item))
    story.append(Spacer(1, 4))

    # ── Education ──
    story.append(Paragraph(f"<b>{T['edu_title']}</b>", s["heading"]))
    story.append(hr())
    for item in T["edu"]:
        story.append(bullet_p(s["bullet"], item))
    story.append(Spacer(1, 4))

    # ── Technical Competencies Table ──
    story.append(Paragraph(f"<b>{T['tech_title']}</b>", s["heading"]))
    story.append(hr())

    header = T["tech_header"]
    rows = T["tech_rows"]

    table_data = [[
        Paragraph(f"<b>{header[0]}</b>", s["table_header"]),
        Paragraph(f"<b>{header[1]}</b>", s["table_header"]),
    ]]
    for row in rows:
        table_data.append([
            Paragraph(f"<b>{row[0]}</b>", s["table_cell_bold"]),
            Paragraph(row[1], s["table_cell"]),
        ])

    col_w = [usable_w * 0.22, usable_w * 0.78]
    tech_table = Table(table_data, colWidths=col_w, repeatRows=1)
    tech_style = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE_COLOR),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    # Alternating row backgrounds
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            tech_style.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT_BG))
    tech_table.setStyle(TableStyle(tech_style))
    story.append(tech_table)

    # ════════════════ PAGE 4 ════════════════

    # ── Work Style ──
    story.append(Paragraph(f"<b>{T['style_title']}</b>", s["heading"]))
    story.append(hr())
    for item in T["style"]:
        story.append(bullet_p(s["bullet"], item))
    story.append(Spacer(1, 6))

    # ── Objective ──
    story.append(Paragraph(f"<b>{T['obj_title']}</b>", s["heading"]))
    story.append(hr())
    story.append(Paragraph(T["obj"], s["body"]))
    story.append(Spacer(1, 6))

    # ── References ──
    story.append(Paragraph(f"<b>{T['ref_title']}</b>", s["heading"]))
    story.append(hr())
    story.append(Paragraph(f"<b>{T['ref_name']}</b>", s["subheading"]))
    story.append(Paragraph(T["ref_role"], s["body"]))
    story.append(Paragraph(T["ref_mobile"], s["body"]))

    # ── Build ──
    doc.build(story)
    print(f"  [OK] {filename}")
    return output_path


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    print("Generating portfolio PDFs...")
    for lang in ["es", "en", "pt", "it", "fr", "zh"]:
        build_portfolio(lang)
    print("Done. All 6 portfolio PDFs generated.")


if __name__ == "__main__":
    main()
