
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)
    country = Column(String(100), server_default=text("'India'"))
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
