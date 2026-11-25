
import re
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.connection import get_db
from app.core.auth import get_current_user
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember

router = APIRouter(prefix="/api/organizations", tags=["Organizations"])


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    industry: str | None = None
    company_size: str | None = None
    country: str = "India"


@router.post("/", status_code=201)
def create_organization(
    data: OrganizationCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Generate a URL-friendly organization slug.
    base_slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        data.name.lower()
    ).strip("-")

    slug = f"{base_slug}-{str(current_user.id)[:8]}"

    organization = Organization(
        name=data.name,
        slug=slug,
        industry=data.industry,
        company_size=data.company_size,
        country=data.country
    )

    try:
        db.add(organization)
        db.flush()

        membership = OrganizationMember(
            organization_id=organization.id,
            user_id=UUID(str(current_user.id)),
            role="owner"
        )

        db.add(membership)
        db.commit()
        db.refresh(organization)

        return {
            "message": "Organization created successfully",
            "organization": {
                "id": str(organization.id),
                "name": organization.name,
                "slug": organization.slug,
                "industry": organization.industry,
                "company_size": organization.company_size,
                "country": organization.country
            },
            "role": "owner"
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Could not create organization due to a database conflict."
        )
    except Exception:
        db.rollback()
        raise
