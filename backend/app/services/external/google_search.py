"""
Optional Google Custom Search (Programmable Search Engine) integration.

Used as a general-purpose web search to find similar startups / competitors
for any idea, since it isn't limited to a single data provider's catalog.
Requires GOOGLE_API_KEY and GOOGLE_CSE_ID. If either is missing, this module
is skipped and the heuristic fallback takes over.

Setup: https://developers.google.com/custom-search/v1/overview
"""
from typing import List

import httpx

from ...config import settings

SEARCH_URL = "https://www.googleapis.com/customsearch/v1"


def web_search(query: str, limit: int = 5) -> List[dict]:
    if not settings.GOOGLE_API_KEY or not settings.GOOGLE_CSE_ID:
        return []

    try:
        params = {
            "key": settings.GOOGLE_API_KEY,
            "cx": settings.GOOGLE_CSE_ID,
            "q": query,
            "num": min(limit, 10),
        }
        with httpx.Client(timeout=settings.EXTERNAL_API_TIMEOUT_SECONDS) as client:
            resp = client.get(SEARCH_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        items = data.get("items", []) or []
        results = []
        for item in items[:limit]:
            title = item.get("title")
            link = item.get("link")
            if title and link:
                results.append({"name": title, "url": link})
        return results
    except Exception:
        return []
