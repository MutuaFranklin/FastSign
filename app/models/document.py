from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    file_path = Column(String(255))  # Path to stored document
    signed_file_path = Column(String(255))  # Path to signed version
    access_token = Column(String(100), unique=True, index=True)  # For public access
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    signed_at = Column(DateTime, nullable=True)

    # Add relationship
    user = relationship("User", back_populates="documents")
    signatures = relationship("Signature", back_populates="document") 