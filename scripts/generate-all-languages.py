#!/usr/bin/env python3
"""
Generate unified recruiter CVs + standalone ATS CVs for ALL languages.
Languages: ES, EN, PT, IT, FR, ZH
Outputs:
  - cv-reclutador.pdf (ES unified)
  - cv-reclutador-english.pdf (EN unified)
  - cv-reclutador-portuguese.pdf (PT unified)
  - cv-reclutador-italian.pdf (IT unified)
  - cv-reclutador-french.pdf (FR unified)
  - cv-reclutador-chinese.pdf (ZH unified)
  - cv-ats.pdf (ES standalone)
  - cv-ats-english.pdf (EN standalone)
  - cv-ats-portuguese.pdf (PT standalone)
  - cv-ats-italian.pdf (IT standalone)
  - cv-ats-french.pdf (FR standalone)
  - cv-ats-chinese.pdf (ZH standalone)
"""

import os, sys

# Add parent to path so we can import the other scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "assets"))

# We reuse the unified CV engine
sys.path.insert(0, SCRIPT_DIR)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, Frame, PageTemplate,
    BaseDocTemplate, FrameBreak, NextPageTemplate, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

PAGE_W, PAGE_H = letter
SIDEBAR_W = 2.4 * inch
MAIN_W = PAGE_W - SIDEBAR_W
HEADER_H = 1.15 * inch
MARGIN = 0.35 * inch
SIDEBAR_PAD = 0.25 * inch

# ═══════════════════════════════════════════════════
# SHARED DATA (common across languages)
# ═══════════════════════════════════════════════════

CONTACT_LINES = [
    "Santiago, Chile",
    "+56 9 8121 8838",
    "vladimir.acuna.dev@gmail.com",
]

CONTACT_LINKS_LABELS = {
    "es": "Sitio web / portafolio",
    "en": "Website / portfolio",
    "pt": "Site / portf\u00f3lio",
    "it": "Sito web / portfolio",
    "fr": "Site web / portfolio",
    "zh": "\u7f51\u7ad9 / \u4f5c\u54c1\u96c6",
}

GITHUB_URL = "https://github.com/vladimiracunadev-create"
GITLAB_URL = "https://gitlab.com/vladimir.acuna.dev-group"
LINKEDIN_URL = "https://www.linkedin.com/in/vladimir-acuna-valdebenito"
WEB_URL = "https://vladimiracunadev-create.github.io/"

PROJECTS_URLS = {
    "aws_gh": "https://github.com/vladimiracunadev-create/proyectos-aws",
    "aws_gl": "https://gitlab.com/vladimir.acuna.dev-group/proyectos-aws-gitlab",
    "micro": "https://github.com/vladimiracunadev-create/microsistemas",
    "social": "https://github.com/vladimiracunadev-create/social-bot-scheduler",
    "docker": "https://github.com/vladimiracunadev-create/docker-labs",
    "langgraph": "https://github.com/vladimiracunadev-create/langgraph-realworld",
    "mcp": "https://github.com/vladimiracunadev-create/mcp-ollama-local",
    "unikernel": "https://github.com/vladimiracunadev-create/unikernel-labs",
    "chofyai": "https://github.com/vladimiracunadev-create/chofyai-studio",
    "problem": "https://github.com/vladimiracunadev-create/problem-driven-systems-lab",
    "python": "https://github.com/vladimiracunadev-create/python-data-science-program",
    "claude": "https://github.com/vladimiracunadev-create/claude-skills-toolkit",
    "gabysql": "https://github.com/vladimiracunadev-create/gabysql",
    "automa": "https://github.com/vladimiracunadev-create/automa-pc",
    "rootcause": "https://github.com/vladimiracunadev-create/rootcause-windows-inspector",
    "modern": "https://github.com/vladimiracunadev-create/modern-gamedev-program",
    "machine": "https://github.com/vladimiracunadev-create/machine-operator-program",
    "rhino": "https://github.com/vladimiracunadev-create/rhino-suite",
    "human": "https://github.com/vladimiracunadev-create/human-genome-labs",
    "wsl": "https://github.com/vladimiracunadev-create/wsl-labs",
    "computational": "https://github.com/vladimiracunadev-create/computational-mathematics-program",
    "executive": "https://github.com/vladimiracunadev-create/executive-leadership-founder-program",
    "finance": "https://github.com/vladimiracunadev-create/finance-and-banking-evolution-program",
    "blockchain": "https://github.com/vladimiracunadev-create/blockchain-learning-path",
    "universal": "https://github.com/vladimiracunadev-create/universal-code-scanner",
    "sandbox": "https://github.com/vladimiracunadev-create/sandbox-labs",
    "artificial": "https://github.com/vladimiracunadev-create/artificial-intelligence-evolution-program",
    "violin": "https://github.com/vladimiracunadev-create/violin-adventure",
    "multi": "https://github.com/vladimiracunadev-create/multi-cloud-engineering-program",
    "neural": "https://github.com/vladimiracunadev-create/neural-network-training-labs",
    "polyglot": "https://github.com/vladimiracunadev-create/polyglot-programming-labs",
    "rootcause_mobile": "https://github.com/vladimiracunadev-create/rootcause-mobile-inspector",
    "rootcause_web": "https://github.com/vladimiracunadev-create/rootcause-web-inspector",
    "modern_business": "https://github.com/vladimiracunadev-create/modern-business-creation-program",
    "modern_cyber": "https://github.com/vladimiracunadev-create/modern-cybersecurity-program",
    "education": "https://github.com/vladimiracunadev-create/education-pedagogy-learning-sciences-program",
    "marketing": "https://github.com/vladimiracunadev-create/marketing-sales-growth-evolution-program",
    "guitarra": "https://github.com/vladimiracunadev-create/guitarra-adventure",
    "agentic": "https://github.com/vladimiracunadev-create/agentic-plugins-toolkit",
    "operational": "https://github.com/vladimiracunadev-create/operational-ai-agents",
    "empresa": "https://github.com/vladimiracunadev-create/empresa-operativa-chile",
    "rootcause_macos": "https://github.com/vladimiracunadev-create/rootcause-macos-inspector",
}

PREVIOUS_CAREER = {
    "es": "CONACE / Gobierno de Chile (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 Centro Europeo para la Capacitaci\u00f3n (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 Amigos Defensores de los Animales (2001-2002)",
    "en": "CONACE / Government of Chile (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 European Training Center (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 Friends Defenders of Animals (2001-2002)",
    "pt": "CONACE / Governo do Chile (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 Centro Europeu de Capacita\u00e7\u00e3o (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 Amigos Defensores dos Animais (2001-2002)",
    "it": "CONACE / Governo del Cile (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 Centro Europeo di Formazione (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 Amici Difensori degli Animali (2001-2002)",
    "fr": "CONACE / Gouvernement du Chili (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 Centre Europ\u00e9en de Formation (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 Amis D\u00e9fenseurs des Animaux (2001-2002)",
    "zh": "CONACE / \u667a\u5229\u653f\u5e9c (2008-2011) \u00b7 E-syste (2011) \u00b7 Corpvida / Servytech (2007-2008) \u00b7 PointPay Chile (2006-2007) \u00b7 Giro Ingenier\u00eda Ltda. (2004-2006) \u00b7 \u6b27\u6d32\u57f9\u8bad\u4e2d\u5fc3 (2003-2004) \u00b7 Busquesbc (2003) \u00b7 Sygnum Consultores (2003) \u00b7 Golden Guide Chile (2003) \u00b7 \u52a8\u7269\u4fdd\u62a4\u4e4b\u53cb (2001-2002)",
}

# ═══════════════════════════════════════════════════
# LANGUAGE CONTENT
# ═══════════════════════════════════════════════════

