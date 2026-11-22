# Raw AI Conversation Transcript — Sprint 1
**Project:** AutoRecall Copilot  
**Participant:** Mohammed Zain (38001477)  
**Supervisor:** Prof. Dr. Humera Noor Minhas  
**Module:** MSc Data Science Capstone (Winter 2026/2027)  
**Date Window:** 3 November – 9 November 2026  

---

### Turn 1: Ingestion Architecture & Data Source Strategy

**Mohammed Zain:**  
I'm starting my MSc Capstone project on vehicle defect detection using official NHTSA Office of Defects Investigation (ODI) data. My goal is to build an evaluated assistant that vehicle quality engineers can use to query complaints and recalls. I've downloaded the raw flat files `FLAT_CMPL.txt` and `FLAT_RCL.txt` from nhtsa.gov covering 2015 to 2025. 

Before I write code, I want to discuss how to structure the ingestion. The complaints file has over 650k rows for this decade and each row has over 40 fields, with the primary narrative in `CDESCR`. Should I dump this straight into a vector database, or should I maintain a hybrid store? Also, Dr. Humera emphasizes that this cannot just be a basic demo; it must have a rigorous comparative evaluation. How should the storage layer be architected to support both qualitative symptom retrieval and quantitative aggregations?

**AI Assistant:**  
Dumping all 650k raw complaints directly into a vector database is a major architectural mistake for vehicle defect analysis. Here is why:

1. **Analytical Queries Fail in Vector Stores:** If an engineer asks, *"How many complaints did Harley-Davidson receive for clutch slipping on 2017–2020 Touring models?"*, semantic vector search will only retrieve the top-$k$ nearest neighbors (e.g., 5 or 10 chunks). The LLM will then either hallucinate an aggregate count from that small sample or confess it cannot count.
2. **High Metadata Overhead:** Complaints contain structured metadata (Make, Model, Model Year, Component Code, Date Received, Crash Indicator, Injury Count) that requires exact relational filtering.

**Recommended Hybrid Architecture:**
- **Relational / Analytical Engine (DuckDB):** Ingest the clean pipe-delimited data directly into DuckDB. DuckDB runs embedded, handles 650k rows in memory or disk with columnar compression, and executes SQL aggregations in sub-50 milliseconds.
- **Vector Search Engine (ChromaDB):** Extract the complaint narrative `CDESCR` alongside foreign keys (`CMPLID`, `MAKE`, `MODEL`, `YEAR`), generate dense embeddings with a lightweight model (e.g., `all-MiniLM-L6-v2`), and index them for qualitative similarity search.
- **Agent Router:** The agent receives the user prompt, determines if the question requires quantitative metrics (SQL tool), qualitative symptom descriptions (semantic search tool), or both, and synthesizes the answer with explicit record ID citations.

---

### Turn 2: Solving the Motorcycle vs. Car Separation Heuristic

**Mohammed Zain:**  
I looked into the raw `FLAT_CMPL.txt` schema. There is no clean `VEHICLE_TYPE` binary flag. In `MAKETXT`, passenger cars and motorcycles overlap. For example, `BMW` produces both passenger SUVs (X5, 3 Series) and motorcycles (R1200GS, S1000RR). `HONDA` produces Civics and Accords, but also Goldwings and CBR600s. 

My proposal specifically commits to evaluating motorcycle defects because powersports represent a smaller market where defect signals get drowned out by car volume. How can I reliably segment motorcycles from passenger vehicles without manually checking thousands of rows?

**AI Assistant:**  
This is a classic data-cleaning challenge in NHTSA ODI data. Here is an effective two-tier classification pipeline:

1. **Dedicated Motorcycle OEMs:** First, create an explicit OEM list that *only* manufactures motorcycles/powersports:
   - `HARLEY-DAVIDSON`, `HARLEY DAVIDSON`, `DUCATI`, `KTM`, `TRIUMPH`, `INDIAN MOTORCYCLE`, `HUSQVARNA`, `APRILIA`, `MOTO GUZZI`, `ROYAL ENFIELD`. Any record matching these makes is automatically tagged `vehicle_category = 'motorcycle'`.
