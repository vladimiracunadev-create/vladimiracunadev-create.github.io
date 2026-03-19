#!/usr/bin/env python3
"""
Generate Professional Achievements Statement PDFs for all 6 languages.
Replicates the format of the existing ES/EN versions:
  - Navy header table with professional info
  - Scope note box
  - 7 numbered sections with headings, bullets, tables
  - Footer with page numbers
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "assets"))

# ── Colors ──
NAVY = HexColor("#2c5282")
DARK = HexColor("#1a1a1a")
MUTED = HexColor("#444444")
LIGHT_BG = HexColor("#f7fafc")
BORDER = HexColor("#cbd5e0")

PAGE_W, PAGE_H = letter

# ── Styles ──
def make_styles():
    return dict(
        main_title=ParagraphStyle(
            "MainTitle", fontName="Helvetica-Bold", fontSize=18, leading=22,
            textColor=DARK, spaceAfter=4, alignment=TA_CENTER,
        ),
        main_subtitle=ParagraphStyle(
            "MainSubtitle", fontName="Helvetica-Oblique", fontSize=11, leading=14,
            textColor=MUTED, spaceAfter=16, alignment=TA_CENTER,
        ),
        section_heading=ParagraphStyle(
            "SectionHeading", fontName="Helvetica-Bold", fontSize=14, leading=18,
            textColor=NAVY, spaceBefore=16, spaceAfter=8,
        ),
        sub_heading=ParagraphStyle(
            "SubHeading", fontName="Helvetica-Bold", fontSize=11, leading=14,
            textColor=NAVY, spaceBefore=10, spaceAfter=4,
        ),
        body=ParagraphStyle(
            "Body", fontName="Helvetica", fontSize=10, leading=13.5,
            textColor=DARK, spaceAfter=4, alignment=TA_JUSTIFY,
        ),
        bullet=ParagraphStyle(
            "Bullet", fontName="Helvetica", fontSize=10, leading=13.5,
            textColor=DARK, spaceAfter=4, leftIndent=18, bulletIndent=6,
            alignment=TA_JUSTIFY,
        ),
        scope_note=ParagraphStyle(
            "ScopeNote", fontName="Helvetica", fontSize=9, leading=12,
            textColor=DARK, spaceAfter=4, alignment=TA_JUSTIFY,
        ),
        important=ParagraphStyle(
            "Important", fontName="Helvetica", fontSize=9, leading=12,
            textColor=MUTED, spaceAfter=4, alignment=TA_JUSTIFY,
        ),
        table_header=ParagraphStyle(
            "TableHeader", fontName="Helvetica-Bold", fontSize=10, leading=13,
            textColor=white,
        ),
        table_header_dark=ParagraphStyle(
            "TableHeaderDark", fontName="Helvetica-Bold", fontSize=10, leading=13,
            textColor=NAVY,
        ),
        table_cell=ParagraphStyle(
            "TableCell", fontName="Helvetica", fontSize=10, leading=13,
            textColor=DARK,
        ),
        footer=ParagraphStyle(
            "Footer", fontName="Helvetica", fontSize=8.5, leading=11,
            textColor=MUTED, alignment=TA_RIGHT,
        ),
    )


# ═══════════════════════════════════════════════════
# TRANSLATIONS
# ═══════════════════════════════════════════════════

def get_content(lang):
    T = {
        # ── SPANISH ──
        "es": {
            "main_title": "DECLARACIÓN DE LOGROS PROFESIONALES",
            "main_subtitle": "con referencia de validación externa",
            "footer_label": "Declaración de Logros Profesionales - Página",
            # Info table
            "lbl_professional": "Profesional",
            "lbl_period": "Período",
            "lbl_organization": "Organización",
            "lbl_document": "Documento",
            "lbl_reference": "Referencia laboral",
            "lbl_email": "Correo institucional",
            "val_period": "Mayo 2011 - 31 octubre 2025",
            "val_document": "Elaborado por el propio profesional",
            # Scope note
            "scope_label": "Nota de alcance.",
            "scope_text": "Este documento fue preparado por el propio profesional como antecedente formal para procesos laborales, de reclutamiento y validación de experiencia. La referencia externa incluida más adelante permite verificar contexto, relación laboral y alcance general de funciones, sin atribuir autoría automática del presente documento al contacto mencionado.",
            # Sections
            "s1_title": "1. Propósito del documento",
            "s1_body": "Dejar constancia, de forma ordenada y profesional, de los principales aportes técnicos, funcionales y de continuidad operacional desarrollados por Vladimir Bernardo Acuña Valdebenito durante su desempeño en Fundación CEIS Marista. El documento busca servir como respaldo curricular y laboral, presentando logros, mejoras observables y competencias demostradas en contextos reales de operación.",
            "s2_title": "2. Contexto general del desempeño",
            "s2_body": "Durante el período señalado, el profesional desempeñó funciones técnicas y estratégicas asociadas al desarrollo, mantenimiento, modernización, soporte, automatización e integración de plataformas utilizadas en entornos productivos reales. Su trabajo combinó análisis, desarrollo full stack, resolución de incidentes, mejora de rendimiento, coordinación técnica y continuidad operacional, atendiendo simultáneamente múltiples frentes de trabajo y restricciones de infraestructura.",
            "s3_title": "3. Principales logros y contribuciones",
            "s3_sub1": "Modernización tecnológica y reducción de deuda técnica",
            "s3_sub1_items": [
                "Participación en procesos de modernización progresiva de sistemas legacy, especialmente en entornos PHP, favoreciendo la transición hacia bases tecnológicas más actuales y mantenibles.",
                "Refactorización y mejora de módulos críticos, elevando legibilidad, mantenibilidad, estabilidad y proyección evolutiva de componentes relevantes.",
                "Preparación técnica de plataformas existentes para su continuidad y mejora futura, incluso en escenarios donde no era posible una renovación integral inmediata.",
            ],
            "s3_sub2": "Rendimiento, estabilidad y continuidad operacional",
            "s3_sub2_items": [
                "Optimización de procesos de ejecución crítica, con reducción de tiempos de respuesta y mejora de la experiencia operativa de usuarios internos y externos.",
                "Atención de incidentes en producción con enfoque analítico, identificando causas, definiendo correcciones y aplicando medidas preventivas para disminuir recurrencias.",
                "Sostenimiento de continuidad operacional en contextos con limitaciones técnicas, resolviendo contingencias con pragmatismo y compromiso con la disponibilidad del servicio.",
            ],
            "s3_sub3": "Migraciones, infraestructura y estandarización",
            "s3_sub3_items": [
                "Participación en migraciones de servidores y plataformas, aportando coordinación técnica para reducir riesgos de interrupción.",
                "Colaboración en la estandarización de configuraciones y entornos, favoreciendo una operación más estable y controlada.",
                "Adaptación de soluciones a infraestructuras restrictivas, obteniendo resultados funcionales aun con recursos limitados.",
            ],
            "s3_sub4": "Automatización, herramientas internas e integraciones",
            "s3_sub4_items": [
                "Diseño e implementación de herramientas y soluciones internas orientadas a resolver necesidades operativas concretas.",
                "Automatización de procesos manuales, disminuyendo carga operativa, errores y tiempos de ejecución.",
                "Soporte e implementación sobre plataformas como LimeSurvey y WordPress, junto con integraciones sobre SQL Server y MySQL.",
            ],
            "s3_sub5": "Comunicaciones, eficiencia e innovación aplicada",
            "s3_sub5_items": [
                "Implementación de procesos de envío masivo de correos mediante PHP y Constant Contact, apoyando la continuidad de las comunicaciones institucionales.",
                "Propuesta de alternativas orientadas a reducción de costos operativos asociados a comunicaciones masivas.",
                "Uso de tecnologías de inteligencia artificial durante 2024 y 2025 como apoyo para análisis, resolución de problemas y exploración de soluciones técnicas.",
            ],
            "s4_title": "4. Resultados observables y mejoras reportadas",
            "s4_items": [
                "Mejoras de desempeño estimadas de hasta un 80% en determinados procesos del sistema, especialmente en generación de reportes y carga de servicios de la plataforma Batería Online, incluyendo traslado de parte de la lógica a JavaScript para optimizar respuesta.",
                "Reducción estimada cercana al 90% en procesos de atención a clientes de la Batería Online entre 2020 y la fecha de desvinculación, sustentada en mejoras de flujo, mayor claridad de instrucciones y mecanismos de continuidad frente a interrupciones o pérdidas de conexión.",
                "Optimización aproximada del 45% en ciertos componentes del sistema de baterías, tanto a nivel de base de datos como de código, mediante eliminación de duplicidades, depuración de estructuras obsoletas y reorganización de información hacia esquemas más eficientes.",
                "Cumplimiento consistente de tareas y entregables, adaptándose tanto a calendarizaciones formales como a cambios de requerimientos surgidos durante el desarrollo.",
                "Resolución anticipada de tareas programadas durante 2025 y, en al menos un caso relevante, evitación de apoyo externo mediante estudio y resolución interna de un problema inicialmente proyectado para nueva contratación.",
                "Atención simultánea de múltiples productos o líneas de trabajo dentro de la institución, llegando en ciertos períodos a intervenir en hasta cinco frentes de manera concurrente.",
            ],
            "s5_title": "5. Competencias evidenciadas",
            "s5_header": ["Competencia", "Descripción"],
            "s5_rows": [
                ["Arquitectura y desarrollo", "Participación full stack en análisis, desarrollo, integración y soporte de plataformas productivas."],
                ["Modernización de sistemas legacy", "Capacidad para evolucionar sistemas existentes sin comprometer la continuidad operacional."],
                ["Optimización de rendimiento", "Mejora de tiempos, procesos críticos y eficiencia funcional."],
                ["Resolución de incidentes", "Diagnóstico, contención y corrección de problemas en producción."],
                ["Automatización y mejora continua", "Diseño de soluciones internas, reducción de tareas manuales y foco permanente en eficiencia."],
            ],
            "s6_title": "6. Referencia de validación externa",
            "s6_intro": "Para fines de verificación de contexto laboral, relación de trabajo y alcance general de funciones, puede utilizarse la siguiente referencia profesional:",
            "s6_lbl_name": "Nombre",
            "s6_lbl_title": "Cargo",
            "s6_lbl_email": "Correo electrónico",
            "s6_lbl_mobile": "Celular",
            "s6_val_title": "Production Manager / Fundación CEIS Orientación",
            "s6_important": "Importante: la referencia anterior se incorpora con el único objeto de facilitar la validación del contexto laboral y profesional. Su inclusión no implica autoría, revisión previa, aprobación escrita ni emisión de este documento por parte de la persona indicada, salvo confirmación expresa posterior.",
            "s7_title": "7. Declaración del profesional",
            "s7_body": "Declaro que la información aquí presentada ha sido elaborada de buena fe, a partir de funciones efectivamente desempeñadas, resultados observados y antecedentes profesionales disponibles. Este documento puede complementarse con CV, portafolio, carta de recomendación, repositorios y otros respaldos que sean solicitados en un proceso de evaluación laboral.",
            "s7_issued_by": "Documento emitido por el profesional",
            "s7_issue_date": "Fecha de emisión: 13 de marzo de 2026",
        },
        # ── ENGLISH ──
        "en": {
            "main_title": "PROFESSIONAL ACHIEVEMENTS STATEMENT",
            "main_subtitle": "with external validation reference",
            "footer_label": "Professional Achievements Statement - Page",
            "lbl_professional": "Professional",
            "lbl_period": "Period",
            "lbl_organization": "Organization",
            "lbl_document": "Document",
            "lbl_reference": "Employment reference",
            "lbl_email": "Institutional email",
            "val_period": "May 2011 - October 31, 2025",
            "val_document": "Prepared by the professional",
            "scope_label": "Scope note.",
            "scope_text": "This document was prepared by the professional as a formal supporting record for employment, recruitment, and experience-validation processes. The external reference included below allows validation of the employment context, working relationship, and general scope of responsibilities, without automatically attributing authorship of this document to the contact mentioned.",
            "s1_title": "1. Purpose of the document",
            "s1_body": "To formally and professionally document the main technical, functional, and operational continuity contributions developed by Vladimir Bernardo Acuña Valdebenito during his tenure at Fundación CEIS Marista. This document is intended to serve as professional and employment support material, presenting achievements, observable improvements, and competencies demonstrated in real operating environments.",
            "s2_title": "2. Overall context of performance",
            "s2_body": "During the stated period, the professional carried out technical and strategic functions related to the development, maintenance, modernization, support, automation, and integration of platforms used in real production environments. This work combined analysis, full-stack development, incident resolution, performance improvement, technical coordination, and operational continuity, while simultaneously addressing multiple workstreams and infrastructure constraints.",
            "s3_title": "3. Main achievements and contributions",
            "s3_sub1": "Technology modernization and technical debt reduction",
            "s3_sub1_items": [
                "Participation in progressive modernization processes for legacy systems, especially in PHP environments, supporting the transition toward more current and maintainable technology foundations.",
                "Refactoring and improvement of critical modules, increasing readability, maintainability, stability, and future evolution potential for relevant components.",
                "Technical preparation of existing platforms for continuity and future improvement, even in scenarios where a full immediate overhaul was not feasible.",
            ],
            "s3_sub2": "Performance, stability, and operational continuity",
            "s3_sub2_items": [
                "Optimization of critical execution processes, reducing response times and improving the operational experience of internal and external users.",
                "Production incident handling with an analytical approach, identifying root causes, defining corrective actions, and applying preventive measures to reduce recurrence.",
                "Maintenance of operational continuity in contexts with technical limitations, resolving contingencies pragmatically and with commitment to service availability.",
            ],
            "s3_sub3": "Migrations, infrastructure, and standardization",
            "s3_sub3_items": [
                "Participation in server and platform migrations, providing technical coordination to reduce interruption risks.",
                "Collaboration in the standardization of configurations and environments, contributing to a more stable and controlled operation.",
                "Adaptation of solutions to restrictive infrastructures, achieving functional results even with limited resources.",
            ],
            "s3_sub4": "Automation, internal tools, and integrations",
            "s3_sub4_items": [
                "Design and implementation of internal tools and solutions aimed at addressing specific operational needs.",
                "Automation of manual processes, reducing operational workload, errors, and execution times.",
                "Support and implementation on platforms such as LimeSurvey and WordPress, together with integrations on SQL Server and MySQL.",
            ],
            "s3_sub5": "Communications, efficiency, and applied innovation",
            "s3_sub5_items": [
                "Implementation of mass email sending processes through PHP and Constant Contact, supporting the continuity of institutional communications.",
                "Proposal of alternatives aimed at reducing operating costs associated with mass communications.",
                "Use of artificial intelligence technologies during 2024 and 2025 to support analysis, problem solving, and the exploration of technical solutions.",
            ],
            "s4_title": "4. Observable results and reported improvements",
            "s4_items": [
                "Estimated performance improvements of up to 80% in certain system processes, especially in report generation and service loading within the Batería Online platform, including the migration of part of the logic to JavaScript to optimize responsiveness.",
                "Estimated reduction of close to 90% in customer support processes for Batería Online between 2020 and the date of separation, supported by workflow improvements, clearer instructions, and continuity mechanisms for interruptions or connection losses.",
                "Approximate 45% optimization in certain components of the battery system, both at the database and code levels, through the elimination of duplication, cleanup of obsolete structures, and reorganization of information into more efficient schemes.",
                "Consistent completion of tasks and deliverables, adapting to both formal schedules and changing requirements arising during development.",
                "Early completion of scheduled tasks during 2025 and, in at least one relevant case, avoidance of external support through internal study and resolution of a problem initially projected to require a new hire.",
                "Simultaneous support for multiple products or work lines within the institution, reaching up to five concurrent fronts during certain periods.",
            ],
            "s5_title": "5. Demonstrated competencies",
            "s5_header": ["Competency", "Description"],
            "s5_rows": [
                ["Architecture and development", "Full-stack involvement in the analysis, development, integration, and support of production platforms."],
                ["Legacy system modernization", "Ability to evolve existing systems without compromising operational continuity."],
                ["Performance optimization", "Improvement of timelines, critical processes, and functional efficiency."],
                ["Incident resolution", "Diagnosis, containment, and correction of production issues."],
                ["Automation and continuous improvement", "Design of internal solutions, reduction of manual tasks, and sustained focus on efficiency."],
            ],
            "s6_title": "6. External validation reference",
            "s6_intro": "For purposes of verifying employment context, working relationship, and general scope of responsibilities, the following professional reference may be used:",
            "s6_lbl_name": "Name",
            "s6_lbl_title": "Title",
            "s6_lbl_email": "Email",
            "s6_lbl_mobile": "Mobile",
            "s6_val_title": "Production Manager / Fundación CEIS Orientación",
            "s6_important": "Important: the above reference is included solely to facilitate validation of the employment and professional context. Its inclusion does not imply authorship, prior review, written approval, or issuance of this document by the person named above, unless later expressly confirmed.",
            "s7_title": "7. Statement by the professional",
            "s7_body": "I declare that the information presented here has been prepared in good faith, based on functions effectively performed, observed results, and available professional background. This document may be supplemented with a CV, portfolio, recommendation letter, repositories, and other supporting materials requested during an employment evaluation process.",
            "s7_issued_by": "Document issued by the professional",
            "s7_issue_date": "Issue date: March 13, 2026",
        },
        # ── PORTUGUESE ──
        "pt": {
            "main_title": "DECLARAÇÃO DE CONQUISTAS PROFISSIONAIS",
            "main_subtitle": "com referência de validação externa",
            "footer_label": "Declaração de Conquistas Profissionais - Página",
            "lbl_professional": "Profissional",
            "lbl_period": "Período",
            "lbl_organization": "Organização",
            "lbl_document": "Documento",
            "lbl_reference": "Referência profissional",
            "lbl_email": "E-mail institucional",
            "val_period": "Maio 2011 - 31 outubro 2025",
            "val_document": "Elaborado pelo próprio profissional",
            "scope_label": "Nota de escopo.",
            "scope_text": "Este documento foi preparado pelo próprio profissional como antecedente formal para processos trabalhistas, de recrutamento e validação de experiência. A referência externa incluída mais adiante permite verificar o contexto, a relação de trabalho e o alcance geral das funções, sem atribuir autoria automática do presente documento ao contato mencionado.",
            "s1_title": "1. Propósito do documento",
            "s1_body": "Registrar, de forma ordenada e profissional, as principais contribuições técnicas, funcionais e de continuidade operacional desenvolvidas por Vladimir Bernardo Acuña Valdebenito durante sua atuação na Fundação CEIS Marista. O documento busca servir como respaldo curricular e profissional, apresentando conquistas, melhorias observáveis e competências demonstradas em contextos reais de operação.",
            "s2_title": "2. Contexto geral do desempenho",
            "s2_body": "Durante o período indicado, o profissional desempenhou funções técnicas e estratégicas associadas ao desenvolvimento, manutenção, modernização, suporte, automação e integração de plataformas utilizadas em ambientes produtivos reais. Seu trabalho combinou análise, desenvolvimento full stack, resolução de incidentes, melhoria de desempenho, coordenação técnica e continuidade operacional, atendendo simultaneamente múltiplas frentes de trabalho e restrições de infraestrutura.",
            "s3_title": "3. Principais conquistas e contribuições",
            "s3_sub1": "Modernização tecnológica e redução de dívida técnica",
            "s3_sub1_items": [
                "Participação em processos de modernização progressiva de sistemas legados, especialmente em ambientes PHP, favorecendo a transição para bases tecnológicas mais atuais e mantíveis.",
                "Refatoração e melhoria de módulos críticos, elevando legibilidade, manutenibilidade, estabilidade e projeção evolutiva de componentes relevantes.",
                "Preparação técnica de plataformas existentes para continuidade e melhoria futura, mesmo em cenários onde não era possível uma renovação integral imediata.",
            ],
            "s3_sub2": "Desempenho, estabilidade e continuidade operacional",
            "s3_sub2_items": [
                "Otimização de processos de execução crítica, com redução de tempos de resposta e melhoria da experiência operativa de usuários internos e externos.",
                "Atendimento de incidentes em produção com abordagem analítica, identificando causas, definindo correções e aplicando medidas preventivas para diminuir recorrências.",
                "Manutenção da continuidade operacional em contextos com limitações técnicas, resolvendo contingências com pragmatismo e compromisso com a disponibilidade do serviço.",
            ],
            "s3_sub3": "Migrações, infraestrutura e padronização",
            "s3_sub3_items": [
                "Participação em migrações de servidores e plataformas, contribuindo com coordenação técnica para reduzir riscos de interrupção.",
                "Colaboração na padronização de configurações e ambientes, favorecendo uma operação mais estável e controlada.",
                "Adaptação de soluções a infraestruturas restritivas, obtendo resultados funcionais mesmo com recursos limitados.",
            ],
            "s3_sub4": "Automação, ferramentas internas e integrações",
            "s3_sub4_items": [
                "Projeto e implementação de ferramentas e soluções internas orientadas a resolver necessidades operacionais concretas.",
                "Automação de processos manuais, diminuindo carga operacional, erros e tempos de execução.",
                "Suporte e implementação em plataformas como LimeSurvey e WordPress, junto com integrações em SQL Server e MySQL.",
            ],
            "s3_sub5": "Comunicações, eficiência e inovação aplicada",
            "s3_sub5_items": [
                "Implementação de processos de envio massivo de e-mails mediante PHP e Constant Contact, apoiando a continuidade das comunicações institucionais.",
                "Proposta de alternativas orientadas à redução de custos operacionais associados a comunicações massivas.",
                "Uso de tecnologias de inteligência artificial durante 2024 e 2025 como apoio para análise, resolução de problemas e exploração de soluções técnicas.",
            ],
            "s4_title": "4. Resultados observáveis e melhorias reportadas",
            "s4_items": [
                "Melhorias de desempenho estimadas de até 80% em determinados processos do sistema, especialmente em geração de relatórios e carregamento de serviços da plataforma Batería Online, incluindo transferência de parte da lógica para JavaScript para otimizar resposta.",
                "Redução estimada próxima a 90% em processos de atendimento a clientes da Batería Online entre 2020 e a data de desligamento, sustentada em melhorias de fluxo, maior clareza de instruções e mecanismos de continuidade frente a interrupções ou perdas de conexão.",
                "Otimização aproximada de 45% em certos componentes do sistema de baterias, tanto a nível de banco de dados quanto de código, mediante eliminação de duplicidades, depuração de estruturas obsoletas e reorganização de informação em esquemas mais eficientes.",
                "Cumprimento consistente de tarefas e entregáveis, adaptando-se tanto a cronogramas formais quanto a mudanças de requisitos surgidas durante o desenvolvimento.",
                "Resolução antecipada de tarefas programadas durante 2025 e, em pelo menos um caso relevante, eliminação da necessidade de apoio externo mediante estudo e resolução interna de um problema inicialmente projetado para nova contratação.",
                "Atendimento simultâneo de múltiplos produtos ou linhas de trabalho dentro da instituição, chegando em certos períodos a intervir em até cinco frentes de maneira concorrente.",
            ],
            "s5_title": "5. Competências evidenciadas",
            "s5_header": ["Competência", "Descrição"],
            "s5_rows": [
                ["Arquitetura e desenvolvimento", "Participação full stack em análise, desenvolvimento, integração e suporte de plataformas produtivas."],
                ["Modernização de sistemas legados", "Capacidade de evoluir sistemas existentes sem comprometer a continuidade operacional."],
                ["Otimização de desempenho", "Melhoria de tempos, processos críticos e eficiência funcional."],
                ["Resolução de incidentes", "Diagnóstico, contenção e correção de problemas em produção."],
                ["Automação e melhoria contínua", "Projeto de soluções internas, redução de tarefas manuais e foco permanente em eficiência."],
            ],
            "s6_title": "6. Referência de validação externa",
            "s6_intro": "Para fins de verificação de contexto laboral, relação de trabalho e alcance geral de funções, pode ser utilizada a seguinte referência profissional:",
            "s6_lbl_name": "Nome",
            "s6_lbl_title": "Cargo",
            "s6_lbl_email": "E-mail",
            "s6_lbl_mobile": "Celular",
            "s6_val_title": "Production Manager / Fundación CEIS Orientación",
            "s6_important": "Importante: a referência acima é incluída com o único objetivo de facilitar a validação do contexto laboral e profissional. Sua inclusão não implica autoria, revisão prévia, aprovação escrita nem emissão deste documento pela pessoa indicada, salvo confirmação expressa posterior.",
            "s7_title": "7. Declaração do profissional",
            "s7_body": "Declaro que as informações aqui apresentadas foram elaboradas de boa-fé, a partir de funções efetivamente desempenhadas, resultados observados e antecedentes profissionais disponíveis. Este documento pode ser complementado com CV, portfólio, carta de recomendação, repositórios e outros respaldos que sejam solicitados em um processo de avaliação profissional.",
            "s7_issued_by": "Documento emitido pelo profissional",
            "s7_issue_date": "Data de emissão: 13 de março de 2026",
        },
        # ── ITALIAN ──
        "it": {
            "main_title": "DICHIARAZIONE DI RISULTATI PROFESSIONALI",
            "main_subtitle": "con riferimento di validazione esterna",
            "footer_label": "Dichiarazione di Risultati Professionali - Pagina",
            "lbl_professional": "Professionista",
            "lbl_period": "Periodo",
            "lbl_organization": "Organizzazione",
            "lbl_document": "Documento",
            "lbl_reference": "Riferimento lavorativo",
            "lbl_email": "E-mail istituzionale",
            "val_period": "Maggio 2011 - 31 ottobre 2025",
            "val_document": "Redatto dal professionista stesso",
            "scope_label": "Nota di ambito.",
            "scope_text": "Questo documento è stato preparato dal professionista stesso come antecedente formale per processi lavorativi, di reclutamento e validazione dell'esperienza. Il riferimento esterno incluso di seguito consente di verificare il contesto, il rapporto di lavoro e l'ambito generale delle funzioni, senza attribuire automaticamente la paternità del presente documento al contatto menzionato.",
            "s1_title": "1. Scopo del documento",
            "s1_body": "Documentare, in modo ordinato e professionale, i principali contributi tecnici, funzionali e di continuità operativa sviluppati da Vladimir Bernardo Acuña Valdebenito durante il suo operato presso la Fondazione CEIS Marista. Il documento intende servire come supporto curriculare e professionale, presentando risultati, miglioramenti osservabili e competenze dimostrate in contesti operativi reali.",
            "s2_title": "2. Contesto generale delle prestazioni",
            "s2_body": "Durante il periodo indicato, il professionista ha svolto funzioni tecniche e strategiche associate allo sviluppo, manutenzione, modernizzazione, supporto, automazione e integrazione di piattaforme utilizzate in ambienti produttivi reali. Il suo lavoro ha combinato analisi, sviluppo full stack, risoluzione di incidenti, miglioramento delle prestazioni, coordinamento tecnico e continuità operativa, gestendo simultaneamente molteplici fronti di lavoro e vincoli infrastrutturali.",
            "s3_title": "3. Principali risultati e contributi",
            "s3_sub1": "Modernizzazione tecnologica e riduzione del debito tecnico",
            "s3_sub1_items": [
                "Partecipazione a processi di modernizzazione progressiva di sistemi legacy, specialmente in ambienti PHP, favorendo la transizione verso basi tecnologiche più attuali e manutenibili.",
                "Refactoring e miglioramento di moduli critici, aumentando leggibilità, manutenibilità, stabilità e potenziale evolutivo dei componenti rilevanti.",
                "Preparazione tecnica delle piattaforme esistenti per la continuità e il miglioramento futuro, anche in scenari dove non era possibile un rinnovamento integrale immediato.",
            ],
            "s3_sub2": "Prestazioni, stabilità e continuità operativa",
            "s3_sub2_items": [
                "Ottimizzazione di processi di esecuzione critica, con riduzione dei tempi di risposta e miglioramento dell'esperienza operativa degli utenti interni ed esterni.",
                "Gestione degli incidenti in produzione con approccio analitico, identificando le cause, definendo azioni correttive e applicando misure preventive per ridurre le ricorrenze.",
                "Mantenimento della continuità operativa in contesti con limitazioni tecniche, risolvendo le contingenze con pragmatismo e impegno per la disponibilità del servizio.",
            ],
            "s3_sub3": "Migrazioni, infrastruttura e standardizzazione",
            "s3_sub3_items": [
                "Partecipazione a migrazioni di server e piattaforme, fornendo coordinamento tecnico per ridurre i rischi di interruzione.",
                "Collaborazione nella standardizzazione di configurazioni e ambienti, contribuendo a un'operazione più stabile e controllata.",
                "Adattamento di soluzioni a infrastrutture restrittive, ottenendo risultati funzionali anche con risorse limitate.",
            ],
            "s3_sub4": "Automazione, strumenti interni e integrazioni",
            "s3_sub4_items": [
                "Progettazione e implementazione di strumenti e soluzioni interne orientate a risolvere esigenze operative concrete.",
                "Automazione di processi manuali, riducendo il carico operativo, gli errori e i tempi di esecuzione.",
                "Supporto e implementazione su piattaforme come LimeSurvey e WordPress, insieme a integrazioni su SQL Server e MySQL.",
            ],
            "s3_sub5": "Comunicazioni, efficienza e innovazione applicata",
            "s3_sub5_items": [
                "Implementazione di processi di invio massivo di e-mail tramite PHP e Constant Contact, supportando la continuità delle comunicazioni istituzionali.",
                "Proposta di alternative orientate alla riduzione dei costi operativi associati alle comunicazioni massive.",
                "Utilizzo di tecnologie di intelligenza artificiale durante il 2024 e 2025 come supporto per analisi, risoluzione di problemi ed esplorazione di soluzioni tecniche.",
            ],
            "s4_title": "4. Risultati osservabili e miglioramenti riportati",
            "s4_items": [
                "Miglioramenti delle prestazioni stimati fino all'80% in determinati processi del sistema, specialmente nella generazione di report e nel caricamento dei servizi della piattaforma Batería Online, incluso il trasferimento di parte della logica a JavaScript per ottimizzare la reattività.",
                "Riduzione stimata vicina al 90% nei processi di assistenza clienti della Batería Online tra il 2020 e la data di separazione, supportata da miglioramenti del flusso, maggiore chiarezza delle istruzioni e meccanismi di continuità per interruzioni o perdite di connessione.",
                "Ottimizzazione approssimativa del 45% in alcuni componenti del sistema di batterie, sia a livello di database che di codice, mediante eliminazione di duplicazioni, pulizia di strutture obsolete e riorganizzazione delle informazioni in schemi più efficienti.",
                "Completamento consistente di compiti e deliverable, adattandosi sia a pianificazioni formali che a cambiamenti di requisiti emersi durante lo sviluppo.",
                "Completamento anticipato di compiti programmati durante il 2025 e, in almeno un caso rilevante, evitamento di supporto esterno mediante studio e risoluzione interna di un problema inizialmente previsto per una nuova assunzione.",
                "Supporto simultaneo di molteplici prodotti o linee di lavoro all'interno dell'istituzione, arrivando in certi periodi a intervenire su fino a cinque fronti in modo concorrente.",
            ],
            "s5_title": "5. Competenze dimostrate",
            "s5_header": ["Competenza", "Descrizione"],
            "s5_rows": [
                ["Architettura e sviluppo", "Coinvolgimento full stack nell'analisi, sviluppo, integrazione e supporto di piattaforme produttive."],
                ["Modernizzazione di sistemi legacy", "Capacità di evolvere sistemi esistenti senza compromettere la continuità operativa."],
                ["Ottimizzazione delle prestazioni", "Miglioramento dei tempi, processi critici ed efficienza funzionale."],
                ["Risoluzione di incidenti", "Diagnosi, contenimento e correzione di problemi in produzione."],
                ["Automazione e miglioramento continuo", "Progettazione di soluzioni interne, riduzione di compiti manuali e focus permanente sull'efficienza."],
            ],
            "s6_title": "6. Riferimento di validazione esterna",
            "s6_intro": "Per fini di verifica del contesto lavorativo, del rapporto di lavoro e dell'ambito generale delle funzioni, può essere utilizzato il seguente riferimento professionale:",
            "s6_lbl_name": "Nome",
            "s6_lbl_title": "Carica",
            "s6_lbl_email": "E-mail",
            "s6_lbl_mobile": "Cellulare",
            "s6_val_title": "Production Manager / Fundación CEIS Orientación",
            "s6_important": "Importante: il riferimento sopra indicato è incluso al solo scopo di facilitare la validazione del contesto lavorativo e professionale. La sua inclusione non implica paternità, revisione preventiva, approvazione scritta né emissione di questo documento da parte della persona indicata, salvo conferma espressa successiva.",
            "s7_title": "7. Dichiarazione del professionista",
            "s7_body": "Dichiaro che le informazioni qui presentate sono state elaborate in buona fede, a partire da funzioni effettivamente svolte, risultati osservati e precedenti professionali disponibili. Questo documento può essere integrato con CV, portfolio, lettera di raccomandazione, repository e altri materiali di supporto richiesti durante un processo di valutazione professionale.",
            "s7_issued_by": "Documento emesso dal professionista",
            "s7_issue_date": "Data di emissione: 13 marzo 2026",
        },
        # ── FRENCH ──
        "fr": {
            "main_title": "DÉCLARATION DE RÉALISATIONS PROFESSIONNELLES",
            "main_subtitle": "avec référence de validation externe",
            "footer_label": "Déclaration de Réalisations Professionnelles - Page",
            "lbl_professional": "Professionnel",
            "lbl_period": "Période",
            "lbl_organization": "Organisation",
            "lbl_document": "Document",
            "lbl_reference": "Référence professionnelle",
            "lbl_email": "E-mail institutionnel",
            "val_period": "Mai 2011 - 31 octobre 2025",
            "val_document": "Rédigé par le professionnel lui-même",
            "scope_label": "Note de portée.",
            "scope_text": "Ce document a été préparé par le professionnel lui-même comme antécédent formel pour des processus d'emploi, de recrutement et de validation d'expérience. La référence externe incluse ci-dessous permet de vérifier le contexte, la relation de travail et la portée générale des fonctions, sans attribuer automatiquement la paternité du présent document au contact mentionné.",
            "s1_title": "1. Objet du document",
            "s1_body": "Consigner, de manière ordonnée et professionnelle, les principales contributions techniques, fonctionnelles et de continuité opérationnelle développées par Vladimir Bernardo Acuña Valdebenito au cours de son activité à la Fondation CEIS Marista. Ce document vise à servir de support curriculaire et professionnel, présentant des réalisations, des améliorations observables et des compétences démontrées dans des contextes opérationnels réels.",
            "s2_title": "2. Contexte général des performances",
            "s2_body": "Au cours de la période indiquée, le professionnel a exercé des fonctions techniques et stratégiques liées au développement, à la maintenance, à la modernisation, au support, à l'automatisation et à l'intégration de plateformes utilisées dans des environnements de production réels. Son travail a combiné analyse, développement full stack, résolution d'incidents, amélioration des performances, coordination technique et continuité opérationnelle, tout en gérant simultanément de multiples fronts de travail et contraintes d'infrastructure.",
            "s3_title": "3. Principales réalisations et contributions",
            "s3_sub1": "Modernisation technologique et réduction de la dette technique",
            "s3_sub1_items": [
                "Participation à des processus de modernisation progressive de systèmes legacy, notamment dans des environnements PHP, favorisant la transition vers des bases technologiques plus actuelles et maintenables.",
                "Refactoring et amélioration de modules critiques, augmentant la lisibilité, la maintenabilité, la stabilité et le potentiel d'évolution des composants pertinents.",
                "Préparation technique des plateformes existantes pour leur continuité et amélioration future, même dans des scénarios où un renouvellement intégral immédiat n'était pas possible.",
            ],
            "s3_sub2": "Performance, stabilité et continuité opérationnelle",
            "s3_sub2_items": [
                "Optimisation des processus d'exécution critique, avec réduction des temps de réponse et amélioration de l'expérience opérationnelle des utilisateurs internes et externes.",
                "Traitement des incidents en production avec une approche analytique, identifiant les causes, définissant des actions correctives et appliquant des mesures préventives pour réduire les récurrences.",
                "Maintien de la continuité opérationnelle dans des contextes avec des limitations techniques, résolvant les contingences avec pragmatisme et engagement envers la disponibilité du service.",
            ],
            "s3_sub3": "Migrations, infrastructure et standardisation",
            "s3_sub3_items": [
                "Participation aux migrations de serveurs et plateformes, fournissant une coordination technique pour réduire les risques d'interruption.",
                "Collaboration à la standardisation des configurations et environnements, contribuant à une exploitation plus stable et contrôlée.",
                "Adaptation des solutions aux infrastructures restrictives, obtenant des résultats fonctionnels même avec des ressources limitées.",
            ],
            "s3_sub4": "Automatisation, outils internes et intégrations",
            "s3_sub4_items": [
                "Conception et implémentation d'outils et solutions internes visant à répondre à des besoins opérationnels concrets.",
                "Automatisation de processus manuels, réduisant la charge opérationnelle, les erreurs et les temps d'exécution.",
                "Support et implémentation sur des plateformes telles que LimeSurvey et WordPress, ainsi que des intégrations sur SQL Server et MySQL.",
            ],
            "s3_sub5": "Communications, efficacité et innovation appliquée",
            "s3_sub5_items": [
                "Mise en place de processus d'envoi massif d'e-mails via PHP et Constant Contact, soutenant la continuité des communications institutionnelles.",
                "Proposition d'alternatives visant à réduire les coûts opérationnels liés aux communications de masse.",
                "Utilisation de technologies d'intelligence artificielle en 2024 et 2025 comme support d'analyse, de résolution de problèmes et d'exploration de solutions techniques.",
            ],
            "s4_title": "4. Résultats observables et améliorations rapportées",
            "s4_items": [
                "Améliorations de performance estimées jusqu'à 80 % dans certains processus du système, notamment dans la génération de rapports et le chargement de services de la plateforme Batería Online, incluant le transfert d'une partie de la logique vers JavaScript pour optimiser la réactivité.",
                "Réduction estimée proche de 90 % dans les processus de support client de la Batería Online entre 2020 et la date de séparation, soutenue par des améliorations de flux, des instructions plus claires et des mécanismes de continuité face aux interruptions ou pertes de connexion.",
                "Optimisation approximative de 45 % dans certains composants du système de batteries, tant au niveau de la base de données que du code, par élimination des doublons, nettoyage des structures obsolètes et réorganisation de l'information en schémas plus efficaces.",
                "Accomplissement constant des tâches et livrables, s'adaptant aussi bien aux planifications formelles qu'aux changements de besoins apparus en cours de développement.",
                "Réalisation anticipée de tâches programmées en 2025 et, dans au moins un cas pertinent, évitement d'un recours externe par étude et résolution interne d'un problème initialement prévu pour une nouvelle embauche.",
                "Support simultané de multiples produits ou lignes de travail au sein de l'institution, atteignant jusqu'à cinq fronts concurrents pendant certaines périodes.",
            ],
            "s5_title": "5. Compétences démontrées",
            "s5_header": ["Compétence", "Description"],
            "s5_rows": [
                ["Architecture et développement", "Implication full stack dans l'analyse, le développement, l'intégration et le support de plateformes de production."],
                ["Modernisation de systèmes legacy", "Capacité à faire évoluer des systèmes existants sans compromettre la continuité opérationnelle."],
                ["Optimisation des performances", "Amélioration des délais, processus critiques et efficacité fonctionnelle."],
                ["Résolution d'incidents", "Diagnostic, confinement et correction de problèmes en production."],
                ["Automatisation et amélioration continue", "Conception de solutions internes, réduction des tâches manuelles et focus permanent sur l'efficacité."],
            ],
            "s6_title": "6. Référence de validation externe",
            "s6_intro": "Aux fins de vérification du contexte professionnel, de la relation de travail et de la portée générale des fonctions, la référence professionnelle suivante peut être utilisée :",
            "s6_lbl_name": "Nom",
            "s6_lbl_title": "Poste",
            "s6_lbl_email": "E-mail",
            "s6_lbl_mobile": "Mobile",
            "s6_val_title": "Production Manager / Fundación CEIS Orientación",
            "s6_important": "Important : la référence ci-dessus est incluse dans le seul but de faciliter la validation du contexte professionnel et d'emploi. Son inclusion n'implique pas la paternité, la révision préalable, l'approbation écrite ni l'émission de ce document par la personne nommée ci-dessus, sauf confirmation expresse ultérieure.",
            "s7_title": "7. Déclaration du professionnel",
            "s7_body": "Je déclare que les informations présentées ici ont été élaborées de bonne foi, à partir de fonctions effectivement exercées, de résultats observés et d'antécédents professionnels disponibles. Ce document peut être complété par un CV, un portfolio, une lettre de recommandation, des dépôts et d'autres documents justificatifs demandés lors d'un processus d'évaluation professionnelle.",
            "s7_issued_by": "Document émis par le professionnel",
            "s7_issue_date": "Date d'émission : 13 mars 2026",
        },
        # ── CHINESE ──
        "zh": {
            "main_title": "专业成就声明",
            "main_subtitle": "附外部验证参考",
            "footer_label": "专业成就声明 - 第",
            "lbl_professional": "专业人员",
            "lbl_period": "期间",
            "lbl_organization": "组织",
            "lbl_document": "文件",
            "lbl_reference": "工作推荐人",
            "lbl_email": "机构邮箱",
            "val_period": "2011年5月 - 2025年10月31日",
            "val_document": "由本人编写",
            "scope_label": "范围说明。",
            "scope_text": "本文件由专业人员本人作为就业、招聘和经验验证流程的正式支持记录而编写。下文包含的外部参考允许验证就业背景、工作关系和职责的一般范围，而不自动将本文件的署名权归于所提及的联系人。",
            "s1_title": "1. 文件目的",
            "s1_body": "以有序和专业的方式正式记录Vladimir Bernardo Acuña Valdebenito在CEIS Marista基金会任职期间的主要技术、功能和运营连续性贡献。本文件旨在作为简历和就业支持材料，展示在实际运营环境中证明的成就、可观察到的改进和能力。",
            "s2_title": "2. 工作表现总体背景",
            "s2_body": "在上述期间，该专业人员执行了与实际生产环境中使用的平台的开发、维护、现代化、支持、自动化和集成相关的技术和战略职能。其工作结合了分析、全栈开发、事件解决、性能改进、技术协调和运营连续性，同时处理多个工作线和基础设施限制。",
            "s3_title": "3. 主要成就和贡献",
            "s3_sub1": "技术现代化和技术债务减少",
            "s3_sub1_items": [
                "参与遗留系统的渐进式现代化过程，特别是在PHP环境中，支持向更现代和可维护的技术基础过渡。",
                "重构和改进关键模块，提高相关组件的可读性、可维护性、稳定性和未来演进潜力。",
                "为现有平台的连续性和未来改进做好技术准备，即使在无法立即进行全面更新的场景中也是如此。",
            ],
            "s3_sub2": "性能、稳定性和运营连续性",
            "s3_sub2_items": [
                "优化关键执行流程，减少响应时间，改善内部和外部用户的运营体验。",
                "以分析方法处理生产事件，识别根本原因，定义纠正措施，并应用预防措施以减少再发生。",
                "在技术受限的环境中维持运营连续性，以务实的态度和对服务可用性的承诺解决突发情况。",
            ],
            "s3_sub3": "迁移、基础设施和标准化",
            "s3_sub3_items": [
                "参与服务器和平台迁移，提供技术协调以减少中断风险。",
                "协助配置和环境的标准化，促进更稳定和可控的运营。",
                "将解决方案适配受限的基础设施，即使资源有限也能获得功能性成果。",
            ],
            "s3_sub4": "自动化、内部工具和集成",
            "s3_sub4_items": [
                "设计和实施面向解决具体运营需求的内部工具和解决方案。",
                "自动化手动流程，减少运营负担、错误和执行时间。",
                "在LimeSurvey和WordPress等平台上提供支持和实施，以及在SQL Server和MySQL上的集成。",
            ],
            "s3_sub5": "通信、效率和应用创新",
            "s3_sub5_items": [
                "通过PHP和Constant Contact实施大规模邮件发送流程，支持机构通信的连续性。",
                "提出旨在降低与大规模通信相关的运营成本的替代方案。",
                "在2024年和2025年使用人工智能技术作为分析、问题解决和技术解决方案探索的支持。",
            ],
            "s4_title": "4. 可观察到的成果和报告的改进",
            "s4_items": [
                "某些系统流程中估计性能提升高达80%，特别是在Batería Online平台的报告生成和服务加载方面，包括将部分逻辑迁移到JavaScript以优化响应。",
                "2020年至离职日期之间，Batería Online的客户支持流程估计减少近90%，得益于流程改进、更清晰的说明以及应对中断或连接丢失的连续性机制。",
                "电池系统某些组件在数据库和代码层面约45%的优化，通过消除重复、清理过时结构和将信息重组为更高效的架构。",
                "持续完成任务和可交付成果，适应正式计划和开发过程中出现的需求变更。",
                "在2025年提前完成计划任务，并且在至少一个相关案例中，通过内部研究和解决避免了外部支持，该问题最初计划需要新招聘。",
                "同时支持机构内的多个产品或工作线，在某些时期达到五个并发前线。",
            ],
            "s5_title": "5. 已证明的能力",
            "s5_header": ["能力", "描述"],
            "s5_rows": [
                ["架构和开发", "全栈参与生产平台的分析、开发、集成和支持。"],
                ["遗留系统现代化", "在不影响运营连续性的情况下演进现有系统的能力。"],
                ["性能优化", "改进时间线、关键流程和功能效率。"],
                ["事件解决", "生产问题的诊断、遏制和纠正。"],
                ["自动化和持续改进", "设计内部解决方案，减少手动任务，持续关注效率。"],
            ],
            "s6_title": "6. 外部验证参考",
            "s6_intro": "为验证就业背景、工作关系和职责的一般范围，可使用以下专业参考：",
            "s6_lbl_name": "姓名",
            "s6_lbl_title": "职位",
            "s6_lbl_email": "电子邮件",
            "s6_lbl_mobile": "手机",
            "s6_val_title": "Production Manager / Fundación CEIS Orientación",
            "s6_important": "重要提示：上述参考的纳入仅为便于验证就业和专业背景。其纳入不意味着上述人员对本文件的署名、事先审查、书面批准或签发，除非后续明确确认。",
            "s7_title": "7. 专业人员声明",
            "s7_body": "本人声明，此处呈现的信息是基于实际执行的职能、观察到的结果和可用的专业背景，以诚信原则编写的。本文件可由简历、作品集、推荐信、代码库和就业评估过程中要求的其他支持材料补充。",
            "s7_issued_by": "由专业人员签发的文件",
            "s7_issue_date": "签发日期：2026年3月13日",
        },
    }
    return T[lang]


LANG_SUFFIX = {
    "es": "", "en": "-english", "pt": "-portuguese",
    "it": "-italian", "fr": "-french", "zh": "-chinese",
}


class AchievementsDoc(SimpleDocTemplate):
    """Custom doc to add page footer."""
    def __init__(self, *args, footer_label="", **kwargs):
        self._footer_label = footer_label
        super().__init__(*args, **kwargs)

    def afterPage(self):
        canvas = self.canv
        page_num = canvas.getPageNumber()
        canvas.saveState()
        canvas.setFont("Helvetica", 8.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(
            PAGE_W - 0.7 * inch, 0.45 * inch,
            f"{self._footer_label} {page_num}"
        )
        canvas.restoreState()


def build_statement(lang, output_path):
    T = get_content(lang)
    s = make_styles()

    doc = AchievementsDoc(
        output_path, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.6 * inch, bottomMargin=0.7 * inch,
        footer_label=T["footer_label"],
    )

    story = []
    usable_w = PAGE_W - 1.4 * inch

    # ── Title ──
    story.append(Paragraph(f"<b>{T['main_title']}</b>", s["main_title"]))
    story.append(Paragraph(T["main_subtitle"], s["main_subtitle"]))

    # ── Info table ──
    info_data = [
        [Paragraph(f"<b>{T['lbl_professional']}</b>", s["table_header_dark"]),
         Paragraph("Vladimir Bernardo Acuña Valdebenito", s["table_cell"]),
         Paragraph(f"<b>{T['lbl_period']}</b>", s["table_header_dark"]),
         Paragraph(T["val_period"], s["table_cell"])],
        [Paragraph(f"<b>{T['lbl_organization']}</b>", s["table_header_dark"]),
         Paragraph("Fundación CEIS Marista", s["table_cell"]),
         Paragraph(f"<b>{T['lbl_document']}</b>", s["table_header_dark"]),
         Paragraph(T["val_document"], s["table_cell"])],
        [Paragraph(f"<b>{T['lbl_reference']}</b>", s["table_header_dark"]),
         Paragraph("Jean Claude Dupry", s["table_cell"]),
         Paragraph(f"<b>{T['lbl_email']}</b>", s["table_header_dark"]),
         Paragraph("jdupry@ceismaristas.cl", s["table_cell"])],
    ]
    col_w = [usable_w * 0.20, usable_w * 0.30, usable_w * 0.22, usable_w * 0.28]
    info_table = Table(info_data, colWidths=col_w)
    info_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
        ("BACKGROUND", (2, 0), (2, -1), LIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 12))

    # ── Scope note box ──
    scope_content = f"<b>{T['scope_label']}</b> {T['scope_text']}"
    scope_tbl = Table([[Paragraph(scope_content, s["scope_note"])]], colWidths=[usable_w - 12])
    scope_tbl.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(scope_tbl)
    story.append(Spacer(1, 8))

    # ── Section 1 ──
    story.append(Paragraph(T["s1_title"], s["section_heading"]))
    story.append(Paragraph(T["s1_body"], s["body"]))

    # ── Section 2 ──
    story.append(Paragraph(T["s2_title"], s["section_heading"]))
    story.append(Paragraph(T["s2_body"], s["body"]))

    # ── Section 3 ──
    story.append(Paragraph(T["s3_title"], s["section_heading"]))
    for sub_key in ["s3_sub1", "s3_sub2", "s3_sub3", "s3_sub4", "s3_sub5"]:
        story.append(Paragraph(f"<b>{T[sub_key]}</b>", s["sub_heading"]))
        for item in T[f"{sub_key}_items"]:
            story.append(Paragraph(f"\u2022 {item}", s["bullet"]))

    # ── Section 4 ──
    story.append(Paragraph(T["s4_title"], s["section_heading"]))
    for item in T["s4_items"]:
        story.append(Paragraph(f"\u2022 {item}", s["bullet"]))

    # ── Section 5 — competencies table ──
    story.append(Paragraph(T["s5_title"], s["section_heading"]))
    comp_header = [Paragraph(f"<b>{h}</b>", s["table_header"]) for h in T["s5_header"]]
    comp_rows = [[Paragraph(f"<b>{r[0]}</b>", s["table_cell"]), Paragraph(r[1], s["table_cell"])] for r in T["s5_rows"]]
    comp_data = [comp_header] + comp_rows
    comp_table = Table(comp_data, colWidths=[usable_w * 0.40, usable_w * 0.60])
    comp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(comp_table)

    # ── Section 6 — validation reference ──
    story.append(Paragraph(T["s6_title"], s["section_heading"]))
    story.append(Paragraph(T["s6_intro"], s["body"]))
    story.append(Spacer(1, 4))

    ref_data = [
        [Paragraph(f"<b>{T['s6_lbl_name']}</b>", s["table_header_dark"]), Paragraph("Jean Claude Dupry", s["table_cell"])],
        [Paragraph(f"<b>{T['s6_lbl_title']}</b>", s["table_header_dark"]), Paragraph(T["s6_val_title"], s["table_cell"])],
        [Paragraph(f"<b>{T['s6_lbl_email']}</b>", s["table_header_dark"]), Paragraph("jdupry@ceismaristas.cl", s["table_cell"])],
        [Paragraph(f"<b>{T['s6_lbl_mobile']}</b>", s["table_header_dark"]), Paragraph("+56 9 9415 6984", s["table_cell"])],
    ]
    ref_table = Table(ref_data, colWidths=[usable_w * 0.30, usable_w * 0.70])
    ref_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(ref_table)
    story.append(Spacer(1, 8))
    # Bold the first word (Important/Importante/etc.) — find first colon (ASCII or full-width)
    imp_text = T["s6_important"]
    for sep in [":", "："]:
        if sep in imp_text:
            parts = imp_text.split(sep, 1)
            imp_text = f"<b>{parts[0]}{sep}</b>{parts[1]}"
            break
    story.append(Paragraph(imp_text, s["important"]))

    # ── Section 7 — professional declaration ──
    story.append(Paragraph(T["s7_title"], s["section_heading"]))
    story.append(Paragraph(T["s7_body"], s["body"]))
    story.append(Spacer(1, 20))

    # Signature block
    sig_data = [
        [Paragraph("Vladimir Bernardo Acuña Valdebenito", s["body"]),
         Paragraph(T["s7_issue_date"], s["body"])],
        [Paragraph(T["s7_issued_by"], s["important"]), Paragraph("", s["body"])],
    ]
    sig_table = Table(sig_data, colWidths=[usable_w * 0.55, usable_w * 0.45])
    sig_table.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (0, 0), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(sig_table)

    doc.build(story)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"  -> {output_path} ({size_kb:.1f} KB)")


def main():
    print("Generating achievements statements...")
    print("=" * 50)
    for lang in ["es", "en", "pt", "it", "fr", "zh"]:
        suffix = LANG_SUFFIX[lang]
        path = os.path.normpath(os.path.join(ASSETS_DIR, f"declaracion-logros-validacion{suffix}.pdf"))
        build_statement(lang, path)
    print("=" * 50)
    print("Done. 6 achievements statement PDFs generated.")


if __name__ == "__main__":
    main()