def get_content(lang):
    """Return all content for a given language."""

    T = {
        "es": {
            "subtitle_rec": "Arquitecto de Soluciones | Senior Full-Stack | Modernización, Automatización e IA Aplicada",
            "subtitle_ats": "Arquitecto de Soluciones | Senior Full-Stack | Modernización, Automatización e IA Aplicada",
            "h_contact": "CONTACTO", "h_skills": "SKILLS", "h_education": "EDUCACI\u00d3N",
            "h_languages": "IDIOMAS", "h_summary": "RESUMEN", "h_experience": "EXPERIENCIA DESTACADA",
            "h_previous": "TRAYECTORIA PREVIA (S\u00cdNTESIS)", "h_projects": "PROYECTOS DESTACADOS",
            "h_training": "FORMACI\u00d3N Y ACTIVIDAD RECIENTE", "h_notes": "NOTAS",
            "h_ats_experience": "EXPERIENCIA", "h_ats_education": "FORMACI\u00d3N Y ACTIVIDAD RECIENTE",
            "h_degrees": "EDUCACI\u00d3N",
            "exp_title_rec": "Fundaci\u00f3n CEIS Maristas \u2014 Arquitecto de Software \u00b7 Analista y Desarrollador Full-Stack",
            "exp_title_ats": "Fundaci\u00f3n CEIS Maristas \u2014 Arquitecto de Software y Desarrollador Full-Stack (2011-2025)",
            "summary": [
                "14 a\u00f1os de experiencia principal en Fundaci\u00f3n CEIS Maristas (2011-2025), desarrollando, manteniendo y modernizando una plataforma educativa/psicom\u00e9trica.",
                "Experiencia previa en desarrollo web y soporte de sistemas para instituciones p\u00fablicas y privadas, con foco en PHP, SQL Server/MySQL, reporter\u00eda PDF/Excel, migraci\u00f3n de datos e integraciones.",
                "Portafolio t\u00e9cnico actual con proyectos y laboratorios en Docker, AWS, CI/CD, observabilidad e IA aplicada a automatizaci\u00f3n, publicados en GitHub y GitLab.",
            ],
            "ats_summary": [
                "14 a\u00f1os liderando el dise\u00f1o, evoluci\u00f3n y operaci\u00f3n de una plataforma educativa/psicom\u00e9trica (2011-2025), con foco en continuidad operacional.",
                "Modernizaci\u00f3n progresiva (PHP 5.4 \u2192 PHP 8.2+), optimizaci\u00f3n de rendimiento y automatizaci\u00f3n de reportes (PDF/Excel) y procesos de datos.",
                "Experiencia en bases de datos (SQL Server, MySQL/MariaDB) y despliegues/entornos reproducibles con Docker y CI/CD.",
                "Portafolio t\u00e9cnico con casos pr\u00e1cticos (Cloud/AWS, microsistemas, agentes IA y observabilidad), documentaci\u00f3n y demos verificables en GitHub y GitLab.",
            ],
            "experience": [
                "Suite de evaluación educacional/psicométrica: <b>PCA</b> (aprendizaje), <b>Baterías Psicoeducativas</b> (desarrollo social/personal) y <b>Batería Online</b> (plataforma online), más mailing institucional, LimeSurvey y WordPress.",
                "<b>Métricas verificadas</b>: 80% mejora en reportes/carga de Batería Online · 90% menos fricción en atención a clientes (2020-2025) · 45% optimización DB/código · hasta 5 frentes concurrentes en ciertos períodos.",
                "<b>Pandemia 2020</b>: migración de servicios presenciales a formato online en tiempo breve (citado en la carta de recomendación).",
                "Modernización PHP 5.4 → 8.2+, refactor de módulos críticos, traslado de lógica a JavaScript y eliminación de duplicidades en DB.",
                "Mailing masivo (PHP + Constant Contact) y <b>adopción interna de IA (2024-2025)</b> para análisis y resolución de problemas técnicos.",
            ],
            "ats_experience": [
                "Diseño, desarrollo y mantención de plataforma de evaluación de alumnos (baterías de test), módulos institucionales y reportes.",
                "Migración tecnológica (PHP 5.4 → PHP 8.2+), actualización de servidores/librerías y mejoras de rendimiento con JavaScript y pruebas de carga.",
                "Desarrollo de reportes avanzados PDF/Excel con indicadores, percentiles y análisis por curso/nivel/establecimiento.",
                "Importación y migración de datos masivos desde Excel con validaciones; automatización de comunicaciones (envíos, segmentación, seguimiento).",
                "Soporte directo a usuarios clave (coordinadores, orientadores, directivos) y operación en producción.",
            ],
            "exp_tech": "Tecnolog\u00edas: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
            "exp_logros_label": "M\u00e9tricas y logros cuantificados del periodo CEIS Maristas",
            "projects_rec": [
                "Cloud/AWS y FinOps — GitHub + GitLab (16 casos AWS A–P, CI/CD 5 stages)",
                "Microsistemas — suite de 11 micro-apps, Hub CLI, MCP server",
                "Social Bot Scheduler — matriz 9 ejes, 18+ motores DB, n8n, Prometheus/Grafana",
                "Docker Labs — 12 labs, Control Center, instalador Windows",
                "LangGraph — 25/25 backends operativos (v4.15, cobertura 100%), Docker por caso, agentes con estado",
                "MCP + Ollama local — chat IA local, herramientas MCP, 100% privado",
                "Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms)",
                "ChofyAI Studio — lanzador IA local macOS (Tauri + Rust + React)",
                "Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable",
                "Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform",
                "Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge",
                "Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones",
                "Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright (headless/visible), pywebview + PyInstaller, SQLite, OCR, uv, 150 pytest tests, instalador firmado",
                "RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust (edition 2024): ETW + WPR, 5 ediciones (GUI Setup.exe, Portable .zip, CLI single-binary rootcause.exe, PowerShell .psm1, VS Code .vsix), SHA256SUMS por release",
                "Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build",
                "Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal",
                "Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura",
                "Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad",
                "Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases",
                "Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego",
                "Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop",
                "Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF",
                "Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF",
                "Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas",
                "Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase",
                "Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline",
                "Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero",
                "Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad",
                "Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera",
                "Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter)",
                "Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases",
                "Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA",
                "Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13",
                "Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje",
                            "Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱",
                "Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱",
                "Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases",
                "Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps",
                "Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform",
                "Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱",
                "Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile",
],
            "projects_ats": [
                ("Cloud/AWS y FinOps — GitHub (demos y documentación):", "aws_gh"),
                ("Cloud/AWS — GitLab (15 casos, CI/CD 5 stages, ~80% SAA-C03):", "aws_gl"),
                ("Microsistemas (suite de 11 micro-apps, Hub CLI, MCP server):", "micro"),
                ("Social Bot Scheduler (matriz 9 ejes de integración, 18+ motores DB, n8n, Prometheus/Grafana):", "social"),
                ("Docker Labs (12 labs, Control Center, instalador Windows):", "docker"),
                ("LangGraph v4.15 (25/25 backends operativos, cobertura 100%, auditoría 8 capas, Docker por caso):", "langgraph"),
                ("MCP + Ollama local (chat IA local, herramientas MCP, 100% privado):", "mcp"),
                ("Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms):", "unikernel"),
                ("ChofyAI Studio — lanzador IA local macOS (Tauri + Rust + React):", "chofyai"),
                ("Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones:", "python"),
                ("Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright, pywebview + PyInstaller, SQLite, OCR, 150 pytest tests, instalador firmado:", "automa"),
                ("RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust: ETW + WPR, 5 ediciones (Setup.exe, Portable .zip, CLI rootcause.exe, PowerShell .psm1, VS Code .vsix):", "rootcause"),
                ("Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura:", "modern_cyber"),
                ("Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable:", "problem"),
                ("Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform:", "claude"),
                ("Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge:", "gabysql"),
                ("Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build:", "rootcause_mobile"),
                ("Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal:", "modern"),
                ("Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad:", "machine"),
                ("Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases:", "rhino"),
                ("Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego:", "human"),
                ("Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop:", "wsl"),
                ("Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF:", "computational"),
                ("Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas:", "executive"),
                ("Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase:", "finance"),
                ("Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline:", "blockchain"),
                ("Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero:", "universal"),
                ("Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad:", "sandbox"),
                ("Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera:", "artificial"),
                ("Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases:", "violin"),
                ("Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13:", "neural"),
                ("Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje:", "polyglot"),
                ("Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF:", "modern_business"),
                ("Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter):", "rootcause_web"),
                ("Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA:", "multi"),
                            ("Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱:", "education"),
                ("Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱:", "marketing"),
                ("Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases:", "guitarra"),
                ("Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps:", "agentic"),
                ("Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform:", "operational"),
                ("Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱:", "empresa"),
                ("Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile:", "rootcause_macos"),
],
            "training": [
                "Formaci\u00f3n continua en automatizaci\u00f3n pr\u00e1ctica, ML/NLP y herramientas de desarrollo.",
                "Consolidaci\u00f3n de portafolio t\u00e9cnico con laboratorios cloud, microsistemas y documentaci\u00f3n orientada a reclutadores.",
            ],
            "notes": [
                "Carta de recomendaci\u00f3n disponible.",
                "Si el proceso usa ATS, favor considerar el CV ATS de la p\u00e1gina web:",
            ],
            "skills_labels": ["<b>Backend:</b>", "<b>Frontend:</b>", "<b>Datos:</b>", "<b>DevOps/Cloud:</b>", "<b>Calidad/Seguridad:</b>", "<b>Observabilidad:</b>", "<b>IA/Agentes:</b>"],
            "degrees": [
                ("Ingenier\u00eda de Ejecuci\u00f3n en Computaci\u00f3n e Inform\u00e1tica", "Universidad de Tarapac\u00e1 (Arica)"),
                ("T\u00e9cnico de Administraci\u00f3n de Empresas (Menci\u00f3n Marketing)", "INACAP (Santiago)"),
            ],
            "language_skill": "Ingl\u00e9s t\u00e9cnico: lectura fluida (documentaci\u00f3n, c\u00f3digo, papers, IA tooling). Conversaci\u00f3n: b\u00e1sica, en mejora activa.",
            "transition_title": "Versi\u00f3n optimizada para ATS",
            "transition_body": "A continuaci\u00f3n se incluye una versi\u00f3n del curr\u00edculum optimizada para sistemas de seguimiento de candidatos (ATS).",
            "transition_reasons": [
                "Los procesos de selecci\u00f3n actuales frecuentemente utilizan inteligencia artificial y filtros autom\u00e1ticos para evaluar curr\u00edculums antes de que lleguen a un reclutador humano.",
                "El formato de columna \u00fanica y texto plano de la siguiente p\u00e1gina est\u00e1 dise\u00f1ado para ser le\u00eddo correctamente por estos sistemas, maximizando la compatibilidad con parsers ATS.",
                "El contenido es el mismo \u2014 solo cambia la presentaci\u00f3n para garantizar que ninguna informaci\u00f3n se pierda en el procesamiento autom\u00e1tico.",
            ],
            "transition_footer": "La p\u00e1gina anterior es para lectura humana. Las siguientes son para procesamiento autom\u00e1tico.",
        },
        "en": {
            "subtitle_rec": "Solutions Architect | Senior Full-Stack | Modernization, Automation & Applied AI",
            "subtitle_ats": "Solutions Architect | Senior Full-Stack | Modernization, Automation & Applied AI",
            "h_contact": "CONTACT", "h_skills": "SKILLS", "h_education": "EDUCATION",
            "h_languages": "LANGUAGES", "h_summary": "SUMMARY", "h_experience": "HIGHLIGHTED EXPERIENCE",
            "h_previous": "PREVIOUS CAREER (SUMMARY)", "h_projects": "SELECTED PROJECTS",
            "h_training": "RECENT TRAINING AND PROJECTS", "h_notes": "NOTES",
            "h_ats_experience": "EXPERIENCE", "h_ats_education": "EDUCATION & RECENT ACTIVITY",
            "h_degrees": "EDUCATION",
            "exp_title_rec": "Fundaci\u00f3n CEIS Maristas \u2014 Software Architect \u00b7 Systems Analyst & Full-Stack Developer",
            "exp_title_ats": "Fundaci\u00f3n CEIS Maristas \u2014 Software Architect and Full-Stack Developer (2011-2025)",
            "summary": [
                "14 years of core experience at Fundaci\u00f3n CEIS Maristas (2011-2025), developing, maintaining, and modernizing an educational/psychometric platform.",
                "Previous experience in web development and systems support for public and private institutions, focused on PHP, SQL Server/MySQL, PDF/Excel reporting, data migration, and integrations.",
                "Current technical portfolio with projects and labs in Docker, AWS, CI/CD, observability, and AI applied to automation, published on GitHub and GitLab.",
            ],
            "ats_summary": [
                "14 years leading the design, evolution, and operation of an educational/psychometric platform (2011-2025), with a strong focus on operational continuity.",
                "Progressive modernization (PHP 5.4 \u2192 PHP 8.2+), performance optimization, and automation of PDF/Excel reports and data processes.",
                "Experience with databases (SQL Server, MySQL/MariaDB) and reproducible deployments/environments using Docker and CI/CD.",
                "Technical portfolio with practical cases (Cloud/AWS, microsystems, AI agents, and observability), documentation, and verifiable demos on GitHub and GitLab.",
            ],
            "experience": [
                "Educational/psychometric assessment suite: <b>PCA</b> (learning), <b>Baterías Psicoeducativas</b> (social/personal development) and <b>Batería Online</b> (online platform), plus institutional mailing, LimeSurvey and WordPress.",
                "<b>Verified metrics</b>: 80% improvement in Batería Online reports/load · 90% less friction in client support (2020-2025) · 45% DB/code optimization · up to 5 concurrent workstreams in certain periods.",
                "<b>2020 Pandemic</b>: migration of in-person services to online format in a short timeframe (cited in the recommendation letter).",
                "PHP 5.4 → 8.2+ modernization, refactor of critical modules, logic offloading to JavaScript, and DB duplicate cleanup.",
                "Mass mailing (PHP + Constant Contact) and <b>internal AI adoption (2024-2025)</b> for analysis and technical problem-solving.",
            ],
            "ats_experience": [
                "Design, development, and maintenance of a student assessment platform (test batteries), institutional modules, and reports.",
                "Technology migration (PHP 5.4 → PHP 8.2+), server/library upgrades, and performance improvements with JavaScript and load testing.",
                "Development of advanced PDF/Excel reports with indicators, percentiles, and analysis by class, level, and school.",
                "Import and migration of high-volume data from Excel with validations; automation of communications (sending, segmentation, follow-up).",
                "Direct support for key users (coordinators, counselors, school leaders) and production operations.",
            ],
            "exp_tech": "Technologies: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
            "exp_logros_label": "Quantified metrics and achievements from CEIS Maristas tenure",
            "projects_rec": [
                "Cloud/AWS and FinOps — GitHub + GitLab (16 AWS cases A–P, 5-stage CI/CD)",
                "Microsystems — suite of 11 micro-apps, Hub CLI, MCP server",
                "Social Bot Scheduler — 9-axis integration matrix, 18+ DB engines, n8n, Prometheus/Grafana",
                "Docker Labs — 12 labs, Control Center, Windows installer",
                "LangGraph — 25/25 operational backends (v4.15, 100% coverage), Docker per case, stateful agents",
                "MCP + local Ollama — local AI chat, MCP tools, 100% private",
                "Unikernel Labs — Windows Control Center (WSL2 + Node.js + WinForms)",
                "ChofyAI Studio — macOS local AI launcher (Tauri + Rust + React)",
                "Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable",
                "Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform",
                "Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge",
                "Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones",
                "Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright (headless/visible), pywebview + PyInstaller, SQLite, OCR, uv, 150 pytest tests, instalador firmado",
                "RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust (edition 2024): ETW + WPR, 5 ediciones (GUI Setup.exe, Portable .zip, CLI single-binary rootcause.exe, PowerShell .psm1, VS Code .vsix), SHA256SUMS por release",
                "Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build",
                "Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal",
                "Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura",
                "Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad",
                "Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases",
                "Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego",
                "Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop",
                "Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF",
                "Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF",
                "Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas",
                "Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase",
                "Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline",
                "Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero",
                "Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad",
                "Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera",
                "Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter)",
                "Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases",
                "Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA",
                "Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13",
                "Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje",
                            "Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱",
                "Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱",
                "Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases",
                "Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps",
                "Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform",
                "Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱",
                "Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile",
],
            "projects_ats": [
                ("Cloud/AWS and FinOps — GitHub (demos and documentation):", "aws_gh"),
                ("Cloud/AWS — GitLab (15 cases, 5-stage CI/CD, ~80% SAA-C03):", "aws_gl"),
                ("Microsystems (suite of 11 micro-apps, Hub CLI, MCP server):", "micro"),
                ("Social Bot Scheduler (9-axis integration matrix, 18+ DB engines, n8n, Prometheus/Grafana):", "social"),
                ("Docker Labs (12 labs, Control Center, Windows installer):", "docker"),
                ("LangGraph v4.15 (25/25 operational backends, 100% coverage, 8-layer hardening, Docker per case):", "langgraph"),
                ("MCP + local Ollama (local AI chat, MCP tools, 100% private):", "mcp"),
                ("Unikernel Labs — Windows Control Center (WSL2 + Node.js + WinForms):", "unikernel"),
                ("ChofyAI Studio — macOS local AI launcher (Tauri + Rust + React):", "chofyai"),
                ("Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones:", "python"),
                ("Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright, pywebview + PyInstaller, SQLite, OCR, 150 pytest tests, instalador firmado:", "automa"),
                ("RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust: ETW + WPR, 5 ediciones (Setup.exe, Portable .zip, CLI rootcause.exe, PowerShell .psm1, VS Code .vsix):", "rootcause"),
                ("Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura:", "modern_cyber"),
                ("Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable:", "problem"),
                ("Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform:", "claude"),
                ("Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge:", "gabysql"),
                ("Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build:", "rootcause_mobile"),
                ("Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal:", "modern"),
                ("Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad:", "machine"),
                ("Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases:", "rhino"),
                ("Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego:", "human"),
                ("Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop:", "wsl"),
                ("Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF:", "computational"),
                ("Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas:", "executive"),
                ("Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase:", "finance"),
                ("Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline:", "blockchain"),
                ("Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero:", "universal"),
                ("Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad:", "sandbox"),
                ("Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera:", "artificial"),
                ("Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases:", "violin"),
                ("Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13:", "neural"),
                ("Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje:", "polyglot"),
                ("Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF:", "modern_business"),
                ("Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter):", "rootcause_web"),
                ("Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA:", "multi"),
                            ("Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱:", "education"),
                ("Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱:", "marketing"),
                ("Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases:", "guitarra"),
                ("Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps:", "agentic"),
                ("Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform:", "operational"),
                ("Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱:", "empresa"),
                ("Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile:", "rootcause_macos"),
],
            "training": [
                "Continuous training in practical automation, ML/NLP, and development tools.",
                "Consolidation of a technical portfolio with cloud labs, microsystems, and recruiter-oriented documentation.",
            ],
            "notes": [
                "Recommendation letter available.",
                "If the hiring process uses ATS, please consider the ATS CV available on the website:",
            ],
            "skills_labels": ["<b>Backend:</b>", "<b>Frontend:</b>", "<b>Data:</b>", "<b>DevOps/Cloud:</b>", "<b>Quality/Security:</b>", "<b>Observability:</b>", "<b>AI/Agents:</b>"],
            "degrees": [
                ("Computer Science and Informatics Engineering", "University of Tarapac\u00e1 (Arica)"),
                ("Business Administration Technician (Marketing specialization)", "INACAP (Santiago)"),
            ],
            "language_skill": "English (technical): fluent reading (documentation, code, papers, AI tooling). Conversation: basic, actively improving.",
            "transition_title": "ATS-Optimized Version",
            "transition_body": "The following pages contain an ATS-optimized version of this resume.",
            "transition_reasons": [
                "Modern hiring processes frequently use artificial intelligence and automated filters to evaluate resumes before they reach a human recruiter.",
                "The single-column, plain-text format on the following pages is designed to be correctly parsed by these systems, maximizing ATS compatibility.",
                "The content is the same \u2014 only the presentation changes to ensure no information is lost during automated processing.",
            ],
            "transition_footer": "The previous page is for human review. The following pages are for automated processing.",
        },
        "pt": {
            "subtitle_rec": "Arquiteto de Soluções | Senior Full-Stack | Modernização, Automação e IA Aplicada",
            "subtitle_ats": "Arquiteto de Soluções | Senior Full-Stack | Modernização, Automação e IA Aplicada",
            "h_contact": "CONTATO", "h_skills": "SKILLS", "h_education": "EDUCA\u00c7\u00c3O",
            "h_languages": "IDIOMAS", "h_summary": "RESUMO", "h_experience": "EXPERI\u00caNCIA DESTACADA",
            "h_previous": "TRAJET\u00d3RIA ANTERIOR (S\u00cdNTESE)", "h_projects": "PROJETOS DESTACADOS",
            "h_training": "FORMA\u00c7\u00c3O E ATIVIDADE RECENTE", "h_notes": "NOTAS",
            "h_ats_experience": "EXPERI\u00caNCIA", "h_ats_education": "FORMA\u00c7\u00c3O E ATIVIDADE RECENTE",
            "h_degrees": "EDUCA\u00c7\u00c3O",
            "exp_title_rec": "Funda\u00e7\u00e3o CEIS Maristas \u2014 Arquiteto de Software \u00b7 Analista e Desenvolvedor Full-Stack",
            "exp_title_ats": "Funda\u00e7\u00e3o CEIS Maristas \u2014 Arquiteto de Software e Desenvolvedor Full-Stack (2011-2025)",
            "summary": [
                "14 anos de experi\u00eancia principal na Funda\u00e7\u00e3o CEIS Maristas (2011-2025), desenvolvendo, mantendo e modernizando uma plataforma educacional/psicom\u00e9trica.",
                "Experi\u00eancia pr\u00e9via em desenvolvimento web e suporte de sistemas para institui\u00e7\u00f5es p\u00fablicas e privadas, com foco em PHP, SQL Server/MySQL, relat\u00f3rios PDF/Excel, migra\u00e7\u00e3o de dados e integra\u00e7\u00f5es.",
                "Portf\u00f3lio t\u00e9cnico atual com projetos e laborat\u00f3rios em Docker, AWS, CI/CD, observabilidade e IA aplicada \u00e0 automa\u00e7\u00e3o, publicados no GitHub e GitLab.",
            ],
            "ats_summary": [
                "14 anos liderando o design, evolu\u00e7\u00e3o e opera\u00e7\u00e3o de uma plataforma educacional/psicom\u00e9trica (2011-2025), com foco em continuidade operacional.",
                "Moderniza\u00e7\u00e3o progressiva (PHP 5.4 \u2192 PHP 8.2+), otimiza\u00e7\u00e3o de desempenho e automa\u00e7\u00e3o de relat\u00f3rios (PDF/Excel) e processos de dados.",
                "Experi\u00eancia em bancos de dados (SQL Server, MySQL/MariaDB) e deploys/ambientes reproduz\u00edveis com Docker e CI/CD.",
                "Portf\u00f3lio t\u00e9cnico com casos pr\u00e1ticos (Cloud/AWS, microsistemas, agentes IA e observabilidade), documenta\u00e7\u00e3o e demos verific\u00e1veis no GitHub e GitLab.",
            ],
            "experience": [
                "Suite de avaliação educacional/psicométrica: <b>PCA</b> (aprendizagem), <b>Baterías Psicoeducativas</b> (desenvolvimento social/pessoal) e <b>Batería Online</b> (plataforma online), além de mailing institucional, LimeSurvey e WordPress.",
                "<b>Métricas verificadas</b>: 80% de melhoria nos relatórios/carga do Batería Online · 90% menos atrito no atendimento a clientes (2020-2025) · 45% de otimização DB/código · até 5 frentes concorrentes em certos períodos.",
                "<b>Pandemia 2020</b>: migração de serviços presenciais para formato online em pouco tempo (citado na carta de recomendação).",
                "Modernização PHP 5.4 → 8.2+, refatoração de módulos críticos, transferência de lógica para JavaScript e eliminação de duplicidades no DB.",
                "Mailing massivo (PHP + Constant Contact) e <b>adoção interna de IA (2024-2025)</b> para análise e resolução de problemas técnicos.",
            ],
            "ats_experience": [
                "Design, desenvolvimento e manutenção de plataforma de avaliação de alunos (baterias de testes), módulos institucionais e relatórios.",
                "Migração tecnológica (PHP 5.4 → PHP 8.2+), atualização de servidores/bibliotecas e melhorias de desempenho com JavaScript e testes de carga.",
                "Desenvolvimento de relatórios avançados PDF/Excel com indicadores, percentis e análise por turma/nível/instituição.",
                "Importação e migração de dados massivos do Excel com validações; automação de comunicações (envios, segmentação, acompanhamento).",
                "Suporte direto a usuários-chave (coordenadores, orientadores, diretores) e operação em produção.",
            ],
            "exp_tech": "Tecnologias: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
            "exp_logros_label": "M\u00e9tricas e conquistas quantificadas do per\u00edodo na CEIS Maristas",
            "projects_rec": [
                "Cloud/AWS e FinOps — GitHub + GitLab (16 casos AWS A–P, CI/CD 5 stages)",
                "Microsistemas — suite de 11 micro-apps, Hub CLI, MCP server",
                "Social Bot Scheduler — matriz 9 eixos, 18+ motores DB, n8n, Prometheus/Grafana",
                "Docker Labs — 12 labs, Control Center, instalador Windows",
                "LangGraph — 25/25 backends operacionais (v4.15, cobertura 100%), Docker por caso, agentes stateful",
                "MCP + Ollama local — chat IA local, ferramentas MCP, 100% privado",
                "Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms)",
                "ChofyAI Studio — launcher IA local macOS (Tauri + Rust + React)",
                "Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable",
                "Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform",
                "Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge",
                "Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones",
                "Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright (headless/visible), pywebview + PyInstaller, SQLite, OCR, uv, 150 pytest tests, instalador firmado",
                "RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust (edition 2024): ETW + WPR, 5 ediciones (GUI Setup.exe, Portable .zip, CLI single-binary rootcause.exe, PowerShell .psm1, VS Code .vsix), SHA256SUMS por release",
                "Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build",
                "Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal",
                "Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura",
                "Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad",
                "Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases",
                "Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego",
                "Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop",
                "Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF",
                "Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF",
                "Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas",
                "Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase",
                "Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline",
                "Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero",
                "Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad",
                "Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera",
                "Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter)",
                "Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases",
                "Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA",
                "Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13",
                "Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje",
                            "Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱",
                "Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱",
                "Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases",
                "Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps",
                "Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform",
                "Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱",
                "Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile",
],
            "projects_ats": [
                ("Cloud/AWS e FinOps — GitHub (demos e documentação):", "aws_gh"),
                ("Cloud/AWS — GitLab (15 casos, CI/CD 5 stages, ~80% SAA-C03):", "aws_gl"),
                ("Microsistemas (suite de 11 micro-apps, Hub CLI, MCP server):", "micro"),
                ("Social Bot Scheduler (matriz 9 eixos de integração, 18+ motores DB, n8n, Prometheus/Grafana):", "social"),
                ("Docker Labs (12 labs, Control Center, instalador Windows):", "docker"),
                ("LangGraph v4.15 (25/25 backends operacionais, cobertura 100%, auditoria 8 camadas, Docker por caso):", "langgraph"),
                ("MCP + Ollama local (chat IA local, ferramentas MCP, 100% privado):", "mcp"),
                ("Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms):", "unikernel"),
                ("ChofyAI Studio — launcher IA local macOS (Tauri + Rust + React):", "chofyai"),
                ("Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones:", "python"),
                ("Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright, pywebview + PyInstaller, SQLite, OCR, 150 pytest tests, instalador firmado:", "automa"),
                ("RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust: ETW + WPR, 5 ediciones (Setup.exe, Portable .zip, CLI rootcause.exe, PowerShell .psm1, VS Code .vsix):", "rootcause"),
                ("Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura:", "modern_cyber"),
                ("Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable:", "problem"),
                ("Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform:", "claude"),
                ("Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge:", "gabysql"),
                ("Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build:", "rootcause_mobile"),
                ("Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal:", "modern"),
                ("Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad:", "machine"),
                ("Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases:", "rhino"),
                ("Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego:", "human"),
                ("Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop:", "wsl"),
                ("Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF:", "computational"),
                ("Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas:", "executive"),
                ("Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase:", "finance"),
                ("Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline:", "blockchain"),
                ("Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero:", "universal"),
                ("Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad:", "sandbox"),
                ("Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera:", "artificial"),
                ("Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases:", "violin"),
                ("Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13:", "neural"),
                ("Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje:", "polyglot"),
                ("Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF:", "modern_business"),
                ("Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter):", "rootcause_web"),
                ("Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA:", "multi"),
                            ("Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱:", "education"),
                ("Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱:", "marketing"),
                ("Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases:", "guitarra"),
                ("Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps:", "agentic"),
                ("Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform:", "operational"),
                ("Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱:", "empresa"),
                ("Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile:", "rootcause_macos"),
],
            "training": [
                "Forma\u00e7\u00e3o cont\u00ednua em automa\u00e7\u00e3o pr\u00e1tica, ML/NLP e ferramentas de desenvolvimento.",
                "Consolida\u00e7\u00e3o de portf\u00f3lio t\u00e9cnico com laborat\u00f3rios cloud, microsistemas e documenta\u00e7\u00e3o orientada a recrutadores.",
            ],
            "notes": [
                "Carta de recomenda\u00e7\u00e3o dispon\u00edvel.",
                "Se o processo utiliza ATS, favor considerar o CV ATS no site:",
            ],
            "skills_labels": ["<b>Backend:</b>", "<b>Frontend:</b>", "<b>Dados:</b>", "<b>DevOps/Cloud:</b>", "<b>Qualidade/Seguran\u00e7a:</b>", "<b>Observabilidade:</b>", "<b>IA/Agentes:</b>"],
            "degrees": [
                ("Engenharia de Execu\u00e7\u00e3o em Computa\u00e7\u00e3o e Inform\u00e1tica", "Universidad de Tarapac\u00e1 (Arica)"),
                ("T\u00e9cnico em Administra\u00e7\u00e3o de Empresas (\u00canfase em Marketing)", "INACAP (Santiago)"),
            ],
            "language_skill": "Ingl\u00eas t\u00e9cnico: leitura fluente (documenta\u00e7\u00e3o, c\u00f3digo, papers, IA tooling). Conversa\u00e7\u00e3o: b\u00e1sica, em melhoria ativa.",
            "transition_title": "Vers\u00e3o otimizada para ATS",
            "transition_body": "A seguir, uma vers\u00e3o do curr\u00edculo otimizada para sistemas de rastreamento de candidatos (ATS).",
            "transition_reasons": [
                "Os processos seletivos atuais frequentemente utilizam intelig\u00eancia artificial e filtros autom\u00e1ticos para avaliar curr\u00edculos antes que cheguem a um recrutador humano.",
                "O formato de coluna \u00fanica e texto plano da p\u00e1gina seguinte foi projetado para ser lido corretamente por esses sistemas, maximizando a compatibilidade com parsers ATS.",
                "O conte\u00fado \u00e9 o mesmo \u2014 apenas a apresenta\u00e7\u00e3o muda para garantir que nenhuma informa\u00e7\u00e3o se perca no processamento autom\u00e1tico.",
            ],
            "transition_footer": "A p\u00e1gina anterior \u00e9 para leitura humana. As seguintes s\u00e3o para processamento autom\u00e1tico.",
        },
        "it": {
            "subtitle_rec": "Architetto di Soluzioni | Senior Full-Stack | Modernizzazione, Automazione e IA Applicata",
            "subtitle_ats": "Architetto di Soluzioni | Senior Full-Stack | Modernizzazione, Automazione e IA Applicata",
            "h_contact": "CONTATTO", "h_skills": "SKILLS", "h_education": "FORMAZIONE",
            "h_languages": "LINGUE", "h_summary": "RIEPILOGO", "h_experience": "ESPERIENZA PRINCIPALE",
            "h_previous": "CARRIERA PRECEDENTE (SINTESI)", "h_projects": "PROGETTI IN EVIDENZA",
            "h_training": "FORMAZIONE E ATTIVIT\u00c0 RECENTE", "h_notes": "NOTE",
            "h_ats_experience": "ESPERIENZA", "h_ats_education": "FORMAZIONE E ATTIVIT\u00c0 RECENTE",
            "h_degrees": "FORMAZIONE",
            "exp_title_rec": "Fondazione CEIS Maristas \u2014 Architetto Software \u00b7 Analista e Sviluppatore Full-Stack",
            "exp_title_ats": "Fondazione CEIS Maristas \u2014 Architetto Software e Sviluppatore Full-Stack (2011-2025)",
            "summary": [
                "14 anni di esperienza principale presso la Fondazione CEIS Maristas (2011-2025), sviluppando, mantenendo e modernizzando una piattaforma educativa/psicometrica.",
                "Esperienza precedente nello sviluppo web e supporto sistemi per istituzioni pubbliche e private, con focus su PHP, SQL Server/MySQL, reportistica PDF/Excel, migrazione dati e integrazioni.",
                "Portfolio tecnico attuale con progetti e laboratori in Docker, AWS, CI/CD, osservabilit\u00e0 e IA applicata all'automazione, pubblicati su GitHub e GitLab.",
            ],
            "ats_summary": [
                "14 anni alla guida del design, evoluzione e operazione di una piattaforma educativa/psicometrica (2011-2025), con focus sulla continuit\u00e0 operativa.",
                "Modernizzazione progressiva (PHP 5.4 \u2192 PHP 8.2+), ottimizzazione delle prestazioni e automazione di report (PDF/Excel) e processi dati.",
                "Esperienza con database (SQL Server, MySQL/MariaDB) e deploy/ambienti riproducibili con Docker e CI/CD.",
                "Portfolio tecnico con casi pratici (Cloud/AWS, microsistemi, agenti IA e osservabilit\u00e0), documentazione e demo verificabili su GitHub e GitLab.",
            ],
            "experience": [
                "Suite di valutazione educativa/psicometrica: <b>PCA</b> (apprendimento), <b>Baterías Psicoeducativas</b> (sviluppo sociale/personale) e <b>Batería Online</b> (piattaforma online), oltre a mailing istituzionale, LimeSurvey e WordPress.",
                "<b>Metriche verificate</b>: 80% miglioramento nei report/carico di Batería Online · 90% meno attrito nell'assistenza clienti (2020-2025) · 45% ottimizzazione DB/codice · fino a 5 fronti concorrenti in certi periodi.",
                "<b>Pandemia 2020</b>: migrazione di servizi in presenza a formato online in poco tempo (citato nella lettera di raccomandazione).",
                "Modernizzazione PHP 5.4 → 8.2+, refactoring di moduli critici, trasferimento di logica a JavaScript ed eliminazione di duplicati nel DB.",
                "Mailing massivo (PHP + Constant Contact) e <b>adozione interna di IA (2024-2025)</b> per analisi e risoluzione di problemi tecnici.",
            ],
            "ats_experience": [
                "Design, sviluppo e manutenzione di piattaforma di valutazione studenti (batterie di test), moduli istituzionali e report.",
                "Migrazione tecnologica (PHP 5.4 → PHP 8.2+), aggiornamento server/librerie e miglioramenti prestazioni con JavaScript e test di carico.",
                "Sviluppo di report avanzati PDF/Excel con indicatori, percentili e analisi per classe/livello/istituto.",
                "Importazione e migrazione massiva dati da Excel con validazioni; automazione comunicazioni (invii, segmentazione, follow-up).",
                "Supporto diretto agli utenti chiave (coordinatori, consulenti, dirigenti) e operazioni in produzione.",
            ],
            "exp_tech": "Tecnologie: PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
            "exp_logros_label": "Metriche e risultati quantificati del periodo in CEIS Maristas",
            "projects_rec": [
                "Cloud/AWS e FinOps — GitHub + GitLab (16 casi AWS A–P, CI/CD 5 stages)",
                "Microsistemi — suite di 11 micro-app, Hub CLI, MCP server",
                "Social Bot Scheduler — matrice 9 assi, 18+ motori DB, n8n, Prometheus/Grafana",
                "Docker Labs — 12 lab, Control Center, installer Windows",
                "LangGraph — 25/25 backend operativi (v4.15, copertura 100%), Docker per caso, agenti stateful",
                "MCP + Ollama locale — chat IA locale, strumenti MCP, 100% privato",
                "Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms)",
                "ChofyAI Studio — launcher IA locale macOS (Tauri + Rust + React)",
                "Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable",
                "Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform",
                "Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge",
                "Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones",
                "Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright (headless/visible), pywebview + PyInstaller, SQLite, OCR, uv, 150 pytest tests, instalador firmado",
                "RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust (edition 2024): ETW + WPR, 5 ediciones (GUI Setup.exe, Portable .zip, CLI single-binary rootcause.exe, PowerShell .psm1, VS Code .vsix), SHA256SUMS por release",
                "Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build",
                "Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal",
                "Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura",
                "Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad",
                "Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases",
                "Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego",
                "Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop",
                "Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF",
                "Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF",
                "Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas",
                "Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase",
                "Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline",
                "Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero",
                "Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad",
                "Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera",
                "Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter)",
                "Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases",
                "Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA",
                "Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13",
                "Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje",
                            "Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱",
                "Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱",
                "Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases",
                "Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps",
                "Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform",
                "Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱",
                "Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile",
],
            "projects_ats": [
                ("Cloud/AWS e FinOps — GitHub (demo e documentazione):", "aws_gh"),
                ("Cloud/AWS — GitLab (15 casi, CI/CD 5 stages, ~80% SAA-C03):", "aws_gl"),
                ("Microsistemi (suite di 11 micro-app, Hub CLI, MCP server):", "micro"),
                ("Social Bot Scheduler (matrice 9 assi di integrazione, 18+ motori DB, n8n, Prometheus/Grafana):", "social"),
                ("Docker Labs (12 lab, Control Center, installer Windows):", "docker"),
                ("LangGraph v4.15 (25/25 backend operativi, copertura 100%, audit 8 livelli, Docker per caso):", "langgraph"),
                ("MCP + Ollama locale (chat IA locale, strumenti MCP, 100% privato):", "mcp"),
                ("Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms):", "unikernel"),
                ("ChofyAI Studio — launcher IA locale macOS (Tauri + Rust + React):", "chofyai"),
                ("Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones:", "python"),
                ("Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright, pywebview + PyInstaller, SQLite, OCR, 150 pytest tests, instalador firmado:", "automa"),
                ("RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust: ETW + WPR, 5 ediciones (Setup.exe, Portable .zip, CLI rootcause.exe, PowerShell .psm1, VS Code .vsix):", "rootcause"),
                ("Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura:", "modern_cyber"),
                ("Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable:", "problem"),
                ("Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform:", "claude"),
                ("Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge:", "gabysql"),
                ("Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build:", "rootcause_mobile"),
                ("Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal:", "modern"),
                ("Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad:", "machine"),
                ("Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases:", "rhino"),
                ("Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego:", "human"),
                ("Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop:", "wsl"),
                ("Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF:", "computational"),
                ("Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas:", "executive"),
                ("Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase:", "finance"),
                ("Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline:", "blockchain"),
                ("Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero:", "universal"),
                ("Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad:", "sandbox"),
                ("Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera:", "artificial"),
                ("Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases:", "violin"),
                ("Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13:", "neural"),
                ("Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje:", "polyglot"),
                ("Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF:", "modern_business"),
                ("Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter):", "rootcause_web"),
                ("Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA:", "multi"),
                            ("Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱:", "education"),
                ("Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱:", "marketing"),
                ("Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases:", "guitarra"),
                ("Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps:", "agentic"),
                ("Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform:", "operational"),
                ("Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱:", "empresa"),
                ("Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile:", "rootcause_macos"),
],
            "training": [
                "Formazione continua in automazione pratica, ML/NLP e strumenti di sviluppo.",
                "Consolidamento del portfolio tecnico con laboratori cloud, microsistemi e documentazione orientata ai recruiter.",
            ],
            "notes": [
                "Lettera di raccomandazione disponibile.",
                "Se il processo utilizza ATS, si prega di considerare il CV ATS sul sito web:",
            ],
            "skills_labels": ["<b>Backend:</b>", "<b>Frontend:</b>", "<b>Dati:</b>", "<b>DevOps/Cloud:</b>", "<b>Qualit\u00e0/Sicurezza:</b>", "<b>Osservabilit\u00e0:</b>", "<b>IA/Agenti:</b>"],
            "degrees": [
                ("Ingegneria Informatica", "Universidad de Tarapac\u00e1 (Arica)"),
                ("Tecnico in Amministrazione Aziendale (Specializzazione Marketing)", "INACAP (Santiago)"),
            ],
            "language_skill": "Inglese tecnico: lettura fluida (documentazione, codice, paper, IA tooling). Conversazione: base, in miglioramento attivo.",
            "transition_title": "Versione ottimizzata per ATS",
            "transition_body": "Di seguito una versione del curriculum ottimizzata per i sistemi di tracciamento candidati (ATS).",
            "transition_reasons": [
                "I processi di selezione attuali utilizzano frequentemente intelligenza artificiale e filtri automatici per valutare i curriculum prima che raggiungano un recruiter umano.",
                "Il formato a colonna singola e testo semplice della pagina seguente \u00e8 progettato per essere letto correttamente da questi sistemi, massimizzando la compatibilit\u00e0 con i parser ATS.",
                "Il contenuto \u00e8 lo stesso \u2014 cambia solo la presentazione per garantire che nessuna informazione venga persa nell'elaborazione automatica.",
            ],
            "transition_footer": "La pagina precedente \u00e8 per la lettura umana. Le seguenti sono per l'elaborazione automatica.",
        },
        "fr": {
            "subtitle_rec": "Architecte de Solutions | Senior Full-Stack | Modernisation, Automatisation et IA Appliquée",
            "subtitle_ats": "Architecte de Solutions | Senior Full-Stack | Modernisation, Automatisation et IA Appliquée",
            "h_contact": "CONTACT", "h_skills": "COMP\u00c9TENCES", "h_education": "FORMATION",
            "h_languages": "LANGUES", "h_summary": "R\u00c9SUM\u00c9", "h_experience": "EXP\u00c9RIENCE PRINCIPALE",
            "h_previous": "CARRI\u00c8RE ANT\u00c9RIEURE (SYNTH\u00c8SE)", "h_projects": "PROJETS EN VEDETTE",
            "h_training": "FORMATION ET ACTIVIT\u00c9 R\u00c9CENTE", "h_notes": "NOTES",
            "h_ats_experience": "EXP\u00c9RIENCE", "h_ats_education": "FORMATION ET ACTIVIT\u00c9 R\u00c9CENTE",
            "h_degrees": "FORMATION",
            "exp_title_rec": "Fondation CEIS Maristas \u2014 Architecte Logiciel \u00b7 Analyste et D\u00e9veloppeur Full-Stack",
            "exp_title_ats": "Fondation CEIS Maristas \u2014 Architecte Logiciel et D\u00e9veloppeur Full-Stack (2011-2025)",
            "summary": [
                "14 ans d'exp\u00e9rience principale \u00e0 la Fondation CEIS Maristas (2011-2025), d\u00e9veloppant, maintenant et modernisant une plateforme \u00e9ducative/psychom\u00e9trique.",
                "Exp\u00e9rience pr\u00e9alable en d\u00e9veloppement web et support syst\u00e8mes pour des institutions publiques et priv\u00e9es, ax\u00e9e sur PHP, SQL Server/MySQL, rapports PDF/Excel, migration de donn\u00e9es et int\u00e9grations.",
                "Portfolio technique actuel avec projets et laboratoires en Docker, AWS, CI/CD, observabilit\u00e9 et IA appliqu\u00e9e \u00e0 l'automatisation, publi\u00e9s sur GitHub et GitLab.",
            ],
            "ats_summary": [
                "14 ans \u00e0 la t\u00eate de la conception, \u00e9volution et op\u00e9ration d'une plateforme \u00e9ducative/psychom\u00e9trique (2011-2025), avec un fort accent sur la continuit\u00e9 op\u00e9rationnelle.",
                "Modernisation progressive (PHP 5.4 \u2192 PHP 8.2+), optimisation des performances et automatisation des rapports (PDF/Excel) et processus de donn\u00e9es.",
                "Exp\u00e9rience avec les bases de donn\u00e9es (SQL Server, MySQL/MariaDB) et d\u00e9ploiements/environnements reproductibles avec Docker et CI/CD.",
                "Portfolio technique avec cas pratiques (Cloud/AWS, microsyst\u00e8mes, agents IA et observabilit\u00e9), documentation et d\u00e9mos v\u00e9rifiables sur GitHub et GitLab.",
            ],
            "experience": [
                "Suite d'évaluation éducative/psychométrique : <b>PCA</b> (apprentissage), <b>Baterías Psicoeducativas</b> (développement social/personnel) et <b>Batería Online</b> (plateforme en ligne), plus mailing institutionnel, LimeSurvey et WordPress.",
                "<b>Métriques vérifiées</b> : 80% d'amélioration des rapports/charge de Batería Online · 90% moins de friction dans le support client (2020-2025) · 45% d'optimisation DB/code · jusqu'à 5 fronts concurrents à certaines périodes.",
                "<b>Pandémie 2020</b> : migration des services en présentiel vers le format en ligne en peu de temps (cité dans la lettre de recommandation).",
                "Modernisation PHP 5.4 → 8.2+, refactoring de modules critiques, transfert de logique vers JavaScript et élimination des doublons en DB.",
                "Mailing de masse (PHP + Constant Contact) et <b>adoption interne d'IA (2024-2025)</b> pour analyse et résolution de problèmes techniques.",
            ],
            "ats_experience": [
                "Conception, développement et maintenance d'une plateforme d'évaluation des élèves (batteries de tests), modules institutionnels et rapports.",
                "Migration technologique (PHP 5.4 → PHP 8.2+), mise à jour des serveurs/bibliothèques et améliorations des performances avec JavaScript et tests de charge.",
                "Développement de rapports avancés PDF/Excel avec indicateurs, percentiles et analyse par classe/niveau/établissement.",
                "Importation et migration massive de données depuis Excel avec validations ; automatisation des communications (envois, segmentation, suivi).",
                "Support direct aux utilisateurs clés (coordinateurs, conseillers, directeurs) et opérations en production.",
            ],
            "exp_tech": "Technologies : PHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
            "exp_logros_label": "M\u00e9triques et r\u00e9alisations quantifi\u00e9es de la p\u00e9riode chez CEIS Maristas",
            "projects_rec": [
                "Cloud/AWS et FinOps — GitHub + GitLab (16 cas AWS A–P, CI/CD 5 stages)",
                "Microsystèmes — suite de 11 micro-apps, Hub CLI, serveur MCP",
                "Social Bot Scheduler — matrice 9 axes, 18+ moteurs DB, n8n, Prometheus/Grafana",
                "Docker Labs — 12 labs, Control Center, installateur Windows",
                "LangGraph — 25/25 backends opérationnels (v4.15, couverture 100%), Docker par cas, agents à état",
                "MCP + Ollama local — chat IA local, outils MCP, 100% privé",
                "Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms)",
                "ChofyAI Studio — lanceur IA locale macOS (Tauri + Rust + React)",
                "Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable",
                "Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform",
                "Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge",
                "Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones",
                "Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright (headless/visible), pywebview + PyInstaller, SQLite, OCR, uv, 150 pytest tests, instalador firmado",
                "RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust (edition 2024): ETW + WPR, 5 ediciones (GUI Setup.exe, Portable .zip, CLI single-binary rootcause.exe, PowerShell .psm1, VS Code .vsix), SHA256SUMS por release",
                "Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build",
                "Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal",
                "Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura",
                "Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad",
                "Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases",
                "Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego",
                "Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop",
                "Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF",
                "Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF",
                "Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas",
                "Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase",
                "Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline",
                "Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero",
                "Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad",
                "Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera",
                "Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter)",
                "Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases",
                "Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA",
                "Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13",
                "Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje",
                            "Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱",
                "Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱",
                "Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases",
                "Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps",
                "Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform",
                "Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱",
                "Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile",
],
            "projects_ats": [
                ("Cloud/AWS et FinOps — GitHub (démos et documentation) :", "aws_gh"),
                ("Cloud/AWS — GitLab (15 cas, CI/CD 5 stages, ~80% SAA-C03) :", "aws_gl"),
                ("Microsystèmes (suite de 11 micro-apps, Hub CLI, serveur MCP) :", "micro"),
                ("Social Bot Scheduler (matrice 9 axes d'intégration, 18+ moteurs DB, n8n, Prometheus/Grafana) :", "social"),
                ("Docker Labs (12 labs, Control Center, installateur Windows) :", "docker"),
                ("LangGraph v4.15 (25/25 backends opérationnels, couverture 100%, audit 8 couches, Docker par cas) :", "langgraph"),
                ("MCP + Ollama local (chat IA local, outils MCP, 100% privé) :", "mcp"),
                ("Unikernel Labs — Control Center Windows (WSL2 + Node.js + WinForms) :", "unikernel"),
                ("ChofyAI Studio — lanceur IA locale macOS (Tauri + Rust + React) :", "chofyai"),
                ("Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones :", "python"),
                ("Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright, pywebview + PyInstaller, SQLite, OCR, 150 pytest tests, instalador firmado :", "automa"),
                ("RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust: ETW + WPR, 5 ediciones (Setup.exe, Portable .zip, CLI rootcause.exe, PowerShell .psm1, VS Code .vsix) :", "rootcause"),
                ("Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura :", "modern_cyber"),
                ("Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable :", "problem"),
                ("Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform :", "claude"),
                ("Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge :", "gabysql"),
                ("Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build :", "rootcause_mobile"),
                ("Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal :", "modern"),
                ("Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad :", "machine"),
                ("Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases :", "rhino"),
                ("Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego :", "human"),
                ("Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop :", "wsl"),
                ("Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF :", "computational"),
                ("Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas :", "executive"),
                ("Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase :", "finance"),
                ("Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline :", "blockchain"),
                ("Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero :", "universal"),
                ("Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad :", "sandbox"),
                ("Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera :", "artificial"),
                ("Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases :", "violin"),
                ("Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13 :", "neural"),
                ("Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje :", "polyglot"),
                ("Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF :", "modern_business"),
                ("Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter) :", "rootcause_web"),
                ("Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA :", "multi"),
                            ("Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱 :", "education"),
                ("Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱 :", "marketing"),
                ("Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases :", "guitarra"),
                ("Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps :", "agentic"),
                ("Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform :", "operational"),
                ("Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱 :", "empresa"),
                ("Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile :", "rootcause_macos"),
],
            "training": [
                "Formation continue en automatisation pratique, ML/NLP et outils de d\u00e9veloppement.",
                "Consolidation du portfolio technique avec laboratoires cloud, microsyst\u00e8mes et documentation orient\u00e9e recruteurs.",
            ],
            "notes": [
                "Lettre de recommandation disponible.",
                "Si le processus utilise un ATS, veuillez consid\u00e9rer le CV ATS disponible sur le site :",
            ],
            "skills_labels": ["<b>Backend :</b>", "<b>Frontend :</b>", "<b>Donn\u00e9es :</b>", "<b>DevOps/Cloud :</b>", "<b>Qualit\u00e9/S\u00e9curit\u00e9 :</b>", "<b>Observabilit\u00e9 :</b>", "<b>IA/Agents :</b>"],
            "degrees": [
                ("Ing\u00e9nierie Informatique", "Universidad de Tarapac\u00e1 (Arica)"),
                ("Technicien en Administration des Entreprises (Sp\u00e9cialisation Marketing)", "INACAP (Santiago)"),
            ],
            "language_skill": "Anglais technique : lecture courante (documentation, code, papers, IA tooling). Conversation : basique, en am\u00e9lioration active.",
            "transition_title": "Version optimis\u00e9e pour ATS",
            "transition_body": "Les pages suivantes contiennent une version du CV optimis\u00e9e pour les syst\u00e8mes de suivi des candidatures (ATS).",
            "transition_reasons": [
                "Les processus de recrutement actuels utilisent fr\u00e9quemment l'intelligence artificielle et des filtres automatiques pour \u00e9valuer les CV avant qu'ils n'atteignent un recruteur humain.",
                "Le format \u00e0 colonne unique et texte brut des pages suivantes est con\u00e7u pour \u00eatre lu correctement par ces syst\u00e8mes, maximisant la compatibilit\u00e9 avec les parseurs ATS.",
                "Le contenu est le m\u00eame \u2014 seule la pr\u00e9sentation change pour garantir qu'aucune information ne soit perdue lors du traitement automatique.",
            ],
            "transition_footer": "La page pr\u00e9c\u00e9dente est pour la lecture humaine. Les suivantes sont pour le traitement automatique.",
        },
        "zh": {
            "subtitle_rec": "解决方案架构师 | 高级全栈开发 | 现代化、自动化与应用AI",
            "subtitle_ats": "解决方案架构师 | 高级全栈开发 | 现代化、自动化与应用AI",
            "h_contact": "\u8054\u7cfb\u65b9\u5f0f", "h_skills": "\u6280\u80fd", "h_education": "\u6559\u80b2\u80cc\u666f",
            "h_languages": "\u8bed\u8a00\u80fd\u529b", "h_summary": "\u6982\u8ff0", "h_experience": "\u4e3b\u8981\u7ecf\u9a8c",
            "h_previous": "\u65e9\u671f\u804c\u4e1a\u7ecf\u5386\uff08\u6458\u8981\uff09", "h_projects": "\u7cbe\u9009\u9879\u76ee",
            "h_training": "\u8fd1\u671f\u57f9\u8bad\u4e0e\u6d3b\u52a8", "h_notes": "\u5907\u6ce8",
            "h_ats_experience": "\u5de5\u4f5c\u7ecf\u9a8c", "h_ats_education": "\u8fd1\u671f\u57f9\u8bad\u4e0e\u6d3b\u52a8",
            "h_degrees": "\u6559\u80b2\u80cc\u666f",
            "exp_title_rec": "CEIS Maristas\u57fa\u91d1\u4f1a \u2014 \u8f6f\u4ef6\u67b6\u6784\u5e08 \u00b7 \u7cfb\u7edf\u5206\u6790\u5e08\u4e0e\u5168\u6808\u5f00\u53d1\u8005",
            "exp_title_ats": "CEIS Maristas\u57fa\u91d1\u4f1a \u2014 \u8f6f\u4ef6\u67b6\u6784\u5e08\u548c\u5168\u6808\u5f00\u53d1\u8005 (2011-2025)",
            "summary": [
                "14\u5e74\u5728CEIS Maristas\u57fa\u91d1\u4f1a\u7684\u6838\u5fc3\u7ecf\u9a8c\uff082011-2025\uff09\uff0c\u5f00\u53d1\u3001\u7ef4\u62a4\u548c\u73b0\u4ee3\u5316\u6559\u80b2/\u5fc3\u7406\u6d4b\u91cf\u5e73\u53f0\u3002",
                "\u5728\u516c\u5171\u548c\u79c1\u8425\u673a\u6784\u7684Web\u5f00\u53d1\u548c\u7cfb\u7edf\u652f\u6301\u65b9\u9762\u7684\u65e9\u671f\u7ecf\u9a8c\uff0c\u4e13\u6ce8\u4e8ePHP\u3001SQL Server/MySQL\u3001PDF/Excel\u62a5\u8868\u3001\u6570\u636e\u8fc1\u79fb\u548c\u96c6\u6210\u3002",
                "\u5f53\u524d\u6280\u672f\u4f5c\u54c1\u96c6\u5305\u62ecDocker\u3001AWS\u3001CI/CD\u3001\u53ef\u89c2\u6d4b\u6027\u548cAI\u81ea\u52a8\u5316\u7684\u9879\u76ee\u548c\u5b9e\u9a8c\u5ba4\uff0c\u53d1\u5e03\u5728GitHub\u548cGitLab\u4e0a\u3002",
            ],
            "ats_summary": [
                "14\u5e74\u9886\u5bfc\u6559\u80b2/\u5fc3\u7406\u6d4b\u91cf\u5e73\u53f0\u7684\u8bbe\u8ba1\u3001\u6f14\u8fdb\u548c\u8fd0\u8425\uff082011-2025\uff09\uff0c\u4e13\u6ce8\u4e8e\u8fd0\u8425\u8fde\u7eed\u6027\u3002",
                "\u6e10\u8fdb\u5f0f\u73b0\u4ee3\u5316\uff08PHP 5.4 \u2192 PHP 8.2+\uff09\uff0c\u6027\u80fd\u4f18\u5316\u4ee5\u53ca\u62a5\u8868\uff08PDF/Excel\uff09\u548c\u6570\u636e\u6d41\u7a0b\u7684\u81ea\u52a8\u5316\u3002",
                "\u6570\u636e\u5e93\u7ecf\u9a8c\uff08SQL Server\u3001MySQL/MariaDB\uff09\u4ee5\u53ca\u4f7f\u7528Docker\u548cCI/CD\u7684\u53ef\u590d\u73b0\u90e8\u7f72/\u73af\u5883\u3002",
                "\u6280\u672f\u4f5c\u54c1\u96c6\u5305\u542b\u5b9e\u9645\u6848\u4f8b\uff08Cloud/AWS\u3001\u5fae\u7cfb\u7edf\u3001AI\u4ee3\u7406\u548c\u53ef\u89c2\u6d4b\u6027\uff09\u3001\u6587\u6863\u548cGitHub/GitLab\u4e0a\u7684\u53ef\u9a8c\u8bc1\u6f14\u793a\u3002",
            ],
            "experience": [
                "教育/心理评估套件：<b>PCA</b>（学习评估）、<b>Baterías Psicoeducativas</b>（社会/个人发展评估）和 <b>Batería Online</b>（在线平台），以及机构邮件、LimeSurvey 和 WordPress。",
                "<b>已验证指标</b>：Batería Online 报表/加载提升 80% · 客户支持摩擦减少 90%（2020-2025）· 数据库/代码优化 45% · 特定时期同时处理多达 5 条工作线。",
                "<b>2020 年疫情</b>：在短时间内将线下服务迁移至在线平台（推荐信中提及）。",
                "PHP 5.4 → 8.2+ 现代化、关键模块重构、逻辑迁移至 JavaScript、数据库去重。",
                "大规模邮件 (PHP + Constant Contact) 及 <b>2024-2025 内部 AI 应用</b>，用于技术分析与问题解决。",
            ],
            "ats_experience": [
                "设计、开发和维护学生评估平台（测试电池）、机构模块和报表。",
                "技术迁移（PHP 5.4 → PHP 8.2+），服务器/库升级，以及JavaScript和负载测试的性能改进。",
                "开发包含指标、百分位和按班级/年级/学校分析的高级PDF/Excel报表。",
                "从Excel大规模导入和迁移数据并进行验证；通信自动化（发送、分组、跟踪）。",
                "直接支持关键用户（协调员、顾问、校领导）和生产运营。",
            ],
            "exp_tech": "\u6280\u672f\u6808\uff1aPHP, JavaScript, SQL Server, MySQL, Apache, JMeter, Excel, FPDF/PhpSpreadsheet, Constant Contact",
            "exp_logros_label": "CEIS Maristas\u671f\u95f4\u7684\u91cf\u5316\u6307\u6807\u4e0e\u6210\u5c31",
            "projects_rec": [
                "Cloud/AWS和FinOps — GitHub + GitLab（16个AWS案例 A–P，CI/CD 5阶段）",
                "微系统 — 11个微应用套件，Hub CLI，MCP服务器",
                "Social Bot Scheduler — 9轴矩阵，18+个DB引擎，n8n，Prometheus/Grafana",
                "Docker Labs — 12个实验室，控制中心，Windows安装程序",
                "LangGraph — 25/25个可运行后端（v4.15，覆盖率100%），每案例Docker，有状态智能体",
                "MCP + 本地Ollama — 本地AI聊天，MCP工具，100%私有",
                "Unikernel Labs — Windows控制中心 (WSL2 + Node.js + WinForms)",
                "ChofyAI Studio — macOS本地AI启动器 (Tauri + Rust + React)",
                "Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable",
                "Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform",
                "Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge",
                "Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones",
                "Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright (headless/visible), pywebview + PyInstaller, SQLite, OCR, uv, 150 pytest tests, instalador firmado",
                "RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust (edition 2024): ETW + WPR, 5 ediciones (GUI Setup.exe, Portable .zip, CLI single-binary rootcause.exe, PowerShell .psm1, VS Code .vsix), SHA256SUMS por release",
                "Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build",
                "Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal",
                "Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura",
                "Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad",
                "Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases",
                "Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego",
                "Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop",
                "Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF",
                "Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF",
                "Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas",
                "Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase",
                "Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline",
                "Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero",
                "Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad",
                "Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera",
                "Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter)",
                "Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases",
                "Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA",
                "Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13",
                "Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje",
                            "Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱",
                "Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱",
                "Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases",
                "Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps",
                "Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform",
                "Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱",
                "Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile",
],
            "projects_ats": [
                ("Cloud/AWS和FinOps — GitHub（演示和文档）：", "aws_gh"),
                ("Cloud/AWS — GitLab（15个案例，CI/CD 5阶段，~80% SAA-C03）：", "aws_gl"),
                ("微系统（11个微应用套件，Hub CLI，MCP服务器）：", "micro"),
                ("Social Bot Scheduler（9轴集成矩阵，18+个DB引擎，n8n，Prometheus/Grafana）：", "social"),
                ("Docker Labs（12个实验室，控制中心，Windows安装程序）：", "docker"),
                ("LangGraph v4.15（25/25个可运行后端，覆盖率100%，8层审计，每案例Docker）：", "langgraph"),
                ("MCP + 本地Ollama（本地AI聊天，MCP工具，100%私有）：", "mcp"),
                ("Unikernel Labs — Windows控制中心 (WSL2 + Node.js + WinForms)：", "unikernel"),
                ("ChofyAI Studio — macOS本地AI启动器 (Tauri + Rust + React)：", "chofyai"),
                ("Python Data Science Program — Python Data Science Program v3.11.0 · 232 clases en 9 partes (100%) · App Windows Qt nativa (PySide6) con la clase en HTML + APK Android con las 232 clases embebidas + lab Python (Flask+Jupyter real) · Currículo Python/Polars, ML+Optuna/SHAP, DL (PyTorch/LLMs/LoRA-DPO/MCP/agentes/multimodal/JAX), estadística+causalidad, MLOps, ética, capstones：", "python"),
                ("Automa · PC Orchestrator v0.3.0 — Orquestador local Windows: 27 flows declarativos JSON (incluye vigilancia web con evidencia SHA-256), Playwright, pywebview + PyInstaller, SQLite, OCR, 150 pytest tests, instalador firmado：", "automa"),
                ("RootCause · Windows Inspector v0.19.0 — Diagnóstico forense Windows 10/11 en Rust: ETW + WPR, 5 ediciones (Setup.exe, Portable .zip, CLI rootcause.exe, PowerShell .psm1, VS Code .vsix)：", "rootcause"),
                ("Modern Cybersecurity Program — El programa de ciberseguridad más completo en español — 340 clases, 19 partes, de fundamentos a nivel experto. Laboratorios Docker, retos CTF, autoevaluaciones, guías PDF/PPTX y mapeo a 7 certificaciones (Security+, PenTest+, CySA+, OSCP, CISSP, BTL1, SANS) con 86–92% de cobertura：", "modern_cyber"),
                ("Problem Driven Systems Lab — Laboratorio Docker-first con 12 problemas reales de ingeniería resueltos en 7 stacks (PHP · Python · Node.js · Java · .NET · Go · Rust): rendimiento, observabilidad, resiliencia, modernización legacy y arquitectura — con evidencia operacional verificable：", "problem"),
                ("Claude Skills Toolkit — claude-skills-toolkit · 14 skills agentic para Claude Code · security-audit (12 capas: OSV/KEV/EPSS/SAST/…) · python-lint-guard (paridad local↔CI) · python-deps-pinning · version-bump · md-to-doc · yaml-control · md-lint-fix · docker-cleanup · Zero-deps por defecto · Cross-platform：", "claude"),
                ("Gabysql — GabySQL · Base de datos embebida en Rust, multiplataforma, archivo único .db, WAL, API HTTP/JSON y admin web liviano. Diseñada para entornos embebidos y edge：", "gabysql"),
                ("Rootcause Mobile Inspector — RootCause Mobile v0.8.0 — sensor forense de diagnóstico para Android e iOS (Flutter). Compara cada app consigo misma para detectar consumo anómalo, señala stalkerware activo y distingue permisos concedidos de los solo pedidos. Evidencia PDF, 5 idiomas. Sin permiso INTERNET: telemetría cero, verificada en cada build：", "rootcause_mobile"),
                ("Modern Gamedev Program — El programa de desarrollo de videojuegos más completo en español — 352 clases en 22 partes, de fundamentos a nivel profesional. 2D/3D, física, shaders, IA, audio, multijugador, VR/AR, optimización y producción; más especialización en ingeniería: sistemas de gameplay, backend, IA generativa y motores. Godot · Unity · Unreal：", "modern"),
                ("Machine Operator Program — Base documental del Programa de Operación y Simulación de Máquinas — mandos, instrumentos, historia, reglamentos y diseño de simulación de motos, autos, buses, grúas, buques, aeronaves y naves espaciales, con foco educativo y de seguridad：", "machine"),
                ("Rhino Suite — Rhino Suite · Suite ofimática web y de escritorio construida desde cero — editor de documentos con modelo estructurado, motores Rust/WASM + motor TypeScript compatible, API Go, intercambio DOCX/ODT y monorepo evolutivo por fases：", "rhino"),
                ("Human Genome Labs — Human Genome Labs v1.0 · Plataforma científica evolutiva y reproducible para genética molecular y genómica · Núcleo TypeScript: secuencias, traducción, ORF, variantes y G-cuádruplex · Contratos ScientificResult · FASTA/GFF3/VCF · Módulos con madurez y evidencia explícitas · CLI + lab web PWA + juego：", "human"),
                ("Wsl Labs — WSL Container Center · Levanta y controla contenedores en Windows con wslc, el motor de contenedores nativo de WSL — 12 casos reales portados de docker-labs, panel de control + launcher. Sin Docker Desktop：", "wsl"),
                ("Computational Mathematics Program — Matemática computacional en español · 18 partes · 360 clases en 5 etapas: de contar con los dedos a reproducir un paper · 360 demostraciones deterministas verificadas en CI · sin dependencias para aprender · 1080 notebooks · 489 términos de glosario · manual completo en PDF：", "computational"),
                ("Executive Leadership Founder Program — Programa ejecutivo abierto de 288 clases en 24 partes · 720 h · De asumir tu primer resultado a dirigir una empresa y crear la tuya: liderazgo, equipos, talento, operaciones, KPI/OKR, finanzas, ventas, marketing, producto, estrategia, riesgo, IA, directorio, M&A y founder track Chile · 24 casos, 96 labs y 39 plantillas：", "executive"),
                ("Finance And Banking Evolution Program — Programa abierto de 356 clases en 23 partes · 534 h · De calcular un porcentaje a construir y defender un banco digital: matemática financiera, contabilidad NIIF, crédito, riesgos, Basilea III, cumplimiento, finanzas abiertas, pagos transfronterizos, DLT, stablecoins, tokenización y MiCA · 26 casos y fuentes oficiales verificables en cada clase：", "finance"),
                ("Blockchain Learning Path — Blockchain Learning Path v0.9.0 · Programa en español: 28 módulos de cero a la infraestructura financiera programable — cripto, Bitcoin, EVM, contratos, seguridad, L2, ZK, DeFi, dinero y liquidación, stablecoins, CBDC/MDBC, pagos y FX, tokenización, RWA, mercados de capitales, custodia y regulación. 70 prácticas, 186 pruebas, apps offline：", "blockchain"),
                ("Universal Code Scanner — Universal Code Scanner v1.1.0 — Lector Flutter de códigos QR y de barras que interpreta antes de actuar: 16 señales de riesgo locales por URL, confirmación explícita, historial e inventario cifrados con AES-256-GCM. Estado de escaneo siempre visible y tono propio de lectura. Android · iOS · macOS · PWA. Telemetría cero：", "universal"),
                ("Sandbox Labs — Laboratorio de aislamiento en Linux: ejecuta código, archivos y modelos de negocio ajenos bajo políticas declaradas, y emite evidencia firmada de qué controles se aplicaron de verdad en tu equipo. 36 casos en dos familias — sandboxes técnicos y mercado de capitales con dinero simulado. Experimental y educativo, no un producto de seguridad：", "sandbox"),
                ("Artificial Intelligence Evolution Program — AI Evolution Program v0.2.0 · 180 clases en 15 partes con materia completa · 540 notebooks con ejercicios y soluciones · PDFs por parte + programa completo (~1.100 pags) · La evolución de la IA en español: simbólica, ML, deep learning, LLMs, RAG, agentes, MLOps, seguridad y frontera：", "artificial"),
                ("Violin Adventure — Mi Aventura con el Violín · App educativa para aprender violín desde los 10 años · 24 lecciones en 6 mundos, afinador cromático, metrónomo y práctica guiada · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0, instaladores firmados en Releases：", "violin"),
                ("Neural Network Training Labs — Neural Network Training Labs v1.0 · 31 rutas (25 labs + 6 especializaciones) · 93 notebooks · Ciclo completo de ingeniería de IA con datasets públicos reales: sellado de test, registro champion/challenger, API de inferencia, ONNX/INT8/edge, DDP/FSDP2 y cadena de suministro (SBOM/SHA-256). PyTorch · Python 3.11–3.13：", "neural"),
                ("Polyglot Programming Labs — El programa de programación comparada en español — 176 clases en 12 partes. Un concepto, 10 lenguajes del núcleo (Python, JS, TS, Java, C#, Go, Rust, C, SQL, PHP) verificados en CI, y un Atlas de ~40 familias. Aprende el concepto una vez y reconócelo en cualquier lenguaje：", "polyglot"),
                ("Modern Business Creation Program — Programa de 24 partes y 336 clases para crear y operar una empresa real en Chile: de la idea a la constitución, el SII, la operación, la crisis y la salida. Con 360 diagramas, glosario de 1.251 términos y manual de 1.541 páginas en PDF：", "modern_business"),
                ("Rootcause Web Inspector — RootCause Web Inspector v0.1.0 — sensor forense de la superficie del navegador: cookies, sesiones de correo, extensiones, descargas y permisos de sitio. Panel local en 127.0.0.1, extension MV3, CERO dependencias y cero telemetria verificada en CI. Hermano de las ediciones Windows (Rust) y Mobile (Flutter)：", "rootcause_web"),
                ("Multi Cloud Engineering Program — Multi-Cloud Engineering Program v2.0.0 · 288 clases en 24 partes · 1.288 horas · El programa de ingeniería multi-cloud más completo en español: AWS, Azure, GCP, Kubernetes, Terraform, SRE, FinOps y arquitectura de sistemas · Manual PDF de 1.220 páginas, 288 labs deterministas con evidencia JSON, CLI con certificado y portal PWA：", "multi"),
                            ("Education Pedagogy Learning Sciences Program — Pedagogía, Docencia y Ciencias del Aprendizaje v2.0.0 · 300 clases en 25 partes · El programa de formación pedagógica más completo en español: aprendizaje, didáctica, inclusión, currículum, evaluación, convivencia, IA educativa y liderazgo · Evidencia declarada por clase, 14 rutas por rol, 60 actividades de aula y portal offline 🇨🇱：", "education"),
                ("Marketing Sales Growth Evolution Program — Marketing, Sales & Growth Evolution Program v1.0.0 · 336 clases en 24 partes · El programa de marketing, ventas y crecimiento más completo en español: posicionamiento, pricing, venta consultiva, RevOps, growth, analítica e IA comercial · 1.344 conceptos, 1.008 métricas, 96 obras, 17 rutas por rol y portal offline 🇨🇱：", "marketing"),
                ("Guitarra Adventure — Mi Aventura con la Guitarra · App educativa para aprender guitarra desde los 10 años · 24 lecciones en 6 mundos, afinador de 6 cuerdas, metrónomo sin deriva y 11 notas grabadas de guitarra real · Tauri 2 + React + TypeScript · Windows, Android, Linux, macOS, iOS y PWA · Sin publicidad, sin cuentas, offline · v1.0.0 con instaladores en Releases：", "guitarra"),
                ("Agentic Plugins Toolkit — agentic-plugins-toolkit · 6 plugins agénticos para Claude Code, OpenAI/Codex, Copilot, Gemini y MCP · repository-engineering · legacy-modernization · learning-program-studio · product-evolution · portfolio-governance · rootcause-response · 69 vistas generadas sin drift · Zero-deps：", "agentic"),
                ("Operational Ai Agents — operational-ai-agents · 13 agentes para Claude Code · repository-evolution · legacy-modernization · curriculum-evolution · portfolio-publication · security-remediation · incident-root-cause · professional-profile · Contrato + gates humanos + evidencia verificable · 39 evals deterministas · Zero-deps · Cross-platform：", "operational"),
                ("Empresa Operativa Chile — v1.4.0 · Crear, operar y controlar una empresa chilena a través del tiempo: constitución con evidencia, capital y CPT, patente municipal con su base legal, IVA/PPM, F29, cierre anual inmutable y auditoría. Guía, manual y glosario dentro de la app. Android, Windows y navegador. Reglas con fuente oficial. Cero telemetría. 🇨🇱：", "empresa"),
                ("Rootcause Macos Inspector — RootCause macOS Inspector v0.1.0 — sensor forense de ciberseguridad para macOS (Rust): persistencia launchd, Gatekeeper, SIP, FileVault, XProtect, permisos TCC, procesos con firma y vecinos de red. Compara cada superficie con un estado bueno conocido y explica qué cambió, con evidencia. Telemetría: cero. Hermano de Windows, Web y Mobile：", "rootcause_macos"),
],
            "training": [
                "\u6301\u7eed\u5b66\u4e60\u5b9e\u7528\u81ea\u52a8\u5316\u3001ML/NLP\u548c\u5f00\u53d1\u5de5\u5177\u3002",
                "\u5de9\u56fa\u6280\u672f\u4f5c\u54c1\u96c6\uff0c\u5305\u62ec\u4e91\u5b9e\u9a8c\u5ba4\u3001\u5fae\u7cfb\u7edf\u548c\u9762\u5411\u62db\u8058\u4eba\u5458\u7684\u6587\u6863\u3002",
            ],
            "notes": [
                "\u63a8\u8350\u4fe1\u53ef\u7528\u3002",
                "\u5982\u679c\u62db\u8058\u6d41\u7a0b\u4f7f\u7528ATS\uff0c\u8bf7\u53c2\u8003\u7f51\u7ad9\u4e0a\u7684ATS\u7b80\u5386\uff1a",
            ],
            "skills_labels": ["<b>\u540e\u7aef\uff1a</b>", "<b>\u524d\u7aef\uff1a</b>", "<b>\u6570\u636e\uff1a</b>", "<b>DevOps/\u4e91\uff1a</b>", "<b>\u8d28\u91cf/\u5b89\u5168\uff1a</b>", "<b>\u53ef\u89c2\u6d4b\u6027\uff1a</b>", "<b>AI/\u4ee3\u7406\uff1a</b>"],
            "degrees": [
                ("\u8ba1\u7b97\u673a\u4e0e\u4fe1\u606f\u5de5\u7a0b", "Universidad de Tarapac\u00e1 (Arica)"),
                ("\u5de5\u5546\u7ba1\u7406\u6280\u672f\u5458\uff08\u5e02\u573a\u8425\u9500\u65b9\u5411\uff09", "INACAP (Santiago)"),
            ],
            "language_skill": "\u6280\u672f\u82f1\u8bed\uff1a\u6d41\u5229\u9605\u8bfb\uff08\u6587\u6863\u3001\u4ee3\u7801\u3001\u8bba\u6587\u3001AI\u5de5\u5177\uff09\u3002\u4f1a\u8bdd\uff1a\u57fa\u7840\uff0c\u6b63\u5728\u79ef\u6781\u63d0\u5347\u3002",
            "transition_title": "ATS\u4f18\u5316\u7248\u672c",
            "transition_body": "\u4ee5\u4e0b\u9875\u9762\u5305\u542b\u9488\u5bf9\u5019\u9009\u4eba\u8ddf\u8e2a\u7cfb\u7edf\uff08ATS\uff09\u4f18\u5316\u7684\u7b80\u5386\u7248\u672c\u3002",
            "transition_reasons": [
                "\u5f53\u524d\u7684\u62db\u8058\u6d41\u7a0b\u7ecf\u5e38\u4f7f\u7528\u4eba\u5de5\u667a\u80fd\u548c\u81ea\u52a8\u8fc7\u6ee4\u5668\u5728\u7b80\u5386\u5230\u8fbe\u4eba\u5de5\u62db\u8058\u4eba\u5458\u4e4b\u524d\u8fdb\u884c\u8bc4\u4f30\u3002",
                "\u4e0b\u4e00\u9875\u7684\u5355\u680f\u7eaf\u6587\u672c\u683c\u5f0f\u65e8\u5728\u88ab\u8fd9\u4e9b\u7cfb\u7edf\u6b63\u786e\u8bfb\u53d6\uff0c\u6700\u5927\u5316ATS\u517c\u5bb9\u6027\u3002",
                "\u5185\u5bb9\u76f8\u540c \u2014 \u53ea\u662f\u5448\u73b0\u65b9\u5f0f\u4e0d\u540c\uff0c\u4ee5\u786e\u4fdd\u5728\u81ea\u52a8\u5904\u7406\u8fc7\u7a0b\u4e2d\u4e0d\u4f1a\u4e22\u5931\u4efb\u4f55\u4fe1\u606f\u3002",
            ],
            "transition_footer": "\u524d\u4e00\u9875\u4f9b\u4eba\u5de5\u9605\u8bfb\u3002\u4ee5\u4e0b\u9875\u9762\u4f9b\u81ea\u52a8\u5316\u5904\u7406\u3002",
        },
    }

    return T[lang]


