
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class SupplierCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    website: str | None = None
    address: str | None = None
    gst_number: str | None = None
    category: str | None = None


class SupplierUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    website: str | None = None
    address: str | None = None
    gst_number: str | None = None
    category: str | None = None
    status: str | None = None


class SupplierResponse(BaseModel):
    id: UUID
    name: str
    email: str | None = None
    phone: str | None = None
    website: str | None = None
    address: str | None = None
    gst_number: str | None = None
    category: str | None = None
    status: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
