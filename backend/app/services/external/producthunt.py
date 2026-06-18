"""
Optional Product Hunt integration (GraphQL API v2).

Used to surface recently launched, comparable products. Requires a
PRODUCTHUNT_API_TOKEN (developer token from https://api.producthunt.com/v2/oauth/applications).
If it isn't set, this module is skipped and the heuristic fallback takes over.

Docs: https://api.producthunt.com/v2/docs
"""
from typing import List

import httpx

from ...config import settings

GRAPHQL_URL = "https://api.producthunt.com/v2/api/graphql"

QUERY = """
query SearchPosts($first: Int!) {
  posts(order: VOTES, first: $first) {
    edges {
      node {
        name
        tagline
        website
      }
    }
  }
}
"""


def search_products(query: str, limit: int = 5) -> List[dict]:
    if not settings.PRODUCTHUNT_API_TOKEN:
        return []

    try:
        headers = {
            "Authorization": f"Bearer {settings.PRODUCTHUNT_API_TOKEN}",
            "Content-Type": "application/json",
        }
        # Product Hunt's v2 API does not expose a generic free-text search
        # endpoint for posts, so we pull currently popular posts and filter
        # them client-side for keyword overlap with the submitted idea.
        with httpx.Client(timeout=settings.EXTERNAL_API_TIMEOUT_SECONDS) as client:
            resp = client.post(GRAPHQL_URL, json={"query": QUERY, "variables": {"first": 50}}, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        edges = (data.get("data", {}) or {}).get("posts", {}).get("edges", [])
        query_words = set(query.lower().split())

        scored = []
        for edge in edges:
            node = edge.get("node", {})
            name = node.get("name", "")
            tagline = (node.get("tagline") or "").lower()
            overlap = sum(1 for w in query_words if w and w in tagline)
            if overlap > 0:
                scored.append((overlap, {"name": name, "url": node.get("website") or "#"}))

        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item for _, item in scored[:limit]]
    except Exception:
        return []
