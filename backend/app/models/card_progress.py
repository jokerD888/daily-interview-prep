from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
import enum


class CardState(str, enum.Enum):
    new = "new"
    level_0 = "level_0"
    level_1 = "level_1"
    level_2 = "level_2"
    level_3 = "level_3"
    level_4 = "level_4"
    level_5 = "level_5"
    mastered = "mastered"


class ReviewResult(str, enum.Enum):
    correct = "correct"
    forgot = "forgot"


class CardProgress(Base):
    __tablename__ = "card_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    state = Column(String(20), default=CardState.new.value)
    next_review_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="card_progresses")
    card = relationship("Card", back_populates="progresses")


class ReviewLog(Base):
    __tablename__ = "review_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    result = Column(String(10), nullable=False)
    reviewed_at = Column(DateTime, server_default=func.now())
