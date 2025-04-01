from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum,Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

class SignatureType(str, PyEnum):
    DRAWN = "drawn"
    TEXT = "text"
    IMAGE = "image"

class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    document_id = Column(Integer, ForeignKey("documents.id"))
    signature_type = Column(SQLEnum(SignatureType))
    signature_data = Column(Text)  # Base64 encoded data
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="signatures")
    document = relationship("Document", back_populates="signatures")

def add_signature_to_pdf(pdf_path: str, signature_image_path: str, output_path: str, x: float, y: float):
    # Read the existing PDF
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Load the signature image
    with open(signature_image_path, "rb") as img_file:
        img_byte_arr = img_file.read()

    # Create a new PDF page for the signature
    c = canvas.Canvas("temp_signature.pdf", pagesize=letter)
    c.drawImage(signature_image_path, x, y, width=2 * inch, height=1 * inch)  # Adjust size as needed
    c.save()

    # Read the temporary signature PDF
    signature_reader = PdfReader("temp_signature.pdf")
    signature_page = signature_reader.pages[0]

    # Add the signature to each page of the original PDF
    for page in reader.pages:
        page.merge_page(signature_page)  # Overlay the signature image
        writer.add_page(page)

    # Write the output PDF
    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf) 