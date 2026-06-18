"""
IdeaForge's own heuristic "validation engine".

This is what guarantees /ideas/analyze and /ideas/save always return a
complete, useful response - even with zero external API keys configured.
When Crunchbase / Product Hunt / Google / Clearbit ARE configured, their
results are layered on top of (and take priority over) this engine's
fallback suggestions for the "similar startups" / "competitors" lists.
Validation scoring and the written suggestions are always produced here,
since none of those four APIs actually generate advice - they only return
raw company/listing data.
"""
import hashlib
import re
from typing import List

from . import knowledge_base as kb

STOPWORDS = {
    "the", "a", "an", "and", "or", "for", "to", "of", "in", "on", "with",
    "that", "this", "is", "are", "be", "by", "it", "as", "at", "from",
    "your", "our", "their", "into", "will", "can", "we", "i", "you",
}


def extract_keywords(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def _stable_choice(seed: str, options: List[str], count: int) -> List[str]:
    """Deterministically pick `count` items from `options` based on a seed
    string, so the same idea text produces the same suggestions, while
    different ideas naturally get different combinations."""
    if not options:
        return []
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    start = int(digest[:8], 16)
    picked = []
    for i in range(count):
        idx = (start + i * 7) % len(options)
        if options[idx] not in picked:
            picked.append(options[idx])
    return picked


def classify_market_category(category: str, keywords: List[str]) -> str:
    base = kb.MARKET_CATEGORY_LABELS.get(category, "General Consumer / SaaS")
    extra_tags = []
    if "ai" in keywords or "machine" in keywords:
        extra_tags.append("AI")
    if "marketplace" in keywords or "peer" in keywords:
        extra_tags.append("Marketplace")
    if "mobile" in keywords or "app" in keywords:
        extra_tags.append("Mobile")
    if extra_tags:
        return f"{base} ({' / '.join(extra_tags)})"
    return base


def generate_improvements(title: str, description: str, category: str, keywords: List[str]) -> List[str]:
    pool = list(kb.IMPROVEMENT_TEMPLATES.get(category, []))
    pool += kb.IMPROVEMENT_TEMPLATES.get("Tech", [])  # general-purpose backup options
    if "ai" in keywords and "Be transparent about where AI can be wrong, and let users correct it easily." not in pool:
        pool.append("Be transparent about where AI can be wrong, and let users correct it easily.")
    if len(description) < 60:
        pool.append("Flesh out the problem statement - a sharper description makes the idea easier to validate and pitch.")
    return _stable_choice(title + description, pool, 3)


def generate_differentiation(title: str, description: str, category: str, keywords: List[str], competitor_count: int) -> List[str]:
    pool = list(kb.DIFFERENTIATION_TEMPLATES)
    if competitor_count == 0:
        pool.insert(0, "No close matches were found, which can mean genuine white space - or that the category needs validating with real users first.")
    elif competitor_count >= 5:
        pool.insert(0, "The space looks crowded - winning will likely come down to a sharper niche or a much better first-run experience.")
    return _stable_choice(title + description + category, pool, 3)


def generate_market_gaps(category: str, keywords: List[str], competitor_count: int) -> List[str]:
    pool = list(kb.MARKET_GAP_TEMPLATES)
    return _stable_choice(category + "".join(keywords) + str(competitor_count), pool, 3)


def compute_validation_score(title: str, description: str, tags: List[str], category: str, live_result_count: int, total_result_count: int) -> int:
    """
    A transparent 0-100 composite score:
      - clarity (0-30): is the description substantial enough to evaluate?
      - market signal (0-30): does a market clearly exist (some, but not too
        many, comparable products)?
      - differentiation potential (0-20): does the text show any
        intentional positioning vs. alternatives?
      - completeness (0-20): title, tags and category all meaningfully filled in.
    """
    word_count = len(description.split())
    if word_count < 8:
        clarity = 8
    elif word_count < 15:
        clarity = 18
    elif word_count <= 80:
        clarity = 30
    elif word_count <= 140:
        clarity = 24
    else:
        clarity = 18

    if total_result_count == 0:
        market_signal = 16  # could be a genuinely novel idea, or just unproven - stay neutral
    elif total_result_count <= 4:
        market_signal = 30  # healthy signal: a market exists, not saturated
    elif total_result_count <= 8:
        market_signal = 22
    else:
        market_signal = 14  # crowded market

    diff_keywords = ["unlike", "unique", "instead of", "first", "better than", "without the", "no one"]
    lowered = description.lower()
    differentiation = 8
    for kw in diff_keywords:
        if kw in lowered:
            differentiation = 20
            break

    completeness = 0
    if title and len(title.strip()) >= 3:
        completeness += 7
    if tags and len(tags) >= 2:
        completeness += 7
    if category:
        completeness += 6

    score = clarity + market_signal + differentiation + completeness
    return max(0, min(100, int(score)))
