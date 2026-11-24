
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.purchase_request import PurchaseRequest
from app.schemas.purchase_request import (
    PurchaseRequestCreate,
    PurchaseRequestUpdate,
    PurchaseRequestResponse
)

router = APIRouter(
    prefix="/api/purchase-requests",
    tags=["Purchase Requests"]
)


@router.post(
    "/",
    response_model=PurchaseRequestResponse,
    status_code=status.HTTP_201_CREATED
)
def create_purchase_request(
    request_data: PurchaseRequestCreate,
    db: Session = Depends(get_db)
):
    purchase_request = PurchaseRequest(
        **request_data.model_dump()
    )

    db.add(purchase_request)
    db.commit()
    db.refresh(purchase_request)

    return purchase_request


@router.get("/", response_model=list[PurchaseRequestResponse])
def get_purchase_requests(db: Session = Depends(get_db)):
    return db.query(PurchaseRequest).order_by(
        PurchaseRequest.created_at.desc()
    ).all()


@router.get("/{request_id}", response_model=PurchaseRequestResponse)
def get_purchase_request(
    request_id: UUID,
    db: Session = Depends(get_db)
):
    request = db.query(PurchaseRequest).filter(
        PurchaseRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Purchase request not found"
        )

    return request


@router.patch("/{request_id}", response_model=PurchaseRequestResponse)
def update_purchase_request(
    request_id: UUID,
    request_data: PurchaseRequestUpdate,
    db: Session = Depends(get_db)
):
    request = db.query(PurchaseRequest).filter(
        PurchaseRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Purchase request not found"
        )

    updates = request_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(request, field, value)

    db.commit()
    db.refresh(request)

    return request


@router.delete("/{request_id}")
def delete_purchase_request(
    request_id: UUID,
    db: Session = Depends(get_db)
):
    request = db.query(PurchaseRequest).filter(
        PurchaseRequest.id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Purchase request not found"
        )

    db.delete(request)
    db.commit()

    return {
        "message": "Purchase request deleted successfully"
    }
