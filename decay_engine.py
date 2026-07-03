"""
CognOS — Decay Engine (Person 2)
=================================
Scores every answer from Cognee with a confidence value between 0.0 and 1.0.

Three signals:
  1. Age decay     — newer sources are more trustworthy
  2. Corroboration — more sources agreeing = higher confidence  
  3. Relevance     — keyword overlap between question and answer

The backend (confidence.py) calls get_decay_score() automatically.
"""

import re
from datetime import datetime
from typing import List


# Current year — used to calculate how old a source is
CURRENT_YEAR = datetime.now().year

# How fast confidence decays with age
# 0.05 means a 10-year-old source loses 0.5 points — quite aggressive
DECAY_RATE = 0.05

# Maximum age we consider (anything older gets minimum age score)
MAX_AGE_YEARS = 20


def _extract_year_from_source(source: str) -> int:
    """
    Try to pull a 4-digit year out of a filename like:
      board_meeting_2019.txt  ->  2019
      speech_2015_london.txt  ->  2015
      ratan_tata_2008.txt     ->  2008
    If no year found, assume it is moderately old (5 years ago).
    """
    match = re.search(r"(19|20)\d{2}", source)
    if match:
        return int(match.group())
    return CURRENT_YEAR - 5  # default: assume 5 years old


def _age_score(sources: List[str]) -> float:
    """
    Signal 1 — Age decay.
    Finds the NEWEST source in the list and scores based on its age.
    A document from this year scores 1.0.
    A document 20+ years old scores close to 0.0.
    """
    if not sources:
        return 0.2  # no sources = low but not zero

    years = [_extract_year_from_source(s) for s in sources]
    newest_year = max(years)
    age = max(0, CURRENT_YEAR - newest_year)
    age_capped = min(age, MAX_AGE_YEARS)

    # Linear decay: score = 1 - (age / max_age)
    score = 1.0 - (age_capped / MAX_AGE_YEARS)
    return round(score, 3)


def _corroboration_score(sources: List[str]) -> float:
    """
    Signal 2 — Corroboration.
    More unique sources saying the same thing = more trustworthy.
    1 source  -> 0.3
    2 sources -> 0.6
    3+ sources -> 1.0
    """
    unique_sources = len(set(sources))
    if unique_sources == 0:
        return 0.1
    if unique_sources == 1:
        return 0.3
    if unique_sources == 2:
        return 0.6
    return 1.0  # 3 or more sources


def _relevance_score(question: str, answer: str) -> float:
    """
    Signal 3 — Keyword relevance.
    Checks how many important words from the question
    actually appear in the answer.
    """
    # Words to ignore — common words that carry no meaning
    stopwords = {
        "the", "a", "an", "is", "was", "were", "are", "did",
        "do", "does", "what", "why", "how", "when", "who",
        "which", "that", "this", "and", "or", "but", "in",
        "on", "at", "to", "for", "of", "with", "by", "from"
    }

    # Extract meaningful words from the question
    q_words = {
        w.lower() for w in re.findall(r"\b\w+\b", question)
        if w.lower() not in stopwords and len(w) > 2
    }

    if not q_words:
        return 0.5  # can't judge, return neutral

    answer_lower = answer.lower()
    matches = sum(1 for w in q_words if w in answer_lower)
    score = matches / len(q_words)
    return round(score, 3)


def get_decay_score(question: str, answer: str, sources: List[str]) -> float:
    """
    MAIN FUNCTION — called by confidence.py automatically.

    Combines all three signals into one final confidence score.

    Weights:
      Age decay     — 35%  (most important: old knowledge = risky)
      Corroboration — 35%  (multiple sources = trustworthy)
      Relevance     — 30%  (answer actually addresses the question)

    Returns a float between 0.0 and 1.0.
    """
    age = _age_score(sources)
    corroboration = _corroboration_score(sources)
    relevance = _relevance_score(question, answer)

    final_score = (
        age           * 0.35 +
        corroboration * 0.35 +
        relevance     * 0.30
    )

    final_score = round(min(final_score, 1.0), 3)

    # Log so you can see it working during the demo
    print(f"[DecayEngine] age={age} | corroboration={corroboration} | relevance={relevance} | final={final_score}")

    return final_score