"""
Optional Crunchbase integration.

Used to look up real organizations related to a submitted idea so the
"similar startups" / "competitors" lists can be backed by live data instead
of the built-in knowledge base. Requires CRUNCHBASE_API_KEY (a paid
Crunchbase Enterprise API key) - if it isn't set, this module is skipped
entirely and the heuristic fallback takes over.

Docs: https://data.crunchbase.com/docs/using-the-api
"""
from typing import List

import httpx

from ...config import settings

SEARCH_URL = "https://api.crunchbase.com/api/v4/searches/organizations"


def search_organizations(query: str, limit: int = 5) -> List[dict]:
    if not settings.CRUNCHBASE_API_KEY:
        return []

    try:
        headers = {"X-cb-user-key": settings.CRUNCHBASE_API_KEY, "Content-Type": "application/json"}
        body = {
            "field_ids": ["identifier", "short_description", "website_url"],
            "query": [
                {"type": "predicate", "field_id": "name", "operator_id": "contains", "values": [query]}
            ],
            "limit": limit,
        }
        with httpx.Client(timeout=settings.EXTERNAL_API_TIMEOUT_SECONDS) as client:
            resp = client.post(SEARCH_URL, json=body, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        results: List[dict] = []
        for entity in data.get("entities", [])[:limit]:
            props = entity.get("properties", {}) or {}
            identifier = props.get("identifier") or {}
            name = identifier.get("value") if isinstance(identifier, dict) else identifier
            website = props.get("website_url")
            if name:
                results.append({"name": name, "url": website or "#"})
        return results
    except Exception:
        # Network errors, auth errors, rate limits, schema changes, etc. - we
        # never want a third-party outage to break idea analysis.
        return []
