from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.signature import Signature
from app.schemas.signature import SignatureCreate, SignatureResponse, SignatureType
from app.models.user import User
from app.models.document import Document
from app.services.auth import get_current_user
from datetime import datetime
import PyPDF2
import io
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import secrets
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

router = APIRouter()

def add_signature_to_pdf(pdf_path: str, signature_image_path: str, output_path: str, x: float, y: float):
    # Read the existing PDF
    reader = PyPDF2.PdfReader(pdf_path)
    writer = PyPDF2.PdfWriter()

    # Load the signature image
    with open(signature_image_path, "rb") as img_file:
        img_byte_arr = img_file.read()

    # Create a temporary PDF for the signature image
    temp_pdf_path = "temp_signature.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=letter)
    c.drawImage(signature_image_path, x, y, width=2 * inch, height=1 * inch)  # Adjust size as needed
    c.save()

    # Read the temporary signature PDF
    signature_reader = PyPDF2.PdfReader(temp_pdf_path)
    signature_page = signature_reader.pages[0]

    # Add the signature to each page of the original PDF
    for page in reader.pages:
        page.merge_page(signature_page)  # Overlay the signature image
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

    # Handle different signature types
    if signature.signature_type == SignatureType.DRAWN:
        # Handle drawn signature (Base64)
        if signature.signature_data.startswith("data:image/png;base64,"):
            base64_data = signature.signature_data.split(",")[1]
            image_data = base64.b64decode(base64_data)

            # Save the image
            signature_image_path = f"documents/signature_{document.id}.png"
            with open(signature_image_path, "wb") as img_file:
                img_file.write(image_data)
        else:
            raise HTTPException(status_code=400, detail="Invalid drawn signature data")

    elif signature.signature_type == SignatureType.TEXT:
        # Handle text signature
        # Create an image from the text
        signature_image_path = f"documents/text_signature_{document.id}.png"
        font = ImageFont.load_default()  # Load a default font
        text_image = Image.new("RGB", (300, 100), (255, 255, 255))  # Create a white background
        draw = ImageDraw.Draw(text_image)
        draw.text((10, 10), signature.signature_data, fill="black", font=font)  # Draw the text
        text_image.save(signature_image_path)  # Save the image

    elif signature.signature_type == SignatureType.IMAGE:
        # Handle uploaded image signature
        signature_image_path = signature.signature_data  # Assuming this is a valid file path
        if not os.path.exists(signature_image_path):
            raise HTTPException(status_code=400, detail="Signature image file not found")

    else:
        raise HTTPException(status_code=400, detail="Invalid signature type")

    # Create signature record
    db_signature = Signature(
        user_id=current_user.id,
        document_id=signature.document_id,
        signature_type=signature.signature_type,
        signature_data=signature_image_path  # Store the path to the image
    )
    db.add(db_signature)

    # Update the signed_at field in the document
    document.signed_at = datetime.now()  # Set the signed_at timestamp

    # Add the signature to the PDF
    add_signature_to_pdf(
        pdf_path=document.file_path,
        signature_image_path=signature_image_path,  # Use the correct path
        output_path=document.signed_file_path,  # Path to save the signed PDF
        x=100,  # X coordinate for the signature
        y=100   # Y coordinate for the signature
    )

    db.commit()
    db.refresh(db_signature)

    return db_signature 