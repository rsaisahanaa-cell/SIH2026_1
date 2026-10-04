from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Application, Document, DocumentRequirement
from ..schemas import DocumentCheck, DocumentOut
from ..services import validate_document

router = APIRouter(prefix="/documents", tags=["Document Validator"])

@router.get("/requirements/{approval_id}")
def requirements(approval_id: int, db: Session = Depends(get_db)):
    return db.query(DocumentRequirement).filter_by(approval_id=approval_id).all()

@router.post("/validate", response_model=DocumentOut)
def validate(payload: DocumentCheck, db: Session = Depends(get_db)):
    req = db.get(DocumentRequirement, payload.requirement_id)
    if not req:
        raise HTTPException(404, "Document requirement not found")
    # Demo endpoint validates metadata/extension; actual file storage/OCR can be attached here.
    status, message = validate_document(payload.filename, req.name)
    doc = Document(
        application_id=0,
        requirement_id=req.id,
        filename=payload.filename,
        status=status,
        validation_message=message,
    )
    # application_id=0 is avoided for persistence in normal usage; this endpoint is a preview validator.
    # Return an unsaved preview object for a standalone pre-check.
    return {
        "id": 0,
        "requirement_id": req.id,
        "filename": payload.filename,
        "status": status,
        "validation_message": message
    }
