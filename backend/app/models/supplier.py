
from sqlalchemy import Column, String, Text, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.database.connection import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    gst_number = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)

    status = Column(
        String(30),
        server_default=text("'pending'")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=text("NOW()")
    )
