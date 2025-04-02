from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

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
    signature_data = Column(Text)  # Base64 encoded data
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="signatures")
    document = relationship("Document", back_populates="signatures")
