# Progress Report 1: AutoRecall Copilot
**An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects**

- **Student:** Mohammed Zain (Matriculation No. 38001477)
- **Supervisor:** Prof. Dr. Humera Noor Minhas
- **Program:** Master of Science in Data Science, University of Europe for Applied Sciences (UE)
- **Reporting Period:** Sprint 1, 3 to 9 November 2026 (*Catch-Up Submission: 22 November 2026*)
- **Project Repository:** `autorecall-copilot` (Local & Version Controlled)

---

## 1. Summary

Sprint 1 focused on formal project initiation, environment configuration, official NHTSA data acquisition, exploratory schema analysis, database ingestion, and drafting the initial benchmark test battery. The comprehensive Capstone Proposal and University of Europe application form were completed and formally approved by Dr. Humera Noor Minhas. Official National Highway Traffic Safety Administration (NHTSA) Office of Defects Investigation (ODI) complaints and recall datasets spanning 2015 to 2025 were downloaded directly from official federal servers (no Kaggle, no synthetic data), verified against official layout dictionaries, and ingested into a local DuckDB analytical database (`autorecall.duckdb`).

Due to unexpected data cleaning hurdles in parsing unstructured vehicle taxonomies and historical timestamps, this progress report was delayed beyond the 9 November deadline. However, Sprint 2 technical tasks (DuckDB schema design and preliminary baseline tests) were commenced early to ensure the overall project trajectory reaches scheduled alignment. 

**Overall status:** Minor issues (behind on sprint paperwork, on track technically).

---

## 2. The Project in Brief

AutoRecall Copilot is an evaluated intelligent assistant designed to help automotive quality engineers, safety analysts, and parts suppliers detect emerging vehicle defects before catastrophic failures occur. Early defect signals lie buried within high-volume, unstructured consumer complaint narratives, while recall campaigns and regulatory investigations reside in structured tables. The system allows users to pose plain-language questions (e.g., *"Which braking sub-components exhibit recurring failure symptoms on 2018–2022 BMW adventure motorcycles?"*) and answers them by dynamically querying structured recall records with SQL and performing dense semantic search over complaint text, enforcing exact supporting record citations (ODI Complaint IDs and NHTSA Campaign Numbers) for every factual claim.

The core scientific deliverable is a rigorous three-way comparative evaluation across three architectural paradigms:
1. **Plain LLM:** Zero-shot parametric memory without retrieval.
2. **Basic RAG:** Dense vector retrieval of top-5 complaint narrative chunks via sentence embeddings.
3. **Agentic RAG:** An autonomous routing agent equipped with SQL execution over DuckDB and vector search over ChromaDB.

All three systems are evaluated against a benchmark of 45 curated domain test questions across three query categories: 15 semantic text queries, 15 quantitative aggregations, and 15 hybrid multi-step queries (with at least 15 specifically targeting motorcycles).

---

## 3. Status Update Against the Project Plan

| Planned in Sprint 1 | Status | Details |
| :--- | :---: | :--- |
| **Repository, CI & Local Environment** | **Done** | Git repository initialized (`main` branch) with clean `.gitignore`, `requirements.txt`, and directory layout: `/data`, `/src/pipeline`, `/src/retrieval`, `/src/agent`, `/eval`, and `/app`. Pinned dependencies: `pandas`, `duckdb`, `chromadb`, `sentence-transformers`, `streamlit`. |
| **Download NHTSA Complaint & Recall Files** | **Done** | Acquired official ODI flat archives (`FLAT_CMPL.zip`, 359.8 MB and `FLAT_RCL_POST_2010.zip`, 14.4 MB) directly from official NHTSA servers. Verified schemas against official `CMPL.txt` and `RCL.txt` layout dictionaries. |
| **Filter Cars and Motorcycles & Count Records** | **Done** | Engineered regex and OEM lookup heuristics in `src/pipeline/ingest_nhtsa.py` to separate powersports/motorcycles (5,591 complaints, 2,805 recalls) from passenger vehicles (1,001,045 complaints, 206,603 recalls) for the 2015–2025 window. |
| **Draft Proposal and Application Form** | **Done** | Drafted 7-page technical proposal covering business questions, system architecture, measurable objectives O1–O6, Gantt chart, and risk mitigation. Submitted and approved by supervisor Dr. Humera Noor Minhas. |
| **Draft First 15 Test Questions** | **Done** | Formulated initial 15 test queries (7 car, 8 motorcycle) with verified ground-truth answers and exact NHTSA citation keys covering safety-critical failure modes (stators, ABS hydraulic fade, throttle body sticking). |
| **Progress Report 1 & LinkedIn Post 1** | **Done late** | Report 1 submitted late on 22 Nov 2026. Catch-up submission pairs this detailed status report with Sprint 1 technical LinkedIn post, real DuckDB database, and raw AI transcript. |

