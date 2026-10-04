# CIVIC@ME — Intelligent Industrial Approvals & Compliance Accelerator

SIH26130 MVP based on the CIVIC@ME idea presentation.

## What is included

- Applicant dashboard
- Business profile
- Rule-based approval mapper
- Approval dependency/sequence display
- Document checklist + upload validation
- Application creation and status tracking
- Parallel departmental workflow simulation
- SLA tracking and overdue detection
- Inspection scheduling/status
- Renewal reminders
- Incentive discovery
- Government/official dashboard
- PostgreSQL database
- FastAPI REST API
- React + Vite frontend
- Docker Compose

> This is an SIH prototype/MVP. Regulatory rules and sample approvals are demo data and must be replaced/verified against authoritative government sources before production use.

## Project structure

```text
CIVIC-ME/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── rules.py
│   │   ├── services.py
│   │   └── routers/
│   │       ├── approvals.py
│   │       ├── applications.py
│   │       ├── dashboard.py
│   │       ├── documents.py
│   │       └── profile.py
│   ├── seed.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Run with Docker

```bash
docker compose up --build
```

Open:
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- API: http://localhost:8000

## Run backend locally

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run frontend locally

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:8000/api` if needed.

## Demo flow

1. Open Dashboard.
2. Create/update the sample industrial profile.
3. Go to Approval Mapper.
4. Select sector/location/project size/stage.
5. Generate the applicable approvals.
6. Create an application.
7. Upload/check required documents.
8. Open Applications to see the workflow.
9. Use the SLA dashboard to see deadlines and overdue items.
10. Check Renewals & Incentives.

## Important production upgrades

- Real government regulatory knowledge base
- Versioned rules with effective dates
- Government API adapters
- Real authentication/RBAC
- Virus scanning and secure object storage
- OCR pipeline
- Human review for low-confidence extraction
- Immutable audit logs
- Digital signatures/e-sign integrations
- Encryption and secrets management
- Production migrations with Alembic
