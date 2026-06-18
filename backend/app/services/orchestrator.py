"""
Combines the (optional) external providers with IdeaForge's heuristic
engine into a single, complete validation analysis for any submitted idea.
"""
from typing import List

from . import heuristics, knowledge_base as kb
from .external import crunchbase, google_search, producthunt


def _dedupe(items: List[dict]) -> List[dict]:
    seen = set()
    out = []
    for item in items:
        name = (item.get("name") or "").strip().lower()
        if name and name not in seen:
            seen.add(name)
            out.append(item)
    return out


def analyze_idea(title: str, description: str, category: str, tags: List[str]) -> dict:
    category = category or "Tech"
    tags = tags or []
    keywords = heuristics.extract_keywords(f"{title} {description} {' '.join(tags)} {category}")

    # 1. Try the live external providers first (each is a no-op if its
    #    API key isn't configured, or fails silently on any error).
    live_results: List[dict] = []
    live_results += crunchbase.search_organizations(title)
    live_results += producthunt.search_products(title)
    live_results += google_search.web_search(f"{title} startup competitor")
    live_results = _dedupe(live_results)

    # 2. Fill in / supplement with the generalized knowledge base so the
    #    response is always complete even with zero API keys configured.
    fallback_results = kb.find_known_players(category, keywords)
    combined = _dedupe(live_results + fallback_results)

    similar_startups = combined[:4] if combined else []
    competitors = combined[4:8] if len(combined) > 4 else combined[:3]

    market_category = heuristics.classify_market_category(category, keywords)

    validation_score = heuristics.compute_validation_score(
        title=title,
        description=description,
        tags=tags,
        category=category,
        live_result_count=len(live_results),
        total_result_count=len(combined),
    )

    suggested_improvements = heuristics.generate_improvements(title, description, category, keywords)
    differentiation_opportunities = heuristics.generate_differentiation(
        title, description, category, keywords, competitor_count=len(combined)
    )
    market_gaps = heuristics.generate_market_gaps(category, keywords, competitor_count=len(combined))

    return {
        "validationScore": validation_score,
        "marketCategory": market_category,
        "similarStartups": similar_startups,
        "competitors": competitors,
        "suggestedImprovements": suggested_improvements,
        "differentiationOpportunities": differentiation_opportunities,
        "marketGaps": market_gaps,
    }