---

## 4. Data Work and Findings (Live NHTSA Data Ingestion)

- **Official Source Verification & Volume:** Ingested official NHTSA ODI flat files directly from `static.nhtsa.gov`. The all-time ODI complaints archive contains 2,269,292 records, of which **1,006,636 complaints** fall within our 2015–2025 observation window. The post-2010 recall database contains 248,586 campaign line-items, of which **209,408 recall records** correspond to the 2015–2025 window. All data was loaded directly into a high-performance local DuckDB instance (`autorecall.duckdb`).
- **Passenger Car vs. Motorcycle Disparity:**
  - *Complaints Breakdown:* Passenger cars account for 1,001,045 complaints (99.44%), while motorcycles account for 5,591 complaints (0.56%).
  - *Recalls Breakdown:* Passenger cars account for 206,603 recall records (98.66%), while motorcycles account for 2,805 recall records (1.34%).
  - *Disparity Ratio & Safety Finding:* Motorcycle representation in recalls (1.34%) is nearly **2.5 times higher** than in complaints (0.56%). Furthermore, motorcycle complaints exhibit a higher crash rate (5.7% involved in crashes, with 320 recorded incidents) compared to minor passenger car grievances. Because motorcycle complaints are submerged by over 1 million automotive complaints, standard global clustering algorithms wash out critical two-wheeler safety anomalies. Domain-specific isolation is mandatory.
- **Top Motorcycle OEMs Identified:**
  - *Harley-Davidson:* 1,630 complaints
  - *Suzuki:* 1,087 complaints
  - *BMW Motorrad:* 782 complaints
  - *Yamaha:* 488 complaints
  - *Ducati:* 313 complaints
  - *KTM:* 285 complaints
  - *Triumph:* 276 complaints
  - *Honda Powersports:* 252 complaints
  - *Kawasaki:* 247 complaints
  - *Husqvarna:* 130 complaints
- **Data Quality Anomalies Identified & Remediated:**
  1. *Unstandardized Vehicle Category Flags:* NHTSA raw files do not maintain a clean binary vehicle type indicator. 'BMW' manufactures both passenger SUVs and motorcycles (R1200GS, S1000RR), while Honda manufactures both Civics and CBR sportbikes. *Solution:* Implemented a two-stage parsing pipeline combining make-level normalization with model regex matching to reliably classify powersports.
  2. *Missing Identifiers:* 45,411 complaints (4.5%) lacked VINs (optional in consumer submissions). *Solution:* Primary record key relies strictly on `CMPLID` (unique NHTSA sequence number).
  3. *Date Corruption:* Identified invalid historical integers (e.g., `99999999` or `00000000` in `FAILDATE`). *Solution:* Nullified corrupted failure dates and anchored temporal filtering to the official receipt date (`DATEA`), parsed strictly into ISO-8601 (`YYYY-MM-DD`).

---

## 5. Delays and What I Learned

Progress Report 1 was scheduled for submission on Monday, 9 November 2026. Submitting this report late on 22 November represents a critical deviation from project milestones. The delay stemmed from two interrelated execution bottlenecks:
1. Underestimating the engineering complexity of downloading, uncompressing (1.5 GB), and harmonizing the raw NHTSA pipe-delimited files, specifically resolving the motorcycle classification heuristics across mixed OEM lines.
2. Allowing the scope of Sprint 1 to inflate into early database construction before formally closing the reporting milestone.

**Key Professional Lesson:** As emphasized in Dr. Humera's lectures, professional project management requires respecting communication deadlines above all else. A concise, punctual report communicating in-flight technical challenges is far superior to delaying a deliverable to bundle "complete" results. To enforce accountability moving forward, I have instituted a strict weekly time-budget audit comparing planned vs. actual task durations. Sprint 2 tasks were initiated during this window, ensuring that Progress Report 2 will be submitted punctually on Monday, 23 November 2026.

---

## 6. Early Start on Sprint 2: Preliminary Architecture & First Check

