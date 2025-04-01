from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class SignatureType(str, Enum):
    DRAWN = "drawn"
    TEXT = "text"
    IMAGE = "image"

class SignatureBase(BaseModel):
    signature_type: SignatureType
    signature_data: str  # Base64 encoded data or path to the signature file

class SignatureCreate(BaseModel):
    document_id: int
    signature_type: SignatureType
    signature_data: str  # Path to the signature image

class SignatureResponse(SignatureCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True 