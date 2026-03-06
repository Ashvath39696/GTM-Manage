from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models import Person
from app.schemas import PersonCreate, PersonResponse, PaginatedResponse

router = APIRouter(prefix="/people", tags=["People"])

SORTABLE_FIELDS = {
    "name": Person.name,
    "email": Person.email,
    "connection_strength": Person.connection_strength,
    "last_email_interaction": Person.last_email_interaction,
    "last_calendar_interaction": Person.last_calendar_interaction,
    "created_at": Person.created_at,
}


@router.get("/", response_model=PaginatedResponse)
def get_people(
    # Filters
    search: Optional[str] = Query(None, description="Search by name or email"),
    name: Optional[str] = Query(None, description="Filter by name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    min_connection_strength: Optional[float] = Query(None, description="Minimum connection strength"),
    last_email_after: Optional[datetime] = Query(None, description="Last email interaction after date"),
    last_email_before: Optional[datetime] = Query(None, description="Last email interaction before date"),
    # Sorting
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort direction: asc or desc"),
    # Pagination
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Person)

    if search:
        query = query.filter(
            Person.name.ilike(f"%{search}%") |
            Person.email.ilike(f"%{search}%")
        )
    if name:
        query = query.filter(Person.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Person.email.ilike(f"%{email}%"))
    if min_connection_strength is not None:
        query = query.filter(Person.connection_strength >= min_connection_strength)
    if last_email_after:
        query = query.filter(Person.last_email_interaction >= last_email_after)
    if last_email_before:
        query = query.filter(Person.last_email_interaction <= last_email_before)

    sort_col = SORTABLE_FIELDS.get(sort_by, Person.created_at)
    query = query.order_by(desc(sort_col) if sort_order == "desc" else asc(sort_col))

    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=[PersonResponse.model_validate(r) for r in records],
    )


@router.get("/{person_id}", response_model=PersonResponse)
def get_person(person_id: str, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.post("/", response_model=PersonResponse, status_code=201)
def create_person(payload: PersonCreate, db: Session = Depends(get_db)):
    person = Person(**payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person