2. **Dual-Category OEMs (BMW, Honda, Suzuki, Yamaha, Kawasaki):**
   - For `BMW`: Look for `BMW MOTORRAD` in `MAKETXT`, or if `MAKETXT == 'BMW'`, match `MODELTXT` against motorcycle series prefixes (`R\s?\d+`, `K\s?\d+`, `F\s?\d+`, `S1000`, `G310`, `C400`, `R18`).
   - For `HONDA`: Match `MODELTXT` against motorcycle keywords (`CBR`, `CRF`, `GOLDWING`, `REBEL`, `SHADOW`, `AFRICA TWIN`, `VFR`, `CB\d+`, `VT\d+`).
   - For `SUZUKI`: Match against (`GSX`, `V-STROM`, `HAYABUSA`, `BOULEVARD`, `BURGMAN`, `SV650`, `DR-Z`).
   - For `YAMAHA` and `KAWASAKI`: Almost all entries in ODI under these brands are powersports (motorcycles, ATVs, watercraft), but you can verify against passenger vehicle lists.
3. **Validation Check:** Run a frequency distribution of top models in the filtered motorcycle subset to ensure no passenger cars (e.g., Honda Accord, BMW 328i) leaked in. Document this exact heuristic in Section 4 of your progress report.

---

### Turn 3: 45-Question Benchmark Design & Evaluation Rubric

**Mohammed Zain:**  
Dr. Humera approved my proposal with 45 test questions. I need to make sure the evaluation is scientifically sound and reproducible. In Objective O2, I planned:
- 15 text-search questions
- 15 structured quantitative questions
- 15 hybrid questions
At least 15 of the 45 must be about motorcycles.

How should I design the ground-truth answers and the grading rubric so that my evaluation isn't subjective?

**AI Assistant:**  
To make the 45-question benchmark objective and reproducible:

1. **Benchmark Schema:**
   Every question in `test_benchmark.json` should have:
   - `question_id`: `Q01` to `Q45`
   - `query`: The natural language string
   - `category`: `semantic_text`, `structured_sql`, or `hybrid`
   - `vehicle_type`: `car` or `motorcycle`
   - `ground_truth_answer`: The exact factual response
   - `target_record_ids`: List of specific `CMPLID`s or `CAMPNO`s that must be cited
   - `expected_sql`: (For SQL/hybrid queries) The deterministic SQL statement to compute the answer

2. **Objective Scoring Rubric:**
   - **Answer Correctness (Categorical: 1.0, 0.5, 0.0):**
     - `1.0 (Correct)`: Factual claims match ground truth; quantitative figures within $\pm 2\%$ tolerance.
     - `0.5 (Partially Correct)`: Correct component identified, but numerical counts missing or partially incomplete.
     - `0.0 (Incorrect)`: Hallucinated failure modes, incorrect counts, or failure to retrieve relevant context.
   - **Faithfulness (Metric: 0.0 to 1.0):**
     - Defined as: $\frac{\text{Number of claims directly supported by cited record IDs}}{\text{Total factual claims in response}}$.
   - **Retrieval Hit Rate @ 5 (For RAG systems):**
     - Binary (1 or 0): Did the top-5 retrieved chunks contain at least one ground-truth `CMPLID`?

3. **Sample Verification:** Manually audit a 20% stratified sample of the LLM responses to verify automated grading consistency.

---

### Turn 4: Sprint 1 Retrospective & Reporting Deadlines

**Mohammed Zain:**  
I spent a lot of time this week getting the raw NHTSA files parsed, debugging regex patterns for motorcycle makes, and drafting the test questions. Because I wanted to have the database loaded before writing the progress report, I missed the 9 November deadline. Dr. Humera emphasized communication and sticking to sprint dates, and I noticed in the class sheet she deducts marks for missing reports. 

How should I address this in Progress Report 1 honestly without sounding defensive?

**AI Assistant:**  
Address the delay with complete professional transparency and accountability:

1. **No Excuses:** State directly in Section 5 (*Delays and what I learned*) that Progress Report 1 is submitted late, noting the planned date (9 Nov) and the actual catch-up submission date.
2. **Identify the Real Engineering Cause:** Explain that you made two classic project management estimation errors:
   - Underestimating the time required for data wrangling (pipe-delimited parsing, unstandardized make/model taxonomy, timestamp nullification).
   - Letting Sprint 1 scope creep into early database implementation rather than pausing to submit a concise status report on time.
3. **Concrete Mitigation:** State that as a result of this lesson, you are instituting a weekly planned vs. actual time audit, and emphasize that because you began Sprint 2 technical tasks early during this window, Sprint 2 deliverables and Progress Report 2 will be submitted punctually on Monday, 23 November 2026.

This demonstrates maturity, self-awareness, and professional ownership—the exact mindset Dr. Humera looks for in graduate capstone students.

