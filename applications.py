from datetime import date, timedelta
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Application, Approval, BusinessProfile, WorkflowStep
from ..schemas import ApplicationCreate, ApplicationOut, WorkflowOut
from ..services import sla_state, make_reference

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("", response_model=ApplicationOut)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    profile = db.get(BusinessProfile, payload.profile_id)
    approval = db.get(Approval, payload.approval_id)
    if not profile or not approval:
        raise HTTPException(404, "Profile or approval not found")

    due = date.today() + timedelta(days=approval.sla_days)
    app = Application(
        reference_no=f"TEMP-{uuid4().hex[:8].upper()}",
        business_profile_id=profile.id,
        approval_id=approval.id,
        status="submitted",
        due_date=due,
    )
    db.add(app); db.flush()
    app.reference_no = make_reference(app.id)

    # Parallel workflow simulation: multiple departments can work independently.
    departments = [approval.department, "Document Scrutiny", "Inspection Cell"]
    for i, dept in enumerate(departments):
        db.add(WorkflowStep(
            application_id=app.id,
            department=dept,
            step_name=["Primary Review", "Document Review", "Inspection / Query"][i],
            status="in_progress" if i == 0 else "pending",
            due_date=date.today() + timedelta(days=max(3, approval.sla_days // len(departments)))
        ))
    db.commit(); db.refresh(app)
    return serialize(app, approval)

@router.get("", response_model=list[ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    rows = db.query(Application, Approval).join(Approval, Application.approval_id == Approval.id).order_by(Application.id.desc()).all()
    return [serialize(a, p) for a, p in rows]

@router.get("/{application_id}/workflow", response_model=list[WorkflowOut])
def workflow(application_id: int, db: Session = Depends(get_db)):
    return db.query(WorkflowStep).filter_by(application_id=application_id).all()

@router.patch("/{application_id}/status")
def update_status(application_id: int, status: str, db: Session = Depends(get_db)):
    app = db.get(Application, application_id)
    if not app: raise HTTPException(404, "Application not found")
    app.status = status
    db.commit()
    return {"ok": True, "status": status}

def serialize(app, approval):
    return {
        "id": app.id,
        "reference_no": app.reference_no,
        "approval_name": approval.name,
        "department": approval.department,
        "status": app.status,
        "submitted_at": app.submitted_at.isoformat(),
        "due_date": app.due_date,
        "sla_state": sla_state(app.due_date)
    }
