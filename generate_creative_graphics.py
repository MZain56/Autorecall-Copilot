import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set font family
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']

ASSETS_DIR = r'c:\Users\Mohammed Zain\Capstone Project\assets'
DESKTOP_DIR = r'C:\Users\Mohammed Zain\OneDrive\Desktop'
ARTIFACT_DIR = r'C:\Users\Mohammed Zain\.gemini\antigravity\brain\5ade54c2-2762-462c-a9e8-a4ca2df3ae9e'

os.makedirs(ASSETS_DIR, exist_ok=True)

# Helper function to draw a modern pill badge
def draw_badge(ax, x, y, width, height, text, bg_color, border_color, text_color, fontsize=8.5, weight='bold'):
    badge = patches.FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.005,rounding_size=0.02",
                                   linewidth=1, edgecolor=border_color, facecolor=bg_color, transform=ax.transAxes)
    ax.add_patch(badge)
    ax.text(x + width/2, y + height/2, text, fontsize=fontsize, weight=weight, color=text_color,
            ha='center', va='center', transform=ax.transAxes)

# ==============================================================================
# CREATIVE GRAPHIC 1: THE COUNTING BLINDNESS OF RAG
# ==============================================================================
def create_creative_post_1():
    fig = plt.figure(figsize=(16, 9), dpi=220, facecolor='#090d16')
    
    # Grid: Top test case split (2 columns), Bottom 2 cards (2 columns)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 0.85], width_ratios=[1, 1],
                          left=0.04, right=0.96, top=0.84, bottom=0.05, wspace=0.12, hspace=0.22)

    # Header section
    ax_head = fig.add_axes([0.04, 0.86, 0.92, 0.12], facecolor='none')
    ax_head.axis('off')
    
    # Category Pill
    draw_badge(ax_head, 0.0, 0.70, 0.28, 0.25, "NHTSA DATA ARCHITECTURE • 1,006,636 RECORDS", 
               "#1e1b4b", "#6366f1", "#c7d2fe", fontsize=8.5)
    
    ax_head.text(0.0, 0.55, "AutoRecall Copilot | The Counting Blindness of Vanilla RAG", 
                 fontsize=21, weight='bold', color='#f8fafc', va='top')
    ax_head.text(0.0, 0.12, "Why semantic vector search undercounts automotive safety defects by 74%—and why mission-critical AI needs SQL.", 
                 fontsize=11.5, color='#94a3b8', va='top')

    # -------------------------------------------------------------------------
    # Panel 1 (Top Left): The Failure Case (Basic RAG)
    # -------------------------------------------------------------------------
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor('#111827')
    ax1.axis('off')
    
    # Outer Card Box with Red accent border
    card1 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.025",
                                   linewidth=1.2, edgecolor='#dc2626', facecolor='#111827', transform=ax1.transAxes)
    ax1.add_patch(card1)
    
    # Top accent bar
    top_bar1 = patches.FancyBboxPatch((0.02, 0.96), 0.96, 0.02, boxstyle="round,pad=0.002,rounding_size=0.005",
                                     linewidth=0, facecolor='#ef4444', transform=ax1.transAxes)
    ax1.add_patch(top_bar1)

    draw_badge(ax1, 0.04, 0.86, 0.38, 0.07, "VANILLA RAG (SEMANTIC VECTOR SEARCH)", 
               "#450a0a", "#ef4444", "#fca5a5", fontsize=8)
    
    ax1.text(0.04, 0.78, "Query: 'How many complaints for BMW R1200GS rear brake pressure loss?'", 
             fontsize=9.5, style='italic', color='#94a3b8', va='top', transform=ax1.transAxes)

    # Visual Flow Box
    flow_box_1 = patches.FancyBboxPatch((0.04, 0.38), 0.92, 0.33, boxstyle="round,pad=0.01,rounding_size=0.015",
                                        linewidth=0.8, edgecolor='#374151', facecolor='#0b0f19', transform=ax1.transAxes)
    ax1.add_patch(flow_box_1)
    
    ax1.text(0.07, 0.65, "1. Vector Retrieval  -->  Fetches Top-5 nearest neighbors (k=5)", fontsize=9, color='#e2e8f0', va='top', transform=ax1.transAxes)
    ax1.text(0.07, 0.55, "2. Context Window   -->  Language model only sees 5 complaint narratives", fontsize=9, color='#e2e8f0', va='top', transform=ax1.transAxes)
    ax1.text(0.07, 0.45, "3. Synthesis Step   -->  LLM guesses: 'There appear to be around 10 to 12.'", fontsize=9, color='#f87171', weight='bold', va='top', transform=ax1.transAxes)

    # Stat Callout Banner
    stat_box_1 = patches.FancyBboxPatch((0.04, 0.07), 0.92, 0.25, boxstyle="round,pad=0.01,rounding_size=0.015",
                                        linewidth=1, edgecolor='#ef4444', facecolor='#1f1315', transform=ax1.transAxes)
    ax1.add_patch(stat_box_1)
    ax1.text(0.08, 0.25, "74% UNDERCOUNT ERROR", fontsize=15, weight='bold', color='#ef4444', va='top', transform=ax1.transAxes)
    ax1.text(0.08, 0.13, "Vector similarity measures linguistic proximity, NOT dataset volume.\nTruncating to top-5 chunks hides 88% of real component failures.", 
             fontsize=8.5, color='#cbd5e1', va='top', transform=ax1.transAxes)

    # -------------------------------------------------------------------------
    # Panel 2 (Top Right): The Solution (AutoRecall Copilot)
    # -------------------------------------------------------------------------
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#111827')
    ax2.axis('off')
    
    card2 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.025",
                                   linewidth=1.2, edgecolor='#059669', facecolor='#111827', transform=ax2.transAxes)
    ax2.add_patch(card2)

    top_bar2 = patches.FancyBboxPatch((0.02, 0.96), 0.96, 0.02, boxstyle="round,pad=0.002,rounding_size=0.005",
                                     linewidth=0, facecolor='#10b981', transform=ax2.transAxes)
    ax2.add_patch(top_bar2)

    draw_badge(ax2, 0.04, 0.86, 0.42, 0.07, "AUTORECALL COPILOT (AGENT + COLUMNAR SQL)", 
               "#064e3b", "#10b981", "#6ee7b7", fontsize=8)

    ax2.text(0.04, 0.78, "Query: 'How many complaints for BMW R1200GS rear brake pressure loss?'", 
             fontsize=9.5, style='italic', color='#94a3b8', va='top', transform=ax2.transAxes)

    flow_box_2 = patches.FancyBboxPatch((0.04, 0.38), 0.92, 0.33, boxstyle="round,pad=0.01,rounding_size=0.015",
                                        linewidth=0.8, edgecolor='#374151', facecolor='#0b0f19', transform=ax2.transAxes)
    ax2.add_patch(flow_box_2)

    ax2.text(0.07, 0.65, "1. Intent Router    -->  Detects aggregation intent ('how many')", fontsize=9, color='#e2e8f0', va='top', transform=ax2.transAxes)
    ax2.text(0.07, 0.55, "2. SQL Dispatch     -->  DuckDB scans 1,006,636 records in 32 milliseconds", fontsize=9, color='#e2e8f0', va='top', transform=ax2.transAxes)
    ax2.text(0.07, 0.45, "3. Hybrid Result    -->  Exact count: 43 verified complaints + CMPLID citations", fontsize=9, color='#34d399', weight='bold', va='top', transform=ax2.transAxes)

    stat_box_2 = patches.FancyBboxPatch((0.04, 0.07), 0.92, 0.25, boxstyle="round,pad=0.01,rounding_size=0.015",
                                        linewidth=1, edgecolor='#10b981', facecolor='#0d1f18', transform=ax2.transAxes)
    ax2.add_patch(stat_box_2)
    ax2.text(0.08, 0.25, "100% MATHEMATICAL EXACTNESS", fontsize=15, weight='bold', color='#10b981', va='top', transform=ax2.transAxes)
    ax2.text(0.08, 0.13, "Pairs qualitative symptom retrieval with exact SQL analytical counting.\nEvery factual statement is backed by verifiable regulatory record IDs.", 
             fontsize=8.5, color='#cbd5e1', va='top', transform=ax2.transAxes)

    # -------------------------------------------------------------------------
    # Panel 3 (Bottom Left): The Motorcycle Defect Disparity Infographic
    # -------------------------------------------------------------------------
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor('#111827')
    ax3.axis('off')
    
    card3 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.025",
                                   linewidth=1.2, edgecolor='#f59e0b', facecolor='#111827', transform=ax3.transAxes)
    ax3.add_patch(card3)

    draw_badge(ax3, 0.04, 0.84, 0.48, 0.09, "DATA DISPARITY: CARS VS. MOTORCYCLES (2015-2025)", 
               "#451a03", "#f59e0b", "#fde68a", fontsize=8)

    # Proportional visualization bars
    ax3.text(0.05, 0.73, "Complaints Volume Share", fontsize=9, weight='bold', color='#e2e8f0', va='top', transform=ax3.transAxes)
    bar_bg1 = patches.Rectangle((0.05, 0.58), 0.90, 0.07, facecolor='#1f2937', edgecolor='#374151', transform=ax3.transAxes)
    ax3.add_patch(bar_bg1)
    bar_car = patches.Rectangle((0.05, 0.58), 0.89, 0.07, facecolor='#3b82f6', transform=ax3.transAxes)
    ax3.add_patch(bar_car)
    bar_moto = patches.Rectangle((0.94, 0.58), 0.01, 0.07, facecolor='#f59e0b', transform=ax3.transAxes)
    ax3.add_patch(bar_moto)
    ax3.text(0.07, 0.625, "Passenger Cars: 1,001,045 (99.44%)", fontsize=8, weight='bold', color='#ffffff', va='center', transform=ax3.transAxes)
    ax3.text(0.95, 0.625, "0.56%", fontsize=8, weight='bold', color='#fbbf24', va='center', transform=ax3.transAxes)

    ax3.text(0.05, 0.49, "Key Safety Finding: Crash Involvement Rate", fontsize=9, weight='bold', color='#e2e8f0', va='top', transform=ax3.transAxes)
    ax3.text(0.05, 0.38, "• Motorcycles: 5.72% Crash Rate (320 crashes) — 5x higher severity than passenger cars!\n"
                         "• Recall Multiplier: Motorcycles represent 1.34% of recalls vs 0.56% of complaints (2.5x ratio).\n"
                         "• Core Rule: Explicit domain gating is mandatory so 1M car complaints don't bury bike defects.",
             fontsize=8.5, color='#cbd5e1', linespacing=1.35, va='top', transform=ax3.transAxes)

    # -------------------------------------------------------------------------
    # Panel 4 (Bottom Right): Two-Tier Architecture Infographic
    # -------------------------------------------------------------------------
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#111827')
    ax4.axis('off')
    
    card4 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.025",
                                   linewidth=1.2, edgecolor='#06b6d4', facecolor='#111827', transform=ax4.transAxes)
    ax4.add_patch(card4)

    draw_badge(ax4, 0.04, 0.84, 0.40, 0.09, "TWO-TIER HYBRID ARCHITECTURE", 
               "#083344", "#06b6d4", "#a5f3fc", fontsize=8)

    layers = [
        ("Tier 1: Columnar Analytical Store (DuckDB)", "Ingests 100% of 1,006,636 complaints & 209k recalls. Sub-50ms exact SQL counts."),
        ("Tier 2: Dense Semantic Index (ChromaDB)", "Indexes all powersports + high-risk car defects with all-MiniLM-L6-v2 embeddings."),
        ("Tier 3: Agentic Router & Citation Enforcement", "Dispatches query intent and validates all CMPLID & CAMPNO citations before reply.")
    ]
    y_layer = 0.70
    for l_title, l_desc in layers:
        ax4.text(0.05, y_layer, l_title, fontsize=9.2, weight='bold', color='#67e8f9', va='top', transform=ax4.transAxes)
        ax4.text(0.05, y_layer - 0.07, l_desc, fontsize=8.2, color='#94a3b8', va='top', transform=ax4.transAxes)
        y_layer -= 0.17

    out_path = os.path.join(ASSETS_DIR, 'linkedin_post_1_graphic.png')
    plt.savefig(out_path, dpi=220, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Created creative Graphic 1 at: {out_path}")
    return out_path

# ==============================================================================
# CREATIVE GRAPHIC 2: 45-QUESTION BENCHMARK PERFORMANCE
# ==============================================================================
def create_creative_post_2():
    fig = plt.figure(figsize=(16, 9), dpi=220, facecolor='#090d16')
    
    # 3 Stat Cards on Top, Bar Chart + Roadmap below
    gs = fig.add_gridspec(2, 3, height_ratios=[0.45, 1.15], width_ratios=[1, 1, 1],
                          left=0.04, right=0.96, top=0.84, bottom=0.05, wspace=0.12, hspace=0.20)

    # Header section
    ax_head = fig.add_axes([0.04, 0.86, 0.92, 0.12], facecolor='none')
    ax_head.axis('off')
    
    draw_badge(ax_head, 0.0, 0.70, 0.28, 0.25, "EMPIRICAL EVALUATION • SPRINT 2 BENCHMARK", 
               "#1e1b4b", "#6366f1", "#c7d2fe", fontsize=8.5)
    
    ax_head.text(0.0, 0.55, "AutoRecall Copilot | 45-Question Safety Benchmark Scorecard", 
                 fontsize=21, weight='bold', color='#f8fafc', va='top')
    ax_head.text(0.0, 0.12, "First evaluation run: Plain LLM (Zero-Shot) vs. Basic RAG (Top-5) vs. Structured Ground Truth across 45 vehicle defect queries.", 
                 fontsize=11.5, color='#94a3b8', va='top')

    # -------------------------------------------------------------------------
    # Top 3 Stat Cards
    # -------------------------------------------------------------------------
    # Card 1: Text Accuracy
    ax_s1 = fig.add_subplot(gs[0, 0])
    ax_s1.set_facecolor('#111827')
    ax_s1.axis('off')
    b1 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.03",
                                linewidth=1, edgecolor='#06b6d4', facecolor='#111827', transform=ax_s1.transAxes)
    ax_s1.add_patch(b1)
    draw_badge(ax_s1, 0.06, 0.70, 0.45, 0.20, "TEXT ACCURACY (15Q)", "#083344", "#06b6d4", "#a5f3fc", fontsize=7.5)
    ax_s1.text(0.06, 0.58, "85.0%", fontsize=22, weight='bold', color='#38bdf8', va='top', transform=ax_s1.transAxes)
    ax_s1.text(0.06, 0.22, "Basic RAG excels at qualitative symptom matching (vs. 60.0% Plain LLM).", 
               fontsize=8, color='#cbd5e1', va='top', transform=ax_s1.transAxes)

    # Card 2: Count Accuracy
    ax_s2 = fig.add_subplot(gs[0, 1])
    ax_s2.set_facecolor('#111827')
    ax_s2.axis('off')
    b2 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.03",
                                linewidth=1.2, edgecolor='#ef4444', facecolor='#111827', transform=ax_s2.transAxes)
    ax_s2.add_patch(b2)
    draw_badge(ax_s2, 0.06, 0.70, 0.48, 0.20, "EXACT COUNT ACCURACY", "#450a0a", "#ef4444", "#fca5a5", fontsize=7.5)
    ax_s2.text(0.06, 0.58, "0.0%", fontsize=22, weight='bold', color='#ef4444', va='top', transform=ax_s2.transAxes)
    ax_s2.text(0.06, 0.22, "Basic RAG suffers 0.0% count accuracy; context window hides dataset volume.", 
               fontsize=8, color='#fca5a5', va='top', transform=ax_s2.transAxes)

    # Card 3: Citations
    ax_s3 = fig.add_subplot(gs[0, 2])
    ax_s3.set_facecolor('#111827')
    ax_s3.axis('off')
    b3 = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.03",
                                linewidth=1, edgecolor='#f59e0b', facecolor='#111827', transform=ax_s3.transAxes)
    ax_s3.add_patch(b3)
    draw_badge(ax_s3, 0.06, 0.70, 0.48, 0.20, "PLAIN LLM CITATION RATE", "#451a03", "#f59e0b", "#fde68a", fontsize=7.5)
    ax_s3.text(0.06, 0.58, "0.0%", fontsize=22, weight='bold', color='#f59e0b', va='top', transform=ax_s3.transAxes)
    ax_s3.text(0.06, 0.22, "Zero-shot LLMs cannot cite real CMPLID or CAMPNO regulatory keys.", 
               fontsize=8, color='#cbd5e1', va='top', transform=ax_s3.transAxes)

    # -------------------------------------------------------------------------
    # Bottom Left: High-Contrast Bar Chart
    # -------------------------------------------------------------------------
    ax_chart = fig.add_subplot(gs[1, :2])
    ax_chart.set_facecolor('#111827')
    for spine in ax_chart.spines.values():
        spine.set_color('#374151')

    cats = ['Text Symptoms (15Q)', 'Structured SQL (15Q)', 'Mixed / Hybrid (15Q)', 'Overall Average (45Q)']
    plain_vals = [60.0, 15.0, 35.0, 36.7]
    rag_vals = [85.0, 10.0, 50.0, 48.3]

    x = np.arange(len(cats))
    width = 0.32

    # Draw bars with modern styling
    r1 = ax_chart.bar(x - width/2, plain_vals, width, label='Plain LLM (Zero-Shot Weights)', color='#f87171', edgecolor='#ef4444', linewidth=1)
    r2 = ax_chart.bar(x + width/2, rag_vals, width, label='Basic RAG (ChromaDB Top-5)', color='#38bdf8', edgecolor='#0284c7', linewidth=1)

    ax_chart.set_ylabel('Factual Accuracy Score (%)', color='#f8fafc', fontsize=10, weight='bold')
    ax_chart.set_title('ACCURACY ACROSS 45-QUESTION BENCHMARK CATEGORIES', color='#38bdf8', fontsize=11, weight='bold', pad=12)
    ax_chart.set_xticks(x)
    ax_chart.set_xticklabels(cats, color='#e2e8f0', fontsize=9.5)
    ax_chart.set_ylim(0, 105)
    ax_chart.grid(axis='y', color='#1f2937', linestyle='--', linewidth=0.8)
    ax_chart.tick_params(axis='y', colors='#94a3b8')
    ax_chart.legend(facecolor='#0b0f19', edgecolor='#374151', labelcolor='#e2e8f0', loc='upper right', fontsize=9)

    for rect in r1:
        h = rect.get_height()
        ax_chart.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                          xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                          color='#fca5a5', fontsize=9, weight='bold')
    for rect in r2:
        h = rect.get_height()
        ax_chart.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                          xytext=(0, 3), textcoords="offset points", ha='center', va='bottom',
                          color='#7dd3fc', fontsize=9, weight='bold')

    # -------------------------------------------------------------------------
    # Bottom Right: Benchmark & Solution Roadmap
    # -------------------------------------------------------------------------
    ax_right = fig.add_subplot(gs[1, 2])
    ax_right.set_facecolor('#111827')
    ax_right.axis('off')
    
    card_r = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.015,rounding_size=0.025",
                                    linewidth=1.2, edgecolor='#10b981', facecolor='#111827', transform=ax_right.transAxes)
    ax_right.add_patch(card_r)

    draw_badge(ax_right, 0.05, 0.88, 0.65, 0.08, "BENCHMARK BREAKDOWN & SPRINT 3 GOAL", 
               "#064e3b", "#10b981", "#6ee7b7", fontsize=8)

    info_text = (
        "45-Question Benchmark Structure:\n"
        "• 15 Text Queries: Qualitative symptom descriptions\n"
        "• 15 SQL Queries: Aggregations, counts, annual trends\n"
        "• 15 Mixed Queries: Symptoms mapped to recalls\n"
        "• 18 Motorcycle Queries (40%): Gated evaluation\n\n"
        "Sprint 3 Target: The Agentic Router:\n"
        "• Intent Router: SQL tool for counts + Vector tool\n"
        "• Success Metric: +10 pp accuracy over Basic RAG\n"
        "• Citation Validator: Enforces valid CMPLID & CAMPNO\n"
        "• Streamlit UI: Interactive safety engineering demo"
    )
    ax_right.text(0.06, 0.78, info_text, fontsize=8.6, color='#cbd5e1', linespacing=1.35, va='top', transform=ax_right.transAxes)

    out_path = os.path.join(ASSETS_DIR, 'linkedin_post_2_graphic.png')
    plt.savefig(out_path, dpi=220, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Created creative Graphic 2 at: {out_path}")
    return out_path

if __name__ == "__main__":
    p1 = create_creative_post_1()
    p2 = create_creative_post_2()
    
    # Overwrite on Desktop
    shutil.copy2(p1, os.path.join(DESKTOP_DIR, 'LinkedIn_Post_1_Graphic.png'))
    shutil.copy2(p2, os.path.join(DESKTOP_DIR, 'LinkedIn_Post_2_Graphic.png'))
    
    # Overwrite in Artifact directory
    shutil.copy2(p1, os.path.join(ARTIFACT_DIR, 'LinkedIn_Post_1_Graphic.png'))
    shutil.copy2(p2, os.path.join(ARTIFACT_DIR, 'LinkedIn_Post_2_Graphic.png'))
    print("Successfully generated and synchronized new creative graphics!")
