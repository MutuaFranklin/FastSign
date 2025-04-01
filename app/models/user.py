from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    full_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Add relationship
    documents = relationship("Document", back_populates="user")
    signatures = relationship("Signature", back_populates="user") 

    