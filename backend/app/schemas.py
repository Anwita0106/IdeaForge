from typing import List, Optional

from pydantic import BaseModel, Field


class LinkItem(BaseModel):
    name: str
    url: str


class IdeaAnalyzeRequest(BaseModel):
    """Body for POST /ideas/analyze and POST /ideas/save."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: Optional[str] = "Tech"
    tags: Optional[List[str]] = []
    author: Optional[str] = "Anonymous"


class AnalysisResult(BaseModel):
    validationScore: int
    marketCategory: str
    similarStartups: List[LinkItem]
    competitors: List[LinkItem]
    suggestedImprovements: List[str]
    differentiationOpportunities: List[str]
    marketGaps: List[str]


class IdeaOut(BaseModel):
    id: int
    ideaID: str
    author: str
    title: str
    desc: str
    category: str
    tags: List[str]

    votes: int
    comments: int
    time: str

    # Client-side-only interaction state. The backend always returns the
    # neutral defaults below; voting/saving/collaborating are handled in the
    # browser for this MVP (see README "Known limitations").
    saved: bool = False
    voted: bool = False
    collaborators: int = 0

    createdAt: int  # epoch milliseconds, used by the existing client sort logic

    validationScore: int
    marketCategory: str
    similarStartups: List[LinkItem]
    competitors: List[LinkItem]
    suggestedImprovements: List[str]
    differentiationOpportunities: List[str]
    marketGaps: List[str]