# Shared skills values (same across all languages)
SKILLS_VALUES = [
    "PHP 8.x, Node.js, TypeScript, Python (FastAPI), Go, Rust, C#, Ruby",
    "JavaScript, HTML, CSS",
    "SQL Server, MySQL/MariaDB, PostgreSQL, MongoDB, Redis, SQLite, DuckDB",
    "Docker/Compose, Kubernetes, CI/CD (GitHub Actions/GitLab CI), AWS (S3, Amplify, CloudFront), Terraform",
    "hardening, secret scanning (Gitleaks, TruffleHog), anti-injection, Trivy, pip-audit",
    "Prometheus/Grafana",
    "LangGraph, MCP (Model Context Protocol), Ollama, n8n",
]


# ═══════════════════════════════════════════════════
# PDF GENERATION ENGINE (reused from generate-unified-cv.py)
# ═══════════════════════════════════════════════════

# Import the full engine inline to keep this self-contained
# (styles, document class, build functions)

exec(open(os.path.join(SCRIPT_DIR, "generate-unified-cv.py"), encoding="utf-8").read().split("def main():")[0])

# ── Standalone ATS builder (from generate-ats-cv.py) ──

def _ats_make_styles():
    """Paragraph styles for standalone ATS PDF."""
    return dict(
        name=ParagraphStyle("AtsName", fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=BLACK, spaceAfter=2, alignment=TA_LEFT),
        subtitle=ParagraphStyle("AtsSub", fontName="Helvetica", fontSize=10, leading=13, textColor=DARK, spaceAfter=1),
        contact=ParagraphStyle("AtsCont", fontName="Helvetica", fontSize=8.5, leading=11, textColor=MUTED, spaceAfter=8),
        heading=ParagraphStyle("AtsHead", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=BLACK, spaceBefore=10, spaceAfter=4),
        subheading=ParagraphStyle("AtsSHead", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=DARK, spaceBefore=4, spaceAfter=2),
        body=ParagraphStyle("AtsBody", fontName="Helvetica", fontSize=9.5, leading=12.5, textColor=DARK, spaceAfter=2),
        bullet=ParagraphStyle("AtsBullet", fontName="Helvetica", fontSize=9.5, leading=12.5, textColor=DARK, spaceAfter=2, leftIndent=12, bulletIndent=0),
        tech=ParagraphStyle("AtsTech", fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED, spaceAfter=1),
        link=ParagraphStyle("AtsLink", fontName="Helvetica", fontSize=9, leading=12, textColor=ACCENT, spaceAfter=2, leftIndent=12, bulletIndent=0),
    )

