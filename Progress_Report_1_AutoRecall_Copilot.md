# Progress Report 1: AutoRecall Copilot
**An Evaluated Agentic RAG System for Early Detection of Car and Motorcycle Defects**

Mohammed Zain (Matriculation No. 38001477) | Supervisor: Prof. Dr. Humera Noor Minhas  
Program: MSc Data Science, University of Europe for Applied Sciences | Reporting Period: Sprint 1, 3 to 9 November 2026

---

## 1. Summary

In Sprint 1, I focused on getting the project environment ready, writing the formal proposal, and downloading the official NHTSA complaints and recalls datasets. My proposal and university application form were approved by Dr. Humera Noor Minhas. I downloaded the official raw data files directly from NHTSA servers (not Kaggle) and built the initial ingestion script to load them into an embedded DuckDB database. I ran into real data issues with unstandardized vehicle types and corrupted date fields, which took longer than I planned and caused me to miss the 9 November reporting deadline. To catch back up, I started the Sprint 2 database setup and baseline checks early. 

**Overall status:** Minor issues with the timeline, but on track technically.

---

## 2. The Project in Brief

When vehicle parts start failing, owners describe their problems in free-text complaints, while manufacturers and regulators track investigations and recalls in structured tables. For quality teams and safety engineers, reading through tens of thousands of complaints to spot early failure trends is slow and tedious work. AutoRecall Copilot is an AI assistant that lets an engineer ask questions in plain English (like *"Which braking components show rising failure complaints on 2018–2022 BMW motorcycles?"*) and gets answers grounded in both structured SQL queries and text search, citing the exact NHTSA Complaint ID or Recall Campaign Number.

Because this is a data science capstone and not a research thesis, my focus is on building and evaluating three practical setups on the exact same 45 questions:
1. **Plain LLM:** Answering from memory with no outside data.
2. **Basic RAG:** Retrieving the 5 most similar complaint narratives using dense embeddings.
3. **Agentic RAG:** An agent with an SQL tool for counts and a vector search tool for symptom text.

The 45 questions cover 15 text search questions, 15 count/trend questions, and 15 mixed questions, with at least 15 focused specifically on motorcycles.

---

## 3. Status Against the Project Plan

| Planned in Sprint 1 | Status | Details |
| :--- | :---: | :--- |
| **Repository and local environment** | **Done** | Created the local repository and linked it to GitHub (`MZain56/Autorecall-Copilot`). Added a project `README.md`, pinned dependencies in `requirements.txt`, and set up `.gitignore` to keep large raw files local. |
| **Download official NHTSA files** | **Done** | Downloaded official raw archives (`FLAT_CMPL.zip` at 359.8 MB and `FLAT_RCL_POST_2010.zip` at 14.4 MB) directly from NHTSA's server. Verified column layouts against official `CMPL.txt` and `RCL.txt` dictionaries. |
| **Filter cars vs. motorcycles & check counts** | **Done** | Wrote `src/pipeline/ingest_nhtsa.py` to separate motorcycles (5,591 complaints, 2,805 recalls) from passenger cars (1,001,045 complaints, 206,603 recalls) for the 2015–2025 observation window. |
| **Write and submit proposal** | **Done** | Submitted the 7-page capstone proposal and UE form with business questions, system diagram, objectives, and Gantt chart. Approved by supervisor. |
| **Draft first 15 test questions** | **Done** | Drafted the first 15 domain questions (7 cars, 8 motorcycles) covering real failure patterns (like stator burnouts, ABS pressure loss, and sticking throttle bodies) with verified ground-truth record IDs. |
| **Progress report 1 & LinkedIn post** | **Done late** | Submitted late on 22 Nov 2026. Includes this honest status report, the real DuckDB database, the LinkedIn post on RAG limitations, and the raw AI conversation log. |

---

## 4. Data Work and Findings (What I Found in the NHTSA Data)

- **Data downloaded:** I downloaded the official flat files directly from `static.nhtsa.gov`. The full NHTSA complaints file holds 2,269,292 records dating back to 1995. For my project window (2015 to 2025), there are **1,006,636 complaints** and **209,408 recall campaign entries**. I loaded these directly into a local DuckDB database (`autorecall.duckdb`) for fast querying.
- **The car vs. motorcycle numbers:**
  - *Complaints:* Passenger cars make up 1,001,045 complaints (99.44%), while motorcycles make up only 5,591 complaints (0.56%).
  - *Recalls:* Passenger cars make up 206,603 recall records (98.66%), while motorcycles account for 2,805 recall records (1.34%).
  - *Why this matters:* Motorcycles have a recall share that is **2.5 times higher** than their complaint share. Also, 5.7% of motorcycle complaints involved an actual crash (320 crashes), which is much higher than minor car defects. Because there are 1 million car complaints, any general search or clustering completely buries motorcycle defect signals. That is why having a dedicated filter for motorcycles is necessary.
