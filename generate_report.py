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
# PDF GENERATOR (HUMANISED VERSION)
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
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=25,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=5
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
        "Mohammed Zain (Matriculation No. 38001477) &nbsp;|&nbsp; Supervisor: Prof. Dr. Humera Noor Minhas<br/>"
        "Program: MSc Data Science, University of Europe for Applied Sciences &nbsp;|&nbsp; Reporting Period: Sprint 1, 3 to 9 November 2026",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=0, spaceAfter=8))
    
    # 1. Summary
    story.append(Paragraph("1. Summary", h1_style))
    story.append(Paragraph(
        "In Sprint 1, I focused on getting the project environment ready, writing the formal proposal, and downloading the official "
        "NHTSA complaints and recalls datasets. My proposal and university application form were approved by Dr. Humera Noor Minhas. "
        "I downloaded the official raw data files directly from NHTSA servers (not Kaggle) and built the initial ingestion script to load "
        "them into an embedded DuckDB database. I ran into real data issues with unstandardized vehicle types and corrupted date fields, "
        "which took longer than I planned and caused me to miss the 9 November reporting deadline. To catch back up, I started the Sprint 2 "
        "database setup and baseline checks early. <b>Overall status:</b> minor issues with the timeline, but on track technically.",
        body_style
    ))
    
    # 2. The project in brief
    story.append(Paragraph("2. The project in brief", h1_style))
    story.append(Paragraph(
        "When vehicle parts start failing, owners describe their problems in free-text complaints, while manufacturers and regulators "
        "track investigations and recalls in structured tables. For quality teams and safety engineers, reading through tens of thousands "
        "of complaints to spot early failure trends is slow and tedious work. AutoRecall Copilot is an AI assistant that lets an engineer "
        "ask questions in plain English (like <i>'Which braking components show rising failure complaints on 2018–2022 BMW motorcycles?'</i>) "
        "and gets answers grounded in both structured SQL queries and text search, citing the exact NHTSA Complaint ID or Recall Campaign Number.",
        body_style
    ))
    story.append(Paragraph(
        "Because this is a data science capstone and not a research thesis, my focus is on building and evaluating three practical setups "
        "on the exact same 45 questions: <b>(1) Plain LLM</b> (answering from memory with no outside data), <b>(2) Basic RAG</b> (retrieving "
        "the 5 most similar complaint narratives), and <b>(3) Agentic RAG</b> (an agent with an SQL tool for counts and a vector search tool "
        "for symptom text). The 45 questions cover 15 text search questions, 15 count/trend questions, and 15 mixed questions, with at least 15 "
        "focused specifically on motorcycles.",
        body_style
    ))
    
    # 3. Status against the project plan
    story.append(Paragraph("3. Status against the project plan", h1_style))
    table_data = [
        [Paragraph("Planned in Sprint 1", th_style), Paragraph("Status", th_style), Paragraph("Details", th_style)],
        [
            Paragraph("Repository and local environment", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Created the local repository and linked it to GitHub (<code>MZain56/Autorecall-Copilot</code>). Added a project <code>README.md</code>, pinned dependencies in <code>requirements.txt</code>, and set up <code>.gitignore</code> to keep large raw files local.", td_style)
        ],
        [
            Paragraph("Download official NHTSA files", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Downloaded official raw archives (<code>FLAT_CMPL.zip</code> at 359.8 MB and <code>FLAT_RCL_POST_2010.zip</code> at 14.4 MB) directly from NHTSA's server. Verified column layouts against official <code>CMPL.txt</code> and <code>RCL.txt</code> dictionaries.", td_style)
        ],
        [
            Paragraph("Filter cars vs. motorcycles & check counts", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Wrote <code>src/pipeline/ingest_nhtsa.py</code> to separate motorcycles (5,591 complaints, 2,805 recalls) from passenger cars (1,001,045 complaints, 206,603 recalls) for the 2015–2025 observation window.", td_style)
        ],
        [
            Paragraph("Write and submit proposal", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Submitted the 7-page capstone proposal and UE form with business questions, system diagram, objectives, and Gantt chart. Approved by supervisor.", td_style)
        ],
        [
            Paragraph("Draft first 15 test questions", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Drafted the first 15 domain questions (7 cars, 8 motorcycles) covering real failure patterns (like stator burnouts, ABS pressure loss, and sticking throttle bodies) with verified ground-truth record IDs.", td_style)
        ],
        [
            Paragraph("Progress report 1 & LinkedIn post", td_bold),
            Paragraph("Done late", td_style),
            Paragraph("Submitted late on 22 Nov 2026. Includes this honest status report, the real DuckDB database, the LinkedIn post on RAG limitations, and the raw AI conversation log.", td_style)
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
    story.append(Spacer(1, 8))
    
    # 4. Data work and findings
    story.append(Paragraph("4. Data work and findings (What I found in the NHTSA data)", h1_style))
    story.append(Paragraph(
        "<b>• Data downloaded:</b> I downloaded the official flat files directly from <code>static.nhtsa.gov</code>. "
        "The full NHTSA complaints file holds 2,269,292 records dating back to 1995. For my project window (2015 to 2025), "
        "there are <b>1,006,636 complaints</b> and <b>209,408 recall campaign entries</b>. I loaded these directly into a local "
        "DuckDB database (<code>autorecall.duckdb</code>) for fast querying.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>• The car vs. motorcycle numbers:</b>",
        bullet_style
    ))
    story.append(Paragraph(
        "- <i>Complaints:</i> Passenger cars make up 1,001,045 complaints (99.44%), while motorcycles make up only 5,591 complaints (0.56%).",
        ParagraphStyle('SubB1', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "- <i>Recalls:</i> Passenger cars make up 206,603 recall records (98.66%), while motorcycles account for 2,805 recall records (1.34%).",
        ParagraphStyle('SubB2', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "- <i>Why this matters:</i> Motorcycles have a recall share that is <b>2.5 times higher</b> than their complaint share. "
        "Also, 5.7% of motorcycle complaints involved an actual crash (320 crashes), which is much higher than minor car defects. "
        "Because there are 1 million car complaints, any general search or clustering completely buries motorcycle defect signals. "
        "That is why having a dedicated filter for motorcycles is necessary.",
        ParagraphStyle('SubB3', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "<b>• Top motorcycle brands in the data:</b> Harley-Davidson leads with 1,630 complaints, followed by Suzuki (1,087), "
        "BMW Motorrad (782), Yamaha (488), Ducati (313), KTM (285), Triumph (276), Honda Powersports (252), and Kawasaki (247).",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>• Three data quality problems I ran into and fixed:</b>",
        bullet_style
    ))
    story.append(Paragraph(
        "1. <i>Shared brand names:</i> NHTSA doesn't have a clean 'motorcycle' checkbox. 'BMW' makes both X5 SUVs and R1200GS adventure bikes; 'Honda' makes Civics and CBR sportbikes. I wrote regex rules matching motorcycle model series (like R-series, CBR, GSX, Ninja) to tag them accurately.",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "2. <i>Missing VINs:</i> 45,411 complaints (4.5%) had empty VIN fields because consumers filing online often don't have their VIN handy. I made sure my tables rely on NHTSA's unique sequence number (<code>CMPLID</code>) instead of VIN.",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=24)
    ))
    story.append(Paragraph(
        "3. <i>Corrupted dates:</i> Several thousand records had bad date entries like <code>99999999</code> or <code>00000000</code> in the failure date field. I nullified those and used the official receipt date (<code>DATEA</code>) formatted as <code>YYYY-MM-DD</code>.",
        ParagraphStyle('SubBullet', parent=bullet_style, leftIndent=24)
    ))
    story.append(Spacer(1, 8))
    
    # 5. Delays and what I learned
    story.append(Paragraph("5. Delays and what I learned", h1_style))
    story.append(Paragraph(
        "Progress Report 1 was due on Monday, 9 November 2026, and I am submitting it late. The honest reason is poor time estimation: "
        "I spent much longer than expected downloading the 1.5 GB file, fixing the tab-delimited formatting, and writing regex rules "
        "to separate motorcycle models from cars. Instead of pausing to submit a brief status report on the due date, I kept working to get "
        "the database populated first. That was a mistake.",
        body_style
    ))
    story.append(Paragraph(
        "<b>What I learned:</b> As Dr. Humera emphasized in class, deadlines in professional life are about communication, not waiting for "
        "perfection. Sending a short, punctual report explaining what is delayed is much better than going silent to finish extra work. "
        "To make sure this doesn't happen again, I am tracking my actual hours against my estimates each week. Because I already started "
        "Sprint 2 tasks during this window, Progress Report 2 will be submitted on time on Monday, 23 November.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    # 6. Early start on Sprint 2
    story.append(Paragraph("6. Early start on Sprint 2: A first baseline test", h1_style))
    story.append(Paragraph(
        "While catching up on reporting, I started Sprint 2 technical tasks early to stay on schedule:",
        body_style
    ))
    story.append(Paragraph(
        "<b>• DuckDB tables:</b> Ingested the cleaned complaints and recalls into <code>autorecall.duckdb</code>, indexed by complaint ID, recall campaign number, make, model, year, and component code.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>• Testing basic RAG vs. SQL:</b> I ran a quick test to see if semantic search alone could handle counting questions. "
        "I asked: <i>'How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?'</i> "
        "A basic RAG setup pulled 5 relevant complaint chunks describing soft brake pedals, but it guessed an answer ('around 10 to 12 complaints'). "
        "Running a simple SQL query on DuckDB gave the exact count: <b>43 complaints</b>. This simple test confirms the main idea of my project: "
        "pure RAG cannot do math or counts, so giving the agent an SQL tool is necessary.",
        bullet_style
    ))
    story.append(Spacer(1, 8))
    
    # 7. Next steps
    story.append(Paragraph("7. Next steps (Sprint 2: 10 to 23 November)", h1_style))
    story.append(Paragraph("<b>• Vector store:</b> Chunk the complaint descriptions (<code>CDESCR</code>) and build the ChromaDB index using <code>all-MiniLM-L6-v2</code>.", bullet_style))
    story.append(Paragraph("<b>• Baseline pipelines:</b> Write the test runner for the Plain LLM baseline and the Basic RAG baseline.", bullet_style))
    story.append(Paragraph("<b>• Finish the 45 test questions:</b> Complete the full question benchmark with reference answers and record IDs (15 text, 15 SQL, 15 mixed).", bullet_style))
    story.append(Paragraph("<b>• Submission:</b> Publish LinkedIn post 2 and submit Progress Report 2 on Monday, 23 November 2026.", bullet_style))
    story.append(Spacer(1, 8))
    
    # 8. Five organisations
    story.append(Paragraph("8. Five organisations that need this use case", h1_style))
    org_data = [
        [Paragraph("Organisation", th_style), Paragraph("Why it matters to them", th_style), Paragraph("Reference / Link", th_style)],
        [
            Paragraph("BMW Group (BMW Motorrad & Quality, Munich)", td_bold),
            Paragraph("Builds both cars and high-end adventure bikes. Needs unified defect monitoring to catch low-volume motorcycle safety flaws before warranty claims turn into recalls.", td_style),
            Paragraph("BMW Group Product Safety & Recalls", td_style)
        ],
        [
            Paragraph("KTM AG / Pierer Mobility (Mattighofen, Austria)", td_bold),
            Paragraph("Specialist motorcycle maker where component defects (like clutch cylinders or camshaft wear) show up in small numbers but create serious rider crash risks.", td_style),
            Paragraph("KTM Customer Care & Safety Recalls", td_style)
        ],
        [
            Paragraph("Robert Bosch GmbH (Chassis Systems, Stuttgart)", td_bold),
            Paragraph("Major safety supplier for motorcycle ABS, stability control (MSC), and radar sensors. Needs independent defect tracking to know whether field failures are component issues or OEM assembly issues.", td_style),
            Paragraph("Bosch Mobility — Two-Wheeler Safety", td_style)
        ],
        [
            Paragraph("NHTSA ODI (Washington D.C.)", td_bold),
            Paragraph("The federal regulator that sifts through 60,000+ citizen complaints every year to decide when to open defect investigations and push for safety recalls.", td_style),
            Paragraph("NHTSA ODI Investigation Process", td_style)
        ],
        [
            Paragraph("Continental AG (Safety & Motion, Hanover)", td_bold),
            Paragraph("Supplies motorcycle brake actuators and electronic rider aids. Needs automated complaint monitoring to spot early field glitches across different brands.", td_style),
            Paragraph("Continental Automotive Safety", td_style)
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
    
    # 9. Three LinkedIn thought leaders
    story.append(Paragraph("9. Three LinkedIn thought leaders I want to model", h1_style))
    leader_data = [
        [Paragraph("Person", th_style), Paragraph("LinkedIn Profile", th_style), Paragraph("What I like about their writing style", th_style)],
        [
            Paragraph("Eugene Yan", td_bold),
            Paragraph("linkedin.com/in/eugeneyan", td_style),
            Paragraph("Writes clear, practical engineering retrospectives on search, RAG, and evaluation. Always explains real trade-offs and failure cases without hype.", td_style)
        ],
        [
            Paragraph("Chip Huyen", td_bold),
            Paragraph("linkedin.com/in/chiphuyen", td_style),
            Paragraph("Breaks complex ML system architectures down into clear, structured decisions. Always connects technical choices to practical business reliability.", td_style)
        ],
        [
            Paragraph("Hamel Husain", td_bold),
            Paragraph("linkedin.com/in/hamelhusain", td_style),
            Paragraph("Focuses heavily on rigorous evaluation, error analysis, and domain-specific benchmarks instead of generic LLM leaderboards. Explains evaluation in plain language.", td_style)
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
# DOCX GENERATOR (HUMANISED VERSION)
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
    
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    p_title = doc.add_paragraph()
    run_title = p_title.add_run("Progress Report 1: AutoRecall Copilot")
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    p_title.paragraph_format.space_after = Pt(2)
    
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects")
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    p_sub.paragraph_format.space_after = Pt(4)
    
    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run(
        "Mohammed Zain (Matriculation No. 38001477) | Supervisor: Prof. Dr. Humera Noor Minhas\n"
        "Program: MSc Data Science, University of Europe for Applied Sciences | Reporting Period: Sprint 1, 3 to 9 November 2026"
    )
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    p_meta.paragraph_format.space_after = Pt(12)
    
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
        "In Sprint 1, I focused on getting the project environment ready, writing the formal proposal, and downloading the official "
        "NHTSA complaints and recalls datasets. My proposal and university application form were approved by Dr. Humera Noor Minhas. "
        "I downloaded the official raw data files directly from NHTSA servers (not Kaggle) and built the initial ingestion script to load "
        "them into an embedded DuckDB database. I ran into real data issues with unstandardized vehicle types and corrupted date fields, "
        "which took longer than I planned and caused me to miss the 9 November reporting deadline. To catch back up, I started the Sprint 2 "
        "database setup and baseline checks early. Overall status: minor issues with the timeline, but on track technically."
    )
    
    # 2. The project in brief
    add_sec_heading("2. The project in brief")
    doc.add_paragraph(
        "When vehicle parts start failing, owners describe their problems in free-text complaints, while manufacturers and regulators "
        "track investigations and recalls in structured tables. For quality teams and safety engineers, reading through tens of thousands "
        "of complaints to spot early failure trends is slow and tedious work. AutoRecall Copilot is an AI assistant that lets an engineer "
        "ask questions in plain English (like 'Which braking components show rising failure complaints on 2018–2022 BMW motorcycles?') "
        "and gets answers grounded in both structured SQL queries and text search, citing the exact NHTSA Complaint ID or Recall Campaign Number."
    )
    doc.add_paragraph(
        "Because this is a data science capstone and not a research thesis, my focus is on building and evaluating three practical setups "
        "on the exact same 45 questions: (1) Plain LLM (answering from memory with no outside data), (2) Basic RAG (retrieving the 5 most "
        "similar complaint narratives), and (3) Agentic RAG (an agent with an SQL tool for counts and a vector search tool for symptom text). "
        "The 45 questions cover 15 text search questions, 15 count/trend questions, and 15 mixed questions, with at least 15 focused specifically on motorcycles."
    )
    
    # 3. Status against the project plan
    add_sec_heading("3. Status against the project plan")
    table_data = [
        ("Planned in Sprint 1", "Status", "Details"),
        ("Repository and local environment", "Done", "Created the local repository and linked it to GitHub (MZain56/Autorecall-Copilot). Added a project README.md, pinned dependencies in requirements.txt, and set up .gitignore to keep large raw files local."),
        ("Download official NHTSA files", "Done", "Downloaded official raw archives (FLAT_CMPL.zip at 359.8 MB and FLAT_RCL_POST_2010.zip at 14.4 MB) directly from NHTSA's server. Verified column layouts against official CMPL.txt and RCL.txt dictionaries."),
        ("Filter cars vs. motorcycles & check counts", "Done", "Wrote src/pipeline/ingest_nhtsa.py to separate motorcycles (5,591 complaints, 2,805 recalls) from passenger cars (1,001,045 complaints, 206,603 recalls) for the 2015–2025 observation window."),
        ("Write and submit proposal", "Done", "Submitted the 7-page capstone proposal and UE form with business questions, system diagram, objectives, and Gantt chart. Approved by supervisor."),
        ("Draft first 15 test questions", "Done", "Drafted the first 15 domain questions (7 cars, 8 motorcycles) covering real failure patterns (like stator burnouts, ABS pressure loss, and sticking throttle bodies) with verified ground-truth record IDs."),
        ("Progress report 1 & LinkedIn post", "Done late", "Submitted late on 22 Nov 2026. Includes this honest status report, the real DuckDB database, the LinkedIn post on RAG limitations, and the raw AI conversation log.")
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
    add_sec_heading("4. Data work and findings (What I found in the NHTSA data)")
    doc.add_paragraph(
        "• Data downloaded: I downloaded the official flat files directly from static.nhtsa.gov. "
        "The full NHTSA complaints file holds 2,269,292 records dating back to 1995. For my project window (2015 to 2025), "
        "there are 1,006,636 complaints and 209,408 recall campaign entries. I loaded these directly into a local "
        "DuckDB database (autorecall.duckdb) for fast querying."
    )
    doc.add_paragraph("• The car vs. motorcycle numbers:")
    doc.add_paragraph("  - Complaints: Passenger cars make up 1,001,045 complaints (99.44%), while motorcycles make up only 5,591 complaints (0.56%).")
    doc.add_paragraph("  - Recalls: Passenger cars make up 206,603 recall records (98.66%), while motorcycles account for 2,805 recall records (1.34%).")
    doc.add_paragraph(
        "  - Why this matters: Motorcycles have a recall share that is 2.5 times higher than their complaint share. "
        "Also, 5.7% of motorcycle complaints involved an actual crash (320 crashes), which is much higher than minor car defects. "
        "Because there are 1 million car complaints, any general search or clustering completely buries motorcycle defect signals. "
        "That is why having a dedicated filter for motorcycles is necessary."
    )
    doc.add_paragraph(
        "• Top motorcycle brands in the data: Harley-Davidson leads with 1,630 complaints, followed by Suzuki (1,087), "
        "BMW Motorrad (782), Yamaha (488), Ducati (313), KTM (285), Triumph (276), Honda Powersports (252), and Kawasaki (247)."
    )
    doc.add_paragraph("• Three data quality problems I ran into and fixed:")
    doc.add_paragraph("  1. Shared brand names: NHTSA doesn't have a clean 'motorcycle' checkbox. 'BMW' makes both X5 SUVs and R1200GS adventure bikes; 'Honda' makes Civics and CBR sportbikes. I wrote regex rules matching motorcycle model series (like R-series, CBR, GSX, Ninja) to tag them accurately.")
    doc.add_paragraph("  2. Missing VINs: 45,411 complaints (4.5%) had empty VIN fields because consumers filing online often don't have their VIN handy. I made sure my tables rely on NHTSA's unique sequence number (CMPLID) instead of VIN.")
    doc.add_paragraph("  3. Corrupted dates: Several thousand records had bad date entries like 99999999 or 00000000 in the failure date field. I nullified those and used the official receipt date (DATEA) formatted as YYYY-MM-DD.")
    
    # 5. Delays and what I learned
    add_sec_heading("5. Delays and what I learned")
    doc.add_paragraph(
        "Progress Report 1 was due on Monday, 9 November 2026, and I am submitting it late. The honest reason is poor time estimation: "
        "I spent much longer than expected downloading the 1.5 GB file, fixing the tab-delimited formatting, and writing regex rules "
        "to separate motorcycle models from cars. Instead of pausing to submit a brief status report on the due date, I kept working to get "
        "the database populated first. That was a mistake."
    )
    doc.add_paragraph(
        "What I learned: As Dr. Humera emphasized in class, deadlines in professional life are about communication, not waiting for "
        "perfection. Sending a short, punctual report explaining what is delayed is much better than going silent to finish extra work. "
        "To make sure this doesn't happen again, I am tracking my actual hours against my estimates each week. Because I already started "
        "Sprint 2 tasks during this window, Progress Report 2 will be submitted on time on Monday, 23 November."
    )
    
    # 6. Early start on Sprint 2
    add_sec_heading("6. Early start on Sprint 2: A first baseline test")
    doc.add_paragraph(
        "While catching up on reporting, I started Sprint 2 technical tasks early to stay on schedule:"
    )
    doc.add_paragraph(
        "• DuckDB tables: Ingested the cleaned complaints and recalls into autorecall.duckdb, indexed by complaint ID, recall campaign number, make, model, year, and component code."
    )
    doc.add_paragraph(
        "• Testing basic RAG vs. SQL: I ran a quick test to see if semantic search alone could handle counting questions. "
        "I asked: 'How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?' "
        "A basic RAG setup pulled 5 relevant complaint chunks describing soft brake pedals, but it guessed an answer ('around 10 to 12 complaints'). "
        "Running a simple SQL query on DuckDB gave the exact count: 43 complaints. This simple test confirms the main idea of my project: "
        "pure RAG cannot do math or counts, so giving the agent an SQL tool is necessary."
    )
    
    # 7. Next steps
    add_sec_heading("7. Next steps (Sprint 2: 10 to 23 November)")
    doc.add_paragraph("• Vector store: Chunk the complaint descriptions (CDESCR) and build the ChromaDB index using all-MiniLM-L6-v2.")
    doc.add_paragraph("• Baseline pipelines: Write the test runner for the Plain LLM baseline and the Basic RAG baseline.")
    doc.add_paragraph("• Finish the 45 test questions: Complete the full question benchmark with reference answers and record IDs (15 text, 15 SQL, 15 mixed).")
    doc.add_paragraph("• Submission: Publish LinkedIn post 2 and submit Progress Report 2 on Monday, 23 November 2026.")
    
    # 8. Five organisations
    add_sec_heading("8. Five organisations that need this use case")
    org_data = [
        ("Organisation", "Why it matters to them", "Reference / Link"),
        ("BMW Group (BMW Motorrad & Quality, Munich)", "Builds both cars and high-end adventure bikes. Needs unified defect monitoring to catch low-volume motorcycle safety flaws before warranty claims turn into recalls.", "BMW Group Product Safety & Recalls"),
        ("KTM AG / Pierer Mobility (Mattighofen, Austria)", "Specialist motorcycle maker where component defects (like clutch cylinders or camshaft wear) show up in small numbers but create serious rider crash risks.", "KTM Customer Care & Safety Recalls"),
        ("Robert Bosch GmbH (Chassis Systems, Stuttgart)", "Major safety supplier for motorcycle ABS, stability control (MSC), and radar sensors. Needs independent defect tracking to know whether field failures are component issues or OEM assembly issues.", "Bosch Mobility — Two-Wheeler Safety"),
        ("NHTSA ODI (Washington D.C.)", "The federal regulator that sifts through 60,000+ citizen complaints every year to decide when to open defect investigations and push for safety recalls.", "NHTSA ODI Investigation Process"),
        ("Continental AG (Safety & Motion, Hanover)", "Supplies motorcycle brake actuators and electronic rider aids. Needs automated complaint monitoring to spot early field glitches across different brands.", "Continental Automotive Safety")
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
    add_sec_heading("9. Three LinkedIn thought leaders I want to model")
    leader_data = [
        ("Person", "LinkedIn Profile", "What I like about their writing style"),
        ("Eugene Yan", "linkedin.com/in/eugeneyan", "Writes clear, practical engineering retrospectives on search, RAG, and evaluation. Always explains real trade-offs and failure cases without hype."),
        ("Chip Huyen", "linkedin.com/in/chiphuyen", "Breaks complex ML system architectures down into clear, structured decisions. Always connects technical choices to practical business reliability."),
        ("Hamel Husain", "linkedin.com/in/hamelhusain", "Focuses heavily on rigorous evaluation, error analysis, and domain-specific benchmarks instead of generic LLM leaderboards. Explains evaluation in plain language.")
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
    
    def safe_copy(src, dst):
        try:
            shutil.copy2(src, dst)
            print(f"Successfully copied to: {dst}")
        except PermissionError:
            print(f"Notice: {dst} is currently open in another program (e.g. Word/PDF viewer). File in workspace is updated.")
        except Exception as e:
            print(f"Could not copy to {dst}: {e}")

    safe_copy(workspace_pdf, sem3_pdf)
    safe_copy(workspace_docx, sem3_docx)
    
    downloads_dir = r'c:\Users\Mohammed Zain\Downloads'
    desktop_dir = r'C:\Users\Mohammed Zain\OneDrive\Desktop'
    
    safe_copy(workspace_pdf, os.path.join(downloads_dir, 'Progress_Report_1_AutoRecall_Copilot.pdf'))
    safe_copy(workspace_docx, os.path.join(downloads_dir, 'Progress_Report_1_AutoRecall_Copilot.docx'))
    
    if os.path.exists(desktop_dir):
        safe_copy(workspace_pdf, os.path.join(desktop_dir, 'Progress_Report_1_AutoRecall_Copilot.pdf'))
        safe_copy(workspace_docx, os.path.join(desktop_dir, 'Progress_Report_1_AutoRecall_Copilot.docx'))
        
    print("Report generation and sync complete!")
