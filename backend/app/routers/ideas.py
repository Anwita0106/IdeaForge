from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Idea
from ..schemas import AnalysisResult, IdeaAnalyzeRequest, IdeaOut
from ..services import idea_generator, orchestrator
from ..utils import relative_time, to_epoch_ms

router = APIRouter(prefix="/ideas", tags=["ideas"])


def _idea_to_out(idea: Idea) -> IdeaOut:
    return IdeaOut(
        id=idea.id,
        ideaID=f"IDEA-{idea.id:06d}",
        author=idea.author,
        title=idea.title,
        desc=idea.description,
        category=idea.category,
        tags=idea.tags or [],
        votes=idea.votes,
        comments=idea.comments,
        time=relative_time(idea.created_at),
        saved=False,
        voted=False,
        collaborators=0,
        createdAt=to_epoch_ms(idea.created_at),
        validationScore=idea.validation_score,
        marketCategory=idea.market_category,
        similarStartups=idea.similar_startups or [],
        competitors=idea.competitors or [],
        suggestedImprovements=idea.suggested_improvements or [],
        differentiationOpportunities=idea.differentiation_opportunities or [],
        marketGaps=idea.market_gaps or [],
    )


@router.post("/analyze", response_model=AnalysisResult)
def analyze_idea(payload: IdeaAnalyzeRequest):
    """
    Analyze any startup idea on demand WITHOUT saving it. Useful for a
    "preview before you publish" flow, or for calling this API directly.
    """
    result = orchestrator.analyze_idea(
        title=payload.title,
        description=payload.description,
        category=payload.category or "Tech",
        tags=payload.tags or [],
    )
    return AnalysisResult(**result)


@router.post("/save", response_model=IdeaOut)
def save_idea(payload: IdeaAnalyzeRequest, db: Session = Depends(get_db)):
    """
    Analyze AND persist a new idea to the database. This is what the
    "Share Your Idea" form on the frontend calls.
    """
    analysis = orchestrator.analyze_idea(
        title=payload.title,
        description=payload.description,
        category=payload.category or "Tech",
        tags=payload.tags or [],
    )

    idea = Idea(
        author=(payload.author or "Anonymous").strip() or "Anonymous",
        title=payload.title.strip(),
        description=payload.description.strip(),
        category=payload.category or "Tech",
        tags=(payload.tags or [])[:4],
        votes=1,
        comments=0,
        source="user",
        validation_score=analysis["validationScore"],
        market_category=analysis["marketCategory"],
        similar_startups=[item for item in analysis["similarStartups"]],
        competitors=[item for item in analysis["competitors"]],
        suggested_improvements=analysis["suggestedImprovements"],
        differentiation_opportunities=analysis["differentiationOpportunities"],
        market_gaps=analysis["marketGaps"],
    )
    db.add(idea)
    db.commit()
    db.refresh(idea)
    return _idea_to_out(idea)


@router.post("/generate", response_model=IdeaOut)
def generate_idea(db: Session = Depends(get_db)):
    """
    Bonus endpoint (beyond the required four) that powers the existing
    "Generate AI Idea" button: synthesizes a new concept, analyzes it, saves
    it, and returns it - all in one call.
    """
    title, description, category, tags = idea_generator.generate_idea_seed()
    analysis = orchestrator.analyze_idea(title=title, description=description, category=category, tags=tags)

    idea = Idea(
        author="IdeaForge AI",
        title=title,
        description=description,
        category=category,
        tags=tags,
        votes=8,
        comments=1,
        source="ai_generated",
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
    db.refresh(idea)
    return _idea_to_out(idea)


@router.get("", response_model=List[IdeaOut])
def list_ideas(db: Session = Depends(get_db)):
    """Returns every idea, newest first. Filtering/sorting/search continue
    to happen on the frontend, exactly as in the original prototype."""
    ideas = db.query(Idea).order_by(desc(Idea.created_at)).limit(500).all()
    return [_idea_to_out(idea) for idea in ideas]


@router.get("/{idea_id}", response_model=IdeaOut)
def get_idea(idea_id: int, db: Session = Depends(get_db)):
    idea = db.query(Idea).filter(Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    return _idea_to_out(idea)
