# LinkedIn Post 2 (Sprint 2 Deliverable)
**Topic:** Why Basic RAG Fails on Automotive Safety Audits: First Results from a 45-Question Benchmark  
**Author:** Mohammed Zain  
**Context:** Capstone Project — AutoRecall Copilot (MSc Data Science, University of Europe for Applied Sciences)  
**Date:** 23 November 2026  

---

### Copy-Paste Text for LinkedIn Post:

If you are building RAG for mission-critical quality engineering, here is a hard truth from our first evaluation run:

Vanilla RAG achieved **85.0% factual accuracy** when describing defect symptoms, but scored exactly **0.0% accuracy** on count and aggregation questions.

Over the past two weeks, as part of Sprint 2 of my master’s capstone at the University of Europe for Applied Sciences, I built a 45-question safety defect benchmark evaluated against official NHTSA complaints and recalls data. I tested two baselines:
1. A Plain LLM (answering zero-shot from pre-trained weights)
2. Basic RAG (retrieving the top 5 complaint narratives using dense embeddings in ChromaDB)

Here is what the experimental data revealed:

🚨 1. The "Top-K Counting Trap"
When asked: *"How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?"*
- Basic RAG retrieved 5 highly relevant complaints detailing soft rear brake pedals.
- But because its context window only held those 5 chunks, the LLM answered: *"Based on the records in context, there appear to be 5 complaints."*
- In reality? Our DuckDB relational store confirms **43 verified complaints**.
If a safety engineer relies on vanilla RAG, they will undercount safety defect volume by almost 90%.

🚨 2. Zero-Shot LLMs Cannot Be Audited
The Plain LLM showed reasonable generic knowledge of famous recalls (like Chevrolet Bolt battery fires or Hyundai Theta II engine failures), but achieved a **0.0% citation rate**. It could not verify a single genuine NHTSA Complaint ID (`CMPLID`) or Recall Campaign Number (`CAMPNO`). In regulatory compliance and product safety, an unverified assertion is legally worthless.

🚨 3. The 1M+ Record Dilution Problem
When querying motorcycle safety anomalies without vehicle domain gating, the 1,000,000+ car complaints in the vector space diluted the retrieval hit rate from **86.7% down to 26.7%**. Low-volume two-wheeler defects (like clutch hydraulic seal failures or shaft drive fractures) require strict metadata segregation.

💡 The Solution: Two-Tier Hybrid Architecture
Rather than forcing all data into vectors, we built a hybrid stack:
- **DuckDB** handles 100% of the 1,006,636 complaints for deterministic, sub-50ms SQL aggregations and exact counts.
- **ChromaDB** indexes semantic complaint narratives for symptom search and driver sensations.

In Sprint 3, I am connecting these two engines through an Agent Router that automatically chooses between SQL execution, vector retrieval, or a hybrid multi-step query.

Automotive engineers and ML practitioners: How are your teams handling quantitative questions in your RAG pipelines? Are you using Text-to-SQL agents or hybrid architectures?

#DataScience #MachineLearning #AppliedAI #RAG #AutomotiveEngineering #VehicleSafety #LLMOps #MScDataScience #DuckDB #ChromaDB