def _ats_hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE_COLOR, spaceBefore=2, spaceAfter=6)

def _ats_bullet(style, text):
    return Paragraph(f"\u2022 {text}", style)

from reportlab.platypus import SimpleDocTemplate

def build_cv(data, output_path, lang="es"):
    """Build a standalone ATS CV PDF."""
    s = _ats_make_styles()
    if lang == "zh":
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
            for st in s.values():
                st.fontName = "STSong-Light"
        except Exception:
            pass
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=0.7*inch, rightMargin=0.7*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    story.append(Paragraph("Vladimir Acu\u00f1a", s["name"]))
    story.append(Paragraph(data["subtitle"], s["subtitle"]))
    story.append(Paragraph(data["contact_line1"], s["contact"]))
    story.append(Paragraph(data["contact_line2"], s["contact"]))
    story.append(Paragraph(data["contact_line3"], s["contact"]))
    story.append(_ats_hr())
    story.append(Paragraph(data["h_summary"], s["heading"]))
    for item in data["summary"]:
        story.append(_ats_bullet(s["bullet"], item))
    story.append(_ats_hr())
    story.append(Paragraph(data["h_skills"], s["heading"]))
    for label, value in data["skills"]:
        story.append(Paragraph(f"{label} {value}", s["tech"]))
    story.append(_ats_hr())
    story.append(Paragraph(data["h_experience"], s["heading"]))
    story.append(Paragraph(data["exp_title"], s["subheading"]))
    for item in data["experience"]:
        story.append(_ats_bullet(s["bullet"], item))
    story.append(Paragraph(data["exp_tech"], s["tech"]))
    story.append(_ats_hr())
    story.append(Paragraph(data["h_projects"], s["heading"]))
    for desc, url in data["projects"]:
        story.append(_ats_bullet(s["link"], f'{desc} <link href="{url}">{url}</link>'))
    story.append(_ats_hr())
    story.append(Paragraph(data["h_education"], s["heading"]))
    for item in data["education_activity"]:
        story.append(_ats_bullet(s["bullet"], item))
    for title, institution in data["degrees"]:
        story.append(Paragraph(f"<b>{title}</b>", s["body"]))
        story.append(Paragraph(institution, s["tech"]))
        story.append(Spacer(1, 3))
    story.append(_ats_hr())
    story.append(Paragraph(data["h_languages"], s["heading"]))
    story.append(_ats_bullet(s["bullet"], data["languages"]))
    doc.build(story)
    size_kb = os.path.getsize(output_path) / 1024
    print(f" -> {output_path} ({size_kb:.1f} KB)")

