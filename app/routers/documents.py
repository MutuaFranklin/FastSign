from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
import secrets
import os  # Import os for file path handling
from fastapi.responses import FileResponse  # Import FileResponse
from app.database import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.auth import get_current_user
from app.models.user import User
from app.config import settings  # Import settings to access environment variables

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate unique access token
    access_token = secrets.token_urlsafe(32)
    
    # Define the file path
    file_path = f"documents/{access_token}_{file.filename}"
    signed_file_path = f"documents/signed_{access_token}_{file.filename}"

    # Ensure the documents directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Create document record
    db_document = Document(
        filename=file.filename,
        file_path=file_path,
        signed_file_path=signed_file_path,
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

@router.get("/metadata/{access_token}", response_model=DocumentResponse)
async def get_document(
    access_token: str,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(Document.access_token == access_token).first()
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # Construct the file link and signed link using BASE_URL from environment variables
    file_link = f"{settings.BASE_URL}/{document.file_path}"  # Use BASE_URL
    signed_link = f"{settings.BASE_URL}/{document.signed_file_path}"  # Use BASE_URL

    print(f"File link: {file_link}")
    print(f"Signed link: {signed_link}")

    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        access_token=document.access_token,
        created_at=document.created_at,
        signed_at=document.signed_at,
        file_link=file_link,
        signed_link=signed_link
    )

@router.get("/view/{access_token}")
async def view_document(
    access_token: str,
    db: Session = Depends(get_db)
):
    document = db.query(Document).filter(Document.access_token == access_token).first()
    
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # Check if the document is signed
    if document.signed_at:
        # Serve the signed document
        return FileResponse(document.signed_file_path)  # Directly return the signed document
    else:
        # Serve the original document
        return FileResponse(document.file_path)  # Directly return the original document 