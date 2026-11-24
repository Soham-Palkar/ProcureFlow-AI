
from sqlalchemy import (
    Column, String, Text, Integer, Numeric,
    Date, DateTime, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database.connection import Base


class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)

    quantity = Column(Integer, nullable=False)
    unit = Column(String(50), nullable=True)

    specifications = Column(
        JSONB,
        server_default=text("'{}'::jsonb")
    )

    budget = Column(Numeric(12, 2), nullable=True)
    required_by = Column(Date, nullable=True)

    status = Column(
        String(30),
        server_default=text("'draft'")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()")
    )
