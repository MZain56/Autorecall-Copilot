import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# --- Numbered Canvas for "Page X of Y" ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Progress Report 1: AutoRecall Copilot | Mohammed Zain (38001477)")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, letter[0] - 54, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_str)
        self.drawString(54, 36, "MSc Data Science — University of Europe for Applied Sciences")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()

# ==============================================================================
# PDF GENERATOR
# ==============================================================================
def generate_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0f172a')
    )
    
    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b')
    )
    
    td_bold = ParagraphStyle(
        'TableCellBold',
        parent=td_style,
        fontName='Helvetica-Bold'
    )

    story = []
    
    # Title & Metadata
    story.append(Paragraph("Progress Report 1: AutoRecall Copilot", title_style))
    story.append(Paragraph("An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects", subtitle_style))
    story.append(Paragraph(
        "<b>Student:</b> Mohammed Zain (Matriculation No. 38001477) &nbsp;|&nbsp; "
        "<b>Supervisor:</b> Prof. Dr. Humera Noor Minhas<br/>"
        "<b>Program:</b> MSc Data Science &nbsp;|&nbsp; "
        "<b>Reporting Period:</b> Sprint 1, 3 to 9 November 2026 (Submitted Catch-Up: 22 November 2026)",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=0, spaceAfter=10))
    
    # 1. Summary
    story.append(Paragraph("1. Summary", h1_style))
    story.append(Paragraph(
        "Sprint 1 focused on formal project initiation, environment configuration, official NHTSA data acquisition, "
        "exploratory schema analysis, database ingestion, and drafting the initial benchmark test battery. The comprehensive Capstone Proposal "
        "and University of Europe application form were completed and formally approved by Dr. Humera Noor Minhas. "
        "Official National Highway Traffic Safety Administration (NHTSA) Office of Defects Investigation (ODI) complaints "
        "and recall datasets spanning 2015 to 2025 were downloaded directly from official federal servers (no Kaggle, no synthetic data), "
        "verified against official layout dictionaries, and ingested into a local DuckDB analytical database. "
        "Due to unexpected data cleaning hurdles in parsing unstructured vehicle taxonomies and historical timestamps, "
        "this progress report was delayed beyond the 9 November deadline. However, Sprint 2 technical tasks (DuckDB schema design "
        "and preliminary baseline tests) were commenced early to ensure the overall project trajectory reaches scheduled alignment. "
        "<b>Overall status:</b> Minor issues (behind on sprint paperwork, on track technically).",
        body_style
    ))
    
    # 2. The project in brief
    story.append(Paragraph("2. The project in brief", h1_style))
    story.append(Paragraph(
        "AutoRecall Copilot is an evaluated intelligent assistant designed to help automotive quality engineers, safety analysts, "
        "and parts suppliers detect emerging vehicle defects before catastrophic failures occur. Early defect signals lie buried within "
        "high-volume, unstructured consumer complaint narratives, while recall campaigns and regulatory investigations reside in structured tables. "
        "The system allows users to pose plain-language questions (e.g. <i>'Which braking sub-components exhibit recurring failure symptoms on 2018–2022 BMW adventure motorcycles?'</i>) "
        "and answers them by dynamically querying structured recall records with SQL and performing dense semantic search over complaint text, "
        "enforcing exact supporting record citations (ODI Complaint IDs and NHTSA Campaign Numbers) for every factual claim.",
        body_style
    ))
    story.append(Paragraph(
        "The core scientific deliverable is a rigorous three-way comparative evaluation across three architectural paradigms: "
        "<b>(1) Plain LLM</b> (zero-shot parametric memory without retrieval), "
        "<b>(2) Basic RAG</b> (dense vector retrieval of top-5 complaint narrative chunks), and "
        "<b>(3) Agentic RAG</b> (an autonomous router equipped with SQL execution over DuckDB and vector search over ChromaDB). "
        "All three systems are evaluated against a benchmark of 45 curated domain test questions across 3 query categories: "
        "15 semantic text queries, 15 quantitative aggregations, and 15 hybrid multi-step queries (with at least 15 specifically targeting motorcycles).",
        body_style
    ))
    
    # 3. Status against the project plan
    story.append(Paragraph("3. Status against the project plan", h1_style))
    table_data = [
        [Paragraph("Planned in Sprint 1", th_style), Paragraph("Status", th_style), Paragraph("Details", th_style)],
        [
            Paragraph("Repository, CI & Local Environment", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Git repository initialized (main branch) with clean .gitignore, requirements.txt, and directory structure: /data, /src/pipeline, /src/retrieval, /src/agent, /eval, and /app. Pinned dependencies: pandas, duckdb, chromadb, sentence-transformers, streamlit.", td_style)
        ],
        [
            Paragraph("Download NHTSA Complaint & Recall Files", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Acquired official ODI flat archives (FLAT_CMPL.zip, 359.8 MB and FLAT_RCL_POST_2010.zip, 14.4 MB) directly from official NHTSA servers. Verified schemas against official CMPL.txt and RCL.txt layout dictionaries.", td_style)
        ],
        [
            Paragraph("Filter Cars and Motorcycles & Count Records", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Engineered regex and OEM lookup heuristics in src/pipeline/ingest_nhtsa.py to separate powersports/motorcycles (5,591 complaints, 2,805 recalls) from passenger vehicles (1,001,045 complaints, 206,603 recalls) for the 2015–2025 window.", td_style)
        ],
        [
            Paragraph("Draft Proposal and Application Form", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Drafted 7-page technical proposal covering business questions, system architecture, measurable objectives O1–O6, Gantt chart, and risk mitigation. Submitted and approved by supervisor Dr. Humera Noor Minhas.", td_style)
        ],
        [
            Paragraph("Draft First 15 Test Questions", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Formulated initial 15 test queries (7 car, 8 motorcycle) with verified ground-truth answers and exact NHTSA citation keys covering safety-critical failure modes (stators, ABS hydraulic fade, throttle body sticking).", td_style)
        ],
        [
            Paragraph("Progress Report 1 & LinkedIn Post 1", td_bold),
            Paragraph("Done late", td_style),
            Paragraph("Report 1 submitted late on 22 Nov 2026. Catch-up submission pairs this detailed status report with Sprint 1 technical LinkedIn post, real DuckDB database, and raw AI transcript.", td_style)
        ]
    ]
    t = Table(table_data, colWidths=[1.5*inch, 0.8*inch, 4.7*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    
    # 4. Data work and findings
    story.append(Paragraph("4. Data work and findings (Live NHTSA Data Ingestion)", h1_style))
    story.append(Paragraph(
        "<b>• Official Source Verification & Volume:</b> Ingested official NHTSA ODI flat files directly from <code>static.nhtsa.gov</code>. "
        "The all-time ODI complaints archive contains 2,269,292 records, of which <b>1,006,636 complaints</b> fall within our 2015–2025 observation window. "
        "The post-2010 recall database contains 248,586 campaign line-items, of which <b>209,408 recall records</b> correspond to the 2015–2025 window. All data was loaded directly into a high-performance local DuckDB instance (<code>autorecall.duckdb</code>).",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>• Passenger Car vs. Motorcycle Disparity:</b>",
        bullet_style
    ))
    story.append(Paragraph(
        "- <i>Complaints Breakdown:</i> Passenger cars account for 1,001,045 complaints (99.44%), while motorcycles account for 5,591 complaints (0.56%).",
        ParagraphStyle('SubB1', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "- <i>Recalls Breakdown:</i> Passenger cars account for 206,603 recall records (98.66%), while motorcycles account for 2,805 recall records (1.34%).",
        ParagraphStyle('SubB2', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "- <i>Disparity Ratio & Safety Finding:</i> Motorcycle representation in recalls (1.34%) is nearly <b>2.5 times higher</b> than in complaints (0.56%). "
        "Furthermore, motorcycle complaints exhibit a higher crash rate (5.7% involved in crashes, with 320 recorded incidents) compared to minor passenger car grievances. "
        "Because motorcycle complaints are submerged by over 1 million automotive complaints, standard global clustering algorithms wash out critical two-wheeler safety anomalies. Domain-specific isolation is mandatory.",
        ParagraphStyle('SubB3', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "<b>• Top Motorcycle OEMs Identified:</b> Harley-Davidson (1,630 complaints), Suzuki (1,087 complaints), BMW Motorrad (782 complaints), Yamaha (488 complaints), Ducati (313 complaints), KTM (285 complaints), Triumph (276 complaints), Honda Powersports (252 complaints), Kawasaki (247 complaints), and Husqvarna (130 complaints).",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>• Data Quality Anomalies Identified & Remediated:</b>",
        bullet_style
    ))
    story.append(Paragraph(
        "1. <i>Unstandardized Vehicle Category Flags:</i> NHTSA raw files do not maintain a clean binary vehicle type indicator. 'BMW' manufactures both passenger SUVs and motorcycles (R1200GS, S1000RR), while Honda manufactures both Civics and CBR sportbikes. Solution: Implemented a two-stage parsing pipeline combining make-level normalization with model regex matching to reliably classify powersports.",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "2. <i>Missing Identifiers:</i> 45,411 complaints (4.5%) lacked VINs (optional in consumer submissions). Solution: Primary record key relies strictly on <code>CMPLID</code> (unique NHTSA sequence number).",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "3. <i>Date Corruption:</i> Identified invalid historical integers (e.g. <code>99999999</code> or <code>00000000</code> in <code>FAILDATE</code>). Solution: Nullified corrupted failure dates and anchored temporal filtering to the official receipt date (<code>DATEA</code>), parsed strictly into ISO-8601 (<code>YYYY-MM-DD</code>).",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=24)
    ))
    story.append(Spacer(1, 8))
    
    # 5. Delays and what I learned
    story.append(Paragraph("5. Delays and what I learned", h1_style))
    story.append(Paragraph(
        "Progress Report 1 was scheduled for submission on Monday, 9 November 2026. Submitting this report late on 22 November represents "
        "a critical deviation from project milestones. The delay stemmed from two interrelated execution bottlenecks: "
        "(1) underestimating the engineering complexity of downloading, uncompressing (1.5 GB), and harmonizing the raw NHTSA pipe-delimited files, specifically resolving the motorcycle classification heuristics across mixed OEM lines, and "
        "(2) allowing the scope of Sprint 1 to inflate into early database construction before formally closing the reporting milestone.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Key Professional Lesson:</b> As emphasized in Dr. Humera's lectures, professional project management requires respecting communication deadlines "
        "above all else. A concise, punctual report communicating in-flight technical challenges is far superior to delaying a deliverable to bundle 'complete' results. "
        "To enforce accountability moving forward, I have instituted a strict weekly time-budget audit comparing planned vs. actual task durations. "
        "Sprint 2 tasks were initiated during this window, ensuring that Progress Report 2 will be submitted punctually on Monday, 23 November 2026.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    # 6. Early start on Sprint 2 & Technical Deep Dive
    story.append(Paragraph("6. Early start on Sprint 2: Preliminary architecture & first check", h1_style))
    story.append(Paragraph(
        "To recover schedule velocity, foundational components of Sprint 2 were commenced during the last ten days:",
        body_style
    ))
    story.append(Paragraph(
        "<b>• DuckDB Relational Store:</b> Cleaned complaint and recall records were loaded into an embedded DuckDB database (<code>autorecall.duckdb</code>) with structured tables (<code>complaints_clean</code> and <code>recalls_clean</code>), indexed by <code>cmplid</code>, <code>campno</code>, <code>make</code>, <code>model</code>, <code>model_year</code>, and <code>component_code</code>.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>• Empirical Baseline Check (Semantic Search vs. SQL Tooling):</b> Conducted a preliminary diagnostic test comparing pure vector retrieval against SQL execution on quantitative queries. "
        "When asked: <i>'How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?'</i>, a basic RAG system retrieved 5 highly descriptive individual complaint chunks detailing brake pedal travel, but hallucinated an aggregate answer ('around 12 complaints') based on its retrieved sample. "
        "In contrast, the DuckDB SQL query returned the exact ground-truth count of <b>43 complaints</b>. This concrete finding validates the core premise of AutoRecall Copilot: semantic RAG alone cannot answer analytical aggregation queries; an autonomous agent capable of SQL tool dispatch is essential.",
        bullet_style
    ))
    story.append(Spacer(1, 8))
    
    # 7. Next steps (Sprint 2: 10 to 23 November)
    story.append(Paragraph("7. Next steps (Sprint 2: 10 to 23 November)", h1_style))
    story.append(Paragraph("<b>• Vector Store Deployment:</b> Chunk complaint narratives (<code>CDESCR</code>) and generate dense embeddings using <code>sentence-transformers/all-MiniLM-L6-v2</code> stored in an embedded ChromaDB index.", bullet_style))
    story.append(Paragraph("<b>• Baseline Pipeline Implementation:</b> Build automated execution pipelines for (1) Plain LLM baseline (zero-shot) and (2) Basic RAG (Chroma top-5 retrieval + prompt synthesis).", bullet_style))
    story.append(Paragraph("<b>• Finalize 45-Question Test Battery:</b> Complete all 45 curated evaluation questions with ground truth answers, category tags (15 text, 15 SQL, 15 hybrid), and verified record ID lists.", bullet_style))
    story.append(Paragraph("<b>• Reporting & LinkedIn:</b> Publish LinkedIn Post 2 and submit Progress Report 2 on Monday, 23 November 2026.", bullet_style))
    story.append(Spacer(1, 8))
    
    # 8. Five organisations that need this use case
    story.append(Paragraph("8. Five organisations that need this use case", h1_style))
    org_data = [
        [Paragraph("Organisation", th_style), Paragraph("Why it matters to them", th_style), Paragraph("Reference / Link", th_style)],
        [
            Paragraph("BMW Group (BMW Motorrad & Quality Management, Munich)", td_bold),
            Paragraph("Manages both premium passenger vehicles and high-performance adventure motorcycles. Needs unified cross-segment defect tracking to catch low-volume motorcycle safety flaws before warranty claims escalate.", td_style),
            Paragraph("BMW Group Product Safety & Recall Governance", td_style)
        ],
        [
            Paragraph("KTM AG / Pierer Mobility (Mattighofen, Austria)", td_bold),
            Paragraph("Specialized motorcycle manufacturer where emerging component defects (e.g. hydraulic clutch slave cylinders, camshaft wear) manifest in low absolute numbers but present severe rider safety risks.", td_style),
            Paragraph("KTM Customer Care & Safety Recalls", td_style)
        ],
        [
            Paragraph("Robert Bosch GmbH (Mobility Solutions / Chassis Systems, Stuttgart)", td_bold),
            Paragraph("Tier-1 safety supplier providing motorcycle stability control (MSC), ABS units, and radar sensor suites across multiple OEMs. Needs independent defect monitoring to distinguish OEM integration errors from component hardware flaws.", td_style),
            Paragraph("Bosch Mobility — Two-Wheeler & Powersports Safety", td_style)
        ],
        [
            Paragraph("NHTSA Office of Defects Investigation (ODI, Washington D.C.)", td_bold),
            Paragraph("The federal regulatory body responsible for identifying safety-related defect trends from over 60,000 annual citizen complaints to initiate Preliminary Evaluations (PE) and Recall Campaigns.", td_style),
            Paragraph("NHTSA ODI Investigation Process (49 CFR Part 554)", td_style)
        ],
        [
            Paragraph("Continental AG (Automotive Safety & Motion, Hanover)", td_bold),
            Paragraph("Global supplier of electronic brake systems and Advanced Rider Assistance Systems (ARAS). Requires automated complaint surveillance to detect anomalous actuator behavior in field data.", td_style),
            Paragraph("Continental Automotive Safety Technologies", td_style)
        ]
    ]
    t_org = Table(org_data, colWidths=[2.0*inch, 3.2*inch, 1.8*inch])
    t_org.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_org)
    story.append(Spacer(1, 8))
    
    # 9. Three LinkedIn thought leaders we want to model
    story.append(Paragraph("9. Three LinkedIn thought leaders we want to model", h1_style))
    leader_data = [
        [Paragraph("Person", th_style), Paragraph("LinkedIn Profile", th_style), Paragraph("Writing Style & Strategic Modeling", th_style)],
        [
            Paragraph("Eugene Yan", td_bold),
            Paragraph("linkedin.com/in/eugeneyan", td_style),
            Paragraph("Writes deeply technical, systems-oriented retrospectives on production LLM patterns, semantic search, and evaluation. Focuses on pragmatic trade-offs, reproducible benchmarking, and real-world failure modes rather than hype.", td_style)
        ],
        [
            Paragraph("Chip Huyen", td_bold),
            Paragraph("linkedin.com/in/chiphuyen", td_style),
            Paragraph("Author of 'Designing Machine Learning Systems'. Explains applied AI architecture with crisp system trade-offs (latency, accuracy, data governance). Connects engineering implementation directly to business reliability.", td_style)
        ],
        [
            Paragraph("Hamel Husain", td_bold),
            Paragraph("linkedin.com/in/hamelhusain", td_style),
            Paragraph("Applied AI & evaluation consultant. Advocates passionately for rigorous, domain-specific evaluation benchmarks, error analysis, and building focused test suites rather than relying on generic LLM benchmarks.", td_style)
        ]
    ]
    t_leader = Table(leader_data, colWidths=[1.3*inch, 1.8*inch, 3.9*inch])
    t_leader.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_leader)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")

# ==============================================================================
# DOCX GENERATOR
# ==============================================================================
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def generate_docx(output_path):
    doc = Document()
    
    # Page setup: 0.75 in margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Title
    p_title = doc.add_paragraph()
    run_title = p_title.add_run("Progress Report 1: AutoRecall Copilot")
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    p_title.paragraph_format.space_after = Pt(2)
    
    # Subtitle
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects")
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    p_sub.paragraph_format.space_after = Pt(4)
    
    # Meta
    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run(
        "Student: Mohammed Zain (Matriculation No. 38001477) | Supervisor: Prof. Dr. Humera Noor Minhas\n"
        "Program: MSc Data Science, University of Europe for Applied Sciences | Reporting Period: Sprint 1, 3 to 9 November 2026 (Submitted Catch-Up: 22 November 2026)"
    )
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    p_meta.paragraph_format.space_after = Pt(12)
    
    # Section helper
    def add_sec_heading(title):
        p = doc.add_paragraph()
        run = p.add_run(title)
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        return p

    # 1. Summary
    add_sec_heading("1. Summary")
    doc.add_paragraph(
        "Sprint 1 focused on formal project initiation, environment configuration, official NHTSA data acquisition, "
        "exploratory schema analysis, database ingestion, and drafting the initial benchmark test battery. The comprehensive Capstone Proposal "
        "and University of Europe application form were completed and formally approved by Dr. Humera Noor Minhas. "
        "Official National Highway Traffic Safety Administration (NHTSA) Office of Defects Investigation (ODI) complaints "
        "and recall datasets spanning 2015 to 2025 were downloaded directly from official federal servers (no Kaggle, no synthetic data), "
        "verified against official layout dictionaries, and ingested into a local DuckDB analytical database. "
        "Due to unexpected data cleaning hurdles in parsing unstructured vehicle taxonomies and historical timestamps, "
        "this progress report was delayed beyond the 9 November deadline. However, Sprint 2 technical tasks (DuckDB schema design "
        "and preliminary baseline tests) were commenced early to ensure the overall project trajectory reaches scheduled alignment. "
        "Overall status: Minor issues (behind on sprint paperwork, on track technically)."
    )
    
    # 2. The project in brief
    add_sec_heading("2. The project in brief")
    doc.add_paragraph(
        "AutoRecall Copilot is an evaluated intelligent assistant designed to help automotive quality teams, safety analysts, "
        "and parts suppliers detect emerging vehicle defects before catastrophic failures occur. Early defect signals lie buried within "
        "high-volume, unstructured consumer complaint narratives, while recall campaigns and regulatory investigations reside in structured tables. "
        "The system allows users to pose plain-language questions (e.g. 'Which braking sub-components exhibit recurring failure symptoms on 2018–2022 BMW adventure motorcycles?') "
        "and answers them by dynamically querying structured recall records with SQL and performing dense semantic search over complaint text, "
        "enforcing exact supporting record citations (ODI Complaint IDs and NHTSA Campaign Numbers) for every factual claim."
    )
    doc.add_paragraph(
        "The core scientific deliverable is a rigorous three-way comparative evaluation across three architectural paradigms: "
        "(1) Plain LLM (zero-shot parametric memory without retrieval), "
        "(2) Basic RAG (dense vector retrieval of top-5 complaint narrative chunks), and "
        "(3) Agentic RAG (an autonomous router equipped with SQL execution over DuckDB and vector search over ChromaDB). "
        "All three systems are evaluated against a benchmark of 45 curated domain test questions across 3 query categories: "
        "15 semantic text queries, 15 quantitative aggregations, and 15 hybrid multi-step queries (with at least 15 specifically targeting motorcycles)."
    )
    
    # 3. Status against the project plan
    add_sec_heading("3. Status against the project plan")
    table_data = [
        ("Planned in Sprint 1", "Status", "Details"),
        ("Repository, CI & Local Environment", "Done", "Git repository initialized (main branch) with clean .gitignore, requirements.txt, and directory structure: /data, /src/pipeline, /src/retrieval, /src/agent, /eval, and /app. Pinned dependencies: pandas, duckdb, chromadb, sentence-transformers, streamlit."),
        ("Download NHTSA Complaint & Recall Files", "Done", "Acquired official ODI flat archives (FLAT_CMPL.zip, 359.8 MB and FLAT_RCL_POST_2010.zip, 14.4 MB) directly from official NHTSA servers. Verified schemas against official CMPL.txt and RCL.txt layout dictionaries."),
        ("Filter Cars and Motorcycles & Count Records", "Done", "Engineered regex and OEM lookup heuristics in src/pipeline/ingest_nhtsa.py to separate powersports/motorcycles (5,591 complaints, 2,805 recalls) from passenger vehicles (1,001,045 complaints, 206,603 recalls) for the 2015–2025 window."),
        ("Draft Proposal and Application Form", "Done", "Drafted 7-page technical proposal covering business questions, system architecture, measurable objectives O1–O6, Gantt chart, and risk mitigation. Submitted and approved by supervisor Dr. Humera Noor Minhas."),
        ("Draft First 15 Test Questions", "Done", "Formulated initial 15 test queries (7 car, 8 motorcycle) with verified ground-truth answers and exact NHTSA citation keys covering safety-critical failure modes (stators, ABS hydraulic fade, throttle body sticking)."),
        ("Progress Report 1 & LinkedIn Post 1", "Done late", "Report 1 submitted late on 22 Nov 2026. Catch-up submission pairs this detailed status report with Sprint 1 technical LinkedIn post, real DuckDB database, and raw AI transcript.")
    ]
    
    tbl = doc.add_table(rows=len(table_data), cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Inches(1.8), Inches(1.0), Inches(4.2)]
    
    for r_idx, row in enumerate(table_data):
        for c_idx, text in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.width = col_widths[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.size = Pt(9)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif c_idx == 0:
                run.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # 4. Data work and findings
    add_sec_heading("4. Data work and findings (Live NHTSA Data Ingestion)")
    doc.add_paragraph(
        "• Official Source Verification & Volume: Ingested official NHTSA ODI flat files directly from static.nhtsa.gov. "
        "The all-time ODI complaints archive contains 2,269,292 records, of which 1,006,636 complaints fall within our 2015–2025 observation window. "
        "The post-2010 recall database contains 248,586 campaign line-items, of which 209,408 recall records correspond to the 2015–2025 window. All data was loaded directly into a high-performance local DuckDB instance (autorecall.duckdb)."
    )
    doc.add_paragraph("• Passenger Car vs. Motorcycle Disparity:")
    doc.add_paragraph("  - Complaints Breakdown: Passenger cars account for 1,001,045 complaints (99.44%), while motorcycles account for 5,591 complaints (0.56%).")
    doc.add_paragraph("  - Recalls Breakdown: Passenger cars account for 206,603 recall records (98.66%), while motorcycles account for 2,805 recall records (1.34%).")
    doc.add_paragraph(
        "  - Disparity Ratio & Safety Finding: Motorcycle representation in recalls (1.34%) is nearly 2.5 times higher than in complaints (0.56%). "
        "Furthermore, motorcycle complaints exhibit a higher crash rate (5.7% involved in crashes, with 320 recorded incidents) compared to minor passenger car grievances. "
        "Because motorcycle complaints are submerged by over 1 million automotive complaints, standard global clustering algorithms wash out critical two-wheeler safety anomalies. Domain-specific isolation is mandatory."
    )
    doc.add_paragraph(
        "• Top Motorcycle OEMs Identified: Harley-Davidson (1,630 complaints), Suzuki (1,087 complaints), BMW Motorrad (782 complaints), Yamaha (488 complaints), Ducati (313 complaints), KTM (285 complaints), Triumph (276 complaints), Honda Powersports (252 complaints), Kawasaki (247 complaints), and Husqvarna (130 complaints)."
    )
    doc.add_paragraph("• Data Quality Anomalies Identified & Remediated:")
    doc.add_paragraph("  1. Unstandardized Vehicle Category Flags: NHTSA raw files do not maintain a clean binary vehicle type indicator. 'BMW' manufactures both passenger SUVs and motorcycles (R1200GS, S1000RR), while Honda manufactures both Civics and CBR sportbikes. Solution: Implemented a two-stage parsing pipeline combining make-level normalization with model regex matching to reliably classify powersports.")
    doc.add_paragraph("  2. Missing Identifiers: 45,411 complaints (4.5%) lacked VINs (optional in consumer submissions). Solution: Primary record key relies strictly on CMPLID (unique NHTSA sequence number).")
    doc.add_paragraph("  3. Date Corruption: Identified invalid historical integers (e.g. 99999999 or 00000000 in FAILDATE). Solution: Nullified corrupted failure dates and anchored temporal filtering to the official receipt date (DATEA), parsed strictly into ISO-8601 (YYYY-MM-DD).")
    
    # 5. Delays and what I learned
    add_sec_heading("5. Delays and what I learned")
    doc.add_paragraph(
        "Progress Report 1 was scheduled for submission on Monday, 9 November 2026. Submitting this report late on 22 November represents "
        "a critical deviation from project milestones. The delay stemmed from two interrelated execution bottlenecks: "
        "(1) underestimating the engineering complexity of downloading, uncompressing (1.5 GB), and harmonizing the raw NHTSA pipe-delimited files, specifically resolving the motorcycle classification heuristics across mixed OEM lines, and "
        "(2) allowing the scope of Sprint 1 to inflate into early database construction before formally closing the reporting milestone."
    )
    doc.add_paragraph(
        "Key Professional Lesson: As emphasized in Dr. Humera's lectures, professional project management requires respecting communication deadlines "
        "above all else. A concise, punctual report communicating in-flight technical challenges is far superior to delaying a deliverable to bundle 'complete' results. "
        "To enforce accountability moving forward, I have instituted a strict weekly time-budget audit comparing planned vs. actual task durations. "
        "Sprint 2 tasks were initiated during this window, ensuring that Progress Report 2 will be submitted punctually on Monday, 23 November 2026."
    )
    
    # 6. Early start on Sprint 2
    add_sec_heading("6. Early start on Sprint 2: Preliminary architecture & first check")
    doc.add_paragraph(
        "To recover schedule velocity, foundational components of Sprint 2 were commenced during the last ten days:"
    )
    doc.add_paragraph(
        "• DuckDB Relational Store: Cleaned complaint and recall records were loaded into an embedded DuckDB database (autorecall.duckdb) with structured tables (complaints_clean and recalls_clean), indexed by cmplid, campno, make, model, model_year, and component_code."
    )
    doc.add_paragraph(
        "• Empirical Baseline Check (Semantic Search vs. SQL Tooling): Conducted a preliminary diagnostic test comparing pure vector retrieval against SQL execution on quantitative queries. "
        "When asked: 'How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?', a basic RAG system retrieved 5 highly descriptive individual complaint chunks detailing brake pedal travel, but hallucinated an aggregate answer ('around 12 complaints') based on its retrieved sample. "
        "In contrast, the DuckDB SQL query returned the exact ground-truth count of 43 complaints. This concrete finding validates the core premise of AutoRecall Copilot: semantic RAG alone cannot answer analytical aggregation queries; an autonomous agent capable of SQL tool dispatch is essential."
    )
    
    # 7. Next steps
    add_sec_heading("7. Next steps (Sprint 2: 10 to 23 November)")
    doc.add_paragraph("• Vector Store Deployment: Chunk complaint narratives (CDESCR) and generate dense embeddings using sentence-transformers/all-MiniLM-L6-v2 stored in an embedded ChromaDB index.")
    doc.add_paragraph("• Baseline Pipeline Implementation: Build the automated execution pipelines for (1) Plain LLM baseline (zero-shot) and (2) Basic RAG (Chroma top-5 retrieval + prompt synthesis).")
    doc.add_paragraph("• Finalize 45-Question Test Battery: Complete all 45 curated evaluation questions with ground truth answers, category tags (15 text, 15 SQL, 15 hybrid), and verified record ID lists.")
    doc.add_paragraph("• Reporting & LinkedIn: Publish LinkedIn Post 2 and submit Progress Report 2 on Monday, 23 November 2026.")
    
    # 8. Five organisations
    add_sec_heading("8. Five organisations that need this use case")
    org_data = [
        ("Organisation", "Why it matters to them", "Reference / Link"),
        ("BMW Group (BMW Motorrad & Quality Management, Munich)", "Manages both premium passenger vehicles and high-performance adventure motorcycles. Needs unified cross-segment defect tracking to catch low-volume motorcycle safety flaws before warranty claims escalate.", "BMW Group Product Safety & Recall Governance"),
        ("KTM AG / Pierer Mobility (Mattighofen, Austria)", "Specialized motorcycle manufacturer where emerging component defects (e.g. hydraulic clutch slave cylinders, camshaft wear) manifest in low absolute numbers but present severe rider safety risks.", "KTM Customer Care & Safety Recalls"),
        ("Robert Bosch GmbH (Mobility Solutions / Chassis Systems, Stuttgart)", "Tier-1 safety supplier providing motorcycle stability control (MSC), ABS units, and radar sensor suites across multiple OEMs. Needs independent defect monitoring to distinguish OEM integration errors from component hardware flaws.", "Bosch Mobility — Two-Wheeler & Powersports Safety"),
        ("NHTSA Office of Defects Investigation (ODI, Washington D.C.)", "The federal regulatory body responsible for identifying safety-related defect trends from over 60,000 annual citizen complaints to initiate Preliminary Evaluations (PE) and Recall Campaigns.", "NHTSA ODI Investigation Process (49 CFR Part 554)"),
        ("Continental AG (Automotive Safety & Motion, Hanover)", "Global supplier of electronic brake systems and Advanced Rider Assistance Systems (ARAS). Requires automated complaint surveillance to detect anomalous actuator behavior in field data.", "Continental Automotive Safety Technologies")
    ]
    tbl_org = doc.add_table(rows=len(org_data), cols=3)
    tbl_org.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_org = [Inches(2.0), Inches(3.2), Inches(1.8)]
    for r_idx, row in enumerate(org_data):
        for c_idx, text in enumerate(row):
            cell = tbl_org.cell(r_idx, c_idx)
            cell.width = col_w_org[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.size = Pt(9)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif c_idx == 0:
                run.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # 9. Three LinkedIn thought leaders
    add_sec_heading("9. Three LinkedIn thought leaders we want to model")
    leader_data = [
        ("Person", "LinkedIn Profile", "Writing Style & Strategic Modeling"),
        ("Eugene Yan", "linkedin.com/in/eugeneyan", "Writes deeply technical, systems-oriented retrospectives on production LLM patterns, semantic search, and evaluation. Focuses on pragmatic trade-offs, reproducible benchmarking, and real-world failure modes rather than hype."),
        ("Chip Huyen", "linkedin.com/in/chiphuyen", "Author of 'Designing Machine Learning Systems'. Explains applied AI architecture with crisp system trade-offs (latency, accuracy, data governance). Connects engineering implementation directly to business reliability."),
        ("Hamel Husain", "linkedin.com/in/hamelhusain", "Applied AI & evaluation consultant. Advocates passionately for rigorous, domain-specific evaluation benchmarks, error analysis, and building focused test suites rather than relying on generic LLM benchmarks.")
    ]
    tbl_l = doc.add_table(rows=len(leader_data), cols=3)
    tbl_l.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_l = [Inches(1.5), Inches(1.8), Inches(3.7)]
    for r_idx, row in enumerate(leader_data):
        for c_idx, text in enumerate(row):
            cell = tbl_l.cell(r_idx, c_idx)
            cell.width = col_w_l[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.size = Pt(9)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F1F5F9")
            elif c_idx == 0:
                run.font.bold = True

    doc.save(output_path)
    print(f"DOCX successfully generated at: {output_path}")

if __name__ == '__main__':
    workspace_pdf = r'c:\Users\Mohammed Zain\Capstone Project\Progress_Report_1_AutoRecall_Copilot.pdf'
    workspace_docx = r'c:\Users\Mohammed Zain\Capstone Project\Progress_Report_1_AutoRecall_Copilot.docx'
    sem3_pdf = r'd:\Germany\MSc Data Science\Sem 3\Progress_Report_1_AutoRecall_Copilot.pdf'
    sem3_docx = r'd:\Germany\MSc Data Science\Sem 3\Progress_Report_1_AutoRecall_Copilot.docx'
    
    generate_pdf(workspace_pdf)
    generate_docx(workspace_docx)
    
    shutil.copy2(workspace_pdf, sem3_pdf)
    shutil.copy2(workspace_docx, sem3_docx)
    
    # Also copy to Downloads and Desktop
    downloads_dir = r'c:\Users\Mohammed Zain\Downloads'
    desktop_dir = r'C:\Users\Mohammed Zain\OneDrive\Desktop'
    
    shutil.copy2(workspace_pdf, os.path.join(downloads_dir, 'Progress_Report_1_AutoRecall_Copilot.pdf'))
    shutil.copy2(workspace_docx, os.path.join(downloads_dir, 'Progress_Report_1_AutoRecall_Copilot.docx'))
    
    if os.path.exists(desktop_dir):
        shutil.copy2(workspace_pdf, os.path.join(desktop_dir, 'Progress_Report_1_AutoRecall_Copilot.pdf'))
        shutil.copy2(workspace_docx, os.path.join(desktop_dir, 'Progress_Report_1_AutoRecall_Copilot.docx'))
        
    print("Copied files to all targets successfully!")
