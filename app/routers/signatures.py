from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.signature import Signature
from app.schemas.signature import SignatureCreate, SignatureResponse
from app.models.user import User
from app.models.document import Document
from app.services.auth import get_current_user
from datetime import datetime
import PyPDF2
import io

router = APIRouter()

def add_signature_to_pdf(pdf_path: str, signature_image_path: str, output_path: str, x: float, y: float):
    # Read the existing PDF
    reader = PyPDF2.PdfReader(pdf_path)
    writer = PyPDF2.PdfWriter()

    # Load the signature image
    with open(signature_image_path, "rb") as img_file:
        img_byte_arr = img_file.read()

    # Add the signature to each page
    for page in reader.pages:
        # Create a new page with the signature overlay
        page.merge_page(PyPDF2.PdfReader(io.BytesIO(img_byte_arr)).pages[0])  # Overlay the signature image
        writer.add_page(page)

    # Write the output PDF
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)

@router.post("/add-signature/", response_model=SignatureResponse)
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

    # Update the signed_at field in the document
    document.signed_at = datetime.now()  # Set the signed_at timestamp

    # Add the signature to the PDF
    add_signature_to_pdf(
        pdf_path=document.file_path,
        signature_image_path=signature.signature_data,  # Assuming this is the path to the signature image
        output_path=document.signed_file_path,  # Path to save the signed PDF
        x=100,  # X coordinate for the signature
        y=100   # Y coordinate for the signature
    )

    db.commit()
    db.refresh(db_signature)

    return db_signature 