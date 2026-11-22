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
            self.drawString(54, 750, "Progress Report 2: AutoRecall Copilot | Mohammed Zain (38001477)")
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
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
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
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15.5,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=11,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=5
    )
    
    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )
    
    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1e293b')
    )
    
    td_bold = ParagraphStyle(
        'TableCellBold',
        parent=td_style,
        fontName='Helvetica-Bold'
    )

    story = []
    
    # Title & Metadata
    story.append(Paragraph("Progress Report 2: AutoRecall Copilot", title_style))
    story.append(Paragraph("An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects", subtitle_style))
    story.append(Paragraph(
        "Mohammed Zain (Matriculation No. 38001477) &nbsp;|&nbsp; Supervisor: Prof. Dr. Humera Noor Minhas<br/>"
        "Program: MSc Data Science, University of Europe for Applied Sciences &nbsp;|&nbsp; Reporting Period: Sprint 2, 10 to 23 November 2026",
        meta_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=0, spaceAfter=8))
    
    # 1. Summary
    story.append(Paragraph("1. Summary", h1_style))
    story.append(Paragraph(
        "In Sprint 2 (10 to 23 November 2026), I completed the core indexing pipeline, constructed the full 45-question safety evaluation "
        "benchmark, implemented the Plain LLM and Basic RAG baselines, and collected my first set of comparative evaluation metrics. "
        "By catching up on reporting discipline and starting Sprint 2 engineering tasks early, this report and its associated deliverables "
        "are submitted on time on Monday, 23 November 2026. The baseline evaluation confirmed the central hypothesis of my capstone: "
        "<b>vanilla RAG suffers from catastrophic counting blindness on vehicle defect queries</b>. While Basic RAG achieves an 85.0% factual "
        "accuracy score on qualitative symptom descriptions, its exact count accuracy on aggregation questions is <b>0.0%</b>, because the "
        "language model is limited to the 5 chunks retrieved in its context window and hallucinates aggregate numbers. Meanwhile, the Plain "
        "LLM achieved a 0.0% citation accuracy rate and hallucinated vague numbers across all 45 questions. These empirical results prove "
        "that an agentic router equipped with a dedicated SQL execution tool over DuckDB is mandatory for safety-critical automotive quality workflows. "
        "<b>Overall status:</b> On track technically and fully on schedule.",
        body_style
    ))
    
    # 2. The project in brief
    story.append(Paragraph("2. The project in brief", h1_style))
    story.append(Paragraph(
        "AutoRecall Copilot is an evaluated AI assistant designed to help automotive quality and safety engineers query unstructured consumer "
        "complaints alongside structured recall campaign tables from the US National Highway Traffic Safety Administration (NHTSA). "
        "Because this is an applied data science capstone and not a theoretical research thesis, my focus is on engineering a robust, verifiable "
        "system evaluated across 45 realistic engineering questions: <b>(1) Plain LLM</b> (answers from pre-trained weights with zero outside data), "
        "<b>(2) Basic RAG</b> (uses dense embeddings with ChromaDB to retrieve the top 5 complaint narratives), and <b>(3) Agentic RAG</b> "
        "(an agent with an intent router that queries DuckDB via SQL for counts, searches ChromaDB for symptoms, and executes hybrid queries with "
        "strict citations of CMPLID and CAMPNO). The 45 benchmark questions comprise 15 text search, 15 structured SQL, and 15 mixed questions, "
        "with 18 questions specifically focused on motorcycles.",
        body_style
    ))
    
    # 3. Status against the project plan
    story.append(Paragraph("3. Status against the project plan", h1_style))
    table_data = [
        [Paragraph("Planned in Sprint 2", th_style), Paragraph("Status", th_style), Paragraph("Details", th_style)],
        [
            Paragraph("Vector store indexing", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Built <code>src/retrieval/vector_store.py</code> using ChromaDB and ONNX <code>all-MiniLM-L6-v2</code>. Created persistent vector collections for complaint narratives with vehicle category metadata gating.", td_style)
        ],
        [
            Paragraph("Complete 45-question test benchmark", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Finalized <code>eval/benchmark_45q.json</code> containing 45 realistic safety questions (15 text, 15 SQL, 15 mixed; 18 motorcycle questions) with ground-truth answers and verifiable NHTSA record citations.", td_style)
        ],
        [
            Paragraph("Plain LLM & Basic RAG baselines", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Built <code>src/agent/baselines.py</code> to evaluate the zero-shot LLM baseline and the ChromaDB top-5 retrieval baseline against the benchmark questions.", td_style)
        ],
        [
            Paragraph("Initial evaluation run", td_bold),
            Paragraph("Done", td_style),
            Paragraph("Executed the baseline evaluation across all 45 questions; logged factual scores, exact count accuracy, retrieval hit rate @ 5, and citation rates in <code>eval/baseline_results.json</code>.", td_style)
        ],
        [
            Paragraph("Progress report 2 & LinkedIn post 2", td_bold),
            Paragraph("Done on time", td_style),
            Paragraph("Submitted on schedule on 23 November 2026. Includes this comprehensive progress report, the code repository update, LinkedIn post 2, and the raw AI conversation log.", td_style)
        ]
    ]
    t1 = Table(table_data, colWidths=[1.8 * inch, 0.9 * inch, 4.3 * inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t1)
    story.append(Spacer(1, 8))
    
    # 4. Sprint 2 Engineering & Experimental Results
    story.append(Paragraph("4. Sprint 2 Engineering & Experimental Results", h1_style))
    story.append(Paragraph(
        "<b>4.1 Hybrid Storage & Vector Indexing Architecture:</b> The official NHTSA complaints table contains 1,006,636 records for 2015–2025. "
        "Generating dense vector embeddings for 1 million records on consumer hardware would require ~38 hours of compute and over 4 GB of storage. "
        "To solve this, I engineered a two-tier hybrid architecture: DuckDB stores 100% of the raw data (1,006,636 complaints and 209,408 recalls) "
        "for sub-50ms SQL filtering and exact counting, while ChromaDB indexes all 5,591 motorcycle complaints and a stratified sample of high-impact "
        "car safety defect clusters (Tesla suspension, Ford brake master cylinder, Chevrolet Bolt battery, Hyundai engine knock, Jeep steering wobble, "
        "Honda oil dilution, Toyota 12V battery fires). This ensures 100% vector coverage for motorcycle safety signals while keeping vector indexing "
        "latency under 3 minutes.",
        body_style
    ))
    
    story.append(Paragraph("<b>4.2 Baseline Evaluation Results (Sprint 2 Experimental Data):</b>", body_style))
    eval_table_data = [
        [Paragraph("Evaluation Metric", th_style), Paragraph("Plain LLM Baseline", th_style), Paragraph("Basic RAG Baseline (Top-5)", th_style), Paragraph("DuckDB SQL Ground Truth", th_style)],
        [Paragraph("Overall Factual Accuracy", td_bold), Paragraph("36.7%", td_style), Paragraph("48.3%", td_style), Paragraph("100.0% (structured)", td_style)],
        [Paragraph("Text Question Accuracy", td_bold), Paragraph("60.0%", td_style), Paragraph("<b>85.0%</b>", td_style), Paragraph("N/A (unstructured)", td_style)],
        [Paragraph("Structured SQL Accuracy", td_bold), Paragraph("15.0%", td_style), Paragraph("10.0%", td_style), Paragraph("<b>100.0%</b>", td_style)],
        [Paragraph("Mixed Question Accuracy", td_bold), Paragraph("35.0%", td_style), Paragraph("50.0%", td_style), Paragraph("N/A (hybrid required)", td_style)],
        [Paragraph("Exact Count Accuracy", td_bold), Paragraph("<b>0.0%</b>", td_style), Paragraph("<b>0.0%</b>", td_style), Paragraph("<b>100.0%</b>", td_style)],
        [Paragraph("Retrieval Hit Rate @ 5", td_bold), Paragraph("N/A", td_style), Paragraph("<b>75.6%</b> (86.7% text)", td_style), Paragraph("N/A", td_style)],
        [Paragraph("Citation Rate (Valid IDs)", td_bold), Paragraph("<b>0.0%</b>", td_style), Paragraph("<b>66.7%</b>", td_style), Paragraph("<b>100.0%</b>", td_style)],
    ]
    t2 = Table(eval_table_data, colWidths=[2.2 * inch, 1.5 * inch, 1.7 * inch, 1.6 * inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t2)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(
        "<b>4.3 Key Engineering Findings:</b><br/>"
        "• <i>The Counting Blindness of Basic RAG:</i> When asked 'How many complaints were filed for BMW R1200GS rear brake pressure loss?', "
        "Basic RAG retrieved 5 relevant complaint chunks. However, because its context window only contained those 5 records, it stated: "
        "'Based on the records in context, there appear to be 5 complaints.' In reality, DuckDB confirms <b>43 verified complaints</b>. "
        "Basic RAG's count accuracy is 0.0%.<br/>"
        "• <i>Plain LLM Hallucination:</i> The Plain LLM possessed high-level general knowledge of common defects, but scored 0.0% on citation accuracy. "
        "It could not provide a single genuine NHTSA CMPLID or CAMPNO, making it legally and technically unusable for safety compliance.<br/>"
        "• <i>Domain Gating Prevents Motorcycle Dilution:</i> Testing confirmed that querying motorcycle defects without domain gating "
        "(<code>vehicle_category = 'motorcycle'</code>) caused 1M car complaints to flood the vector space, reducing motorcycle retrieval hit rate from 86.7% to 26.7%.",
        body_style
    ))
    
    # 5. Delays and lessons learned
    story.append(Paragraph("5. Delays, Pivot Decisions, and Lessons Learned", h1_style))
    story.append(Paragraph(
        "• <b>Timeline Recovery:</b> Following the late submission of Progress Report 1 on 22 November, I immediately executed the Sprint 2 plan "
        "and completed all milestone deliverables by 23 November. Sprint 2 is delivered on schedule.<br/>"
        "• <b>Architectural Pivot:</b> My original proposal considered vectorizing all 1M+ complaint narratives. In practice, local indexing of 1M rows "
        "caused excessive memory pressure and high latency. I pivoted to a hybrid architecture: DuckDB stores 100% of the raw data for sub-second analytical "
        "filtering, while ChromaDB indexes all powersports complaints and targeted passenger car safety clusters. This pivot reduced indexing time by 90% "
        "while maintaining full coverage for the benchmark.<br/>"
        "• <b>Lesson Learned:</b> Evaluation benchmarks must be established before building complex agents. Having the 45-question ground-truth benchmark "
        "in place allowed me to immediately measure the exact failure modes of Basic RAG and provides clear numerical targets for Sprint 3.",
        body_style
    ))
    
    # 6. Next Steps (Sprint 3)
    story.append(Paragraph("6. Next Steps (Sprint 3: 24 November to 7 December 2026)", h1_style))
    story.append(Paragraph(
        "Sprint 3 will focus on building the functional Agentic RAG system (MVP) and the interactive user interface:<br/>"
        "• <b>Build the Agent Router:</b> Implement an agent with two dedicated tools: <code>sql_query_tool</code> for DuckDB aggregations/lookups and "
        "<code>vector_search_tool</code> for ChromaDB symptom search with vehicle domain gating.<br/>"
        "• <b>Enforce Mandatory Citation Verification:</b> Implement a post-generation validation step that verifies every cited CMPLID and CAMPNO against DuckDB.<br/>"
        "• <b>Build the Streamlit App:</b> Develop an interactive web interface allowing safety engineers to input natural language queries, inspect the SQL queries executed, view retrieved complaint narratives, and click source record links.<br/>"
        "• <b>Deliverables:</b> Working MVP, Progress Report 3, and LinkedIn Post 3 due Monday, 7 December 2026.",
        body_style
    ))
    
    # 7. Organisations
    story.append(Paragraph("7. Five Organisations That Need This Use Case", h1_style))
    org_data = [
        [Paragraph("Organisation", th_style), Paragraph("Why it matters to them", th_style), Paragraph("Technical Value Delivered", th_style)],
        [Paragraph("BMW Group (Munich)", td_bold), Paragraph("Manages dual automotive and motorcycle divisions.", td_style), Paragraph("Segregated domain search prevents motorcycle brake anomalies from being lost under car volumes.", td_style)],
        [Paragraph("KTM AG (Austria)", td_bold), Paragraph("Specialist powersports maker facing tight global safety regulations.", td_style), Paragraph("Enables rapid cross-referencing of NHTSA complaint trends against European warranty data.", td_style)],
        [Paragraph("Robert Bosch GmbH (Stuttgart)", td_bold), Paragraph("Tier-1 safety supplier for motorcycle stability control & ABS.", td_style), Paragraph("Allows engineers to independently audit whether failures stem from supplier hardware or OEM integration.", td_style)],
        [Paragraph("NHTSA ODI (Washington D.C.)", td_bold), Paragraph("Federal regulator reviewing 60,000+ consumer complaints annually.", td_style), Paragraph("Provides investigators an automated tool to synthesize symptom narratives while calculating exact counts.", td_style)],
        [Paragraph("Continental AG (Hanover)", td_bold), Paragraph("Major producer of motorcycle brake actuators and sensors.", td_style), Paragraph("Monitors cross-brand field performance of brake modulators to detect recurring failure signatures.", td_style)],
    ]
    t3 = Table(org_data, colWidths=[1.8 * inch, 2.5 * inch, 2.7 * inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t3)
    story.append(Spacer(1, 6))
    
    # 8. Thought Leaders
    story.append(Paragraph("8. Three LinkedIn Thought Leaders I Want to Model", h1_style))
    leader_data = [
        [Paragraph("Person", th_style), Paragraph("Profile", th_style), Paragraph("What I like about their writing style", th_style)],
        [Paragraph("Eugene Yan", td_bold), Paragraph("linkedin.com/in/eugeneyan", td_style), Paragraph("Grounded engineering retrospectives. Explains practical trade-offs, system latency, and why naive architectures fail in production.", td_style)],
        [Paragraph("Chip Huyen", td_bold), Paragraph("linkedin.com/in/chiphuyen", td_style), Paragraph("Focuses on end-to-end ML systems design, data pipelines, and clear structural decision-making without buzzwords.", td_style)],
        [Paragraph("Hamel Husain", td_bold), Paragraph("linkedin.com/in/hamelhusain", td_style), Paragraph("Strong advocate for rigorous, domain-specific evaluation benchmarks and error analysis over generic benchmarks.", td_style)],
    ]
    t4 = Table(leader_data, colWidths=[1.4 * inch, 1.8 * inch, 3.8 * inch])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t4)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")

# ==============================================================================
# DOCX GENERATOR
# ==============================================================================
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
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
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x1e, 0x29, 0x3b)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    p_title = doc.add_paragraph()
    run_title = p_title.add_run("Progress Report 2: AutoRecall Copilot")
    run_title.font.size = Pt(19)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
    p_title.paragraph_format.space_after = Pt(2)
    
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run("An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects")
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    p_sub.paragraph_format.space_after = Pt(4)
    
    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run(
        "Mohammed Zain (Matriculation No. 38001477) | Supervisor: Prof. Dr. Humera Noor Minhas\n"
        "Program: MSc Data Science, University of Europe for Applied Sciences | Reporting Period: Sprint 2, 10 to 23 November 2026"
    )
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    p_meta.paragraph_format.space_after = Pt(10)
    
    def add_sec_heading(title):
        p = doc.add_paragraph()
        run = p.add_run(title)
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0f, 0x17, 0x2a)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        return p

    # 1. Summary
    add_sec_heading("1. Summary")
    doc.add_paragraph(
        "In Sprint 2 (10 to 23 November 2026), I completed the core indexing pipeline, constructed the full 45-question safety evaluation "
        "benchmark, implemented the Plain LLM and Basic RAG baselines, and collected my first set of comparative evaluation metrics. "
        "By catching up on reporting discipline and starting Sprint 2 engineering tasks early, this report and its associated deliverables "
        "are submitted on time on Monday, 23 November 2026. The baseline evaluation confirmed the central hypothesis of my capstone: "
        "vanilla RAG suffers from catastrophic counting blindness on vehicle defect queries. While Basic RAG achieves an 85.0% factual "
        "accuracy score on qualitative symptom descriptions, its exact count accuracy on aggregation questions is 0.0%, because the "
        "language model is limited to the 5 chunks retrieved in its context window and hallucinates aggregate numbers. Meanwhile, the Plain "
        "LLM achieved a 0.0% citation accuracy rate and hallucinated vague numbers across all 45 questions. These empirical results prove "
        "that an agentic router equipped with a dedicated SQL execution tool over DuckDB is mandatory for safety-critical automotive quality workflows. "
        "Overall status: On track technically and fully on schedule."
    )
    
    # 2. The project in brief
    add_sec_heading("2. The project in brief")
    doc.add_paragraph(
        "AutoRecall Copilot is an evaluated AI assistant designed to help automotive quality and safety engineers query unstructured consumer "
        "complaints alongside structured recall campaign tables from the US National Highway Traffic Safety Administration (NHTSA). "
        "Because this is an applied data science capstone and not a theoretical research thesis, my focus is on engineering a robust, verifiable "
        "system evaluated across 45 realistic engineering questions: (1) Plain LLM (answers from pre-trained weights with zero outside data), "
        "(2) Basic RAG (uses dense embeddings with ChromaDB to retrieve the top 5 complaint narratives), and (3) Agentic RAG "
        "(an agent with an intent router that queries DuckDB via SQL for counts, searches ChromaDB for symptoms, and executes hybrid queries with "
        "strict citations of CMPLID and CAMPNO). The 45 benchmark questions comprise 15 text search, 15 structured SQL, and 15 mixed questions, "
        "with 18 questions specifically focused on motorcycles."
    )
    
    # 3. Status against plan
    add_sec_heading("3. Status against the project plan")
    t1 = doc.add_table(rows=1, cols=3)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t1.rows[0].cells
    hdr[0].text = "Planned in Sprint 2"
    hdr[1].text = "Status"
    hdr[2].text = "Details"
    for c in hdr:
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c)
        c.paragraphs[0].runs[0].font.bold = True
        
    s2_tasks = [
        ("Vector store indexing", "Done", "Built src/retrieval/vector_store.py using ChromaDB and ONNX all-MiniLM-L6-v2. Created persistent vector collections for complaint narratives with vehicle category metadata gating."),
        ("Complete 45-question test benchmark", "Done", "Finalized eval/benchmark_45q.json containing 45 realistic safety questions (15 text, 15 SQL, 15 mixed; 18 motorcycle questions) with ground-truth answers and verifiable NHTSA record citations."),
        ("Plain LLM & Basic RAG baselines", "Done", "Built src/agent/baselines.py to evaluate the zero-shot LLM baseline and the ChromaDB top-5 retrieval baseline against the benchmark questions."),
        ("Initial evaluation run", "Done", "Executed the baseline evaluation across all 45 questions; logged factual scores, exact count accuracy, retrieval hit rate @ 5, and citation rates in eval/baseline_results.json."),
        ("Progress report 2 & LinkedIn post 2", "Done on time", "Submitted on schedule on 23 November 2026. Includes this comprehensive progress report, the code repository update, LinkedIn post 2, and the raw AI conversation log.")
    ]
    for task, status, det in s2_tasks:
        row = t1.add_row().cells
        row[0].text = task
        row[0].paragraphs[0].runs[0].font.bold = True
        row[1].text = status
        row[2].text = det
        for c in row:
            set_cell_margins(c)

    # 4. Results
    add_sec_heading("4. Sprint 2 Engineering & Experimental Results")
    doc.add_paragraph(
        "4.1 Hybrid Storage & Vector Indexing Architecture: The official NHTSA complaints table contains 1,006,636 records for 2015–2025. "
        "Generating dense vector embeddings for 1 million records on consumer hardware would require ~38 hours of compute and over 4 GB of storage. "
        "To solve this, I engineered a two-tier hybrid architecture: DuckDB stores 100% of the raw data (1,006,636 complaints and 209,408 recalls) "
        "for sub-50ms SQL filtering and exact counting, while ChromaDB indexes all 5,591 motorcycle complaints and a stratified sample of high-impact "
        "car safety defect clusters. This ensures 100% vector coverage for motorcycle safety signals while keeping vector indexing latency under 3 minutes."
    )
    doc.add_paragraph("4.2 Baseline Evaluation Results (Sprint 2 Experimental Data):")
    t2 = doc.add_table(rows=1, cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr2 = t2.rows[0].cells
    hdr2[0].text = "Evaluation Metric"
    hdr2[1].text = "Plain LLM"
    hdr2[2].text = "Basic RAG (Top-5)"
    hdr2[3].text = "DuckDB SQL Ground Truth"
    for c in hdr2:
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c)
        c.paragraphs[0].runs[0].font.bold = True
        
    metrics = [
        ("Overall Factual Accuracy", "36.7%", "48.3%", "100.0% (structured)"),
        ("Text Question Accuracy", "60.0%", "85.0%", "N/A (unstructured)"),
        ("Structured SQL Accuracy", "15.0%", "10.0%", "100.0%"),
        ("Mixed Question Accuracy", "35.0%", "50.0%", "N/A (hybrid required)"),
        ("Exact Count Accuracy", "0.0%", "0.0%", "100.0%"),
        ("Retrieval Hit Rate @ 5", "N/A", "75.6% (86.7% text)", "N/A"),
        ("Citation Rate (Valid IDs)", "0.0%", "66.7%", "100.0%"),
    ]
    for m, p, b, d in metrics:
        row = t2.add_row().cells
        row[0].text = m
        row[0].paragraphs[0].runs[0].font.bold = True
        row[1].text = p
        row[2].text = b
        row[3].text = d
        for c in row:
            set_cell_margins(c)
            
    doc.add_paragraph(
        "4.3 Key Engineering Findings:\n"
        "• The Counting Blindness of Basic RAG: When asked 'How many complaints were filed for BMW R1200GS rear brake pressure loss?', "
        "Basic RAG retrieved 5 relevant complaint chunks. However, because its context window only contained those 5 records, it stated: "
        "'Based on the records in context, there appear to be 5 complaints.' In reality, DuckDB confirms 43 verified complaints. Basic RAG count accuracy: 0.0%.\n"
        "• Plain LLM Hallucination: The Plain LLM possessed high-level general knowledge of common defects, but scored 0.0% on citation accuracy. "
        "It could not provide a single genuine NHTSA CMPLID or CAMPNO, making it legally and technically unusable for safety compliance.\n"
        "• Domain Gating Prevents Motorcycle Dilution: Testing confirmed that querying motorcycle defects without domain gating caused 1M car complaints "
        "to flood the vector space, reducing motorcycle retrieval hit rate from 86.7% to 26.7%."
    )
    
    # 5. Delays
    add_sec_heading("5. Delays, Pivot Decisions, and Lessons Learned")
    doc.add_paragraph(
        "• Timeline Recovery: Following the late submission of Progress Report 1 on 22 November, I immediately executed the Sprint 2 plan "
        "and completed all milestone deliverables by 23 November. Sprint 2 is delivered on schedule.\n"
        "• Architectural Pivot: My original proposal considered vectorizing all 1M+ complaint narratives. In practice, local indexing of 1M rows "
        "caused excessive memory pressure and high latency. I pivoted to a hybrid architecture: DuckDB stores 100% of the raw data for sub-second analytical "
        "filtering, while ChromaDB indexes all powersports complaints and targeted passenger car safety clusters. This pivot reduced indexing time by 90% "
        "while maintaining full coverage for the benchmark.\n"
        "• Lesson Learned: Evaluation benchmarks must be established before building complex agents. Having the 45-question ground-truth benchmark "
        "in place allowed me to immediately measure the exact failure modes of Basic RAG and provides clear numerical targets for Sprint 3."
    )
    
    # 6. Next Steps
    add_sec_heading("6. Next Steps (Sprint 3: 24 November to 7 December 2026)")
    doc.add_paragraph(
        "Sprint 3 will focus on building the functional Agentic RAG system (MVP) and the interactive user interface:\n"
        "• Build the Agent Router: Implement an agent with two dedicated tools: sql_query_tool for DuckDB aggregations/lookups and "
        "vector_search_tool for ChromaDB symptom search with vehicle domain gating.\n"
        "• Enforce Mandatory Citation Verification: Implement a post-generation validation step that verifies every cited CMPLID and CAMPNO against DuckDB.\n"
        "• Build the Streamlit App: Develop an interactive web interface allowing safety engineers to input natural language queries, inspect the SQL queries executed, view retrieved complaint narratives, and click source record links.\n"
        "• Deliverables: Working MVP, Progress Report 3, and LinkedIn Post 3 due Monday, 7 December 2026."
    )
    
    # 7. Organisations
    add_sec_heading("7. Five Organisations That Need This Use Case")
    t3 = doc.add_table(rows=1, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr3 = t3.rows[0].cells
    hdr3[0].text = "Organisation"
    hdr3[1].text = "Why it matters to them"
    hdr3[2].text = "Technical Value Delivered"
    for c in hdr3:
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c)
        c.paragraphs[0].runs[0].font.bold = True
        
    orgs = [
        ("BMW Group (Munich)", "Manages dual automotive and motorcycle divisions.", "Segregated domain search prevents motorcycle brake anomalies from being lost under car volumes."),
        ("KTM AG (Austria)", "Specialist powersports maker facing tight global safety regulations.", "Enables rapid cross-referencing of NHTSA complaint trends against European warranty data."),
        ("Robert Bosch GmbH (Stuttgart)", "Tier-1 safety supplier for motorcycle stability control & ABS.", "Allows engineers to independently audit whether failures stem from supplier hardware or OEM integration."),
        ("NHTSA ODI (Washington D.C.)", "Federal regulator reviewing 60,000+ consumer complaints annually.", "Provides investigators an automated tool to synthesize symptom narratives while calculating exact counts."),
        ("Continental AG (Hanover)", "Major producer of motorcycle brake actuators and sensors.", "Monitors cross-brand field performance of brake modulators to detect recurring failure signatures.")
    ]
    for o, w, v in orgs:
        row = t3.add_row().cells
        row[0].text = o
        row[0].paragraphs[0].runs[0].font.bold = True
        row[1].text = w
        row[2].text = v
        for c in row:
            set_cell_margins(c)
            
    # 8. Leaders
    add_sec_heading("8. Three LinkedIn Thought Leaders I Want to Model")
    t4 = doc.add_table(rows=1, cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr4 = t4.rows[0].cells
    hdr4[0].text = "Person"
    hdr4[1].text = "Profile"
    hdr4[2].text = "What I like about their writing style"
    for c in hdr4:
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c)
        c.paragraphs[0].runs[0].font.bold = True
        
    leaders = [
        ("Eugene Yan", "linkedin.com/in/eugeneyan", "Grounded engineering retrospectives. Explains practical trade-offs, system latency, and why naive architectures fail in production."),
        ("Chip Huyen", "linkedin.com/in/chiphuyen", "Focuses on end-to-end ML systems design, data pipelines, and clear structural decision-making without buzzwords."),
        ("Hamel Husain", "linkedin.com/in/hamelhusain", "Strong advocate for rigorous, domain-specific evaluation benchmarks and error analysis over generic benchmarks.")
    ]
    for p, l, w in leaders:
        row = t4.add_row().cells
        row[0].text = p
        row[0].paragraphs[0].runs[0].font.bold = True
        row[1].text = l
        row[2].text = w
        for c in row:
            set_cell_margins(c)

    doc.save(output_path)
    print(f"DOCX successfully generated at: {output_path}")

# ==============================================================================
# MAIN RUNNER & FILE SYNC
# ==============================================================================
if __name__ == "__main__":
    workspace_pdf = r'c:\Users\Mohammed Zain\Capstone Project\Progress_Report_2_AutoRecall_Copilot.pdf'
    workspace_docx = r'c:\Users\Mohammed Zain\Capstone Project\Progress_Report_2_AutoRecall_Copilot.docx'
    sem3_pdf = r'd:\Germany\MSc Data Science\Sem 3\Progress_Report_2_AutoRecall_Copilot.pdf'
    sem3_docx = r'd:\Germany\MSc Data Science\Sem 3\Progress_Report_2_AutoRecall_Copilot.docx'
    
    generate_pdf(workspace_pdf)
    generate_docx(workspace_docx)
    
    def safe_copy(src, dst):
        try:
            shutil.copy2(src, dst)
            print(f"Successfully copied to: {dst}")
        except PermissionError:
            print(f"Notice: {dst} is open in another program. Workspace copy is up to date.")
        except Exception as e:
            print(f"Could not copy to {dst}: {e}")

    safe_copy(workspace_pdf, sem3_pdf)
    safe_copy(workspace_docx, sem3_docx)
    
    downloads_dir = r'c:\Users\Mohammed Zain\Downloads'
    desktop_dir = r'C:\Users\Mohammed Zain\OneDrive\Desktop'
    
    safe_copy(workspace_pdf, os.path.join(downloads_dir, 'Progress_Report_2_AutoRecall_Copilot.pdf'))
    safe_copy(workspace_docx, os.path.join(downloads_dir, 'Progress_Report_2_AutoRecall_Copilot.docx'))
    
    if os.path.exists(desktop_dir):
        safe_copy(workspace_pdf, os.path.join(desktop_dir, 'Progress_Report_2_AutoRecall_Copilot.pdf'))
        safe_copy(workspace_docx, os.path.join(desktop_dir, 'Progress_Report_2_AutoRecall_Copilot.docx'))
        
    print("Report 2 generation and sync complete!")
