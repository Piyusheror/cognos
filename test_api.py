"""
Quick end-to-end test for the CognOS API.

1. Start the server in one terminal:   uvicorn main:app --reload --port 8000
2. Run this in a second terminal:      python test_api.py

It stores two facts, waits for indexing, then asks a question.
"""

import time
import requests

BASE = "http://localhost:8000"

print("1) Health check...")
r = requests.get(f"{BASE}/health")
print("   ", r.status_code, r.json())

print("\n2) Ingesting test knowledge (this triggers Cognee's pipeline — can take a minute)...")
facts = [
    {
        "text": "In 2019 the founder decided not to expand to Southeast Asia because "
                "the supply chain costs were 40% higher than projected and the team "
                "lacked local regulatory expertise.",
        "source_name": "board_meeting_2019.txt",
    },
    {
        "text": "The founder consistently prioritized long-term trust over short-term "
                "profit, a principle repeated in speeches from 2008, 2015 and 2021.",
        "source_name": "speeches_collection.txt",
    },
]
for f in facts:
    r = requests.post(f"{BASE}/ingest", json=f, timeout=600)
    print("   ", r.status_code, r.json())

print("\n3) Waiting 10s for indexing to settle...")
time.sleep(10)

print("\n4) Asking a question...")
r = requests.post(
    f"{BASE}/ask",
    json={"question": "Why did the founder decide not to expand to Southeast Asia?"},
    timeout=300,
)
print("   Status:", r.status_code)
data = r.json()
print("   Answer:    ", data.get("answer"))
print("   Confidence:", data.get("confidence"), f"({data.get('confidence_score')})")
print("   Sources:   ", data.get("sources"))
print("   Latency:   ", data.get("latency_ms"), "ms")