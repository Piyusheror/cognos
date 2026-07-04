# CognOS — Institutional Memory Operating System

> *Clone any mind. Query forever.*

## What is CognOS?

CognOS is an AI engine that preserves how a person thinks — not just what they wrote, but how they connected ideas, made decisions, and weighed tradeoffs. Feed it any person's data. Ask it anything. Get answers the way that person would have answered, with a confidence score.

**Built for the WeMakeDevs × Cognee Hackathon 2026 — Best Use of Open Source track.**

---

## The Problem

Every time a key person leaves an organization, their knowledge walks out with them. A founder retires. A CEO passes away. A senior engineer moves on. The reasoning behind years of decisions — gone.

Current tools like Notion and Confluence store documents. They cannot store *how someone thinks*.

**The cost is real:**
- Average cost to replace one employee: **$45,236**
- Replacing a senior leader costs up to **200% of their annual salary**
- US businesses lose **$1 trillion per year** from knowledge attrition

---

## The Solution

CognOS ingests any person's data — speeches, emails, interviews, documents — and builds a living knowledge graph using Cognee. When someone asks a question, even one never explicitly answered, the engine traverses the graph and responds the way that person would have.

**What makes CognOS different:**

1. **Knowledge graph, not document search** — stores relationships between ideas, not just text
2. **Decay engine** — every fact is scored by age, corroboration, and relevance. Old, unreferenced knowledge gets low confidence. Principles repeated across years get high confidence. No other tool does this.
3. **Person-agnostic** — works with any person's data. Ratan Tata today. Your CEO tomorrow.

---

## Demo

We demonstrate CognOS using Ratan Tata's public speeches, interviews, and documented decisions.

**Demo question:** *"What would be your concerns about expanding into a new Asian market?"*

**CognOS answers:** Based on Ratan Tata's reasoning across 10 documents spanning 2007-2015, drawing on his Southeast Asia decision, his ethics philosophy, and his approach to worker welfare — with a confidence score and source attribution.

---

## Architecture
**Four components:**
- `ingest.py` — accepts any folder of .txt files, feeds into Cognee
- `decay_engine.py` — scores every answer by age, corroboration, and keyword relevance
- `main.py` — FastAPI backend with /ingest, /ask, /forget endpoints
- `ui.py` — Streamlit chat interface

---

## Tech Stack

| Tool | Purpose | Cost |
|------|---------|------|
| Cognee (open source) | Knowledge graph + memory engine | Free |
| Groq (Llama 3.3 70B) | LLM inference | Free |
| FastAPI | Backend API | Free |
| Streamlit | Frontend UI | Free |
| fastembed | Embeddings | Free |

---

## Setup

```bash
git clone https://github.com/Piyusheror/cognos.git
cd cognos
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install "cognee[fastembed]"
copy .env.example .env
# Add your Groq API key to .env
```

**Run:**
```bash
# Terminal 1 — start the backend
uvicorn main:app --reload --port 8000

# Terminal 2 — ingest data
python ingest.py --folder data

# Terminal 3 — start the UI
streamlit run ui.py
```

---

## The Decay Engine

The decay engine is CognOS's secret weapon. Every answer from Cognee is scored using three signals:

| Signal | Weight | What it measures |
|--------|--------|-----------------|
| Age decay | 35% | How recent is the source? Newer = higher confidence |
| Corroboration | 35% | How many sources agree? More = higher confidence |
| Keyword relevance | 30% | Do the answer's key terms match the question? |

Final score maps to: **HIGH** (≥0.7) · **MEDIUM** (≥0.4) · **LOW** (<0.4)

---

## Team

Built at the WeMakeDevs × Cognee Hackathon, July 2026.

- Decay engine & ML architecture
- Query API & backend
- Data ingestion pipeline  
- Frontend UI