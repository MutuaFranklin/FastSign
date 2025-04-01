from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.signature import Signature
from app.schemas.signature import SignatureCreate, SignatureResponse
from app.models.user import User
from app.models.document import Document
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/signatures/", response_model=SignatureResponse)
async def create_signature(
    signature: SignatureCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the document exists
    document = db.query(Document).filter(Document.id == signature.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Create signature record
    db_signature = Signature(
        user_id=current_user.id,
        document_id=signature.document_id,
        signature_type=signature.signature_type,
        signature_data=signature.signature_data
    )
    db.add(db_signature)
    db.commit()
    db.refresh(db_signature)

    return db_signature 