#!/usr/bin/env python3
"""Generate the five translated CEIS institutional-context notes.

The Spanish PDF is the user-provided source and is copied without alteration
when --source-es is supplied. The translated variants preserve the source's
scope, disclaimer, institutional facts, validation guidance, and references.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
BASE_NAME = "nota-vigencia-contexto-institucional-ceis"

LANG_SUFFIX = {
    "en": "-english",
    "pt": "-portuguese",
    "it": "-italian",
    "fr": "-french",
    "zh": "-chinese",
}

SOURCE_URLS = [
    (
        "Maristas Chile - New Executive Secretary of CEIS Marista, 24-09-2026",
        "https://www.maristas.cl/noticia/2026/9/bm90aWNpYTg%3D",
    ),
    (
        "Maristas Chile - Marist Mission Area",
        "https://maristas.cl/sector_chile/equipo_educacion",
    ),
    (
        "Instituto San Martin - news published 08-09-2026",
        "https://ism.maristas.cl/noticia/2026/9/bm90aWNpYTg%3D",
    ),
    ("Fundacion CEIS Maristas - official website", "https://www.ceismaristas.cl/"),
    (
        "Fundacion CEIS Maristas - About us",
        "https://www.ceismaristas.cl/sobre-nosotros/",
    ),
    (
        "Professional portfolio - public recommendation-letter transcription",
        "https://vladimiracunadev-create.github.io/assets/carta-recomendacion_sin_firma.pdf",
    ),
]

SOURCE_LABELS = {
    "en": [label for label, _ in SOURCE_URLS],
    "pt": [
        "Maristas Chile - Novo Secretário Executivo do CEIS Marista, 24-09-2026",
        "Maristas Chile - Âmbito da Missão Marista",
        "Instituto San Martín - notícia publicada em 08-09-2026",
        "Fundação CEIS Maristas - site oficial",
        "Fundação CEIS Maristas - Sobre nós",
        "Portfólio profissional - transcrição pública da carta de recomendação",
    ],
    "it": [
        "Maristas Chile - Nuovo Segretario Esecutivo di CEIS Marista, 24-09-2026",
        "Maristas Chile - Ambito della Missione Marista",
        "Instituto San Martín - notizia pubblicata il 08-09-2026",
        "Fundación CEIS Maristas - sito ufficiale",
        "Fundación CEIS Maristas - Chi siamo",
        "Portfolio professionale - trascrizione pubblica della lettera di raccomandazione",
    ],
    "fr": [
        "Maristas Chile - Nouveau Secrétaire exécutif du CEIS Marista, 24-09-2026",
        "Maristas Chile - Domaine de la Mission mariste",
        "Instituto San Martín - actualité publiée le 08-09-2026",
        "Fundación CEIS Maristas - site officiel",
        "Fundación CEIS Maristas - À propos",
        "Portfolio professionnel - transcription publique de la lettre de recommandation",
    ],
    "zh": [
        "Maristas Chile - CEIS Marista新任执行秘书，2026-09-24",
        "Maristas Chile - 马利斯特使命领域",
        "Instituto San Martín - 2026-09-08发布的消息",
        "Fundación CEIS Maristas - 官方网站",
        "Fundación CEIS Maristas - 关于我们",
        "专业作品集 - 推荐信公开转录件",
    ],
}


TRANSLATIONS = {
    "en": {
        "title": "VALIDITY AND INSTITUTIONAL CONTEXT NOTE",
        "subtitle": "Fundacion CEIS Marista employment reference - authority update and referee continuity",
        "professional": "Professional",
        "verification_date": "Verification date",
        "date": "October 1, 2026",
        "related_document": "Related document",
        "related_value": "CEIS Recommendation Letter dated January 12, 2026",
        "version": "Version",
        "important": "IMPORTANT: the published institutional position is Executive Secretary. The letter was issued during a previous CEIS administration. Since September 2026, Exequiel Silva Sepulveda has been the new Executive Secretary. Jorge Radic Henrici remains connected to the Marist Network in sector animation and education roles.",
        "disclaimer": "Professional supporting document - not issued by Fundacion CEIS Marista",
        "s1": "1. Purpose and scope",
        "p1": "This note accompanies the recommendation letter related to Vladimir Bernardo Acuna Valdebenito's career at Fundacion CEIS Marista. Its purpose is to prevent confusion when validating an employment reference issued under a previous executive authority and to record the institutional structure published as of October 2026.",
        "p2": "It is not a new recommendation letter, an employment certificate, or a document issued by CEIS. It is supporting material prepared by the professional from public, verifiable institutional sources.",
        "s2": "2. CEIS authority: before and now",
        "authority_headers": ["Context", "Name", "Institutional situation"],
        "authority_rows": [
            ["Previous administration", "Jorge Antonio Radic Henrici", "Served as Executive Secretary of Fundacion CEIS Marista when the recommendation letter was issued. The official communication dated September 24, 2026 states that he left that responsibility and continues in new roles within the Marist Network's sector animation."],
            ["Current administration", "Exequiel Silva Sepulveda", "Became the new Executive Secretary of CEIS Marista in September 2026, replacing Jorge Radic H. The official announcement was published by Maristas Chile on September 24, 2026."],
        ],
        "web_warning": "Website update warning: the public CEIS website still shows Jorge Radic as Executive Secretary in some sections. The most recent institutional communication of September 24, 2026 should prevail when identifying the current authority.",
        "s3": "3. Jorge Radic's institutional continuity",
        "continuity_intro": "The change of Executive Secretary does not mean that Jorge Radic has left the Marist Network. The official sources reviewed show institutional continuity and current or recently published roles within the same network.",
        "continuity_headers": ["Public reference", "Role / background"],
        "continuity_rows": [
            ["Maristas Chile - 24-09-2026", "The change announcement expressly states that Jorge Radic will continue in new roles linked to the Marist Network's sector animation."],
            ["Marist Mission Area", "The current institutional page identifies him as Coordinator of the Marist Mission Area, an interdisciplinary sector body for animation and support of the educational mission project."],
            ["Instituto San Martin - 08-09-2026", "An official publication identifies him as Director of the Marist Educators Training School."],
        ],
        "s4": "4. Current institutional details of Fundacion CEIS Marista",
        "contact_rows": [["Institution", "Fundacion CEIS Marista - Center for Psychoeducational Evaluation and Research"], ["Address", "Santa Monica 2056, Santiago, Chile"], ["Telephone", "+56 2 3293 3001"], ["Institutional mobile", "+56 9 9266 5876"], ["Email", "contacto@ceismaristas.cl"], ["Website", "www.ceismaristas.cl"]],
        "s5": "5. How to manage validation of the recommendation letter",
        "validation": [
            "First validation route: contact Fundacion CEIS Marista through its current institutional channels and explain that a letter issued during the previous administration is being verified.",
            "Second contextual route: consider that Jorge Radic remains within the Marist Network. His change of role does not by itself invalidate a reference related to the period in which he served as CEIS Executive Secretary.",
            "Current authority: Exequiel Silva Sepulveda currently holds the CEIS Executive Secretariat, and the institution can indicate which person or unit should confirm historical employment information.",
            "Name and position: when citing the historical letter, identify Jorge Radic as CEIS Executive Secretary during the issuance period, not as the current executive authority.",
            "Original document: retain the signed original as the primary supporting record. The portfolio's public version is a transcription and states that the signed original is available upon request.",
            "File placement: place this note immediately after the CEIS Recommendation Letter when the letter is attached to an application or professional file.",
        ],
        "s6": "6. Recommended reading by a third party",
        "interpretation": "Correct interpretation: the recommendation letter belongs to a period when CEIS had a different executive authority. An institutional transition occurred afterward. The former referee, Jorge Radic, continues to perform roles within the Marist Network; the current executive authority of CEIS is Exequiel Silva Sepulveda. Any current formal verification should use CEIS's current institutional channels.",
        "s7": "7. Version management and control",
        "control_rows": [["Recommended name", "Validity and Institutional Context Note for an Employment Reference - Fundacion CEIS Marista"], ["Responsible", "Vladimir Bernardo Acuna Valdebenito"], ["Status", "Supporting document / updated institutional reference"], ["Review", "Update if CEIS changes its Executive Secretariat, contact details, or relevant institutional structure again."], ["External use", "Attach only together with the recommendation letter or when a third party needs to understand the authority change and the referee's institutional continuity."]],
        "s8": "8. Verified institutional sources",
        "update_criterion": "Update criterion: when an older institutional page and a more recent official communication differ regarding an authority, record both dates and use the most recent information to identify the current authority. The historical letter retains its value as evidence of the period in which it was issued, subject to authenticity and institutional validation.",
    },
    "pt": {
        "title": "NOTA DE VIGENCIA E CONTEXTO INSTITUCIONAL",
        "subtitle": "Referencia profissional Fundacao CEIS Marista - atualizacao de autoridade e continuidade do referente",
        "professional": "Profissional", "verification_date": "Data de verificacao", "date": "1 de outubro de 2026", "related_document": "Documento relacionado", "related_value": "Carta de Recomendacao CEIS, datada de 12 de janeiro de 2026", "version": "Versao",
        "important": "IMPORTANTE: o cargo institucional publicado e Secretario Executivo. A carta foi emitida durante uma gestao anterior do CEIS. Desde setembro de 2026, Exequiel Silva Sepulveda e o novo Secretario Executivo. Jorge Radic Henrici continua vinculado a Rede Marista em funcoes de animacao setorial e educacao.",
        "disclaimer": "Documento de apoio profissional - nao emitido pela Fundacao CEIS Marista",
        "s1": "1. Objetivo e alcance",
        "p1": "Esta nota acompanha a carta de recomendacao relacionada a trajetoria de Vladimir Bernardo Acuna Valdebenito na Fundacao CEIS Marista. Sua finalidade e evitar confusoes ao validar uma referencia profissional emitida sob uma autoridade executiva anterior, registrando a estrutura institucional publicada em outubro de 2026.",
        "p2": "Nao constitui uma nova carta de recomendacao, um certificado de trabalho ou um documento emitido pelo CEIS. E um antecedente de apoio preparado pelo profissional a partir de fontes institucionais publicas e verificaveis.",
        "s2": "2. Autoridade do CEIS: antes e agora",
        "authority_headers": ["Contexto", "Nome", "Situacao institucional"],
        "authority_rows": [["Gestao anterior", "Jorge Antonio Radic Henrici", "Exerceu a funcao de Secretario Executivo da Fundacao CEIS Marista quando a carta foi emitida. A comunicacao oficial de 24 de setembro de 2026 informa que deixou essa responsabilidade e continua em novas funcoes na animacao setorial da Rede Marista."], ["Gestao atual", "Exequiel Silva Sepulveda", "Assumiu como novo Secretario Executivo do CEIS Marista em setembro de 2026, substituindo Jorge Radic H. O anuncio oficial foi publicado pela Maristas Chile em 24 de setembro de 2026."]],
        "web_warning": "Aviso de atualizacao web: o site publico do CEIS ainda mostra Jorge Radic como Secretario Executivo em algumas secoes. Para identificar a autoridade vigente, deve prevalecer a comunicacao institucional mais recente, de 24 de setembro de 2026.",
        "s3": "3. Continuidade institucional de Jorge Radic",
        "continuity_intro": "A mudanca de Secretario Executivo nao significa que Jorge Radic tenha deixado a Rede Marista. As fontes oficiais revisadas mostram continuidade institucional e funcoes atuais ou recentemente publicadas dentro da mesma rede.",
        "continuity_headers": ["Referencia publica", "Funcao / antecedente"],
        "continuity_rows": [["Maristas Chile - 24-09-2026", "A noticia sobre a mudanca afirma expressamente que Jorge Radic continuara em novas funcoes ligadas a animacao setorial da Rede Marista."], ["Ambito da Missao Marista", "A pagina institucional vigente o identifica como Coordenador do Ambito da Missao Marista, instancia setorial interdisciplinar de animacao e acompanhamento do projeto de missao educativa."], ["Instituto San Martin - 08-09-2026", "Uma publicacao oficial o identifica como Diretor da Escola de Formacao de Educadores Maristas."]],
        "s4": "4. Dados institucionais atuais da Fundacao CEIS Marista",
        "contact_rows": [["Instituicao", "Fundacao CEIS Marista - Centro de Avaliacao e Pesquisa Psicoeducacional"], ["Endereco", "Santa Monica 2056, Santiago, Chile"], ["Telefone", "+56 2 3293 3001"], ["Celular institucional", "+56 9 9266 5876"], ["E-mail", "contacto@ceismaristas.cl"], ["Site", "www.ceismaristas.cl"]],
        "s5": "5. Como realizar a validacao da carta de recomendacao",
        "validation": ["Primeira via de validacao: contatar a Fundacao CEIS Marista por seus canais institucionais atuais e explicar que se deseja verificar uma carta emitida durante a gestao anterior.", "Segunda via contextual: considerar que Jorge Radic continua na Rede Marista. Sua mudanca de funcao nao invalida por si so uma referencia relativa ao periodo em que exerceu a Secretaria Executiva do CEIS.", "Autoridade atual: Exequiel Silva Sepulveda ocupa atualmente a Secretaria Executiva do CEIS, e a instituicao pode indicar a pessoa ou unidade responsavel por confirmar antecedentes profissionais historicos.", "Uso do nome e cargo: ao citar a carta historica, identificar Jorge Radic como Secretario Executivo do CEIS durante o periodo de emissao, nao como autoridade executiva atual.", "Documento original: conservar o original assinado como respaldo principal. A versao publica do portfolio e uma transcricao e informa que o original assinado esta disponivel mediante solicitacao.", "Localizacao no expediente: colocar esta nota imediatamente depois da Carta de Recomendacao CEIS quando a carta for anexada a uma candidatura ou expediente profissional."],
        "s6": "6. Leitura recomendada por terceiros",
        "interpretation": "Interpretacao correta: a carta de recomendacao pertence a um periodo em que o CEIS tinha outra autoridade executiva. Posteriormente houve uma transicao institucional. O referente anterior, Jorge Radic, continua exercendo funcoes na Rede Marista; a autoridade executiva atual do CEIS e Exequiel Silva Sepulveda. Para qualquer verificacao formal vigente, devem ser utilizados os canais institucionais atuais do CEIS.",
        "s7": "7. Gestao e controle de versao",
        "control_rows": [["Nome recomendado", "Nota de Vigencia e Contexto Institucional de Referencia Profissional - Fundacao CEIS Marista"], ["Responsavel", "Vladimir Bernardo Acuna Valdebenito"], ["Estado", "Documento de apoio / referencia institucional atualizada"], ["Revisao", "Atualizar se o CEIS modificar novamente sua Secretaria Executiva, dados de contato ou estrutura institucional relevante."], ["Uso externo", "Anexar somente junto com a carta de recomendacao ou quando um terceiro precisar compreender a mudanca de autoridade e a continuidade institucional do referente."]],
        "s8": "8. Fontes institucionais verificadas",
        "update_criterion": "Criterio de atualizacao: quando uma pagina institucional antiga e uma comunicacao oficial mais recente divergirem sobre uma autoridade, registrar as duas datas e usar a informacao mais recente para identificar a autoridade vigente. A carta historica conserva seu valor como antecedente do periodo em que foi emitida, sujeita a autenticidade e validacao institucional.",
    },
    "it": {
        "title": "NOTA DI VALIDITA E CONTESTO ISTITUZIONALE",
        "subtitle": "Referenza professionale Fundacion CEIS Marista - aggiornamento dell'autorita e continuita del referente",
        "professional": "Professionista", "verification_date": "Data di verifica", "date": "1 ottobre 2026", "related_document": "Documento correlato", "related_value": "Lettera di raccomandazione CEIS del 12 gennaio 2026", "version": "Versione",
        "important": "IMPORTANTE: la carica istituzionale pubblicata e Segretario Esecutivo. La lettera e stata emessa durante una precedente amministrazione CEIS. Da settembre 2026, Exequiel Silva Sepulveda e il nuovo Segretario Esecutivo. Jorge Radic Henrici rimane legato alla Rete Marista con funzioni di animazione settoriale e formazione.",
        "disclaimer": "Documento di supporto professionale - non emesso da Fundacion CEIS Marista",
        "s1": "1. Scopo e ambito",
        "p1": "Questa nota accompagna la lettera di raccomandazione relativa alla carriera di Vladimir Bernardo Acuna Valdebenito presso Fundacion CEIS Marista. Il suo scopo e prevenire confusioni nella convalida di una referenza professionale emessa sotto una precedente autorita esecutiva e documentare la struttura istituzionale pubblicata a ottobre 2026.",
        "p2": "Non costituisce una nuova lettera di raccomandazione, un certificato di lavoro o un documento emesso dal CEIS. E un documento di supporto preparato dal professionista sulla base di fonti istituzionali pubbliche e verificabili.",
        "s2": "2. Autorita CEIS: prima e oggi",
        "authority_headers": ["Contesto", "Nome", "Situazione istituzionale"],
        "authority_rows": [["Gestione precedente", "Jorge Antonio Radic Henrici", "Ha svolto il ruolo di Segretario Esecutivo di Fundacion CEIS Marista quando e stata emessa la lettera. La comunicazione ufficiale del 24 settembre 2026 informa che ha lasciato tale responsabilita e prosegue in nuovi ruoli nell'animazione settoriale della Rete Marista."], ["Gestione attuale", "Exequiel Silva Sepulveda", "E diventato il nuovo Segretario Esecutivo di CEIS Marista nel settembre 2026, sostituendo Jorge Radic H. L'annuncio ufficiale e stato pubblicato da Maristas Chile il 24 settembre 2026."]],
        "web_warning": "Avviso di aggiornamento web: il sito pubblico del CEIS mostra ancora Jorge Radic come Segretario Esecutivo in alcune sezioni. Per identificare l'autorita vigente deve prevalere la comunicazione istituzionale piu recente del 24 settembre 2026.",
        "s3": "3. Continuita istituzionale di Jorge Radic",
        "continuity_intro": "Il cambio del Segretario Esecutivo non significa che Jorge Radic abbia lasciato la Rete Marista. Le fonti ufficiali esaminate mostrano continuita istituzionale e ruoli attuali o recentemente pubblicati nella stessa rete.",
        "continuity_headers": ["Riferimento pubblico", "Ruolo / precedente"],
        "continuity_rows": [["Maristas Chile - 24-09-2026", "La notizia del cambio afferma espressamente che Jorge Radic continuera in nuovi ruoli legati all'animazione settoriale della Rete Marista."], ["Ambito della Missione Marista", "La pagina istituzionale vigente lo identifica come Coordinatore dell'Ambito della Missione Marista, organismo settoriale interdisciplinare di animazione e accompagnamento del progetto educativo."], ["Instituto San Martin - 08-09-2026", "Una pubblicazione ufficiale lo identifica come Direttore della Scuola di Formazione degli Educatori Maristi."]],
        "s4": "4. Dati istituzionali attuali di Fundacion CEIS Marista",
        "contact_rows": [["Istituzione", "Fundacion CEIS Marista - Centro di Valutazione e Ricerca Psicoeducativa"], ["Indirizzo", "Santa Monica 2056, Santiago, Cile"], ["Telefono", "+56 2 3293 3001"], ["Cellulare istituzionale", "+56 9 9266 5876"], ["E-mail", "contacto@ceismaristas.cl"], ["Sito web", "www.ceismaristas.cl"]],
        "s5": "5. Come gestire la convalida della lettera di raccomandazione",
        "validation": ["Prima via di convalida: contattare Fundacion CEIS Marista tramite i suoi attuali canali istituzionali e spiegare che si desidera verificare una lettera emessa durante la precedente gestione.", "Seconda via contestuale: considerare che Jorge Radic rimane nella Rete Marista. Il cambio di ruolo non invalida di per se una referenza relativa al periodo in cui ricopriva la Segreteria Esecutiva del CEIS.", "Autorita attuale: Exequiel Silva Sepulveda ricopre attualmente la Segreteria Esecutiva del CEIS e l'istituzione puo indicare la persona o unita competente per confermare i precedenti professionali storici.", "Uso del nome e della carica: citando la lettera storica, identificare Jorge Radic come Segretario Esecutivo del CEIS durante il periodo di emissione, non come autorita esecutiva attuale.", "Documento originale: conservare l'originale firmato come prova principale. La versione pubblica del portfolio e una trascrizione e indica che l'originale firmato e disponibile su richiesta.", "Posizione nel fascicolo: collocare questa nota subito dopo la Lettera di raccomandazione CEIS quando la lettera viene allegata a una candidatura o a un fascicolo professionale."],
        "s6": "6. Lettura consigliata da parte di terzi",
        "interpretation": "Interpretazione corretta: la lettera di raccomandazione appartiene a un periodo in cui il CEIS aveva un'altra autorita esecutiva. In seguito si e verificato un avvicendamento istituzionale. Il precedente referente, Jorge Radic, continua a svolgere funzioni nella Rete Marista; l'attuale autorita esecutiva del CEIS e Exequiel Silva Sepulveda. Per qualsiasi verifica formale vigente vanno utilizzati gli attuali canali istituzionali del CEIS.",
        "s7": "7. Gestione e controllo della versione",
        "control_rows": [["Nome consigliato", "Nota di validita e contesto istituzionale della referenza professionale - Fundacion CEIS Marista"], ["Responsabile", "Vladimir Bernardo Acuna Valdebenito"], ["Stato", "Documento di supporto / referenza istituzionale aggiornata"], ["Revisione", "Aggiornare se il CEIS modifica nuovamente la Segreteria Esecutiva, i contatti o la struttura istituzionale rilevante."], ["Uso esterno", "Allegare solo insieme alla lettera di raccomandazione o quando un terzo deve comprendere il cambio di autorita e la continuita istituzionale del referente."]],
        "s8": "8. Fonti istituzionali verificate",
        "update_criterion": "Criterio di aggiornamento: quando una pagina istituzionale precedente e una comunicazione ufficiale piu recente differiscono su un'autorita, registrare entrambe le date e usare l'informazione piu recente per identificare l'autorita vigente. La lettera storica conserva il suo valore come antecedente del periodo in cui e stata emessa, subordinatamente ad autenticita e convalida istituzionale.",
    },
    "fr": {
        "title": "NOTE DE VALIDITE ET DE CONTEXTE INSTITUTIONNEL",
        "subtitle": "Reference professionnelle Fundacion CEIS Marista - mise a jour de l'autorite et continuite du referent",
        "professional": "Professionnel", "verification_date": "Date de verification", "date": "1 octobre 2026", "related_document": "Document associe", "related_value": "Lettre de recommandation CEIS datee du 12 janvier 2026", "version": "Version",
        "important": "IMPORTANT : la fonction institutionnelle publiee est Secretaire executif. La lettre a ete emise sous une precedente direction du CEIS. Depuis septembre 2026, Exequiel Silva Sepulveda est le nouveau Secretaire executif. Jorge Radic Henrici reste lie au Reseau mariste dans des fonctions d'animation sectorielle et d'education.",
        "disclaimer": "Document d'appui professionnel - non emis par Fundacion CEIS Marista",
        "s1": "1. Objet et portee",
        "p1": "Cette note accompagne la lettre de recommandation relative au parcours de Vladimir Bernardo Acuna Valdebenito au sein de Fundacion CEIS Marista. Elle vise a eviter toute confusion lors de la validation d'une reference professionnelle emise sous une ancienne autorite executive et a consigner la structure institutionnelle publiee en octobre 2026.",
        "p2": "Elle ne constitue ni une nouvelle lettre de recommandation, ni un certificat de travail, ni un document emis par le CEIS. Il s'agit d'un document d'appui prepare par le professionnel a partir de sources institutionnelles publiques et verifiables.",
        "s2": "2. Autorite du CEIS : avant et maintenant",
        "authority_headers": ["Contexte", "Nom", "Situation institutionnelle"],
        "authority_rows": [["Direction precedente", "Jorge Antonio Radic Henrici", "Il exercait comme Secretaire executif de Fundacion CEIS Marista lors de l'emission de la lettre. La communication officielle du 24 septembre 2026 indique qu'il a quitte cette responsabilite et poursuit de nouvelles fonctions dans l'animation sectorielle du Reseau mariste."], ["Direction actuelle", "Exequiel Silva Sepulveda", "Il a pris ses fonctions de nouveau Secretaire executif du CEIS Marista en septembre 2026, en remplacement de Jorge Radic H. L'annonce officielle a ete publiee par Maristas Chile le 24 septembre 2026."]],
        "web_warning": "Avertissement de mise a jour web : le site public du CEIS affiche encore Jorge Radic comme Secretaire executif dans certaines rubriques. Pour identifier l'autorite actuelle, la communication institutionnelle la plus recente du 24 septembre 2026 doit prevaloir.",
        "s3": "3. Continuite institutionnelle de Jorge Radic",
        "continuity_intro": "Le changement de Secretaire executif ne signifie pas que Jorge Radic a quitte le Reseau mariste. Les sources officielles consultees montrent une continuite institutionnelle et des fonctions actuelles ou recemment publiees au sein du meme reseau.",
        "continuity_headers": ["Reference publique", "Fonction / antecedent"],
        "continuity_rows": [["Maristas Chile - 24-09-2026", "L'annonce du changement indique expressement que Jorge Radic poursuivra de nouvelles fonctions liees a l'animation sectorielle du Reseau mariste."], ["Domaine de la Mission mariste", "La page institutionnelle actuelle l'identifie comme Coordinateur du Domaine de la Mission mariste, instance sectorielle interdisciplinaire d'animation et d'accompagnement du projet de mission educative."], ["Instituto San Martin - 08-09-2026", "Une publication officielle l'identifie comme Directeur de l'Ecole de formation des educateurs maristes."]],
        "s4": "4. Coordonnees institutionnelles actuelles de Fundacion CEIS Marista",
        "contact_rows": [["Institution", "Fundacion CEIS Marista - Centre d'evaluation et de recherche psychoeducative"], ["Adresse", "Santa Monica 2056, Santiago, Chili"], ["Telephone", "+56 2 3293 3001"], ["Portable institutionnel", "+56 9 9266 5876"], ["Courriel", "contacto@ceismaristas.cl"], ["Site web", "www.ceismaristas.cl"]],
        "s5": "5. Comment gerer la validation de la lettre de recommandation",
        "validation": ["Premiere voie de validation : contacter Fundacion CEIS Marista par ses canaux institutionnels actuels et expliquer que l'on souhaite verifier une lettre emise sous la direction precedente.", "Deuxieme voie contextuelle : tenir compte du fait que Jorge Radic reste au sein du Reseau mariste. Son changement de fonction n'invalide pas en soi une reference liee a la periode ou il exercait le Secretariat executif du CEIS.", "Autorite actuelle : Exequiel Silva Sepulveda occupe actuellement le Secretariat executif du CEIS et l'institution peut indiquer la personne ou l'unite competente pour confirmer les antecedents professionnels historiques.", "Usage du nom et de la fonction : lors de la citation de la lettre historique, identifier Jorge Radic comme Secretaire executif du CEIS pendant la periode d'emission, et non comme autorite executive actuelle.", "Document original : conserver l'original signe comme preuve principale. La version publique du portfolio est une transcription indiquant que l'original signe est disponible sur demande.", "Classement dans le dossier : placer cette note immediatement apres la Lettre de recommandation CEIS lorsque celle-ci est jointe a une candidature ou a un dossier professionnel."],
        "s6": "6. Lecture recommandee par un tiers",
        "interpretation": "Interpretation correcte : la lettre de recommandation appartient a une periode ou le CEIS avait une autre autorite executive. Une transition institutionnelle est intervenue par la suite. L'ancien referent, Jorge Radic, continue d'exercer des fonctions au sein du Reseau mariste ; l'autorite executive actuelle du CEIS est Exequiel Silva Sepulveda. Toute verification formelle actuelle doit utiliser les canaux institutionnels actuels du CEIS.",
        "s7": "7. Gestion et controle de version",
        "control_rows": [["Nom recommande", "Note de validite et de contexte institutionnel de la reference professionnelle - Fundacion CEIS Marista"], ["Responsable", "Vladimir Bernardo Acuna Valdebenito"], ["Statut", "Document d'appui / reference institutionnelle mise a jour"], ["Revision", "Mettre a jour si le CEIS modifie a nouveau son Secretariat executif, ses coordonnees ou sa structure institutionnelle pertinente."], ["Usage externe", "Joindre uniquement avec la lettre de recommandation ou lorsqu'un tiers doit comprendre le changement d'autorite et la continuite institutionnelle du referent."]],
        "s8": "8. Sources institutionnelles verifiees",
        "update_criterion": "Critere de mise a jour : lorsqu'une ancienne page institutionnelle et une communication officielle plus recente divergent au sujet d'une autorite, consigner les deux dates et utiliser l'information la plus recente pour identifier l'autorite actuelle. La lettre historique conserve sa valeur comme antecedent de la periode ou elle a ete emise, sous reserve d'authenticite et de validation institutionnelle.",
    },
    "zh": {
        "title": "有效性与机构背景说明",
        "subtitle": "Fundacion CEIS Marista工作证明背景 - 负责人更新与推荐人连续性",
        "professional": "专业人士", "verification_date": "核验日期", "date": "2026年10月1日", "related_document": "相关文件", "related_value": "2026年1月12日CEIS推荐信", "version": "版本",
        "important": "重要说明：公开的机构职务为执行秘书。该推荐信签发于CEIS上一届管理期间。自2026年9月起，Exequiel Silva Sepulveda担任新任执行秘书。Jorge Radic Henrici仍在马利斯特网络从事部门协调与教育工作。",
        "disclaimer": "专业辅助文件 - 非Fundacion CEIS Marista签发",
        "s1": "1. 目的与范围",
        "p1": "本说明随附于Vladimir Bernardo Acuna Valdebenito在Fundacion CEIS Marista任职经历相关的推荐信。其目的是在核验由上一任行政负责人签发的工作推荐时避免混淆，并记录截至2026年10月公开的机构架构。",
        "p2": "本说明不是新的推荐信、工作证明或CEIS签发的文件，而是由本人依据公开且可核验的机构来源编制的辅助材料。",
        "s2": "2. CEIS负责人：过去与现在",
        "authority_headers": ["背景", "姓名", "机构情况"],
        "authority_rows": [["上一届管理", "Jorge Antonio Radic Henrici", "推荐信签发时担任Fundacion CEIS Marista执行秘书。2026年9月24日的官方通知说明，他已不再承担该职责，并将在马利斯特网络的部门协调工作中继续担任新职务。"], ["现任管理", "Exequiel Silva Sepulveda", "自2026年9月起接替Jorge Radic H.担任CEIS Marista新任执行秘书。Maristas Chile于2026年9月24日发布正式公告。"]],
        "web_warning": "网站更新提示：CEIS公开网站的部分栏目仍将Jorge Radic列为执行秘书。确认现任负责人时，应以2026年9月24日发布的最新机构通知为准。",
        "s3": "3. Jorge Radic的机构连续性",
        "continuity_intro": "执行秘书的更换并不意味着Jorge Radic已经离开马利斯特网络。经核验的官方来源显示，他在同一网络内仍保持机构连续性，并担任当前或近期公开的职务。",
        "continuity_headers": ["公开来源", "职务 / 背景"],
        "continuity_rows": [["Maristas Chile - 2026-09-24", "负责人变更公告明确指出，Jorge Radic将继续承担与马利斯特网络部门协调有关的新职务。"], ["马利斯特使命领域", "现行机构页面将其列为马利斯特使命领域协调员，该领域是负责教育使命项目推动与支持的跨学科部门机构。"], ["Instituto San Martin - 2026-09-08", "一则官方消息将其列为马利斯特教育工作者培训学校主任。"]],
        "s4": "4. Fundacion CEIS Marista现行机构信息",
        "contact_rows": [["机构", "Fundacion CEIS Marista - 心理教育评估与研究中心"], ["地址", "Santa Monica 2056, Santiago, Chile"], ["电话", "+56 2 3293 3001"], ["机构手机", "+56 9 9266 5876"], ["电子邮件", "contacto@ceismaristas.cl"], ["网站", "www.ceismaristas.cl"]],
        "s5": "5. 如何核验推荐信",
        "validation": ["第一种核验方式：通过Fundacion CEIS Marista当前机构渠道联系，并说明需要核验上一届管理期间签发的推荐信。", "第二种背景方式：考虑Jorge Radic仍在马利斯特网络任职。其职务变化本身并不否定与其担任CEIS执行秘书期间有关的推荐内容。", "现任负责人：Exequiel Silva Sepulveda目前担任CEIS执行秘书，机构可说明应由哪位人员或部门确认历史任职资料。", "姓名与职务用法：引用历史推荐信时，应将Jorge Radic表述为签发期间的CEIS执行秘书，而不是现任行政负责人。", "原始文件：应将签署原件保留为主要证明。作品集公开版本为转录件，并注明签署原件可应要求提供。", "材料顺序：在求职或专业材料中附上CEIS推荐信时，应将本说明紧随推荐信之后。"],
        "s6": "6. 第三方建议解读",
        "interpretation": "正确解读：该推荐信属于CEIS由另一位行政负责人管理的时期，之后发生了机构负责人更替。原推荐人Jorge Radic仍在马利斯特网络担任职务；CEIS现任行政负责人为Exequiel Silva Sepulveda。任何当前正式核验都应使用CEIS现行机构渠道。",
        "s7": "7. 版本管理与控制",
        "control_rows": [["建议名称", "工作推荐有效性与机构背景说明 - Fundacion CEIS Marista"], ["负责人", "Vladimir Bernardo Acuna Valdebenito"], ["状态", "辅助文件 / 更新后的机构参考"], ["复核", "如果CEIS再次更换执行秘书、联系方式或相关机构架构，应更新本文件。"], ["外部使用", "仅在随附推荐信，或第三方需要了解负责人变更及推荐人机构连续性时使用。"]],
        "s8": "8. 已核验的机构来源",
        "update_criterion": "更新标准：当较早的机构页面与较新的官方通知对负责人信息存在差异时，应记录两者日期，并使用最新信息确认现任负责人。历史推荐信仍可作为其签发时期的证明，但须接受真实性与机构核验。",
    },
}


_TAG_SPLIT = re.compile(r"(<[^>]+>)")
_LATIN_RUN = re.compile(r"[^\u2E80-\u9FFF\u3000-\u303F\uFF00-\uFFEF]+")

COMMON_REPLACEMENTS = {
    "Fundacion": "Fundación",
    "Acuna": "Acuña",
    "Sepulveda": "Sepúlveda",
    "San Martin": "San Martín",
    "Santa Monica": "Santa Mónica",
}

LANG_REPLACEMENTS = {
    "pt": {
        "VIGENCIA": "VIGÊNCIA", "REFERENCIA": "REFERÊNCIA",
        "Referencia": "Referência", "referencia": "referência",
        "atualizacao": "atualização", "verificacao": "verificação",
        "Recomendacao": "Recomendação", "recomendacao": "recomendação",
        "Versao": "Versão", "gestao": "gestão", "Gestao": "Gestão",
        "funcoes": "funções", "funcao": "função", "Funcao": "Função",
        "animacao": "animação", "educacao": "educação",
        "publica": "pública", "publicas": "públicas",
        "instituicao": "instituição", "Instituicao": "Instituição",
        "situacao": "situação", "Situacao": "Situação",
        "comunicacao": "comunicação", "secoes": "seções",
        "missao": "missão", "avaliacao": "avaliação",
        "Endereco": "Endereço", "Telefone": "Telefone",
        "validacao": "validação", "Validacao": "Validação",
        "historicos": "históricos", "periodo": "período",
        "portfolio": "portfólio", "transcricao": "transcrição",
        "solicitacao": "solicitação", "candidatura": "candidatura",
        "Leitura": "Leitura", "Interpretacao": "Interpretação",
        "transicao": "transição", "Gestao": "Gestão",
        "Revisao": "Revisão", "modificar": "modificar",
        "Fontes": "Fontes", "Criterio": "Critério",
        "pagina": "página", "periodo": "período",
        "Fundacao": "Fundação", "Nao": "Não", "nao": "não",
        "mudanca": "mudança", "informacao": "informação",
        "Informacao": "Informação", "emissao": "emissão",
        "historica": "histórica", "publico": "público",
        "responsavel": "responsável", "tambem": "também",
        "esta disponivel": "está disponível", "disponivel": "disponível",
        "por si so": "por si só", "e o novo": "é o novo",
        "E um antecedente": "É um antecedente",
        "e uma transcricao": "é uma transcrição",
        "e quem ocupa": "é quem ocupa", "e Exequiel": "é Exequiel",
        "autenticidade": "autenticidade",
    },
    "it": {
        "VALIDITA": "VALIDITÀ", "autorita": "autorità",
        "Autorita": "Autorità", "continuita": "continuità",
        "piu": "più", "responsabilita": "responsabilità",
        "validita": "validità", "e stata": "è stata",
        "e il": "è il", "e un": "è un", "E un": "È un",
        "e stato": "è stato", "e stata": "è stata",
        "e diventato": "è diventato", "e verificabile": "è verificabile",
        "cosi": "così", "puo": "può", "perche": "perché",
    },
    "fr": {
        "VALIDITE": "VALIDITÉ", "REFERENCE": "RÉFÉRENCE",
        "Reference": "Référence", "reference": "référence",
        "mise a jour": "mise à jour", "autorite": "autorité",
        "Autorite": "Autorité", "continuite": "continuité",
        "referent": "référent", "verification": "vérification",
        "associe": "associé", "datee": "datée", "Secretaire": "Secrétaire",
        "execute": "exécuté", "executif": "exécutif", "executive": "exécutive",
        "precedente": "précédente", "precedent": "précédent",
        "direction": "direction", "education": "éducation",
        "emis": "émis", "emission": "émission", "periode": "période",
        "eviter": "éviter", "consigner": "consigner", "portee": "portée",
        "verifiables": "vérifiables", "Situation": "Situation",
        "communication": "communication", "responsabilite": "responsabilité",
        "reseau": "réseau", "Reseau": "Réseau", "recente": "récente",
        "Domaine": "Domaine", "educative": "éducative", "Coordonnees": "Coordonnées",
        "evaluation": "évaluation", "Telephone": "Téléphone",
        "Premiere": "Première", "Deuxieme": "Deuxième", "historique": "historique",
        "signe": "signé", "disponible": "disponible", "Classement": "Classement",
        "recommandee": "recommandée", "Statut": "Statut", "Revision": "Révision",
        "coordonnees": "coordonnées", "pertinente": "pertinente",
        "verifiees": "vérifiées", "Critere": "Critère", "ancienne": "ancienne",
        "differentes": "différentes", "recent": "récent", "authenticite": "authenticité",
    },
}


def normalize_text(text: str, lang: str) -> str:
    for source, replacement in COMMON_REPLACEMENTS.items():
        text = text.replace(source, replacement)
    for source, replacement in LANG_REPLACEMENTS.get(lang, {}).items():
        text = text.replace(source, replacement)
    return text


def zh_latin_runs(text: str) -> str:
    parts = []
    for part in _TAG_SPLIT.split(text):
        if part.startswith("<") and part.endswith(">"):
            parts.append(part)
        else:
            parts.append(
                _LATIN_RUN.sub(
                    lambda match: match.group(0)
                    if not match.group(0).strip()
                    else f'<font name="Helvetica">{match.group(0)}</font>',
                    part,
                )
            )
    return "".join(parts)


def make_paragraph(text: str, style: ParagraphStyle, lang: str) -> Paragraph:
    text = normalize_text(text, lang)
    return Paragraph(zh_latin_runs(text) if lang == "zh" else text, style)


def make_styles(lang: str) -> dict[str, ParagraphStyle]:
    if lang == "zh":
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        regular = "STSong-Light"
        bold = "STSong-Light"
    else:
        regular = "Helvetica"
        bold = "Helvetica-Bold"

    sheet = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("Title", parent=sheet["Title"], fontName=bold, fontSize=16, leading=19, alignment=TA_CENTER, textColor=colors.HexColor("#222222"), spaceAfter=4 * mm),
        "subtitle": ParagraphStyle("Subtitle", parent=sheet["Normal"], fontName=regular, fontSize=8.8, leading=11.5, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=4 * mm),
        "heading": ParagraphStyle("Heading", parent=sheet["Heading2"], fontName=bold, fontSize=11.5, leading=13.5, textColor=colors.HexColor("#252525"), spaceBefore=3 * mm, spaceAfter=1.5 * mm),
        "body": ParagraphStyle("Body", parent=sheet["BodyText"], fontName=regular, fontSize=8.5, leading=11.3, alignment=TA_LEFT, textColor=colors.HexColor("#2b2b2b"), spaceAfter=1.8 * mm),
        "small": ParagraphStyle("Small", parent=sheet["BodyText"], fontName=regular, fontSize=7, leading=9, textColor=colors.HexColor("#4a4a4a")),
        "cell": ParagraphStyle("Cell", parent=sheet["BodyText"], fontName=regular, fontSize=7.2, leading=9, textColor=colors.HexColor("#292929")),
        "cell_bold": ParagraphStyle("CellBold", parent=sheet["BodyText"], fontName=bold, fontSize=7.2, leading=9, textColor=colors.HexColor("#292929")),
        "box": ParagraphStyle("Box", parent=sheet["BodyText"], fontName=bold, fontSize=8, leading=10.5, textColor=colors.HexColor("#252525")),
        "source": ParagraphStyle("Source", parent=sheet["BodyText"], fontName=regular, fontSize=6.8, leading=8.6, textColor=colors.HexColor("#333333"), leftIndent=4 * mm),
    }


def styled_table(rows, widths, styles, lang, header=False):
    converted = []
    for row_index, row in enumerate(rows):
        converted.append([
            make_paragraph(str(cell), styles["cell_bold" if (header and row_index == 0) or col_index == 0 else "cell"], lang)
            for col_index, cell in enumerate(row)
        ])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#9a9a9a")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eeeeee")),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dddddd")))
    table.setStyle(TableStyle(commands))
    return table


def build_translation(lang: str, output: Path) -> None:
    data = TRANSLATIONS[lang]
    styles = make_styles(lang)

    def para(text, style="body"):
        return make_paragraph(text, styles[style], lang)

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setTitle(data["title"])
        canvas.setAuthor("Vladimir Bernardo Acuna Valdebenito")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
        canvas.drawString(18 * mm, 9 * mm, data["disclaimer"])
        canvas.drawRightString(192 * mm, 9 * mm, f"{doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=17 * mm,
        title=data["title"],
        author="Vladimir Bernardo Acuna Valdebenito",
    )

    story = [para(data["title"], "title"), para(data["subtitle"], "subtitle")]
    metadata = [
        [f'{data["professional"]}:', "Vladimir Bernardo Acuna Valdebenito", f'{data["verification_date"]}:', data["date"]],
        [f'{data["related_document"]}:', data["related_value"], f'{data["version"]}:', "2.0"],
    ]
    story.append(styled_table(metadata, [28 * mm, 65 * mm, 31 * mm, 50 * mm], styles, lang))
    story.append(Spacer(1, 4 * mm))
    important = Table([[para(data["important"], "box")]], colWidths=[174 * mm])
    important.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#333333")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eeeeee")), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story.extend([important, para(data["s1"], "heading"), para(data["p1"]), para(data["p2"]), para(data["s2"], "heading")])
    authority = [data["authority_headers"]] + data["authority_rows"]
    story.extend([styled_table(authority, [31 * mm, 46 * mm, 97 * mm], styles, lang, header=True), Spacer(1, 2 * mm), para(data["web_warning"], "small"), para(data["s3"], "heading"), para(data["continuity_intro"])])
    continuity = [data["continuity_headers"]] + data["continuity_rows"]
    story.extend([
        styled_table(continuity, [56 * mm, 118 * mm], styles, lang, header=True),
        KeepTogether([
            para(data["s4"], "heading"),
            styled_table(data["contact_rows"], [43 * mm, 131 * mm], styles, lang),
        ]),
        para(data["s5"], "heading"),
    ])
    for item in data["validation"]:
        story.append(para(f"- {item}"))
    story.append(para(data["s6"], "heading"))
    interpretation = Table([[para(data["interpretation"], "body")]], colWidths=[174 * mm])
    interpretation.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#555555")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f3f3f3")), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.extend([interpretation, para(data["s7"], "heading"), styled_table(data["control_rows"], [45 * mm, 129 * mm], styles, lang), para(data["s8"], "heading")])
    for label, (_, url) in zip(SOURCE_LABELS[lang], SOURCE_URLS):
        story.append(para(f'- <link href="{url}" color="#1d4ed8">{label}</link>', "source"))
    story.append(Spacer(1, 2 * mm))
    criterion = Table([[para(data["update_criterion"], "small")]], colWidths=[174 * mm])
    criterion.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#555555")), ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f3f3f3")), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(criterion)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"OK {lang}: {output.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-es", type=Path, help="Spanish source PDF to copy unchanged")
    args = parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)
    spanish_output = ASSETS / f"{BASE_NAME}.pdf"
    if args.source_es:
        source = args.source_es.resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, spanish_output)
        print(f"OK es: {spanish_output.relative_to(ROOT)} (source preserved)")
    elif not spanish_output.exists():
        raise FileNotFoundError("Provide --source-es or keep the Spanish PDF in assets/")

    for lang, suffix in LANG_SUFFIX.items():
        build_translation(lang, ASSETS / f"{BASE_NAME}{suffix}.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
