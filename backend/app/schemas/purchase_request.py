
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PurchaseRequestCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None
    category: str | None = None

    quantity: int = Field(gt=0)
    unit: str | None = None

    specifications: dict = Field(default_factory=dict)

    budget: Decimal | None = Field(default=None, ge=0)
    required_by: date | None = None


class PurchaseRequestUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    category: str | None = None
    quantity: int | None = Field(default=None, gt=0)
    unit: str | None = None
    specifications: dict | None = None
    budget: Decimal | None = Field(default=None, ge=0)
    required_by: date | None = None
    status: str | None = None


class PurchaseRequestResponse(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    category: str | None = None
    quantity: int
    unit: str | None = None
    specifications: dict = Field(default_factory=dict)
    budget: Decimal | None = None
    required_by: date | None = None
    status: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
