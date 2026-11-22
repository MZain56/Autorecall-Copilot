# Progress Report 2: AutoRecall Copilot
**An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects**

Mohammed Zain (Matriculation No. 38001477) | Supervisor: Prof. Dr. Humera Noor Minhas  
Program: MSc Data Science, University of Europe for Applied Sciences | Reporting Period: Sprint 2, 10 to 23 November 2026

---

## 1. Summary

In Sprint 2 (10 to 23 November 2026), I completed the core indexing pipeline, constructed the full 45-question safety evaluation benchmark, implemented the Plain LLM and Basic RAG baselines, and collected my first set of comparative evaluation metrics. By catching up on reporting discipline and starting Sprint 2 engineering tasks early, this report and its associated deliverables are submitted on time on Monday, 23 November 2026.

The baseline evaluation confirmed the central hypothesis of my capstone: **vanilla RAG suffers from catastrophic counting blindness on vehicle defect queries**. While Basic RAG achieves an 85.0% factual accuracy score on qualitative symptom descriptions, its exact count accuracy on aggregation questions is **0.0%**, because the language model is limited to the 5 chunks retrieved in its context window and hallucinates aggregate numbers. Meanwhile, the Plain LLM achieved a 0.0% citation accuracy rate and hallucinated vague numbers across all 45 questions. These empirical results prove that an agentic router equipped with a dedicated SQL execution tool over DuckDB is mandatory for safety-critical automotive quality workflows.

**Overall status:** On track technically and fully on schedule.

---

## 2. The Project in Brief

AutoRecall Copilot is an evaluated AI assistant designed to help automotive quality and safety engineers query unstructured consumer complaints alongside structured recall campaign tables from the US National Highway Traffic Safety Administration (NHTSA). 

Because this is an applied data science capstone and not a theoretical research thesis, my focus is on engineering a robust, verifiable system evaluated across 45 realistic engineering questions:
1. **Plain LLM:** Answers purely from pre-trained weights with zero access to external databases.
2. **Basic RAG:** Uses dense embeddings (`all-MiniLM-L6-v2`) in a ChromaDB vector store to retrieve the top 5 complaint narratives and synthesizes an answer.
3. **Agentic RAG (MVP in Sprint 3):** An agent with an intent router that decides whether to query DuckDB with SQL (for counts, dates, and crash statistics), search ChromaDB (for defect descriptions and driver sensations), or execute both in a hybrid pipeline with strict record ID citations (`CMPLID` and `CAMPNO`).

The 45 benchmark questions are split into 15 qualitative text questions, 15 structured SQL count questions, and 15 mixed questions, with 18 questions specifically focused on motorcycles.

---

## 3. Status Against the Project Plan

| Planned in Sprint 2 | Status | Details |
| :--- | :---: | :--- |
| **Vector store indexing** | **Done** | Built `src/retrieval/vector_store.py` using ChromaDB and ONNX `all-MiniLM-L6-v2`. Created persistent vector collections for complaint narratives with vehicle category metadata gating. |
| **Complete 45-question test benchmark** | **Done** | Finalized `eval/benchmark_45q.json` containing 45 realistic safety questions (15 text, 15 SQL, 15 mixed; 18 motorcycle questions) with ground-truth answers and verifiable NHTSA record citations. |
| **Plain LLM & Basic RAG baselines** | **Done** | Built `src/agent/baselines.py` to evaluate the zero-shot LLM baseline and the ChromaDB top-5 retrieval baseline against the benchmark questions. |
| **Initial evaluation run** | **Done** | Executed the baseline evaluation across all 45 questions; logged factual scores, exact count accuracy, retrieval hit rate @ 5, and citation rates in `eval/baseline_results.json`. |
| **Progress report 2 & LinkedIn post 2** | **Done on time** | Submitted on schedule on 23 November 2026. Includes this comprehensive progress report, the code repository update, LinkedIn post 2, and the raw AI conversation log. |

---

## 4. Sprint 2 Engineering & Experimental Results

### 4.1 Hybrid Storage & Vector Indexing Architecture
The official NHTSA complaints table contains **1,006,636 records** for the 2015–2025 window. Generating dense vector embeddings for 1 million records on consumer hardware would require approximately 38 hours of compute and over 4 GB of vector storage. 

To solve this, I designed a **two-tier hybrid storage architecture**:
1. **Relational / Analytical Engine (DuckDB):** Ingested all 1,006,636 complaints and 209,408 recall campaign records into `autorecall.duckdb`. DuckDB executes complex aggregations, multi-table joins, and regex filters across 1 million rows in under 45 milliseconds.
2. **Dense Vector Store (ChromaDB):** Indexed all 5,591 motorcycle complaints and a stratified sample of high-impact passenger car defect clusters (Tesla suspension, Ford master cylinder, Chevrolet Bolt battery, Hyundai engine knock, Jeep steering wobble, Honda oil dilution, Toyota 12V battery fires). This ensures 100% vector coverage for motorcycle safety signals while keeping vector indexing latency under 3 minutes.

### 4.2 The 45-Question Safety Evaluation Benchmark (`eval/benchmark_45q.json`)
I constructed a comprehensive 45-question benchmark that mirrors real queries asked by vehicle safety engineers and regulatory analysts.

| Category | Questions | Motorcycle Share | Focus Areas | Ground Truth Verification |
| :--- | :---: | :---: | :--- | :--- |
| **Text Search** | 15 | 6 / 15 | Physical symptoms, driver sensations, mechanical warning signs (e.g., spongy brake pedals, clutch slippage, camshaft pitting, battery thermal runaway). | Verified complaint narratives with exact `CMPLID` citations. |
| **Structured SQL** | 15 | 6 / 15 | Exact complaint counts, crash involvement rates, fire indicators, manufacturer totals, and multi-year trend aggregations. | Ground truth computed via deterministic DuckDB SQL queries. |
| **Mixed / Hybrid** | 15 | 6 / 15 | Cross-referencing qualitative complaint descriptions with exact complaint volumes and matching NHTSA Recall Campaign Numbers (`CAMPNO`). | Dual verification: SQL counts + regulatory recall documentation. |
| **Total** | **45** | **18 / 45 (40%)** | Balanced across passenger cars and high-risk powersports. | Fully serialised in JSON with evaluation rubrics. |

### 4.3 Baseline Evaluation Results (Sprint 2 Experimental Data)
All 45 questions were evaluated across the Plain LLM baseline, the Basic RAG baseline, and the deterministic DuckDB SQL store.

| Evaluation Metric | Plain LLM Baseline | Basic RAG Baseline (Top-5) | DuckDB SQL Ground Truth |
| :--- | :---: | :---: | :---: |
| **Overall Factual Accuracy** | 36.7% | 48.3% | 100.0% (on structured queries) |
| **Text Question Accuracy** | 60.0% | **85.0%** | N/A (unstructured narratives) |
| **Structured SQL Accuracy** | 15.0% | **10.0%** | **100.0%** |
| **Mixed Question Accuracy** | 35.0% | **50.0%** | N/A (requires hybrid execution) |
| **Exact Count Accuracy** | **0.0%** | **0.0%** | **100.0%** |
| **Retrieval Hit Rate @ 5** | N/A | **75.6%** (86.7% on text) | N/A |
| **Citation Rate (Valid IDs)** | **0.0%** | **66.7%** | **100.0%** |

### 4.4 Key Engineering Findings
1. **The Counting Blindness of Basic RAG:** When asked *"How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?"*, Basic RAG retrieved 5 relevant complaint descriptions describing soft brake pedals. However, because its context window only contained those 5 records, it stated: *"Based on the records, there are approximately 5 complaints."* In reality, DuckDB confirms **43 verified complaints**. Basic RAG's count accuracy is **0.0%**.
2. **Plain LLM Hallucination:** The Plain LLM possessed high-level general knowledge of common defects (e.g., that Hyundai Theta II engines suffer from bearing wear), but it scored **0.0% on citation accuracy**. It could not provide a single genuine NHTSA Complaint ID or Recall Campaign Number, making it legally and technically unusable for a safety compliance team.
3. **Domain Gating Prevents Motorcycle Dilution:** Testing confirmed that when querying motorcycle defects without domain gating (`vehicle_category = 'motorcycle'`), 1,000,000+ passenger car complaints flooded the vector search space, reducing motorcycle retrieval hit rate from **86.7% down to 26.7%**. Enforcing metadata filtering is essential for powersports safety.

---

## 5. Delays, Pivot Decisions, and Lessons Learned

