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

class SignatureCreate(SignatureBase):
    document_id: int  # ID of the document to which the signature belongs

class SignatureResponse(SignatureBase):
    id: int
    user_id: int
    document_id: int
    created_at: datetime

    class Config:
        orm_mode = True 