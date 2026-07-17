#!/usr/bin/env python3
"""
CV por solicitud: Instructor / Relator de Programacion y Pensamiento Computacional
Formato: Una columna, visualmente amigable (NO ATS), español.
Salida: assets/no_aplica/cv-capacitaciones.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    Paragraph, Spacer, HRFlowable, SimpleDocTemplate, Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Colores ──────────────────────────────────────────────────────────────────
NAVY      = HexColor("#1e3a5f")
ACCENT    = HexColor("#2563eb")
DARK      = HexColor("#1a1a1a")
MUTED     = HexColor("#555555")
LIGHT_BG  = HexColor("#eef2f7")
LINE      = HexColor("#c8d4e4")
WHITE     = white

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR    = os.path.join(SCRIPT_DIR, "..", "assets", "no_aplica")
OUT_PDF    = os.path.join(OUT_DIR, "cv-capacitaciones.pdf")

PAGE_W, PAGE_H = letter
MARGIN = 0.65 * inch


# ── Estilos ───────────────────────────────────────────────────────────────────
def make_styles():
    name = ParagraphStyle(
        "Name", fontName="Helvetica-Bold", fontSize=22, leading=27,
        textColor=NAVY, alignment=TA_CENTER, spaceAfter=2,
    )
    title = ParagraphStyle(
        "Title", fontName="Helvetica", fontSize=11.5, leading=15,
        textColor=ACCENT, alignment=TA_CENTER, spaceAfter=3,
    )
    contact = ParagraphStyle(
        "Contact", fontName="Helvetica", fontSize=9, leading=12,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=6,
    )
    section_head = ParagraphStyle(
        "SectionHead", fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=NAVY, spaceBefore=10, spaceAfter=4,
    )
    job_title = ParagraphStyle(
        "JobTitle", fontName="Helvetica-Bold", fontSize=10, leading=13,
        textColor=DARK, spaceBefore=5, spaceAfter=1,
    )
    job_company = ParagraphStyle(
        "JobCompany", fontName="Helvetica", fontSize=9.5, leading=12,
        textColor=ACCENT, spaceAfter=1,
    )
    date_loc = ParagraphStyle(
        "DateLoc", fontName="Helvetica", fontSize=8.8, leading=11,
        textColor=MUTED, spaceAfter=3,
    )
    bullet = ParagraphStyle(
        "Bullet", fontName="Helvetica", fontSize=9.2, leading=12.5,
        textColor=DARK, leftIndent=12, bulletIndent=0, spaceAfter=2,
    )
    body = ParagraphStyle(
        "Body", fontName="Helvetica", fontSize=9.2, leading=12.5,
        textColor=DARK, spaceAfter=3,
    )
    highlight_box = ParagraphStyle(
        "HighlightBox", fontName="Helvetica-Bold", fontSize=9.5, leading=13,
        textColor=NAVY, backColor=LIGHT_BG, alignment=TA_CENTER,
        spaceAfter=3, spaceBefore=3, leftIndent=6, rightIndent=6,
        borderPad=4,
    )
    skills_label = ParagraphStyle(
        "SkillsLabel", fontName="Helvetica-Bold", fontSize=9, leading=12,
        textColor=NAVY, spaceAfter=1,
    )
    skills_val = ParagraphStyle(
        "SkillsVal", fontName="Helvetica", fontSize=9, leading=12,
        textColor=DARK, spaceAfter=3,
    )
    footer_style = ParagraphStyle(
        "Footer", fontName="Helvetica", fontSize=8, leading=11,
        textColor=MUTED, alignment=TA_CENTER, spaceBefore=8,
    )
    return dict(
        name=name, title=title, contact=contact,
        section_head=section_head,
        job_title=job_title, job_company=job_company, date_loc=date_loc,
        bullet=bullet, body=body, highlight_box=highlight_box,
        skills_label=skills_label, skills_val=skills_val,
        footer_style=footer_style,
    )


def hr(color=LINE, thickness=0.8):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=4, spaceBefore=2)


def section(label, st):
    return [
        Spacer(1, 4),
        Paragraph(label.upper(), st["section_head"]),
        hr(),
    ]


def bullet_item(text, st):
    return Paragraph(f"\u2022 {text}", st["bullet"])


# ── Documento ─────────────────────────────────────────────────────────────────
def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    st = make_styles()

    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
    )

    story = []

    # ── CABECERA ────────────────────────────────────────────────────────────
    story.append(Paragraph("Vladimir Acuña", st["name"]))
    story.append(Paragraph(
        "Instructor / Relator de Programación y Pensamiento Computacional",
        st["title"]
    ))
    story.append(Paragraph(
        "+56 9 8121 8838  ·  vladimir.acuna.dev@gmail.com  ·  Santiago, Chile<br/>"
        "Web: vladimiracunadev-create.github.io  ·  "
        "LinkedIn: linkedin.com/in/vladimir-acuna-valdebenito",
        st["contact"]
    ))
    story.append(hr(NAVY, 1.5))
    story.append(Spacer(1, 6))

    # ── RESUMEN ─────────────────────────────────────────────────────────────
    story += section("Perfil profesional", st)
    story.append(Paragraph(
        "Ingeniero en Computación e Informática con 16 años de experiencia en desarrollo y "
        "operación de plataformas educativas reales. Acredito más de <b>445 horas</b> dictadas "
        "como relator técnico en programación web, herramientas de oficina y hardware. "
        "Mi proyecto de titulación universitaria (nota 6.7) fue un entorno educativo web "
        "orientado a niños con Síndrome de Down, evidenciando un compromiso temprano con "
        "la educación inclusiva y la tecnología accesible. "
        "Cuento con la capacidad de traducir conceptos técnicos complejos en aprendizaje "
        "práctico y significativo para públicos de distintos niveles.",
        st["body"]
    ))

    # ── BLOQUE DESTACADO ────────────────────────────────────────────────────
    story.append(Spacer(1, 4))
    data = [
        [
            Paragraph("<b>445+ horas</b><br/>Relatorías dictadas\n(2003–2011)", st["highlight_box"]),
            Paragraph("<b>14 años</b><br/>Plataforma educativa\nen producción", st["highlight_box"]),
            Paragraph("<b>Nota 6.7</b><br/>Titulación UTA\nEducación inclusiva", st["highlight_box"]),
            Paragraph("<b>Ing. Computación</b><br/>Universidad de\nTarapacá", st["highlight_box"]),
        ]
    ]
    tbl = Table(data, colWidths=[(PAGE_W - 2 * MARGIN) / 4] * 4)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("ROUNDEDCORNERS", [4]),
        ("BOX",         (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID",   (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING",   (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 6))

    # ── EXPERIENCIA DOCENTE ──────────────────────────────────────────────────
    story += section("Experiencia como Relator / Instructor", st)

    # Centro Europeo
    story.append(Paragraph("Relator Técnico", st["job_title"]))
    story.append(Paragraph("Centro Europeo para la Capacitación", st["job_company"]))
    story.append(Paragraph(
        "Julio 2003 – Junio 2004  ·  Santiago, Chile  ·  "
        "<i>Empresa de capacitación de la época; sin registro digital vigente (OTEC pequeña, ~2003).</i>",
        st["date_loc"]
    ))
    for item in [
        "Diseño Web (HTML, JavaScript, VBScript, ASP) — 8 clases, 6 alumnos, <b>52 horas</b>, nivel intermedio.",
        "HTML y CSS — 7 clases, 20 alumnos, <b>10 horas</b>, nivel básico.",
        "Armado y configuración de computadores — 15 clases, 10 alumnos, <b>45 horas</b>, nivel básico.",
        "Microsoft Office 2000 e Internet — 8 relatorías, 84 clases, 69 alumnos, <b>338 horas</b>, niveles básico e intermedio.",
    ]:
        story.append(bullet_item(item, st))
    story.append(Paragraph(
        "<i>Total acumulado: 445 horas — programación web, ofimática y hardware.</i>",
        st["date_loc"]
    ))
    story.append(Spacer(1, 5))

    # E-syste
    story.append(Paragraph("Relator Técnico", st["job_title"]))
    story.append(Paragraph("E-syste Capacitación S.A.", st["job_company"]))
    story.append(Paragraph(
        "Abril 2011  ·  Santiago, Chile  ·  "
        "<i>Empresa activa — OTEC acreditada por SENCE (RUT 77805400-0), ISO 9001, 130.000+ personas capacitadas.</i>",
        st["date_loc"]
    ))
    story.append(bullet_item(
        "Microsoft Office Visio 2007 — 7 clases, 10 alumnos, <b>21 horas</b>, "
        "niveles intermedio y avanzado.", st
    ))
    story.append(Spacer(1, 5))

    # ── EXPERIENCIA COMPLEMENTARIA RELEVANTE ─────────────────────────────────
    story += section("Experiencia complementaria relevante para docencia", st)

    story.append(Paragraph(
        "Arquitecto de Software y Desarrollador Full-Stack", st["job_title"]
    ))
    story.append(Paragraph("Fundación CEIS Maristas", st["job_company"]))
    story.append(Paragraph(
        "Abril 2011 – Octubre 2025  ·  Santiago, Chile  ·  "
        "<i>Fundación activa desde 1984 — 40 aniversario en 2024, OTEC acreditada, ceismaristas.cl.</i>",
        st["date_loc"]
    ))
    for item in [
        "Operación y evolución de plataforma educativa/psicométrica real durante <b>14 años consecutivos</b>.",
        "Creación de manuales de usuario y video tutoriales para coordinadores, orientadores y directivos.",
        "Formación y soporte directo a usuarios con distintos niveles de competencia digital.",
        "Automatización de reportes académicos (PDF/Excel) con indicadores, percentiles y análisis por "
        "curso, nivel y establecimiento.",
    ]:
        story.append(bullet_item(item, st))
    story.append(Spacer(1, 5))

    # ── PROYECTO DE TITULACION ────────────────────────────────────────────────
    story += section("Proyecto de titulación — Educación inclusiva", st)

    story.append(Paragraph(
        "Entorno educativo web para niños con Síndrome de Down", st["job_title"]
    ))
    story.append(Paragraph(
        "Universidad de Tarapacá (CTI)  ·  Nota 6.7  ·  2002–2003", st["date_loc"]
    ))
    for item in [
        "Diseño e implementación de un entorno educativo interactivo basado en tecnologías web "
        "(PHP, MySQL, JavaScript, HTML, CSS) para apoyar el aprendizaje de niños con Síndrome de Down.",
        "Proyecto publicado originalmente en www.profesordown.cl (dominio ya no operativo — proyecto de 2002). "
        "Modelado con UWE (UML orientado a la web) y Rational Rose.",
        "Reconocimiento académico con nota máxima de titulación, evidenciando compromiso con la "
        "educación inclusiva desde el inicio de la carrera profesional.",
    ]:
        story.append(bullet_item(item, st))
    story.append(Spacer(1, 5))

    # ── HABILIDADES PARA LA ENSEÑANZA ─────────────────────────────────────────
    story += section("Habilidades para la instrucción", st)

    skills = [
        ("Programación web",
         "HTML, CSS, JavaScript, PHP, Python — desde nivel básico hasta avanzado."),
        ("Pensamiento computacional",
         "Algoritmos, lógica, estructuras de datos, resolución de problemas."),
        ("Herramientas de productividad",
         "Microsoft Office (Word, Excel, PowerPoint, Visio), Google Workspace."),
        ("Plataformas y herramientas modernas",
         "GitHub, VS Code, Docker (nivel introductorio), IA aplicada (ChatGPT, GitHub Copilot)."),
        ("Metodología de instrucción",
         "Adaptación de contenido por nivel (básico / intermedio / avanzado), creación de "
         "manuales y materiales didácticos, soporte post-clase."),
        ("Habilidades blandas",
         "Comunicación clara, paciencia, teatro e improvisación (actividad extracurricular) — "
         "apoyo a la expresión oral en aula."),
    ]
    for label, val in skills:
        story.append(Paragraph(f"<b>{label}:</b> {val}", st["skills_val"]))

    # ── FORMACION ─────────────────────────────────────────────────────────────
    story += section("Formación académica y continua", st)

    formacion = [
        ("Ingeniería de Ejecución en Computación e Informática",
         "Universidad de Tarapacá, Arica · Titulado 2003"),
        ("Técnico de Administración de Empresas (Mención Marketing, SAP Usuario)",
         "INACAP, Santiago · Titulado 2014 · 1.705 horas"),
        ("Machine Learning, NLP y Python — Formación continua",
         "Udemy · 2023 · 40+ horas con certificado"),
        ("Taller de Ciberseguridad",
         "Desafío Latam · Junio 2019 · 3 horas"),
        ("Aplicaciones Web para Móviles con Adobe Dreamweaver CS5.5",
         "Training Center Informático · Junio 2011 · 21 horas"),
    ]
    for titulo, detalle in formacion:
        story.append(Paragraph(f"<b>{titulo}</b>", st["job_title"]))
        story.append(Paragraph(detalle, st["date_loc"]))

    # ── IDIOMAS ───────────────────────────────────────────────────────────────
    story += section("Idiomas", st)
    story.append(Paragraph(
        "<b>Español:</b> nativo.   <b>Inglés:</b> técnico — lectura intermedia, escritura y "
        "conversación básica.",
        st["skills_val"]
    ))

    # ── PIE ───────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8))
    story.append(hr(LINE, 0.5))
    story.append(Paragraph(
        "CV preparado para postulación a cargo de Instructor/a de Programación y "
        "Pensamiento Computacional  ·  Santiago, abril 2026",
        st["footer_style"]
    ))

    doc.build(story)
    print(f"PDF generado: {os.path.abspath(OUT_PDF)}")


if __name__ == "__main__":
    build()
