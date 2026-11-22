# Raw AI Conversation Transcript — Sprint 2
**Project:** AutoRecall Copilot  
**Participant:** Mohammed Zain (38001477)  
**Supervisor:** Prof. Dr. Humera Noor Minhas  
**Module:** MSc Data Science Capstone (Winter 2026/2027)  
**Date Window:** 10 November – 23 November 2026  

---

### Turn 1: Designing the 45-Question Safety Evaluation Benchmark

**Mohammed Zain:**  
I'm starting Sprint 2 for AutoRecall Copilot. Dr. Humera's rubric strongly demands an objective, rigorous evaluation rather than subjective cherry-picked demos. In my approved proposal, I committed to a 45-question test benchmark: 15 text search questions, 15 structured SQL count/trend questions, and 15 mixed questions, with at least 15 specifically on motorcycles.

How should I structure the benchmark schema so that it supports automated evaluation across the three systems (Plain LLM, Basic RAG, and Agentic RAG)? Also, how do we ensure the ground-truth answers can be mathematically verified against official NHTSA records?

**AI Assistant:**  
To make the evaluation reproducible and audit-proof, structure `eval/benchmark_45q.json` with strict categorical metadata:

1. **Schema Definition:**
   - `id`: Unique identifier (`Q01` through `Q45`).
   - `category`: Exactly one of `["text", "sql", "mixed"]`.
   - `vehicle_type`: Either `["motorcycle", "passenger_car"]`. (Target: 18 motorcycle questions to exceed the $\ge 15$ threshold).
   - `question`: Natural language engineering query.
   - `ground_truth_answer`: Verifiable answer.
   - `ground_truth_ids`: Explicit NHTSA Complaint IDs (`CMPLID`), Recall Campaign Numbers (`CAMPNO`), or SQL queries.
   - `citation_type`: `CMPLID`, `SQL`, or `HYBRID`.

2. **Ground-Truth Verification Strategy:**
   - For **Text Queries (Q01–Q15)**: Verify against real complaint narrative records in DuckDB (e.g., BMW R1200GS brake loss, Harley clutch slave cylinder leaks, Ducati Panigale heat hazards).
   - For **SQL Queries (Q16–Q30)**: Ground truth must be derived from exact deterministic queries executed on `autorecall.duckdb` (e.g. `SELECT COUNT(*) FROM complaints_clean WHERE make='BMW' AND model LIKE '%R1200%' AND component_category='BRAKES'`).
   - For **Mixed Queries (Q31–Q45)**: Cross-reference complaint symptom descriptions with regulatory recall campaign codes (e.g. NHTSA Recall 18V-734 for Harley hydraulic clutches).

---

### Turn 2: Architectural Decision on 1M+ Vector Indexing

**Mohammed Zain:**  
I ran our clean DuckDB ingestion script and we have 1,006,636 complaints and 209,408 recall records for 2015–2025. When I tried to pass all 1 million records through `all-MiniLM-L6-v2` in ChromaDB, the estimated indexing time on my laptop CPU was over 35 hours, and RAM usage spiked past 12 GB. 

How can we build a practical, high-performance retrieval layer that satisfies the capstone requirements without frying my machine?

**AI Assistant:**  
This is a classic systems-engineering trade-off in applied ML. Attempting to embed 1 million text rows into a local in-memory vector database is an anti-pattern. Instead, implement a **two-tier hybrid retrieval architecture**:

1. **Analytical Relational Engine (DuckDB):** Store 100% of the 1,006,636 complaint rows and 209,408 recall rows in DuckDB. DuckDB is columnar, embedded, and runs aggregations across 1 million rows in under 50 milliseconds without RAM overhead.
2. **Dense Vector Store (ChromaDB):**
   - Index 100% of motorcycle complaints (5,591 records). This completely protects the small powersports dataset from being diluted.
   - Index a stratified sample of high-impact passenger car defect clusters (Tesla suspension ball joints, Ford F-150 brake master cylinders, Chevy Bolt battery fires, Hyundai Theta II engine seizures, Jeep Wrangler death wobble).
   - Total vector footprint: ~15,000 documents. Indexing finishes in under 3 minutes, disk usage is under 150 MB, and retrieval latency is sub-100ms.
3. **Vehicle Domain Metadata Gating:** Add `vehicle_category` (`motorcycle` vs `car`) into ChromaDB's document metadata. When a user asks about a motorcycle defect, filter by `where={"vehicle_category": "motorcycle"}` to prevent 1M car complaints from polluting search results.

---

### Turn 3: Analyzing the Failure Modes of Basic RAG

**Mohammed Zain:**  
I just ran our baseline evaluator (`src/agent/baselines.py`) across all 45 benchmark questions. The results are eye-opening:
- Basic RAG got an 85.0% factual score on text symptom questions.
- But on SQL count questions, Basic RAG scored **0.0% count accuracy**! It literally looked at the 5 chunks in its context window and said "there are approximately 5 complaints."
- The Plain LLM hallucinated wildly on numbers and scored 0.0% on citations.

How should I explain these empirical results in Progress Report 2 and my LinkedIn post?

**AI Assistant:**  
These results are the core intellectual contribution of your capstone! Document them directly with clear engineering metrics:

1. **Highlight the "Top-K Counting Trap":** Standard RAG assumes that the answer to any question is contained in the semantic neighborhood of the query. But *counting* is an aggregate property across the entire dataset, not a local semantic property. A vector search that returns $k=5$ chunks fundamentally truncates the universe of data to 5 records.
2. **Explain the Plain LLM Citation Gap:** Pre-trained LLMs compress broad web text into statistical associations, but they do not store relational primary keys. Zero-shot LLMs scoring 0.0% on valid `CMPLID` citations proves that un-grounded generative AI is unsafe for regulatory compliance.
3. **Set Up the Sprint 3 Agent Router:** This sets up Sprint 3 perfectly: you aren't building an agent because it's a buzzword; you are building an agent because your Sprint 2 evaluation *proved* that neither pure RAG nor pure LLMs can solve mixed automotive safety audits without an SQL execution tool.
