from datetime import date, timedelta
from app.database import Base, engine, SessionLocal
from app.models import BusinessProfile, Approval, DocumentRequirement, Application, WorkflowStep, Incentive, Renewal
from app.rules import APPROVAL_RULES
from app.services import make_reference

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        profile = db.query(BusinessProfile).first()
        if not profile:
            profile = BusinessProfile(
                name="Demo Green Manufacturing Unit",
                sector="manufacturing",
                location="maharashtra",
                project_size="medium",
                operating_stage="setup",
                owner_name="CIVIC@ME Demo Applicant"
            )
            db.add(profile); db.flush()

        for r in APPROVAL_RULES:
            approval = db.query(Approval).filter_by(code=r["code"]).first()
            if not approval:
                approval = Approval(
                    code=r["code"], name=r["name"], department=r["department"],
                    description=r["description"], sector=r["sectors"][0],
                    location="maharashtra", min_size=r["sizes"][0],
                    stage=r["stages"][0], sla_days=r["sla_days"], sequence=r["sequence"]
                )
                db.add(approval); db.flush()
                for name in r["documents"]:
                    db.add(DocumentRequirement(approval_id=approval.id, name=name))

        if db.query(Incentive).count() == 0:
            db.add_all([
                Incentive(
                    name="Manufacturing Expansion Support",
                    description="Demo incentive record for qualifying manufacturing units.",
                    sector="manufacturing", location="maharashtra", stage="expansion"
                ),
                Incentive(
                    name="Food Processing Support",
                    description="Demo incentive record for qualifying food-processing units.",
                    sector="food_processing", location="maharashtra", stage="setup"
                )
            ])

        if db.query(Application).count() == 0:
            approval = db.query(Approval).filter_by(code="SPCB-CONSENT").first()
            app = Application(
                reference_no="CIVIC-2026-00001",
                business_profile_id=profile.id,
                approval_id=approval.id,
                status="document_review",
                due_date=date.today() + timedelta(days=8)
            )
            db.add(app); db.flush()
            db.add_all([
                WorkflowStep(application_id=app.id, department=approval.department,
                             step_name="Primary Review", status="in_progress",
                             due_date=date.today() + timedelta(days=3)),
                WorkflowStep(application_id=app.id, department="Document Scrutiny",
                             step_name="Document Review", status="in_progress",
                             due_date=date.today() + timedelta(days=5)),
                WorkflowStep(application_id=app.id, department="Inspection Cell",
                             step_name="Inspection / Query", status="pending",
                             due_date=date.today() + timedelta(days=8)),
            ])
            db.add(Renewal(
                application_id=app.id,
                approval_name=approval.name,
                renewal_date=date.today() + timedelta(days=45),
                status="upcoming"
            ))

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