To recover schedule velocity, foundational components of Sprint 2 were commenced during the last ten days:
- **DuckDB Relational Store:** Cleaned complaint and recall records were loaded into an embedded DuckDB database (`autorecall.duckdb`) with structured tables (`complaints_clean` and `recalls_clean`), indexed by `cmplid`, `campno`, `make`, `model`, `model_year`, and `component_code`.
- **Empirical Baseline Check (Semantic Search vs. SQL Tooling):** Conducted a preliminary diagnostic test comparing pure vector retrieval against SQL execution on quantitative queries:
  - *Query:* *"How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?"*
  - *Basic RAG Behavior:* Retrieved 5 highly descriptive individual complaint chunks detailing brake pedal travel, but hallucinated an aggregate answer (*"around 12 complaints"*) based on its retrieved sample.
  - *SQL Tool Execution:* The DuckDB SQL query returned the exact ground-truth count of **43 complaints**.
  
  *Takeaway:* This concrete finding validates the core premise of AutoRecall Copilot: semantic RAG alone cannot answer analytical aggregation queries; an autonomous agent capable of SQL tool dispatch is essential.

---

## 7. Next Steps (Sprint 2: 10 to 23 November)

- **Vector Store Deployment:** Chunk complaint narratives (`CDESCR`) and generate dense embeddings using `sentence-transformers/all-MiniLM-L6-v2` stored in an embedded ChromaDB index.
- **Baseline Pipeline Implementation:** Build automated execution pipelines for:
  1. Plain LLM baseline (zero-shot prompt)
  2. Basic RAG (Chroma top-5 retrieval + prompt synthesis)
- **Finalize 45-Question Test Battery:** Complete all 45 curated evaluation questions with ground truth answers, category tags (15 text, 15 SQL, 15 hybrid), and verified record ID lists.
- **Reporting & LinkedIn:** Publish LinkedIn Post 2 and submit Progress Report 2 on Monday, 23 November 2026.

---

## 8. Five Organisations That Need This Use Case

| Organisation | Why it matters to them | Reference / Link |
| :--- | :--- | :--- |
| **BMW Group (BMW Motorrad & Quality Management, Munich)** | Manages both premium passenger vehicles and high-performance adventure motorcycles. Needs unified cross-segment defect tracking to catch low-volume motorcycle safety flaws before warranty claims escalate. | BMW Group Product Safety & Recall Governance |
| **KTM AG / Pierer Mobility (Mattighofen, Austria)** | Specialized motorcycle manufacturer where emerging component defects (e.g., hydraulic clutch slave cylinders, camshaft wear) manifest in low absolute numbers but present severe rider safety risks. | KTM Customer Care & Safety Recalls |
| **Robert Bosch GmbH (Mobility Solutions / Chassis Systems, Stuttgart)** | Tier-1 safety supplier providing motorcycle stability control (MSC), ABS units, and radar sensor suites across multiple OEMs. Needs independent defect monitoring to distinguish OEM integration errors from component hardware flaws. | Bosch Mobility — Two-Wheeler & Powersports Safety |
| **NHTSA Office of Defects Investigation (ODI, Washington D.C.)** | The federal regulatory body responsible for identifying safety-related defect trends from over 60,000 annual citizen complaints to initiate Preliminary Evaluations (PE) and Recall Campaigns. | NHTSA ODI Investigation Process (49 CFR Part 554) |
| **Continental AG (Automotive Safety & Motion, Hanover)** | Global supplier of electronic brake systems and Advanced Rider Assistance Systems (ARAS). Requires automated complaint surveillance to detect anomalous actuator behavior in field data. | Continental Automotive Safety Technologies |

---

## 9. Three LinkedIn Thought Leaders We Want to Model

| Person | LinkedIn Profile | Writing Style & Strategic Modeling |
| :--- | :--- | :--- |
| **Eugene Yan** | `linkedin.com/in/eugeneyan` | Writes deeply technical, systems-oriented retrospectives on production LLM patterns, semantic search, and evaluation. Focuses on pragmatic trade-offs, reproducible benchmarking, and real-world failure modes rather than hype. |
| **Chip Huyen** | `linkedin.com/in/chiphuyen` | Author of *'Designing Machine Learning Systems'*. Explains applied AI architecture with crisp system trade-offs (latency, accuracy, data governance). Connects engineering implementation directly to business reliability. |
| **Hamel Husain** | `linkedin.com/in/hamelhusain` | Applied AI & evaluation consultant. Advocates passionately for rigorous, domain-specific evaluation benchmarks, error analysis, and building focused test suites rather than relying on generic LLM benchmarks. |
