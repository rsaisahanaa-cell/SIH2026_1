from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Application, Document, Renewal

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    apps = db.query(Application).all()
    return {
        "total_applications": len(apps),
        "pending": sum(a.status not in ("approved", "rejected") for a in apps),
        "approved": sum(a.status == "approved" for a in apps),
        "overdue": sum(a.due_date < date.today() and a.status not in ("approved", "rejected") for a in apps),
        "documents_pending": db.query(Document).filter(Document.status == "pending").count(),
        "renewals_due": db.query(Renewal).filter(Renewal.renewal_date <= date.today()).count()
    }

@router.get("/sla")
def sla(db: Session = Depends(get_db)):
    apps = db.query(Application).order_by(Application.due_date).all()
    return [
        {
            "reference_no": a.reference_no,
            "status": a.status,
            "due_date": a.due_date,
            "days_remaining": (a.due_date - date.today()).days
        } for a in apps
    ]

@router.get("/renewals")
def renewals(db: Session = Depends(get_db)):
    return db.query(Renewal).order_by(Renewal.renewal_date).all()

@router.get("/incentives")
def incentives(db: Session = Depends(get_db)):
    from ..models import Incentive
    return db.query(Incentive).filter_by(active=True).all()
