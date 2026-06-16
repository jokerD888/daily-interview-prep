from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    importance_score = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())

    material = relationship("Material", back_populates="cards")
    progresses = relationship("CardProgress", back_populates="card")
