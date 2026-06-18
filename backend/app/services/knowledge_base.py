"""
A small, generalized knowledge base used as a fallback whenever the live
external providers (Crunchbase / Product Hunt / Google / Clearbit) are not
configured or don't return enough results.

Unlike the old frontend prototype - which mapped a handful of *exact* demo
idea titles to a handful of *exact* fake links - everything here is keyed by
category and keyword, so it generalizes to literally any idea a user types
in, instead of only working for a few pre-written titles.
"""
from typing import Dict, List

CATEGORY_PLAYERS: Dict[str, List[dict]] = {
    "Tech": [
        {"name": "Notion", "url": "https://www.notion.so/"},
        {"name": "Linear", "url": "https://linear.app/"},
        {"name": "Slack", "url": "https://slack.com/"},
    ],
    "Health": [
        {"name": "Practo", "url": "https://www.practo.com/"},
        {"name": "Ada Health", "url": "https://ada.com/"},
        {"name": "WebMD", "url": "https://www.webmd.com/"},
    ],
    "Social": [
        {"name": "Discord", "url": "https://discord.com/"},
        {"name": "Meetup", "url": "https://www.meetup.com/"},
        {"name": "Nextdoor", "url": "https://nextdoor.com/"},
    ],
    "Climate": [
        {"name": "Ecosia", "url": "https://www.ecosia.org/"},
        {"name": "Joro", "url": "https://www.joro.tech/"},
        {"name": "Watershed", "url": "https://watershed.com/"},
    ],
    "Education": [
        {"name": "Coursera", "url": "https://www.coursera.org/"},
        {"name": "Udemy", "url": "https://www.udemy.com/"},
        {"name": "Khan Academy", "url": "https://www.khanacademy.org/"},
    ],
    "Finance": [
        {"name": "Mint", "url": "https://mint.intuit.com/"},
        {"name": "Stripe", "url": "https://stripe.com/"},
        {"name": "Plaid", "url": "https://plaid.com/"},
    ],
}

# Keyword -> extra real companies layered on top of the category list above.
# Matching is a simple "is this keyword present in the idea text" check.
KEYWORD_PLAYERS: Dict[str, List[dict]] = {
    "ai": [{"name": "OpenAI", "url": "https://openai.com/"}],
    "machine learning": [{"name": "Hugging Face", "url": "https://huggingface.co/"}],
    "mental health": [{"name": "Calm", "url": "https://www.calm.com/"}, {"name": "BetterHelp", "url": "https://www.betterhelp.com/"}],
    "fitness": [{"name": "Strava", "url": "https://www.strava.com/"}],
    "nutrition": [{"name": "MyFitnessPal", "url": "https://www.myfitnesspal.com/"}],
    "food": [{"name": "DoorDash", "url": "https://www.doordash.com/"}],
    "marketplace": [{"name": "Etsy", "url": "https://www.etsy.com/"}],
    "campus": [{"name": "Handshake", "url": "https://joinhandshake.com/"}],
    "student": [{"name": "Chegg", "url": "https://www.chegg.com/"}],
    "tutor": [{"name": "Khan Academy", "url": "https://www.khanacademy.org/"}],
    "mentor": [{"name": "MentorCruise", "url": "https://mentorcruise.com/"}],
    "security": [{"name": "Cloudflare", "url": "https://www.cloudflare.com/"}],
    "cyber": [{"name": "Cloudflare", "url": "https://www.cloudflare.com/"}],
    "carbon": [{"name": "Joro", "url": "https://www.joro.tech/"}],
    "sustainab": [{"name": "Ecosia", "url": "https://www.ecosia.org/"}],
    "recycle": [{"name": "TerraCycle", "url": "https://www.terracycle.com/"}],
    "thrift": [{"name": "Depop", "url": "https://www.depop.com/"}],
    "budget": [{"name": "YNAB", "url": "https://www.youneedabudget.com/"}],
    "freelance": [{"name": "Upwork", "url": "https://www.upwork.com/"}],
    "skill": [{"name": "Udemy", "url": "https://www.udemy.com/"}],
}

MARKET_CATEGORY_LABELS: Dict[str, str] = {
    "Tech": "Technology / SaaS",
    "Health": "Health & Wellness Tech",
    "Social": "Social & Community Platforms",
    "Climate": "Climate & Sustainability Tech",
    "Education": "Education Technology (EdTech)",
    "Finance": "Financial Technology (FinTech)",
}

IMPROVEMENT_TEMPLATES: Dict[str, List[str]] = {
    "Tech": [
        "Add a mobile-first experience so users can act the moment a need comes up.",
        "Ship a simple analytics dashboard so users can see their own progress.",
        "Offer an API or integrations so power users can plug this into existing tools.",
    ],
    "Health": [
        "Make data privacy and consent explicit and easy to understand.",
        "Add a lightweight way to loop in a clinician or trusted adult when needed.",
        "Support offline or low-bandwidth use so access isn't a barrier.",
    ],
    "Social": [
        "Add lightweight moderation so trust is established early.",
        "Make the first five minutes of onboarding self-explanatory.",
        "Add a referral loop so happy users can invite the people they already trust.",
    ],
    "Climate": [
        "Quantify impact in concrete terms (CO2, waste, dollars) instead of vague claims.",
        "Partner with an existing local institution to bootstrap initial supply or demand.",
        "Gamify small consistent actions instead of asking for one big behavior change.",
    ],
    "Education": [
        "Add spaced-repetition or progress tracking to reinforce learning over time.",
        "Make it easy for an instructor or mentor to plug into the workflow.",
        "Offer a free tier that's genuinely useful, not just a teaser.",
    ],
    "Finance": [
        "Be explicit about how the product makes money - it builds trust fast.",
        "Add bank-grade security messaging early; this category lives and dies on trust.",
        "Start with one very specific money decision instead of trying to cover everything.",
    ],
}

DIFFERENTIATION_TEMPLATES: List[str] = [
    "Focus on one underserved niche first instead of trying to serve everyone at once.",
    "Lean into a workflow or audience the bigger players have been slow to design for.",
    "Win on speed-to-value: make the very first session genuinely useful, not just a demo.",
    "Differentiate on trust and transparency in a space where incumbents feel opaque.",
    "Bundle a feature competitors charge extra for as a default, free part of the experience.",
    "Build for a specific community (e.g. students, local businesses) rather than a generic market.",
]

MARKET_GAP_TEMPLATES: List[str] = [
    "Most existing tools in this space were built for larger organizations, not individuals or small teams.",
    "There's limited support for non-English speakers or non-Western contexts in this category today.",
    "Pricing in this space tends to be opaque or aimed at enterprise budgets, leaving smaller users underserved.",
    "Few products combine this functionality with strong privacy guarantees by default.",
    "Existing solutions assume constant connectivity, leaving low-bandwidth users behind.",
]


def find_known_players(category: str, keywords: List[str], limit: int = 6) -> List[dict]:
    results: List[dict] = []
    seen = set()

    for kw in keywords:
        for key, players in KEYWORD_PLAYERS.items():
            # Exact match for short keys (avoids false positives like "ai"
            # matching inside "sustainability"); substring match for longer,
            # more specific keys like "sustainab" or "marketplace".
            is_match = kw == key if len(key) <= 4 else key in kw
            if is_match:
                for player in players:
                    if player["name"] not in seen:
                        results.append(player)
                        seen.add(player["name"])

    for player in CATEGORY_PLAYERS.get(category, []):
        if player["name"] not in seen:
            results.append(player)
            seen.add(player["name"])

    return results[:limit]
