# CognOS — Query API (Backend)

The brain's output. Receives a question, recalls from Cognee memory, attaches a confidence score, and returns the answer with sources.

## Endpoints

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/health` | Check the server is alive |
| POST | `/ingest` | Store text into memory (`cognee.remember`) |
| POST | `/ask` | Ask a question (`cognee.recall`) — the main one |
| POST | `/forget` | Delete a dataset (`cognee.forget`) |

### POST /ask

Request:
```json
{ "question": "Why did the founder avoid Southeast Asia in 2019?" }
```

Response:
```json
{
  "answer": "...",
  "confidence": "high",
  "confidence_score": 0.82,
  "sources": ["board_meeting_2019.txt"],
  "latency_ms": 1240
}
```

## Setup (Windows)

```bat
cd cognos-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
:: now open .env and paste your real Groq key
```

Note: if `pip install cognee` fails on Python 3.13, install Python 3.12 and recreate the venv with `py -3.12 -m venv venv`. Cognee is newest-Python-sensitive.

## Run

```bat
uvicorn main:app --reload --port 8000
```

Then open http://localhost:8000/docs — FastAPI gives you a free interactive playground where you can test every endpoint from the browser (great for the demo).

## Test end-to-end

In a second terminal (with venv activated):

```bat
python test_api.py
```

This stores two facts, then asks a question and prints the answer + confidence.

## How the decay engine plugs in (for Person 2)

`confidence.py` tries to `import decay_engine`. If your teammate creates a file `decay_engine.py` with this function, the API automatically uses it:

```python
def get_decay_score(question: str, answer: str, sources: list) -> float:
    """Return a confidence score between 0.0 and 1.0"""
```

Until then, a built-in heuristic (result count, answer length, keyword overlap, source presence) keeps the API fully working — so integration day is a file drop, not a rewrite.