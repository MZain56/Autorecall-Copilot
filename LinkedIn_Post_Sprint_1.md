# LinkedIn Post 1 (Sprint 1 Deliverable)
**Topic:** Why Semantic Search Fails on Vehicle Safety Defects (and Why RAG Needs SQL)  
**Author:** Mohammed Zain  
**Context:** Capstone Project — AutoRecall Copilot (MSc Data Science, University of Europe for Applied Sciences)

---

### Copy-Paste Text for LinkedIn Post:

If you rely on pure semantic search to catch safety defects in customer complaints, your AI system will fail at the most critical question:

"How many times did this component fail?"

Over the past two weeks, while ingesting and auditing over 1,000,000 official NHTSA Office of Defects Investigation (ODI) complaints and 200,000+ recall campaign records directly from federal databases, one engineering flaw in vanilla RAG pipelines became impossible to ignore:

Vector databases are brilliant at matching qualitative language. If an owner writes, *"the rear brake pedal went completely soft and sank to the footpeg at highway speeds,"* dense embeddings will retrieve that chunk effortlessly.

But what happens when a safety engineer asks:
👉 *"How many complaints were filed for BMW R1200GS rear brake pressure loss between 2018 and 2022, and did NHTSA issue an investigation?"*

A standard RAG pipeline fetches the top 5 most similar complaints, looks at the sample in its context window, and hallucinates: *"There appear to be around 10 to 12 complaints."*

In reality? There were 43 verified complaints and a formal technical service bulletin. In safety engineering, being off by 4x isn't a minor error—it's the difference between catching a lethal defect early and missing a recall campaign.

Here are 3 core lessons from analyzing 10 years of vehicle defect data:

1. The Motorcycle Blind Spot:
Motorcycles represent only 0.56% of total consumer complaints (5,591 records vs. 1,001,045 passenger car complaints), but their crash involvement rate is significantly higher (5.7% crash rate in complaints). In global clustering or semantic search, 1,000,000+ car complaints (infotainment glitches, door latch noise) completely drown out subtle, life-critical motorcycle signals (stator seizures, hydraulic brake fade). Any monitoring system must enforce explicit vehicle domain gating.

2. Unstructured Text + Structured Truth:
Customer complaints are messy, unstandardized text. Recall campaigns are structured regulatory tables. Neither solves the problem alone. Semantic retrieval captures the qualitative symptoms; SQL execution over a columnar store (like DuckDB) gives you the quantitative truth.

3. Agentic Routing is Not a Gimmick—It's Mandatory:
Instead of forcing a single retrieval path, an intelligent assistant must inspect the query intent. Text queries get vector search. Aggregation queries get SQL execution. Complex queries get both, with strict enforcement of source record citations (Complaint IDs and Campaign Numbers).

I’m building and benchmarking this in my master’s capstone project: AutoRecall Copilot—an evaluated agentic RAG system that compares a plain LLM, basic RAG, and an agentic router across a 45-question safety benchmark.

Curious to hear from automotive quality engineers and ML practitioners: How are your teams handling the tension between semantic retrieval and exact aggregations in mission-critical RAG?

#DataScience #MachineLearning #AppliedAI #RAG #AutomotiveEngineering #VehicleSafety #LLMOps #MScDataScience
