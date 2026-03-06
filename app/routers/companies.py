from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
from app.database import get_db
from app.models import Company
from app.schemas import CompanyCreate, CompanyResponse, PaginatedResponse

router = APIRouter(prefix="/companies", tags=["Companies"])

SORTABLE_FIELDS = {
    "company_name": Company.company_name,
    "email": Company.email,
    "contact": Company.contact,
    "created_at": Company.created_at,
}


@router.get("/", response_model=PaginatedResponse)
def get_companies(
    # Filters
    search: Optional[str] = Query(None, description="Search by name, email, or contact"),
    company_name: Optional[str] = Query(None, description="Filter by company name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    contact: Optional[str] = Query(None, description="Filter by contact/phone"),
    # Sorting
    sort_by: str = Query("created_at", description="Field to sort by: company_name, email, contact, created_at"),
    sort_order: str = Query("asc", description="Sort direction: asc or desc"),
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Records per page"),
    db: Session = Depends(get_db),
):
    query = db.query(Company)

    # Apply filters
    if search:
        query = query.filter(
            Company.company_name.ilike(f"%{search}%") |
            Company.email.ilike(f"%{search}%") |
            Company.contact.ilike(f"%{search}%")
        )
    if company_name:
        query = query.filter(Company.company_name.ilike(f"%{company_name}%"))
    if email:
        query = query.filter(Company.email.ilike(f"%{email}%"))
    if contact:
        query = query.filter(Company.contact.ilike(f"%{contact}%"))

    # Apply sorting
    sort_col = SORTABLE_FIELDS.get(sort_by, Company.created_at)
    query = query.order_by(desc(sort_col) if sort_order == "desc" else asc(sort_col))

    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=[CompanyResponse.model_validate(r) for r in records],
    )


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: str, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.post("/", response_model=CompanyResponse, status_code=201)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