# We need to rebuild content dicts from the translation data

def make_sidebar(lang):
    T = get_content(lang)
    web_label = CONTACT_LINKS_LABELS[lang]
    return dict(
        h_contact=T["h_contact"],
        contact=CONTACT_LINES,
        contact_links=[
            (web_label, WEB_URL),
            ("GitHub: vladimiracunadev-create", GITHUB_URL),
            ("GitLab: vladimir.acuna.dev-group", GITLAB_URL),
            ("LinkedIn: Vladimir Acu\u00f1a", LINKEDIN_URL),
        ],
        h_skills=T["h_skills"],
        skills=[f"{T['skills_labels'][i]} {SKILLS_VALUES[i]}" for i in range(7)],
        h_education=T["h_education"],
        degrees=T["degrees"],
        h_languages=T["h_languages"],
        languages=T["language_skill"],
    )

DOC_LINK_LABELS = {
    "es": {
        "achievements": "Ver declaración de logros profesionales",
        "recommendation": "Ver carta de recomendación",
    },
    "en": {
        "achievements": "View professional achievements statement",
        "recommendation": "View recommendation letter",
    },
    "pt": {
        "achievements": "Ver declaração de conquistas profissionais",
        "recommendation": "Ver carta de recomendação",
    },
    "it": {
        "achievements": "Vedi dichiarazione dei risultati professionali",
        "recommendation": "Vedi lettera di raccomandazione",
    },
    "fr": {
        "achievements": "Voir la déclaration de réalisations professionnelles",
        "recommendation": "Voir la lettre de recommandation",
    },
    "zh": {
        "achievements": "查看专业成就声明",
        "recommendation": "查看推荐信",
    },
}

