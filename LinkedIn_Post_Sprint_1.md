# LinkedIn Post 1 (Sprint 1 Deliverable)
**Topic:** Why Semantic Search Fails on Vehicle Safety Defects (and Why RAG Needs SQL)  
**Author:** Mohammed Zain  
**Context:** Capstone Project — AutoRecall Copilot (MSc Data Science, University of Europe for Applied Sciences)

---

### Copy-Paste Text for LinkedIn Post:

If you rely on pure semantic search to catch vehicle safety defects in customer complaints, your AI system will fail at the most critical question:

"How many times did this component fail?"

While ingesting over 1,000,000 official NHTSA complaints and 200,000+ recall campaign records directly from federal databases, one major engineering flaw in vanilla RAG became impossible to ignore:

Vector databases are brilliant at matching qualitative language. If a rider writes that "the rear brake pedal went completely soft at highway speeds," dense embeddings retrieve that chunk effortlessly.

But what happens when an engineer asks:
👉 "How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022?"

A standard RAG pipeline fetches the top 5 nearest chunks, looks at the sample in its context window, and hallucinates: "There appear to be around 10 to 12 complaints."

In reality? There were 43 verified complaints and a formal service bulletin. In safety engineering, being off by 4x isn't a small error—it's the difference between catching a lethal defect early and missing a recall campaign.

Here are 3 core lessons from analyzing 10 years of vehicle defect data:

1. The Motorcycle Blind Spot:
Motorcycles represent only 0.56% of complaints (5,591 records vs. 1,001,045 car complaints), but their crash involvement rate is 5.72% (320 crashes). Without domain gating, 1M+ car complaints completely submerge subtle, life-critical motorcycle signals (stator seizures, hydraulic brake fade).

2. Unstructured Text + Structured Truth:
Complaints are messy text. Recalls are structured regulatory tables. Semantic retrieval captures qualitative symptoms; columnar SQL execution (DuckDB) delivers exact quantitative metrics.

3. Agentic Routing is Mandatory:
Instead of forcing a single retrieval path, an intelligent assistant must inspect query intent:
• Text queries -> Vector search
• Aggregation queries -> SQL execution
• Complex queries -> Hybrid execution with mandatory source citations (CMPLID / CAMPNO)

I'm building and benchmarking this in my master's capstone: AutoRecall Copilot—an evaluated agentic RAG system tested across a 45-question safety benchmark.

Automotive engineers and ML practitioners: How are your teams handling the tension between semantic search and exact aggregations in RAG?

#DataScience #MachineLearning #AppliedAI #RAG #AutomotiveEngineering #VehicleSafety #LLMOps #MScDataScience #DuckDB