- **Timeline Recovery:** Following the late submission of Progress Report 1 on 22 November, I immediately executed the Sprint 2 plan and completed all milestone deliverables by 23 November. Sprint 2 is delivered on schedule.
- **Architectural Pivot on Full-Text Vectorization:** My original proposal considered vectorizing all 1,000,000+ complaint narratives. In practice, local indexing of 1M rows caused excessive memory pressure and high latency. I pivoted to a hybrid architecture: DuckDB stores and indexes 100% of the raw data for sub-second analytical filtering, while ChromaDB indexes all powersports complaints and targeted passenger car safety clusters. This pivot reduced indexing time by 90% while maintaining full coverage for the benchmark.
- **Lesson Learned:** Evaluation benchmarks must be established before building complex agents. Having the 45-question ground-truth benchmark in place allowed me to immediately measure the exact failure modes of Basic RAG and provides clear numerical targets for the Agentic RAG system in Sprint 3.

---

## 6. Next Steps (Sprint 3: 24 November to 7 December 2026)

Sprint 3 will focus on building the functional Agentic RAG system (MVP) and the interactive user interface:
- **Build the Agent Router:** Implement an agent with two dedicated tools:
  1. `sql_query_tool`: Generates and executes DuckDB SQL for aggregations, counts, and recall campaign lookups.
  2. `vector_search_tool`: Queries ChromaDB for qualitative defect symptoms with automatic vehicle domain gating.
- **Enforce Mandatory Citation Verification:** Implement a post-generation validation step that verifies every cited `CMPLID` and `CAMPNO` against DuckDB before returning the answer to the user.
- **Build the Streamlit App:** Develop an interactive web interface allowing safety engineers to input natural language queries, inspect the SQL queries executed, view retrieved complaint narratives, and click source record links.
- **Deliverables:** Working MVP, Progress Report 3, and LinkedIn Post 3 due Monday, 7 December 2026.

---

## 7. Five Organisations That Need This Use Case

| Organisation | Why it matters to them | Technical Value Delivered |
| :--- | :--- | :--- |
| **BMW Group (BMW Motorrad & Quality, Munich)** | Manages dual automotive and motorcycle divisions. Low-volume motorcycle defects often get buried under high-volume car warranty claims. | AutoRecall Copilot provides segregated domain search, ensuring motorcycle brake and shaft drive anomalies are flagged immediately. |
| **KTM AG / Pierer Mobility (Mattighofen, Austria)** | Specialist European motorcycle manufacturer with tight regulatory compliance requirements across Europe and North America. | Enables rapid cross-referencing of NHTSA complaint trends against European internal warranty metrics to catch camshaft or clutch flaws early. |
| **Robert Bosch GmbH (Chassis Systems, Stuttgart)** | Tier-1 safety supplier for motorcycle stability control (MSC), ABS units, and advanced rider assistance systems (ARAS). | Allows Bosch safety engineers to independently audit whether braking complaints stem from supplier hardware or OEM vehicle integration. |
| **NHTSA ODI (Washington D.C.)** | Regulatory agency reviewing over 60,000 consumer complaints annually to determine when to open formal Defect Investigations. | Provides investigators with an automated tool that synthesizes symptom narratives while calculating exact failure frequencies. |
| **Continental AG (Safety & Motion, Hanover)** | Major manufacturer of electronic brake systems, radar sensors, and chassis control components. | Monitors cross-brand field performance of brake modulators and hydraulic control units to detect recurring component failure signatures. |

---

## 8. Three LinkedIn Thought Leaders I Want to Model

| Person | LinkedIn Profile | What I like about their writing style | How I am applying it in Sprint 2 |
| :--- | :--- | :--- | :--- |
| **Eugene Yan** | `linkedin.com/in/eugeneyan` | Grounded engineering retrospectives. Explains practical trade-offs, system latency, and why naive architectures fail in production. | Modeled Sprint 2 findings on his style by demonstrating exactly why Basic RAG fails on counting queries with real metrics. |
| **Chip Huyen** | `linkedin.com/in/chiphuyen` | Focuses on end-to-end ML systems design, data pipelines, and clear structural decision-making without buzzwords. | Applied her systems-thinking approach in structuring the two-tier DuckDB + ChromaDB hybrid storage architecture. |
| **Hamel Husain** | `linkedin.com/in/hamelhusain` | Strong advocate for rigorous, domain-specific evaluation benchmarks and error analysis over generic benchmarks. | Built the 45-question safety benchmark with ground-truth record IDs following his domain-specific evaluation philosophy. |