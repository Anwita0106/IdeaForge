"""
Powers the "Generate AI Idea" button. Synthesizes a plausible new startup
concept from rotating templates and seeds, instead of picking from the four
hard-coded ideas the original prototype shipped with.

This is intentionally template-based rather than a call to a generative
language model, since no LLM provider/key is in scope for this project. If
you add one later (e.g. the Anthropic API), this is the file to swap in a
real generation call - `analyze_idea()` downstream doesn't care where the
title/description came from.
"""
import random
from typing import Tuple

TEMPLATES = [
    ("Tech", "{noun} Copilot", "An AI assistant that handles the repetitive parts of {domain}, so {audience} can focus on the work that actually needs a human."),
    ("Health", "{noun}Track", "A lightweight tracker that helps {audience} notice patterns in {domain} over time, without needing a clinician for every check-in."),
    ("Social", "{noun}Circle", "A small-group platform that helps {audience} find and keep accountability partners for {domain}."),
    ("Climate", "{noun}Loop", "A circular-economy marketplace that helps {audience} share, repair, or rehome underused items related to {domain}."),
    ("Education", "{noun}Path", "An adaptive study companion that turns {domain} material into summaries, flashcards, and quizzes for {audience}."),
    ("Finance", "{noun}Ledger", "A plain-language budgeting tool that helps {audience} make sense of {domain} without needing a finance background."),
]

NOUNS = ["Dorm", "Pulse", "Nimbus", "Forge", "Loop", "Nest", "Spark", "Drift", "Anchor", "Beacon"]
DOMAINS = ["daily routines", "campus life", "personal finance", "study habits", "local commerce", "wellness habits", "team coordination", "sustainable living"]
AUDIENCES = ["students", "early-career professionals", "small teams", "busy parents", "local communities", "freelancers"]


def generate_idea_seed() -> Tuple[str, str, str, list]:
    """Returns (title, description, category, tags) for a freshly synthesized idea."""
    category, title_template, desc_template = random.choice(TEMPLATES)
    noun = random.choice(NOUNS)
    domain = random.choice(DOMAINS)
    audience = random.choice(AUDIENCES)

    title = title_template.format(noun=noun)
    description = desc_template.format(domain=domain, audience=audience)
    tags = [category, "AI", "Generated"]

    return title, description, category, tags
