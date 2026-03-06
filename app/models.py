from sqlalchemy import Column, String, DateTime, Enum, Float
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class DealStage(str, enum.Enum):
    lead = "lead"
    in_progress = "in_progress"
    won = "won"
    lost = "lost"


class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, default=gen_uuid)
    company_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Person(Base):
    __tablename__ = "people"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    email = Column(String)
    connection_strength = Column(Float, default=0.0)
    last_email_interaction = Column(DateTime(timezone=True))
    last_calendar_interaction = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Deal(Base):
    __tablename__ = "deals"

    id = Column(String, primary_key=True, default=gen_uuid)
    deal_name = Column(String, nullable=False)
    stage = Column(Enum(DealStage), default=DealStage.lead, nullable=False)
    company_name = Column(String)
    value = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
