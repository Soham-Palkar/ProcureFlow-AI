
from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class OrganizationMember(Base):
    __tablename__ = "organization_members"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_organization_user"
        ),
        CheckConstraint(
            "role IN ('owner', 'admin', 'procurement_manager', 'requester', 'approver', 'viewer')",
            name="ck_organization_member_role"
        )
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )

    # Supabase Auth user ID
    user_id = Column(UUID(as_uuid=True), nullable=False)

    role = Column(String(50), nullable=False, server_default=text("'requester'"))

    joined_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
