"""
Confidence scoring for CognOS answers.

Two modes:
  1. If the decay engine (Person 2's part) is available, use its score.
     It just needs to expose:  get_decay_score(question, answer, sources) -> float (0..1)
  2. Otherwise, fall back to a simple built-in heuristic so the API
     works end-to-end even before the decay engine is finished.

Labels: score >= 0.7 -> "high", >= 0.4 -> "medium", else "low"
"""

from typing import Any, List, Tuple

# Try to plug in the teammate's decay engine if it exists.
try:
    from decay_engine import get_decay_score  # type: ignore
    HAS_DECAY_ENGINE = True
except ImportError:
    HAS_DECAY_ENGINE = False


def _heuristic_score(question: str, answer: str, sources: List[str], raw_results: Any) -> float:
    """Simple signals that correlate with answer quality."""
    score = 0.0

    # Signal 1: how many results came back (more corroboration = better)
    n_results = len(raw_results) if isinstance(raw_results, (list, tuple)) else 1
    score += min(n_results / 5.0, 0.4)          # up to 0.4

    # Signal 2: answer length (very short answers are usually weak)
    if len(answer) > 400:
        score += 0.3
    elif len(answer) > 100:
        score += 0.2
    elif len(answer) > 30:
        score += 0.1

    # Signal 3: keyword overlap between question and answer
    q_words = {w.lower() for w in question.split() if len(w) > 3}
    a_lower = answer.lower()
    if q_words:
        overlap = sum(1 for w in q_words if w in a_lower) / len(q_words)
        score += overlap * 0.2                   # up to 0.2

    # Signal 4: do we have source attribution?
    if sources:
        score += 0.1

    return min(score, 1.0)


def score_results(
    question: str,
    answer: str,
    sources: List[str],
    raw_results: Any,
) -> Tuple[str, float]:
    """Return (label, score) where label is high/medium/low."""
    if HAS_DECAY_ENGINE:
        try:
            score = float(get_decay_score(question, answer, sources))
        except Exception:
            score = _heuristic_score(question, answer, sources, raw_results)
    else:
        score = _heuristic_score(question, answer, sources, raw_results)

    if score >= 0.7:
        return "high", score
    if score >= 0.4:
        return "medium", score
    return "low", score