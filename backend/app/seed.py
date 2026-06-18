"""
Optional helper to populate a fresh database with a few demo ideas, purely
for a nicer first-run experience. The app does NOT call this automatically
unless SEED_DEMO_DATA=true is set - by default IdeaForge starts with a
genuinely empty, dynamic feed.

Run manually with:
    python -m app.seed
"""
from .database import SessionLocal, Base, engine
from .models import Idea
from .services import orchestrator

DEMO_IDEAS = [
    {"author": "Priya R.", "title": "CampusCarbon", "description": "A student-run carbon tracking app that rewards low-waste habits on campus with challenges, points, and shared goals.", "category": "Climate", "tags": ["Sustainability", "Campus", "Gamification"]},
    {"author": "Keanu M.", "title": "MedBuddy AI", "description": "An AI-powered symptom journaling tool for students with limited healthcare access, designed to track patterns over time.", "category": "Health", "tags": ["AI", "Healthcare", "Students"]},
    {"author": "Sophie L.", "title": "SkillSwap", "description": "A peer marketplace where students exchange skills directly, from coding support to music lessons, without money.", "category": "Social", "tags": ["Marketplace", "Community", "Education"]},
    {"author": "Dev P.", "title": "LectureLens", "description": "Upload any lecture recording and get summaries, flashcards, and quiz prompts instantly for better revision.", "category": "Tech", "tags": ["AI", "EdTech", "Productivity"]},
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Idea).count() > 0:
            print("Database already has ideas - skipping seed.")
            return

        for entry in DEMO_IDEAS:
            analysis = orchestrator.analyze_idea(
                title=entry["title"],
                description=entry["description"],
                category=entry["category"],
                tags=entry["tags"],
            )
            idea = Idea(
                author=entry["author"],
                title=entry["title"],
                description=entry["description"],
                category=entry["category"],
                tags=entry["tags"],
                votes=12,
                comments=3,
                source="user",
                validation_score=analysis["validationScore"],
                market_category=analysis["marketCategory"],
                similar_startups=analysis["similarStartups"],
                competitors=analysis["competitors"],
                suggested_improvements=analysis["suggestedImprovements"],
                differentiation_opportunities=analysis["differentiationOpportunities"],
                market_gaps=analysis["marketGaps"],
            )
            db.add(idea)
        db.commit()
        print(f"Seeded {len(DEMO_IDEAS)} demo ideas.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
