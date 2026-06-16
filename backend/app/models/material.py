from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base
import enum


class MaterialStatus(str, enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, default="")
    file_type = Column(String(10), nullable=False)
    status = Column(String(20), default=MaterialStatus.uploaded.value)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="materials")
    cards = relationship("Card", back_populates="material", cascade="all, delete-orphan")
