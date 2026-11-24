
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class QuotationCreate(BaseModel):
    supplier_id: UUID
    purchase_request_id: UUID
    total_amount: Decimal | None = Field(default=None, ge=0)
    currency: str = "INR"
    delivery_days: int | None = Field(default=None, ge=0)
    warranty: str | None = None
    payment_terms: str | None = None
    document_path: str | None = None


class QuotationUpdate(BaseModel):
    total_amount: Decimal | None = Field(default=None, ge=0)
    currency: str | None = None
    delivery_days: int | None = Field(default=None, ge=0)
    warranty: str | None = None
    payment_terms: str | None = None
    document_path: str | None = None
    status: str | None = None


class QuotationResponse(BaseModel):
    id: UUID
    supplier_id: UUID
    purchase_request_id: UUID
    total_amount: Decimal | None = None
    currency: str | None = None
    delivery_days: int | None = None
    warranty: str | None = None
    payment_terms: str | None = None
    document_path: str | None = None
    status: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
