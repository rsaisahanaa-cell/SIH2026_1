from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import Base, engine
from .routers import profile, approvals, applications, documents, dashboard

app = FastAPI(
    title="CIVIC@ME API",
    description="SIH26130 Intelligent Industrial Approvals & Compliance Accelerator",
    version="0.1.0"
)

origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(profile.router, prefix="/api")
app.include_router(approvals.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.get("/")
def root():
    return {"name": "CIVIC@ME", "ps": "SIH26130", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