DOC_LINK_SUFFIX = {
    "es": "", "en": "-english", "pt": "-portuguese",
    "it": "-italian", "fr": "-french", "zh": "-chinese",
}

def make_rmain(lang):
    T = get_content(lang)
    suffix = DOC_LINK_SUFFIX[lang]
    labels = DOC_LINK_LABELS[lang]
    base = "https://vladimiracunadev-create.github.io/assets"
    doc_links = [
        (labels["achievements"], f"{base}/declaracion-logros-validacion{suffix}.pdf"),
        (labels["recommendation"], f"{base}/carta-recomendacion_sin_firma{suffix}.pdf"),
    ]
    exp_logros_link = (
        T["exp_logros_label"],
        f"{base}/declaracion-logros-validacion{suffix}.pdf",
    )
    return dict(
        h_summary=T["h_summary"],
        summary=T["summary"],
        h_experience=T["h_experience"],
        exp_title=T["exp_title_rec"],
        exp_date={
            "es": "mayo 2011 — octubre 2025",
            "en": "May 2011 — October 2025",
            "pt": "maio 2011 — outubro 2025",
            "it": "maggio 2011 — ottobre 2025",
            "fr": "mai 2011 — octobre 2025",
            "zh": "2011年5月 — 2025年10月",
        }[lang],
        experience=T["experience"],
        exp_tech=T["exp_tech"],
        exp_logros_link=exp_logros_link,
        h_previous=T["h_previous"],
        previous=PREVIOUS_CAREER[lang],
        h_projects=T["h_projects"],
        projects=T["projects_rec"],
        doc_links=doc_links,
        h_training=T["h_training"],
        training=T["training"],
    )

