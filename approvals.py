from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import BusinessProfile, Approval, DocumentRequirement
from ..rules import applicable_rules
from ..schemas import ApprovalOut

router = APIRouter(prefix="/approvals", tags=["Approval Mapper"])

@router.get("/map/{profile_id}", response_model=list[ApprovalOut])
def approval_map(profile_id: int, db: Session = Depends(get_db)):
    profile = db.get(BusinessProfile, profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    rules = applicable_rules(profile)
    result = []
    for rule in rules:
        approval = db.query(Approval).filter_by(code=rule["code"]).first()
        if not approval:
            approval = Approval(
                code=rule["code"], name=rule["name"], department=rule["department"],
                description=rule["description"], sector=profile.sector,
                location=profile.location, min_size=profile.project_size,
                stage=profile.operating_stage, sla_days=rule["sla_days"],
                sequence=rule["sequence"]
            )
            db.add(approval); db.flush()
            for doc_name in rule["documents"]:
                db.add(DocumentRequirement(approval_id=approval.id, name=doc_name))
        result.append(approval)
    db.commit()
    return result

@router.get("/{approval_id}/documents")
def approval_documents(approval_id: int, db: Session = Depends(get_db)):
    return db.query(DocumentRequirement).filter_by(approval_id=approval_id).all()
