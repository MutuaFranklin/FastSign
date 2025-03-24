from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base

class SignatureType(str, PyEnum):
    DRAWN = "drawn"
    TEXT = "text"
    IMAGE = "image"

class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    document_id = Column(Integer, ForeignKey("documents.id"))
    signature_type = Column(SQLEnum(SignatureType))
    signature_data = Column(String(1000000))  # Base64 encoded data
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="signatures")
    document = relationship("Document", back_populates="signatures") 