def make_transition(lang):
    T = get_content(lang)
    return dict(
        title=T["transition_title"],
        body=T["transition_body"],
        reasons=T["transition_reasons"],
        footer=T["transition_footer"],
    )

def make_ats(lang):
    T = get_content(lang)
    projects = [(desc, PROJECTS_URLS[key]) for desc, key in T["projects_ats"]]
    return dict(
        subtitle=T["subtitle_ats"],
        contact_line1="Santiago, Chile | +56 9 8121 8838 | vladimir.acuna.dev@gmail.com",
        contact_line2=f'Web: <link href="{WEB_URL}">vladimiracunadev-create.github.io</link> | GitHub: <link href="{GITHUB_URL}">github.com/vladimiracunadev-create</link> | GitLab: <link href="{GITLAB_URL}">gitlab.com/vladimir.acuna.dev-group</link>',
        contact_line3=f'LinkedIn: <link href="{LINKEDIN_URL}">linkedin.com/in/vladimir-acuna-valdebenito</link>',
        h_summary=T["h_summary"],
        summary=T["ats_summary"],
        h_skills=T["h_skills"],
        skills=[(T["skills_labels"][i], SKILLS_VALUES[i]) for i in range(7)],
        h_experience=T["h_ats_experience"],
        exp_title=T["exp_title_ats"],
        experience=T["ats_experience"],
        exp_tech=T["exp_tech"],
        h_projects=T["h_projects"],
        projects=projects,
        h_education=T["h_ats_education"],
        education_activity=T["training"],
        h_degrees=T["h_degrees"],
        degrees=T["degrees"],
        h_languages=T["h_languages"],
        languages=T["language_skill"],
    )

