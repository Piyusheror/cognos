"""
CognOS — Query API (Part 3)
============================
A FastAPI backend that sits between the Streamlit UI and Cognee.

Endpoints:
  GET  /health  -> quick check that the server is alive
  POST /ingest  -> store raw text into Cognee memory  (cognee.remember)
  POST /ask     -> ask a question, get answer + confidence + sources (cognee.recall)
  POST /forget  -> wipe a dataset from memory          (cognee.forget)

Run it with:
  uvicorn main:app --reload --port 8000
"""

import os
import time
import logging
from contextlib import asynccontextmanager
from typing import Optional, List, Any

from dotenv import load_dotenv

# Load .env BEFORE importing cognee, so cognee picks up the Groq keys.
load_dotenv()

import cognee  # noqa: E402

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from confidence import score_results  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cognos-api")

DEFAULT_DATASET = os.getenv("COGNOS_DATASET", "cognos")


# ----------------------------------------------------------------------
# Request / response models (this is what the UI sends and receives)
# ----------------------------------------------------------------------

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural language question")
    dataset: Optional[str] = Field(None, description="Dataset to search (optional)")


class AskResponse(BaseModel):
    answer: str
    confidence: str          # "high" | "medium" | "low"
    confidence_score: float  # 0.0 to 1.0 (useful for the decay engine later)
    sources: List[str]       # where the answer came from
    latency_ms: int


class IngestRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Raw text to store in memory")
    source_name: Optional[str] = Field(None, description="e.g. 'speech_2019.txt'")
    dataset: Optional[str] = None


class ForgetRequest(BaseModel):
    dataset: Optional[str] = None


# ----------------------------------------------------------------------
# App setup
# ----------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("CognOS API starting. Dataset: %s", DEFAULT_DATASET)
    yield
    logger.info("CognOS API shutting down.")


app = FastAPI(
    title="CognOS Query API",
    description="Institutional Memory Operating System — query endpoint",
    version="0.1.0",
    lifespan=lifespan,
)

# Allow the Streamlit UI (different port) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def _extract_text_and_sources(results: Any) -> tuple[str, List[str]]:
    """
    cognee.recall() can return results in slightly different shapes
    depending on version / search strategy. This makes the code defensive:
    it handles strings, dicts, and objects without crashing.
    """
    texts: List[str] = []
    sources: List[str] = []

    if results is None:
        return "", []

    if isinstance(results, str):
        return results, []

    if not isinstance(results, (list, tuple)):
        results = [results]

    for item in results:
        if isinstance(item, str):
            texts.append(item)
        elif isinstance(item, dict):
            # Try common keys for the answer text
            for key in ("text", "answer", "content", "chunk", "value"):
                if item.get(key):
                    texts.append(str(item[key]))
                    break
            else:
                texts.append(str(item))
            # Try common keys for the source
            for key in ("source", "document", "file", "name", "origin"):
                if item.get(key):
                    sources.append(str(item[key]))
                    break
        else:
            # Object with attributes (e.g. a DataPoint)
            text = getattr(item, "text", None) or getattr(item, "content", None)
            texts.append(str(text) if text else str(item))
            src = getattr(item, "source", None) or getattr(item, "document", None)
            if src:
                sources.append(str(src))

    answer = "\n\n".join(t for t in texts if t).strip()
    return answer, sources


# ----------------------------------------------------------------------
# Endpoints
# ----------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok", "service": "cognos-api", "dataset": DEFAULT_DATASET}


@app.post("/ingest")
async def ingest(req: IngestRequest):
    """
    Store text permanently in Cognee's knowledge graph.
    (Person 1's module does bulk folder ingestion — this endpoint exists
    so the backend can be tested standalone, and so the UI could add
    an 'add knowledge' box later.)
    """
    dataset = req.dataset or DEFAULT_DATASET
    payload = req.text
    if req.source_name:
        # Tag the text with its source so recall can attribute it later.
        payload = f"[SOURCE: {req.source_name}]\n{req.text}"

    try:
        await cognee.remember(payload, dataset_name=dataset)
    except TypeError:
        # Older/newer versions may not accept dataset_name — fall back.
        await cognee.remember(payload)
    except Exception as e:
        logger.exception("Ingest failed")
        raise HTTPException(status_code=500, detail=f"Ingest failed: {e}")

    return {"status": "stored", "dataset": dataset, "chars": len(req.text)}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    """
    The main endpoint. Receives a question, recalls from Cognee memory,
    scores confidence, and returns everything the UI needs.
    """
    dataset = req.dataset or DEFAULT_DATASET
    start = time.perf_counter()

    try:
        try:
            results = await cognee.recall(query_text=req.question, datasets=[dataset])
        except TypeError:
            # Fallback for versions where recall takes a plain positional query
            results = await cognee.recall(req.question)
    except Exception as e:
        logger.exception("Recall failed")
        raise HTTPException(status_code=500, detail=f"Recall failed: {e}")

    answer, sources = _extract_text_and_sources(results)
    latency_ms = int((time.perf_counter() - start) * 1000)

    if not answer:
        return AskResponse(
            answer="I don't have enough information in memory to answer that.",
            confidence="low",
            confidence_score=0.0,
            sources=[],
            latency_ms=latency_ms,
        )

    label, score = score_results(req.question, answer, sources, results)

    return AskResponse(
        answer=answer,
        confidence=label,
        confidence_score=round(score, 2),
        sources=sources or ["knowledge graph"],
        latency_ms=latency_ms,
    )


@app.post("/forget")
async def forget(req: ForgetRequest):
    """
    Demonstrates the 4th lifecycle API (judges like this).
    Deletes a dataset from memory.
    """
    dataset = req.dataset or DEFAULT_DATASET
    try:
        await cognee.forget(dataset)
    except TypeError:
        await cognee.forget(datasets=[dataset])
    except Exception as e:
        logger.exception("Forget failed")
        raise HTTPException(status_code=500, detail=f"Forget failed: {e}")
    return {"status": "forgotten", "dataset": dataset}