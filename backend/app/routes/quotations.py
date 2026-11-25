
import uuid
from pathlib import Path
from datetime import datetime, timezone
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    status,
)
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

from app.services.quotation_extractor import extract_quotation
from app.services.quotation_analyzer import analyze_quotation
from app.services.specification_matcher import compare_specifications


router = APIRouter(
    prefix="/api/quotations",
    tags=["Quotations"],
)


# --------------------------------------------------
# HELPER: RESET ANALYSIS AND EVALUATION
# --------------------------------------------------

def reset_quotation_analysis(quotation: Quotation):
    quotation.analysis_result = None
    quotation.analysis_status = "not_analyzed"
    quotation.analyzed_at = None
    quotation.analysis_error = None

    quotation.evaluation_result = None
    quotation.evaluation_status = "not_evaluated"
    quotation.evaluated_at = None


# --------------------------------------------------
# CREATE QUOTATION
# --------------------------------------------------

@router.post(
    "/",
    response_model=QuotationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_quotation(
    quotation_data: QuotationCreate,
    db: Session = Depends(get_db),
):
    supplier = db.query(Supplier).filter(
        Supplier.id == quotation_data.supplier_id
    ).first()

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        )

    purchase_request = db.query(PurchaseRequest).filter(
        PurchaseRequest.id == quotation_data.purchase_request_id
    ).first()

    if not purchase_request:
        raise HTTPException(
            status_code=404,
            detail="Purchase request not found",
        )

    quotation = Quotation(**quotation_data.model_dump())

    db.add(quotation)
    db.commit()
    db.refresh(quotation)

    return quotation


# --------------------------------------------------
# GET ALL QUOTATIONS
# --------------------------------------------------

@router.get("/", response_model=list[QuotationResponse])
def get_quotations(db: Session = Depends(get_db)):
    return db.query(Quotation).order_by(
        Quotation.created_at.desc()
    ).all()


# --------------------------------------------------
# GET SINGLE QUOTATION
# --------------------------------------------------

@router.get("/{quotation_id}", response_model=QuotationResponse)
def get_quotation(
    quotation_id: UUID,
    db: Session = Depends(get_db),
):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    return quotation


# --------------------------------------------------
# UPDATE QUOTATION
# --------------------------------------------------

@router.patch("/{quotation_id}", response_model=QuotationResponse)
def update_quotation(
    quotation_id: UUID,
    quotation_data: QuotationUpdate,
    db: Session = Depends(get_db),
):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    updates = quotation_data.model_dump(exclude_unset=True)

    if updates:
        for field, value in updates.items():
            setattr(quotation, field, value)

        # Updated quotation data invalidates old results.
        reset_quotation_analysis(quotation)

        db.commit()
        db.refresh(quotation)

    return quotation


# --------------------------------------------------
# DELETE QUOTATION
# --------------------------------------------------

@router.delete("/{quotation_id}")
def delete_quotation(
    quotation_id: UUID,
    db: Session = Depends(get_db),
):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    db.delete(quotation)
    db.commit()

    return {
        "message": "Quotation deleted successfully"
    }


# --------------------------------------------------
# UPLOAD QUOTATION DOCUMENT
# --------------------------------------------------