- **Top motorcycle brands in the data:** Harley-Davidson leads with 1,630 complaints, followed by Suzuki (1,087), BMW Motorrad (782), Yamaha (488), Ducati (313), KTM (285), Triumph (276), Honda Powersports (252), and Kawasaki (247).
- **Three data quality problems I ran into and fixed:**
  1. *Shared brand names:* NHTSA doesn't have a clean 'motorcycle' checkbox. 'BMW' makes both X5 SUVs and R1200GS adventure bikes; 'Honda' makes Civics and CBR sportbikes. I wrote regex rules matching motorcycle model series (like R-series, CBR, GSX, Ninja) to tag them accurately.
  2. *Missing VINs:* 45,411 complaints (4.5%) had empty VIN fields because consumers filing online often don't have their VIN handy. I made sure my tables rely on NHTSA's unique sequence number (`CMPLID`) instead of VIN.
  3. *Corrupted dates:* Several thousand records had bad date entries like `99999999` or `00000000` in the failure date field. I nullified those and used the official receipt date (`DATEA`) formatted as `YYYY-MM-DD`.

---

## 5. Delays and What I Learned

Progress Report 1 was due on Monday, 9 November 2026, and I am submitting it late. The honest reason is poor time estimation: I spent much longer than expected downloading the 1.5 GB file, fixing the tab-delimited formatting, and writing regex rules to separate motorcycle models from cars. Instead of pausing to submit a brief status report on the due date, I kept working to get the database populated first. That was a mistake.

**What I learned:** As Dr. Humera emphasized in class, deadlines in professional life are about communication, not waiting for perfection. Sending a short, punctual report explaining what is delayed is much better than going silent to finish extra work. To make sure this doesn't happen again, I am tracking my actual hours against my estimates each week. Because I already started Sprint 2 tasks during this window, Progress Report 2 will be submitted on time on Monday, 23 November.

---

## 6. Early Start on Sprint 2: A First Baseline Test

While catching up on reporting, I started Sprint 2 technical tasks early to stay on schedule:
- **DuckDB tables:** Ingested the cleaned complaints and recalls into `autorecall.duckdb`, indexed by complaint ID, recall campaign number, make, model, year, and component code.
- **Testing basic RAG vs. SQL:** I ran a quick test to see if semantic search alone could handle counting questions.
  - *Question:* *"How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?"*
  - *Basic RAG Behavior:* Pulled 5 relevant complaint chunks describing soft brake pedals, but it guessed an answer (*"around 10 to 12 complaints"*).
  - *DuckDB SQL Query:* Returned the exact count: **43 complaints**.
  
  *Takeaway:* This simple test confirms the main idea of my project: pure RAG cannot do math or counts, so giving the agent an SQL tool is necessary.

---

## 7. Next Steps (Sprint 2: 10 to 23 November)

- **Vector store:** Chunk the complaint descriptions (`CDESCR`) and build the ChromaDB index using `all-MiniLM-L6-v2`.
- **Baseline pipelines:** Write the test runner for the Plain LLM baseline and the Basic RAG baseline.
- **Finish the 45 test questions:** Complete the full question benchmark with reference answers and record IDs (15 text, 15 SQL, 15 mixed).
- **Submission:** Publish LinkedIn post 2 and submit Progress Report 2 on Monday, 23 November 2026.

---

## 8. Five Organisations That Need This Use Case

| Organisation | Why it matters to them | Reference / Link |
| :--- | :--- | :--- |
| **BMW Group (BMW Motorrad & Quality, Munich)** | Builds both cars and high-end adventure bikes. Needs unified defect monitoring to catch low-volume motorcycle safety flaws before warranty claims turn into recalls. | BMW Group Product Safety & Recalls |
| **KTM AG / Pierer Mobility (Mattighofen, Austria)** | Specialist motorcycle maker where component defects (like clutch cylinders or camshaft wear) show up in small numbers but create serious rider crash risks. | KTM Customer Care & Safety Recalls |
| **Robert Bosch GmbH (Chassis Systems, Stuttgart)** | Major safety supplier for motorcycle ABS, stability control (MSC), and radar sensors. Needs independent defect tracking to know whether field failures are component issues or OEM assembly issues. | Bosch Mobility — Two-Wheeler Safety |
| **NHTSA ODI (Washington D.C.)** | The federal regulator that sifts through 60,000+ citizen complaints every year to decide when to open defect investigations and push for safety recalls. | NHTSA ODI Investigation Process |
| **Continental AG (Safety & Motion, Hanover)** | Supplies motorcycle brake actuators and electronic rider aids. Needs automated complaint monitoring to spot early field glitches across different brands. | Continental Automotive Safety |

---

## 9. Three LinkedIn Thought Leaders I Want to Model

| Person | LinkedIn Profile | What I like about their writing style |
| :--- | :--- | :--- |
| **Eugene Yan** | `linkedin.com/in/eugeneyan` | Writes clear, practical engineering retrospectives on search, RAG, and evaluation. Always explains real trade-offs and failure cases without hype. |
| **Chip Huyen** | `linkedin.com/in/chiphuyen` | Breaks complex ML system architectures down into clear, structured decisions. Always connects technical choices to practical business reliability. |
| **Hamel Husain** | `linkedin.com/in/hamelhusain` | Focuses heavily on rigorous evaluation, error analysis, and domain-specific benchmarks instead of generic LLM leaderboards. Explains evaluation in plain language. |
