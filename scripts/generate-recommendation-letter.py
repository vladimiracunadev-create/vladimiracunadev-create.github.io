#!/usr/bin/env python3
"""
Generate Recommendation Letter PDFs for all 6 languages.
Replicates the format of the existing ES/EN versions:
  - Top disclaimer in italic
  - CEIS logo placeholder (centered)
  - Title bold centered
  - Body text justified
  - Date right-aligned
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "assets"))

# ── Colors ──
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#666666")

# ── Styles ──
def make_styles():
    return dict(
        disclaimer=ParagraphStyle(
            "Disclaimer", fontName="Helvetica-Oblique", fontSize=8.5, leading=11,
            textColor=MUTED, spaceAfter=20, alignment=TA_LEFT,
        ),
        title=ParagraphStyle(
            "Title", fontName="Helvetica-Bold", fontSize=16, leading=20,
            textColor=DARK, spaceBefore=30, spaceAfter=20, alignment=TA_CENTER,
        ),
        body=ParagraphStyle(
            "Body", fontName="Helvetica", fontSize=11, leading=15,
            textColor=DARK, spaceAfter=6, alignment=TA_JUSTIFY,
            firstLineIndent=24,
        ),
        body_no_indent=ParagraphStyle(
            "BodyNoIndent", fontName="Helvetica", fontSize=11, leading=15,
            textColor=DARK, spaceAfter=6, alignment=TA_JUSTIFY,
        ),
        date=ParagraphStyle(
            "Date", fontName="Helvetica", fontSize=11, leading=15,
            textColor=DARK, spaceBefore=30, alignment=TA_RIGHT,
        ),
    )


# ═══════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════

def get_content(lang):
    T = {
        "es": {
            "disclaimer": "NOTA: Este documento es una TRANSCRIPCIÓN (no es el original). Se omitieron firmas y datos del firmante por privacidad. El original firmado está disponible a solicitud.",
            "title": "Carta de Recomendación",
            "p1": 'El Secretario Ejecutivo de la Fundación CEIS Orientación, perteneciente a la red educativa de la Congregación de los hermanos Maristas en Chile, certifica que el Sr. Vladimir Acuña Valdebenito fue trabajador de nuestra fundación, durante el periodo comprendido entre el 01 de mayo del año 2011 y el 30 de octubre de 2025.',
            "p2": 'Dejamos constancia, que el Sr Vladimir Acuña, se desempeñó como Analista y Desarrollador de Programación, de nuestra Fundación, debiendo diseñar, actualizar y dar soporte al área de evaluación, especialmente a través de las plataformas de PCA (evaluaciones de aprendizaje) y Baterías Psicoeducativas (Evaluaciones de diferentes áreas del desarrollo social y personal de los estudiantes evaluados). Entre sus funciones han estado labores como: soporte de mailing y página web, programación, analista de sistemas y servidor. En su trabajo él destacó, por su responsabilidad, dedicación a la tarea y su interés por el estudio y el mantenerse siempre vigente a los cambios tecnológicos. Su trabajo implicó, relacionarse tanto con clientes (personal de colegios), como también con otros profesionales de nuestra Fundación. Valoramos especialmente su labor durante la etapa de pandemia, en que gran parte de nuestros servicios debieron llevarse a formatos on line en un muy breve tiempo, labor que contó con el aporte fundamental del Sr. Acuña.',
            "p3": 'La razón de su desvinculación, se debe directamente a causas asociadas al rediseño organizacional, debido a un cambio en el mercado de los productos del área en qué él trabajó y que han obligado a una disminución de personal y costos asociados, para poder dar sostenibilidad a la Fundación. Dado lo anterior, con mucho gusto podemos recomendar su labor, que sin duda será un aporte en otras instituciones que requieran su servicio.',
            "p4": 'Ante cualquier detalle mayor que requieran, contacto disponible a solicitud.',
            "date": "Santiago. 12 de enero de 2026",
        },
        "en": {
            "disclaimer": "NOTE: This document is a TRANSCRIPTION (not the original). Signatures and signer details have been omitted for privacy. The original signed version is available upon request.",
            "title": "Letter of Recommendation",
            "p1": 'The Executive Secretary of Fundación CEIS Orientación, part of the educational network of the Marist Brothers Congregation in Chile, certifies that Mr. Vladimir Acuña Valdebenito was an employee of our foundation from May 1, 2011 to October 30, 2025.',
            "p2": 'We hereby state that Mr. Vladimir Acuña worked as an Analyst and Software Developer at our Foundation, where he was responsible for designing, updating, and supporting the assessment area, especially through the PCA platforms (learning assessments) and Psychoeducational Batteries (assessments covering different areas of the social and personal development of the evaluated students). His duties included support for mailing and the website, programming, systems analysis, and server administration. In his work, he stood out for his responsibility, dedication to his duties, and his commitment to continuous learning and staying current with technological changes. His work involved interacting both with clients (school staff) and with other professionals within our Foundation. We especially value his contribution during the pandemic period, when a large part of our services had to be moved online in a very short time, a task to which Mr. Acuña made a fundamental contribution.',
            "p3": 'The reason for his separation from the organization was directly related to an organizational redesign, due to changes in the market for the products in the area where he worked. These changes required a reduction in staff and associated costs in order to ensure the Foundation\'s sustainability. Therefore, we are pleased to recommend his work, and we are confident that he will be a valuable asset to other institutions requiring his services.',
            "p4": 'Should you require any further details, contact information is available upon request.',
            "date": "Santiago, January 12, 2026",
        },
        "pt": {
            "disclaimer": "NOTA: Este documento é uma TRANSCRIÇÃO (não é o original). Assinaturas e dados do signatário foram omitidos por privacidade. A versão original assinada está disponível mediante solicitação.",
            "title": "Carta de Recomendação",
            "p1": 'O Secretário Executivo da Fundação CEIS Orientación, pertencente à rede educativa da Congregação dos Irmãos Maristas no Chile, certifica que o Sr. Vladimir Acuña Valdebenito foi colaborador de nossa fundação, durante o período compreendido entre 01 de maio de 2011 e 30 de outubro de 2025.',
            "p2": 'Deixamos constância de que o Sr. Vladimir Acuña desempenhou funções como Analista e Desenvolvedor de Programação em nossa Fundação, sendo responsável por projetar, atualizar e dar suporte à área de avaliação, especialmente através das plataformas PCA (avaliações de aprendizagem) e Baterias Psicoeducativas (avaliações de diferentes áreas do desenvolvimento social e pessoal dos estudantes avaliados). Entre suas funções estiveram: suporte de mailing e página web, programação, análise de sistemas e administração de servidores. Em seu trabalho, ele se destacou pela responsabilidade, dedicação às tarefas e interesse pelo estudo e por manter-se sempre atualizado com as mudanças tecnológicas. Seu trabalho envolveu relacionar-se tanto com clientes (pessoal de escolas) quanto com outros profissionais de nossa Fundação. Valorizamos especialmente sua contribuição durante o período da pandemia, quando grande parte de nossos serviços precisaram ser migrados para formatos online em tempo muito breve, tarefa que contou com a contribuição fundamental do Sr. Acuña.',
            "p3": 'A razão de seu desligamento está diretamente associada a causas relacionadas ao redesenho organizacional, devido a uma mudança no mercado dos produtos da área em que ele trabalhou, o que obrigou a uma redução de pessoal e custos associados para garantir a sustentabilidade da Fundação. Diante do exposto, temos o prazer de recomendar seu trabalho, que sem dúvida será uma contribuição valiosa em outras instituições que necessitem de seus serviços.',
            "p4": 'Para quaisquer detalhes adicionais que necessitem, informações de contato disponíveis mediante solicitação.',
            "date": "Santiago, 12 de janeiro de 2026",
        },
        "it": {
            "disclaimer": "NOTA: Questo documento è una TRASCRIZIONE (non è l'originale). Firme e dati del firmatario sono stati omessi per motivi di privacy. La versione originale firmata è disponibile su richiesta.",
            "title": "Lettera di Raccomandazione",
            "p1": 'Il Segretario Esecutivo della Fondazione CEIS Orientación, appartenente alla rete educativa della Congregazione dei Fratelli Maristi in Cile, certifica che il Sig. Vladimir Acuña Valdebenito è stato collaboratore della nostra fondazione, durante il periodo compreso tra il 1° maggio 2011 e il 30 ottobre 2025.',
            "p2": 'Attestiamo che il Sig. Vladimir Acuña ha svolto il ruolo di Analista e Sviluppatore di Programmazione presso la nostra Fondazione, con il compito di progettare, aggiornare e fornire supporto all\'area di valutazione, in particolare attraverso le piattaforme PCA (valutazioni dell\'apprendimento) e le Batterie Psicoeducative (valutazioni di diverse aree dello sviluppo sociale e personale degli studenti valutati). Tra le sue mansioni figuravano: supporto mailing e sito web, programmazione, analisi di sistemi e amministrazione server. Nel suo lavoro si è distinto per responsabilità, dedizione alle mansioni assegnate e interesse per lo studio e l\'aggiornamento costante rispetto ai cambiamenti tecnologici. Il suo lavoro ha comportato l\'interazione sia con clienti (personale scolastico) sia con altri professionisti della nostra Fondazione. Apprezziamo in modo particolare il suo contributo durante il periodo della pandemia, quando gran parte dei nostri servizi ha dovuto essere trasferita online in tempi molto brevi, un compito in cui il Sig. Acuña ha fornito un contributo fondamentale.',
            "p3": 'La ragione della sua separazione è direttamente legata a cause associate alla riorganizzazione aziendale, dovuta a un cambiamento nel mercato dei prodotti dell\'area in cui lavorava, che ha reso necessaria una riduzione del personale e dei costi associati per garantire la sostenibilità della Fondazione. Pertanto, raccomandiamo con piacere il suo operato, certi che sarà un valore aggiunto per altre istituzioni che necessitino dei suoi servizi.',
            "p4": 'Per qualsiasi ulteriore dettaglio, le informazioni di contatto sono disponibili su richiesta.',
            "date": "Santiago, 12 gennaio 2026",
        },
        "fr": {
            "disclaimer": "NOTE : Ce document est une TRANSCRIPTION (ce n'est pas l'original). Les signatures et les données du signataire ont été omises pour des raisons de confidentialité. La version originale signée est disponible sur demande.",
            "title": "Lettre de Recommandation",
            "p1": 'Le Secrétaire Exécutif de la Fondation CEIS Orientación, appartenant au réseau éducatif de la Congrégation des Frères Maristes au Chili, certifie que M. Vladimir Acuña Valdebenito a été collaborateur de notre fondation, pendant la période comprise entre le 1er mai 2011 et le 30 octobre 2025.',
            "p2": 'Nous attestons que M. Vladimir Acuña a exercé les fonctions d\'Analyste et Développeur de Programmation au sein de notre Fondation, étant chargé de concevoir, mettre à jour et assurer le support du domaine d\'évaluation, notamment à travers les plateformes PCA (évaluations d\'apprentissage) et les Batteries Psychoéducatives (évaluations de différents domaines du développement social et personnel des élèves évalués). Parmi ses fonctions figuraient : le support mailing et site web, la programmation, l\'analyse de systèmes et l\'administration de serveurs. Dans son travail, il s\'est distingué par sa responsabilité, son dévouement à ses tâches et son intérêt pour l\'étude et la mise à jour constante face aux changements technologiques. Son travail impliquait des interactions tant avec les clients (personnel des établissements scolaires) qu\'avec d\'autres professionnels de notre Fondation. Nous apprécions tout particulièrement sa contribution pendant la période de pandémie, lorsqu\'une grande partie de nos services a dû être transférée en ligne dans un délai très court, une tâche à laquelle M. Acuña a apporté une contribution fondamentale.',
            "p3": 'La raison de son départ est directement liée à des causes associées à la réorganisation de l\'organisation, en raison d\'un changement du marché des produits du domaine dans lequel il travaillait, ce qui a nécessité une réduction du personnel et des coûts associés afin d\'assurer la pérennité de la Fondation. C\'est pourquoi nous recommandons avec plaisir son travail, convaincus qu\'il sera un atout précieux pour d\'autres institutions ayant besoin de ses services.',
            "p4": 'Pour tout renseignement complémentaire, les coordonnées sont disponibles sur demande.',
            "date": "Santiago, le 12 janvier 2026",
        },
        "zh": {
            "disclaimer": "注意：本文件为转录件（非原件）。出于隐私考虑，已省略签名和签署人信息。签署原件可应要求提供。",
            "title": "推荐信",
            "p1": '智利马利斯特兄弟会教育网络所属CEIS Orientación基金会执行秘书特此证明，Vladimir Acuña Valdebenito先生于2011年5月1日至2025年10月30日期间在本基金会工作。',
            "p2": '我们特此声明，Vladimir Acuña先生在本基金会担任分析师和程序开发人员，负责设计、更新和支持评估领域，尤其是通过PCA平台（学习评估）和心理教育测评系统（对被评估学生社会和个人发展不同领域的评估）。他的职责包括：邮件和网站支持、编程、系统分析和服务器管理。在工作中，他以责任心、敬业精神以及对学习和紧跟技术变革的热情而著称。他的工作涉及与客户（学校工作人员）和基金会其他专业人员的互动。我们特别赞赏他在疫情期间的贡献，当时我们的大部分服务需要在极短时间内转移到线上，而Acuña先生在其中做出了根本性的贡献。',
            "p3": '其离职原因直接与组织重组有关，由于其所在领域产品市场的变化，基金会不得不缩减人员和相关成本以确保可持续发展。因此，我们非常乐意推荐他的工作，相信他将成为需要其服务的其他机构的宝贵人才。',
            "p4": '如需更多详细信息，联系方式可应要求提供。',
            "date": "圣地亚哥，2026年1月12日",
        },
    }
    return T[lang]


LANG_SUFFIX = {
    "es": "", "en": "-english", "pt": "-portuguese",
    "it": "-italian", "fr": "-french", "zh": "-chinese",
}


def build_letter(lang, output_path):
    T = get_content(lang)
    s = make_styles()

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        leftMargin=1.0 * inch, rightMargin=1.0 * inch,
        topMargin=0.6 * inch, bottomMargin=0.8 * inch,
    )

    story = []

    # Disclaimer
    story.append(Paragraph(T["disclaimer"], s["disclaimer"]))
    story.append(Spacer(1, 12))

    # CEIS logo placeholder — draw text-based logo reference
    logo_style = ParagraphStyle(
        "LogoRef", fontName="Helvetica-Bold", fontSize=14, leading=18,
        textColor=HexColor("#3a7ca5"), alignment=TA_LEFT, spaceAfter=6,
    )
    logo_sub = ParagraphStyle(
        "LogoSub", fontName="Helvetica", fontSize=8, leading=10,
        textColor=HexColor("#3a7ca5"), alignment=TA_LEFT, spaceAfter=20,
    )
    story.append(Paragraph("CEIS", logo_style))
    story.append(Paragraph("MARISTA", logo_sub))

    # Title
    story.append(Paragraph(f"<b>{T['title']}</b>", s["title"]))
    story.append(Spacer(1, 10))

    # Body paragraphs
    story.append(Paragraph(T["p1"], s["body_no_indent"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(T["p2"], s["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(T["p3"], s["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(T["p4"], s["body"]))

    # Date
    story.append(Paragraph(T["date"], s["date"]))

    doc.build(story)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  -> {output_path} ({size_kb:.1f} KB)")


def main():
    print("Generating recommendation letters...")
    print("=" * 50)
    for lang in ["es", "en", "pt", "it", "fr", "zh"]:
        suffix = LANG_SUFFIX[lang]
        path = os.path.normpath(os.path.join(ASSETS_DIR, f"carta-recomendacion_sin_firma{suffix}.pdf"))
        build_letter(lang, path)
    print("=" * 50)
    print("Done. 6 recommendation letter PDFs generated.")


if __name__ == "__main__":
    main()
