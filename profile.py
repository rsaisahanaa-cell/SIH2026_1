from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import BusinessProfile
from ..schemas import ProfileCreate, ProfileOut

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("", response_model=ProfileOut)
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    profile = BusinessProfile(**payload.model_dump())
    db.add(profile); db.commit(); db.refresh(profile)
    return profile

@router.get("/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    return db.get(BusinessProfile, profile_id)
