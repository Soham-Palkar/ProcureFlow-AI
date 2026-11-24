
import uuid
from pathlib import Path

from fastapi import UploadFile, File
from app.services.quotation_extractor import extract_quotation
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.quotation import Quotation
from app.models.supplier import Supplier
from app.models.purchase_request import PurchaseRequest
from app.schemas.quotation import (
    QuotationCreate,
    QuotationUpdate,
    QuotationResponse,
)

router = APIRouter(
    prefix="/api/quotations",
    tags=["Quotations"]
)


@router.post(
    "/",
    response_model=QuotationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_quotation(
    quotation_data: QuotationCreate,
    db: Session = Depends(get_db)
):
    supplier = db.query(Supplier).filter(
        Supplier.id == quotation_data.supplier_id
    ).first()

    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    purchase_request = db.query(PurchaseRequest).filter(
        PurchaseRequest.id == quotation_data.purchase_request_id
    ).first()

    if not purchase_request:
        raise HTTPException(
            status_code=404,
            detail="Purchase request not found"
        )

    quotation = Quotation(**quotation_data.model_dump())
    db.add(quotation)
    db.commit()
    db.refresh(quotation)

    return quotation


@router.get("/", response_model=list[QuotationResponse])
def get_quotations(db: Session = Depends(get_db)):
    return db.query(Quotation).order_by(
        Quotation.created_at.desc()
    ).all()


@router.get("/{quotation_id}", response_model=QuotationResponse)
def get_quotation(quotation_id: UUID, db: Session = Depends(get_db)):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    return quotation


@router.patch("/{quotation_id}", response_model=QuotationResponse)
def update_quotation(
    quotation_id: UUID,
    quotation_data: QuotationUpdate,
    db: Session = Depends(get_db)
):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    updates = quotation_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(quotation, field, value)

    db.commit()
    db.refresh(quotation)

    return quotation


@router.delete("/{quotation_id}")
def delete_quotation(quotation_id: UUID, db: Session = Depends(get_db)):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")

    db.delete(quotation)
    db.commit()

    return {"message": "Quotation deleted successfully"}



@router.post("/{quotation_id}/upload")
async def upload_quotation_document(
    quotation_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Find the existing quotation
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found"
        )

    # 2. Read the uploaded document
    file_bytes = await file.read()

    # 3. Extract document contents
    try:
        extracted = extract_quotation(
            file_bytes,
            file.filename or ""
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    # 4. Create a unique filename
    extension = Path(file.filename or "").suffix.lower()
    stored_filename = f"{uuid.uuid4()}{extension}"

    upload_directory = (
        Path(__file__).resolve().parents[2]
        / "uploads"
        / "quotations"
    )

    upload_directory.mkdir(parents=True, exist_ok=True)

    file_path = upload_directory / stored_filename

    # 5. Save the original document
    try:
        file_path.write_bytes(file_bytes)

        # 6. Save the relative file path in Supabase
        quotation.document_path = (
            f"uploads/quotations/{stored_filename}"
        )

        db.commit()
        db.refresh(quotation)

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Could not save quotation document"
        )

    # 7. Return extracted contents
    return {
        "message": "Quotation document uploaded successfully",
        "quotation_id": str(quotation.id),
        "filename": extracted["filename"],
        "file_type": extracted["file_type"],
        "document_path": quotation.document_path,
        "extracted_text": extracted["text"],
        "warning": extracted["warning"]
    }
