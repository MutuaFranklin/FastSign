from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import secrets
from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate unique access token
    access_token = secrets.token_urlsafe(32)
    
    # Create document record
    db_document = Document(
        filename=file.filename,
        file_path=f"documents/{access_token}_{file.filename}",  # You'll need to implement file storage
        access_token=access_token,
        user_id=current_user.id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/list", response_model=List[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    return documents

@router.get("/public/{access_token}", response_model=DocumentResponse)
async def get_document(
    access_token: str,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(Document.access_token == access_token).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document 