def make_header(lang):
    T = get_content(lang)
    return dict(
        name="Vladimir Acu\u00f1a",
        subtitle=T["subtitle_rec"],
        contact="Santiago, Chile | +56 9 8121 8838 | vladimir.acuna.dev@gmail.com",
    )


# ═══════════════════════════════════════════════════
# FILE NAMING
# ═══════════════════════════════════════════════════

LANG_SUFFIX = {
    "es": "",
    "en": "-english",
    "pt": "-portuguese",
    "it": "-italian",
    "fr": "-french",
    "zh": "-chinese",
}


def main():
    print("Generating all language versions...")
    print("=" * 50)

    for lang in ["es", "en", "pt", "it", "fr", "zh"]:
        suffix = LANG_SUFFIX[lang]

        # Unified recruiter CV
        rec_path = os.path.normpath(os.path.join(ASSETS_DIR, f"cv-reclutador{suffix}.pdf"))
        header = make_header(lang)
        sidebar = make_sidebar(lang)
        rmain = make_rmain(lang)
        transition = make_transition(lang)
        ats = make_ats(lang)
        build_unified(header, sidebar, rmain, transition, ats, rec_path, lang=lang)

        # Standalone ATS CV
        ats_path = os.path.normpath(os.path.join(ASSETS_DIR, f"cv-ats{suffix}.pdf"))
        build_cv(ats, ats_path, lang=lang) # Uses the ATS-only builder

    print("=" * 50)
    print("Done. All 12 PDFs generated.")


if __name__ == "__main__":
    main()