@router.post("/{quotation_id}/upload")
async def upload_quotation_document(
    quotation_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    file_bytes = await file.read()

    try:
        extracted = extract_quotation(
            file_bytes,
            file.filename or "",
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    extension = Path(file.filename or "").suffix.lower()
    stored_filename = f"{uuid.uuid4()}{extension}"

    upload_directory = (
        Path(__file__).resolve().parents[2]
        / "uploads"
        / "quotations"
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = upload_directory / stored_filename

    try:
        file_path.write_bytes(file_bytes)

        quotation.document_path = (
            f"uploads/quotations/{stored_filename}"
        )

        # New document means old results are no longer valid.
        reset_quotation_analysis(quotation)

        db.commit()
        db.refresh(quotation)

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Could not save quotation document",
        )

    return {
        "message": "Quotation document uploaded successfully",
        "quotation_id": str(quotation.id),
        "filename": extracted["filename"],
        "file_type": extracted["file_type"],
        "document_path": quotation.document_path,
        "extracted_text": extracted["text"],
        "warning": extracted["warning"],
    }


# --------------------------------------------------
# AI QUOTATION ANALYSIS
# --------------------------------------------------

@router.post("/{quotation_id}/analyze")
def analyze_quotation_endpoint(
    quotation_id: UUID,
    db: Session = Depends(get_db),
):
    quotation = db.query(Quotation).filter(
        Quotation.id == quotation_id
    ).first()

    if not quotation:
        raise HTTPException(
            status_code=404,
            detail="Quotation not found",
        )

    purchase_request = db.query(PurchaseRequest).filter(
        PurchaseRequest.id == quotation.purchase_request_id
    ).first()

    if not purchase_request:
        raise HTTPException(
            status_code=404,
            detail="Linked purchase request not found",
        )

    requested_specs = purchase_request.specifications or {}

    if not isinstance(requested_specs, dict) or not requested_specs:
        raise HTTPException(
            status_code=400,
            detail="Purchase request has no valid specifications",
        )

    if not quotation.document_path:
        raise HTTPException(
            status_code=400,
            detail="Upload a quotation document before analysis",
        )

    base_directory = Path(__file__).resolve().parents[2]

    upload_directory = (
        base_directory / "uploads" / "quotations"
    ).resolve()

    document_path = (
        base_directory / quotation.document_path
    ).resolve()

    # Ensure the file is inside the quotation upload directory.
    try:
        document_path.relative_to(upload_directory)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid quotation document path",
        )

    if not document_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Quotation document not found on server",
        )

    # Mark analysis as processing.
    quotation.analysis_status = "processing"
    quotation.analysis_error = None
    db.commit()

    try:
        # Read uploaded document.
        file_bytes = document_path.read_bytes()

        extracted = extract_quotation(
            file_bytes,
            document_path.name,
        )

        extracted_text = extracted.get("text", "")

        if not extracted_text or not extracted_text.strip():
            raise ValueError(
                "No readable text found in quotation document. "
                "The document may require OCR."
            )

        # Gemini structured extraction.
        ai_result = analyze_quotation(extracted_text)
        quotation_data = ai_result["data"]

        quoted_items = quotation_data.get("items", [])

        if not quoted_items:
            raise ValueError(
                "Gemini could not identify any quoted products."
            )

        # Current purchase request structure represents one product.
        # Avoid comparing multiple quoted products against the same specs.
        if len(quoted_items) != 1:
            raise ValueError(
                "This purchase request currently supports one product. "
                "Multiple quotation items require line-item mapping."
            )

        # Compare specifications.
        item = quoted_items[0]

        quoted_specs = item.get("specifications", [])

        comparison = compare_specifications(
            requested_specs,
            quoted_specs,
        )

        comparisons = [{
            "product_name": item.get("product_name"),
            "comparison": comparison,
        }]

        # Summary.
        total_specs = comparison["total_specifications"]
        total_matched = comparison["matched"]
        total_mismatched = comparison["mismatched"]
        total_missing = comparison["missing"]

        all_matched = (
            total_specs > 0
            and total_matched == total_specs
        )

        analysis_result = {
            "quotation_id": str(quotation.id),
            "purchase_request_id": str(purchase_request.id),
            "model": ai_result.get("model"),
            "extraction": quotation_data,
            "specification_comparisons": comparisons,
            "summary": {
                "total_specifications": total_specs,
                "matched": total_matched,
                "mismatched": total_mismatched,
                "missing": total_missing,
                "match_percentage": round(
                    (total_matched / total_specs) * 100,
                    2,
                ) if total_specs else 0,
                "overall_status": (
                    "match" if all_matched
                    else "review_required"
                ),
            },
            "document_warning": extracted.get("warning"),
        }

        # Save successful analysis.
        quotation.analysis_result = analysis_result
        quotation.analysis_status = "completed"
        quotation.analyzed_at = datetime.now(timezone.utc)
        quotation.analysis_error = None

        db.commit()
        db.refresh(quotation)

        return {
            "message": "Quotation analysis completed successfully",
            "analysis_status": quotation.analysis_status,
            "analysis": quotation.analysis_result,
        }

    except Exception as error:
        db.rollback()

        quotation = db.query(Quotation).filter(
            Quotation.id == quotation_id
        ).first()

        if quotation:
            quotation.analysis_status = "failed"
            quotation.analysis_error = str(error)[:1000]
            db.commit()

        if isinstance(error, ValueError):
            raise HTTPException(
                status_code=422,
                detail=str(error),
            )

        raise HTTPException(
            status_code=502,
            detail=(
                "Quotation analysis failed. "
                "Check the server logs and retry."
            ),
        )
