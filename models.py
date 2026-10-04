from datetime import datetime, date
from sqlalchemy import String, Integer, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class BusinessProfile(Base):
    __tablename__ = "business_profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    sector: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    project_size: Mapped[str] = mapped_column(String(50))
    operating_stage: Mapped[str] = mapped_column(String(50))
    owner_name: Mapped[str] = mapped_column(String(150), default="Demo Applicant")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    department: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text, default="")
    sector: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    min_size: Mapped[str] = mapped_column(String(50), default="small")
    stage: Mapped[str] = mapped_column(String(50), default="setup")
    sla_days: Mapped[int] = mapped_column(Integer, default=15)
    sequence: Mapped[int] = mapped_column(Integer, default=1)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class DocumentRequirement(Base):
    __tablename__ = "document_requirements"
    id: Mapped[int] = mapped_column(primary_key=True)
    approval_id: Mapped[int] = mapped_column(ForeignKey("approvals.id"))
    name: Mapped[str] = mapped_column(String(200))
    required: Mapped[bool] = mapped_column(Boolean, default=True)
    allowed_extensions: Mapped[str] = mapped_column(String(100), default=".pdf,.png,.jpg,.jpeg")

class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    reference_no: Mapped[str] = mapped_column(String(50), unique=True)
    business_profile_id: Mapped[int] = mapped_column(ForeignKey("business_profiles.id"))
    approval_id: Mapped[int] = mapped_column(ForeignKey("approvals.id"))
    status: Mapped[str] = mapped_column(String(50), default="submitted")
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    due_date: Mapped[date] = mapped_column(Date)
    query_text: Mapped[str | None] = mapped_column(Text, nullable=True)

class WorkflowStep(Base):
    __tablename__ = "workflow_steps"
    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    department: Mapped[str] = mapped_column(String(150))
    step_name: Mapped[str] = mapped_column(String(150))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    due_date: Mapped[date] = mapped_column(Date)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    requirement_id: Mapped[int] = mapped_column(ForeignKey("document_requirements.id"))
    filename: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    validation_message: Mapped[str] = mapped_column(Text, default="")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Inspection(Base):
    __tablename__ = "inspections"
    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    scheduled_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="not_scheduled")
    notes: Mapped[str] = mapped_column(Text, default="")

class Incentive(Base):
    __tablename__ = "incentives"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    sector: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    stage: Mapped[str] = mapped_column(String(50))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Renewal(Base):
    __tablename__ = "renewals"
    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    approval_name: Mapped[str] = mapped_column(String(200))
    renewal_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), default="upcoming")
