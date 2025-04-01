from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    filename: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    access_token: str
    created_at: datetime
    signed_at: Optional[datetime] = None
    file_link: str
    signed_link: Optional[str] = None

    class Config:
        orm_mode = True 