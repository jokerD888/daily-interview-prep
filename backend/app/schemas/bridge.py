"""Schemas for bridge import from InterviewLens."""
from pydantic import BaseModel, Field


class BridgeCardItem(BaseModel):
    question: str
    answer: str
    importance_score: int = 3
    source_url: str | None = None


class BulkImportRequest(BaseModel):
    cards: list[BridgeCardItem] = Field(min_length=1, max_length=50)


class BulkImportResponse(BaseModel):
    imported: int
    skipped: int
    skipped_reasons: list[str] = Field(default_factory=list)
