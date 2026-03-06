from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models import DealStage


# ── Company ──────────────────────────────────────────────
class CompanyBase(BaseModel):
    company_name: str
    email: str
    contact: str


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Person ───────────────────────────────────────────────
class PersonBase(BaseModel):
    name: str
    email: Optional[str] = None
    connection_strength: Optional[float] = 0.0
    last_email_interaction: Optional[datetime] = None
    last_calendar_interaction: Optional[datetime] = None


class PersonCreate(PersonBase):
    pass


class PersonResponse(PersonBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Deal ─────────────────────────────────────────────────
class DealBase(BaseModel):
    deal_name: str
    stage: DealStage = DealStage.lead
    company_name: Optional[str] = None
    value: Optional[float] = 0.0


class DealCreate(DealBase):
    pass


class DealResponse(DealBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Paginated response wrapper ────────────────────────────
class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list
