
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Numeric,
    DateTime,
    text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.database.connection import Base


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    supplier_id = Column(UUID(as_uuid=True), nullable=False)
    purchase_request_id = Column(UUID(as_uuid=True), nullable=False)

    total_amount = Column(Numeric(12, 2), nullable=True)
    currency = Column(String(10), server_default=text("'INR'"))
    delivery_days = Column(Integer, nullable=True)
    warranty = Column(Text, nullable=True)
    payment_terms = Column(Text, nullable=True)
    document_path = Column(Text, nullable=True)
    status = Column(String(30), server_default=text("'received'"))
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()")
    )

    # AI quotation analysis fields
    analysis_result = Column(JSONB, nullable=True)

    analysis_status = Column(
        String(30),
        server_default=text("'not_analyzed'")
    )

    analyzed_at = Column(DateTime(timezone=True), nullable=True)

    analysis_error = Column(Text, nullable=True)
