from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
from app.database import get_db
from app.models import Deal, DealStage
from app.schemas import DealCreate, DealResponse, PaginatedResponse

router = APIRouter(prefix="/deals", tags=["Deals"])

SORTABLE_FIELDS = {
    "deal_name": Deal.deal_name,
    "stage": Deal.stage,
    "company_name": Deal.company_name,
    "value": Deal.value,
    "created_at": Deal.created_at,
}


@router.get("/", response_model=PaginatedResponse)
def get_deals(
    # Filters
    search: Optional[str] = Query(None, description="Search by deal name or company"),
    deal_name: Optional[str] = Query(None, description="Filter by deal name"),
    stage: Optional[DealStage] = Query(None, description="Filter by stage: lead, in_progress, won, lost"),
    company_name: Optional[str] = Query(None, description="Filter by company name"),
    min_value: Optional[float] = Query(None, description="Minimum deal value"),
    max_value: Optional[float] = Query(None, description="Maximum deal value"),
    # Sorting
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort direction: asc or desc"),
    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Deal)

    if search:
        query = query.filter(
            Deal.deal_name.ilike(f"%{search}%") |
            Deal.company_name.ilike(f"%{search}%")
        )
    if deal_name:
        query = query.filter(Deal.deal_name.ilike(f"%{deal_name}%"))
    if stage:
        query = query.filter(Deal.stage == stage)
    if company_name:
        query = query.filter(Deal.company_name.ilike(f"%{company_name}%"))
    if min_value is not None:
        query = query.filter(Deal.value >= min_value)
    if max_value is not None:
        query = query.filter(Deal.value <= max_value)

    sort_col = SORTABLE_FIELDS.get(sort_by, Deal.created_at)
    query = query.order_by(desc(sort_col) if sort_order == "desc" else asc(sort_col))

    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=[DealResponse.model_validate(r) for r in records],
    )


@router.get("/{deal_id}", response_model=DealResponse)
def get_deal(deal_id: str, db: Session = Depends(get_db)):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.post("/", response_model=DealResponse, status_code=201)
def create_deal(payload: DealCreate, db: Session = Depends(get_db)):
    deal = Deal(**payload.model_dump())
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal
