# AutoRecall Copilot
> **An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects**

[![MSc Capstone](https://img.shields.io/badge/Course-MSc%20Data%20Science%20Capstone-blue.svg)](https://www.ue-germany.com/)
[![Supervisor](https://img.shields.io/badge/Supervisor-Dr.%20Humera%20Noor%20Minhas-orange.svg)](#)
[![Data Source](https://img.shields.io/badge/Data%20Source-NHTSA%20ODI%20Official-green.svg)](https://www.nhtsa.gov/nhtsa-datasets-and-apis)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 📌 Executive Summary

**AutoRecall Copilot** is an applied AI system designed for vehicle quality engineers, product safety investigators, and automotive component suppliers. The platform enables natural language interrogation across **over 650,000 official consumer defect complaints** and **12,000+ safety recall campaigns** maintained by the US National Highway Traffic Safety Administration (NHTSA) Office of Defects Investigation (ODI).

Unlike generic RAG assistants that rely solely on semantic similarity—which reliably fails on aggregate statistical questions like *"how many complaints were filed for ABS hydraulic fade?"*—AutoRecall Copilot implements an **evaluated agentic routing framework** pairing dense vector search with columnar SQL execution over DuckDB, enforcing verifiable source citations (`CMPLID` and `CAMPNO`) for every factual assertion.

A primary technical focus of the system is the **passenger car vs. motorcycle disparity**: while powersports represent under 5% of consumer complaints, their safety severity and recall proportion are more than double, requiring specialized domain gating to prevent critical two-wheeler safety anomalies from being drowned out by passenger car volumes.

---

## 🎯 Benchmark & Evaluation Design

The core scientific contribution is a rigorous three-way empirical comparison across three architectural paradigms evaluated on a benchmark of **45 curated domain test questions** (15 semantic text queries, 15 structured quantitative SQL queries, and 15 hybrid multi-step queries, with at least 15 specifically targeting motorcycle dynamics):

1. **Plain LLM Baseline:** Zero-shot parametric knowledge (no external retrieval).
2. **Basic RAG Baseline:** Dense semantic search over top-5 complaint narrative chunks via `all-MiniLM-L6-v2` in ChromaDB.
3. **Agentic RAG (AutoRecall Copilot):** Dynamic tool routing between DuckDB SQL execution and ChromaDB semantic retrieval with multi-step reasoning and citation enforcement.

**Key Evaluation Metrics:**
- **Answer Correctness:** Graded on an objective categorical scale (Correct / Partially Correct / Incorrect).
- **Faithfulness:** Ratio of claims in generated answers supported directly by cited record IDs.
- **Retrieval Hit Rate @ 5:** Precision of retrieved context against ground-truth safety campaigns.

---

## 🏗️ System Architecture

```
                                 ┌─────────────────────────┐
                                 │   Official NHTSA Data   │
                                 │ (Complaints & Recalls)  │
                                 └────────────┬────────────┘
                                              │ Ingestion & Cleaning
                                              ▼
                                 ┌─────────────────────────┐
                                 │  ETL & Filtering Logic  │
                                 │   (Cars vs Motorcycles) │
                                 └──────┬───────────┬──────┘
                                        │           │
                     Structured Tables  │           │  Unstructured Narratives
                                        ▼           ▼
                           ┌─────────────────┐ ┌─────────────────┐
                           │  DuckDB Engine  │ │ ChromaDB Index  │
                           │(SQL Aggregates) │ │ (Dense Vectors) │
                           └────────┬────────┘ └────────┬────────┘
                                    │                   │
                                    └─────────┬─────────┘
                                              │ Tool Execution
                                              ▼
                                 ┌─────────────────────────┐
                                 │   Agentic Router (LLM)  │
                                 │  Decides: SQL, Vector,  │
                                 │         or Hybrid       │
                                 └────────────┬────────────┘
                                              │ Grounded Response + Citations
                                              ▼
                                 ┌─────────────────────────┐
                                 │ Streamlit Decision App  │
                                 └─────────────────────────┘
```

---

## 📁 Repository Structure

```
.
├── data/
│   ├── raw/                 # Official NHTSA raw zip files (git-ignored)
│   ├── schema/              # NHTSA layout dictionaries (CMPL.txt, RCL.txt)
│   └── processed/           # DuckDB database and parquet stores
├── src/
│   ├── pipeline/            # Ingestion, parsing, and classification pipeline
│   ├── retrieval/           # ChromaDB dense embeddings and indexing
│   ├── agent/               # Tool routing, SQL executor, and citation synthesis
│   └── app/                 # Streamlit interactive dashboard
├── eval/
│   ├── benchmark_45q.json   # 45 curated evaluation questions with ground truth
│   └── evaluate_models.py   # Automated 3-way evaluation harness
├── reports/                 # Academic deliverables and sprint progress reports
│   ├── Progress_Report_1_AutoRecall_Copilot.pdf
│   ├── Progress_Report_1_AutoRecall_Copilot.docx
│   └── LinkedIn_Post_Sprint_1.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Sprint 2 Baseline Evaluation Results

Evaluated across the **45-Question Safety Defect Benchmark** (`eval/benchmark_45q.json`):

| Evaluation Metric | Plain LLM Baseline | Basic RAG Baseline (Top-5) | DuckDB SQL Ground Truth |
| :--- | :---: | :---: | :---: |
| **Overall Factual Accuracy** | 36.7% | 48.3% | 100.0% (structured) |
| **Text Question Accuracy** | 60.0% | **85.0%** | N/A (unstructured) |
| **Structured SQL Accuracy** | 15.0% | **10.0%** | **100.0%** |
| **Mixed Question Accuracy** | 35.0% | **50.0%** | N/A (hybrid required) |
| **Exact Count Accuracy** | **0.0%** | **0.0%** | **100.0%** |
| **Retrieval Hit Rate @ 5** | N/A | **75.6%** (86.7% text) | N/A |
| **Citation Rate (Valid IDs)** | **0.0%** | **66.7%** | **100.0%** |

*Core Insight:* Basic RAG suffers from catastrophic counting blindness (0.0% exact count accuracy) because it only observes the top-5 retrieved chunks in its context window. AutoRecall Copilot addresses this in Sprint 3 via an Agentic Router with DuckDB SQL execution.

---

## 🚀 Quickstart & Reproduction

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/<your-username>/autorecall-copilot.git
cd autorecall-copilot

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Official NHTSA Data
```bash
python src/pipeline/download_nhtsa.py
```

### 3. Ingest into DuckDB & Run Pipeline
```bash
python src/pipeline/ingest_nhtsa.py
```

### 4. Run Baseline & Agentic Evaluation
```bash
python eval/evaluate_models.py
```

---

## 👨‍💻 Author & Academic Context

* **Student:** Mohammed Zain (Matriculation No. 38001477)
* **Program:** MSc Data Science (Semester 3 Capstone, Winter 2026/2027)
* **Institution:** University of Europe for Applied Sciences (UE), Germany
* **Academic Supervisor:** Prof. Dr. Humera Noor Minhas

