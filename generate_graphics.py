import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set style
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

ASSETS_DIR = r'c:\Users\Mohammed Zain\Capstone Project\assets'
DESKTOP_DIR = r'C:\Users\Mohammed Zain\OneDrive\Desktop'
ARTIFACT_DIR = r'C:\Users\Mohammed Zain\.gemini\antigravity\brain\5ade54c2-2762-462c-a9e8-a4ca2df3ae9e'

os.makedirs(ASSETS_DIR, exist_ok=True)

# ==============================================================================
# GRAPHIC 1: SPRINT 1 (Why RAG Fails on Safety Defect Counting)
# ==============================================================================
def create_post_1_graphic():
    fig = plt.figure(figsize=(14, 8), dpi=200, facecolor='#0f172a')
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1.1, 0.9],
                          left=0.06, right=0.94, top=0.88, bottom=0.08, wspace=0.18, hspace=0.32)

    # Title & Subtitle
    fig.text(0.06, 0.94, "AutoRecall Copilot | Why Vanilla RAG Fails on Defect Counting", 
             fontsize=20, weight='bold', color='#f8fafc')
    fig.text(0.06, 0.90, "Evaluating Semantic Vector Search vs. Columnar SQL over 1,000,000+ Official NHTSA Records", 
             fontsize=12, color='#94a3b8')

    # Panel 1: Test Case Failure Mode
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor('#1e293b')
    ax1.axis('off')
    
    # Border
    rect1 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                   linewidth=1.2, edgecolor='#334155', facecolor='#1e293b', transform=ax1.transAxes)
    ax1.add_patch(rect1)

    ax1.text(0.03, 0.85, "TEST CASE: BMW R1200GS REAR BRAKE HYDRAULIC PRESSURE LOSS (2018–2022)", 
             fontsize=11, weight='bold', color='#38bdf8', transform=ax1.transAxes)
    ax1.text(0.03, 0.70, "Engineering Question: 'How many complaints were filed for BMW R1200GS rear brake pressure loss, and what are the symptoms?'", 
             fontsize=10.5, style='italic', color='#e2e8f0', transform=ax1.transAxes)

    # Two comparison cards
    # Left Card: Basic RAG
    card_left = patches.FancyBboxPatch((0.03, 0.08), 0.45, 0.48, boxstyle="round,pad=0.015,rounding_size=0.02",
                                       linewidth=1, edgecolor='#ef4444', facecolor='#0f172a', transform=ax1.transAxes)
    ax1.add_patch(card_left)
    ax1.text(0.05, 0.44, "FAILED: Basic RAG (Vector Top-5)", fontsize=11, weight='bold', color='#f87171', transform=ax1.transAxes)
    ax1.text(0.05, 0.31, "• Retrieves top-5 most similar complaint narratives.\n• Context window contains only 5 chunks.\n• Hallucinates count: 'Around 10 to 12 complaints.'\n• Exact Count Error: 74% undercount!", 
             fontsize=9.5, color='#cbd5e1', transform=ax1.transAxes)

    # Right Card: AutoRecall Copilot
    card_right = patches.FancyBboxPatch((0.52, 0.08), 0.45, 0.48, boxstyle="round,pad=0.015,rounding_size=0.02",
                                        linewidth=1, edgecolor='#10b981', facecolor='#0f172a', transform=ax1.transAxes)
    ax1.add_patch(card_right)
    ax1.text(0.54, 0.44, "GROUND TRUTH: AutoRecall Copilot (DuckDB SQL)", fontsize=11, weight='bold', color='#34d399', transform=ax1.transAxes)
    ax1.text(0.54, 0.31, "• Executes exact SQL aggregation over 1,006,636 rows.\n• Queries vector index for symptom text in parallel.\n• Returns Ground Truth: Exactly 43 verified complaints.\n• Cites exact CMPLID IDs & TSB service bulletin.", 
             fontsize=9.5, color='#cbd5e1', transform=ax1.transAxes)

    # Panel 2: The Motorcycle Blind Spot (Donut & Disparity)
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor('#1e293b')
    rect2 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                   linewidth=1.2, edgecolor='#334155', facecolor='#1e293b', transform=ax2.transAxes)
    ax2.add_patch(rect2)
    ax2.axis('off')

    ax2.text(0.05, 0.86, "THE MOTORCYCLE DATA DISPARITY (NHTSA 2015–2025)", 
             fontsize=10.5, weight='bold', color='#f59e0b', transform=ax2.transAxes)
    ax2.text(0.05, 0.70, "1,001,045 Passenger Car Complaints  (99.44%)\n"
                         "        5,591 Motorcycle Complaints     (0.56%)", 
             fontsize=10, family='monospace', color='#e2e8f0', transform=ax2.transAxes)

    ax2.text(0.05, 0.48, "[!] Crash Rate in Complaints: 5.72% for motorcycles (320 crashes)\n"
                         "[!] Recall Share: 2.5x higher representation than complaints\n"
                         "[!] Signal Dilution: Without domain filtering, 1M car complaints\n"
                         "    completely bury subtle two-wheeler safety anomalies.",
             fontsize=9.5, color='#cbd5e1', transform=ax2.transAxes)

    # Panel 3: Architecture Stack
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor('#1e293b')
    rect3 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                   linewidth=1.2, edgecolor='#334155', facecolor='#1e293b', transform=ax3.transAxes)
    ax3.add_patch(rect3)
    ax3.axis('off')

    ax3.text(0.05, 0.86, "AUTORECALL COPILOT ARCHITECTURE", 
             fontsize=10.5, weight='bold', color='#38bdf8', transform=ax3.transAxes)

    steps = [
        ("1. Official NHTSA Ingestion", "1M+ complaints + 209k recalls loaded directly into DuckDB"),
        ("2. Two-Tier Storage", "DuckDB (sub-50ms SQL) + ChromaDB (symptom vectors)"),
        ("3. Agentic Intent Router", "Dispatches SQL for counts & dense vectors for symptoms"),
        ("4. Audit & Citation Layer", "Every answer verifies CMPLID & CAMPNO against database")
    ]
    y_pos = 0.68
    for title, desc in steps:
        ax3.text(0.05, y_pos, title, fontsize=9.5, weight='bold', color='#67e8f9', transform=ax3.transAxes)
        ax3.text(0.05, y_pos - 0.08, desc, fontsize=8.5, color='#94a3b8', transform=ax3.transAxes)
        y_pos -= 0.17

    # Footer
    fig.text(0.06, 0.025, "Mohammed Zain | MSc Data Science Capstone | University of Europe for Applied Sciences (UE)", 
             fontsize=9.5, color='#64748b')

    out_path = os.path.join(ASSETS_DIR, 'linkedin_post_1_graphic.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Created: {out_path}")
    return out_path

# ==============================================================================
# GRAPHIC 2: SPRINT 2 (45-Question Benchmark Results)
# ==============================================================================
def create_post_2_graphic():
    fig = plt.figure(figsize=(14, 8), dpi=200, facecolor='#0f172a')
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 0.8], width_ratios=[1.1, 0.9],
                          left=0.06, right=0.94, top=0.88, bottom=0.08, wspace=0.18, hspace=0.32)

    # Title & Subtitle
    fig.text(0.06, 0.94, "AutoRecall Copilot | 45-Question Safety Defect Benchmark", 
             fontsize=20, weight='bold', color='#f8fafc')
    fig.text(0.06, 0.90, "First Results: Plain LLM Baseline vs. Basic RAG (Top-5) vs. Structured Ground Truth", 
             fontsize=12, color='#94a3b8')

    # Panel 1: Bar Chart of Accuracies across Categories
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#1e293b')
    for spine in ax1.spines.values():
        spine.set_color('#334155')

    categories = ['Text Symptoms\n(15Q)', 'Structured SQL\n(15Q)', 'Mixed / Hybrid\n(15Q)', 'Overall\n(45Q)']
    plain_acc = [60.0, 15.0, 35.0, 36.7]
    rag_acc = [85.0, 10.0, 50.0, 48.3]
    gt_acc = [100.0, 100.0, 100.0, 100.0]

    x = np.arange(len(categories))
    width = 0.35

    rects1 = ax1.bar(x - width/2, plain_acc, width, label='Plain LLM (Zero-Shot)', color='#f87171', edgecolor='#ef4444')
    rects2 = ax1.bar(x + width/2, rag_acc, width, label='Basic RAG (Top-5)', color='#38bdf8', edgecolor='#0284c7')

    ax1.set_ylabel('Factual Accuracy (%)', color='#f8fafc', fontsize=10.5, weight='bold')
    ax1.set_title('ACCURACY ACROSS QUESTION CATEGORIES', color='#38bdf8', fontsize=11, weight='bold', pad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, color='#e2e8f0', fontsize=9.5)
    ax1.set_ylim(0, 105)
    ax1.grid(axis='y', color='#334155', linestyle='--', alpha=0.7)
    ax1.tick_params(axis='y', colors='#94a3b8')
    ax1.legend(facecolor='#0f172a', edgecolor='#334155', labelcolor='#e2e8f0', loc='upper right', fontsize=9)

    # Bar value labels
    for rect in rects1:
        h = rect.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                     color='#fca5a5', fontsize=8.5, weight='bold')
    for rect in rects2:
        h = rect.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                     color='#7dd3fc', fontsize=8.5, weight='bold')

    # Panel 2: The Two Critical Failure Modes (Cards)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#1e293b')
    rect2 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                   linewidth=1.2, edgecolor='#334155', facecolor='#1e293b', transform=ax2.transAxes)
    ax2.add_patch(rect2)
    ax2.axis('off')

    ax2.text(0.05, 0.88, "CRITICAL SAFETY AUDIT METRICS", 
             fontsize=11, weight='bold', color='#f59e0b', transform=ax2.transAxes)

    # Failure 1
    ax2.text(0.05, 0.74, "1. Exact Count Accuracy: 0.0%", fontsize=10.5, weight='bold', color='#ef4444', transform=ax2.transAxes)
    ax2.text(0.05, 0.58, "• Basic RAG has 0.0% count accuracy on aggregation queries.\n"
                         "• Top-5 retrieval forces the model to observe only 5 chunks.\n"
                         "• When asked for defect volume, it answers 'approximately 5.'",
             fontsize=9, color='#cbd5e1', transform=ax2.transAxes)

    # Failure 2
    ax2.text(0.05, 0.44, "2. Plain LLM Citation Rate: 0.0%", fontsize=10.5, weight='bold', color='#f87171', transform=ax2.transAxes)
    ax2.text(0.05, 0.28, "• Zero-shot LLM cannot cite a single genuine CMPLID or\n"
                         "  NHTSA Recall Campaign Number (CAMPNO).\n"
                         "• In automotive safety compliance, unverified claims are\n"
                         "  legally and technically unacceptable.",
             fontsize=9, color='#cbd5e1', transform=ax2.transAxes)

    # Panel 3: Benchmark Structure Table
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#1e293b')
    rect3 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                   linewidth=1.2, edgecolor='#334155', facecolor='#1e293b', transform=ax3.transAxes)
    ax3.add_patch(rect3)
    ax3.axis('off')

    ax3.text(0.05, 0.84, "BENCHMARK COMPOSITION (eval/benchmark_45q.json)", 
             fontsize=10.5, weight='bold', color='#38bdf8', transform=ax3.transAxes)

    b_text = (
        "• 15 Text Search Queries:  Brake fade, stator burnouts, clutch creep, battery fires\n"
        "• 15 Structured SQL Queries: Exact complaint counts, crash rates, annual trends\n"
        "• 15 Mixed Hybrid Queries: Cross-referencing symptoms with recall campaigns\n"
        "• 18 Motorcycle Questions (40%): Dedicated evaluation to prevent car dilution\n"
        "• Verifiable Ground Truth: Every question backed by official NHTSA primary keys"
    )
    ax3.text(0.05, 0.18, b_text, fontsize=9.2, color='#cbd5e1', transform=ax3.transAxes)

    # Panel 4: Sprint 3 Solution
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#1e293b')
    rect4 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.03",
                                   linewidth=1.2, edgecolor='#10b981', facecolor='#1e293b', transform=ax4.transAxes)
    ax4.add_patch(rect4)
    ax4.axis('off')

    ax4.text(0.05, 0.84, "SPRINT 3 TARGET: THE AGENTIC ROUTER", 
             fontsize=10.5, weight='bold', color='#34d399', transform=ax4.transAxes)

    s3_text = (
        "• Goal: Beat Basic RAG on mixed questions by at least +10 pp.\n"
        "• SQL Tool: Dispatches DuckDB queries for exact mathematical counts.\n"
        "• Vector Tool: ChromaDB queries for qualitative symptom narratives.\n"
        "• Citation Validator: Enforces mandatory CMPLID & CAMPNO citations.\n"
        "• Streamlit App: Interactive decision dashboard for safety engineers."
    )
    ax4.text(0.05, 0.18, s3_text, fontsize=9.2, color='#cbd5e1', transform=ax4.transAxes)

    # Footer
    fig.text(0.06, 0.025, "Mohammed Zain | MSc Data Science Capstone | University of Europe for Applied Sciences (UE)", 
             fontsize=9.5, color='#64748b')

    out_path = os.path.join(ASSETS_DIR, 'linkedin_post_2_graphic.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Created: {out_path}")
    return out_path

if __name__ == "__main__":
    p1 = create_post_1_graphic()
    p2 = create_post_2_graphic()
    
    # Copy to Desktop
    shutil.copy2(p1, os.path.join(DESKTOP_DIR, 'LinkedIn_Post_1_Graphic.png'))
    shutil.copy2(p2, os.path.join(DESKTOP_DIR, 'LinkedIn_Post_2_Graphic.png'))
    
    # Copy to Artifact directory for inline display
    shutil.copy2(p1, os.path.join(ARTIFACT_DIR, 'LinkedIn_Post_1_Graphic.png'))
    shutil.copy2(p2, os.path.join(ARTIFACT_DIR, 'LinkedIn_Post_2_Graphic.png'))
    print("Copied both graphics to Desktop and Artifact directory!")
