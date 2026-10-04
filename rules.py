# Demo rule engine for SIH26130.
# Replace/extend these rules with a versioned regulatory knowledge base.

APPROVAL_RULES = [
    {
        "code": "SPCB-CONSENT",
        "name": "Pollution Control Consent",
        "department": "State Pollution Control Board",
        "description": "Environmental consent workflow for eligible industrial activity.",
        "sectors": ["manufacturing", "food_processing"],
        "locations": ["maharashtra", "all"],
        "sizes": ["small", "medium", "large"],
        "stages": ["setup", "expansion", "operating"],
        "sla_days": 30,
        "sequence": 1,
        "documents": ["Project report", "Site plan", "Environmental declaration"]
    },
    {
        "code": "FACTORY-LIC",
        "name": "Factory / Industrial Establishment Licence",
        "department": "Labour & Industrial Safety",
        "description": "Factory establishment and safety compliance workflow.",
        "sectors": ["manufacturing"],
        "locations": ["maharashtra", "all"],
        "sizes": ["medium", "large"],
        "stages": ["setup", "expansion"],
        "sla_days": 21,
        "sequence": 2,
        "documents": ["Occupancy plan", "Safety plan", "Owner declaration"]
    },
    {
        "code": "FIRE-NOC",
        "name": "Fire Safety NOC",
        "department": "Fire & Emergency Services",
        "description": "Fire safety review and inspection.",
        "sectors": ["manufacturing", "food_processing"],
        "locations": ["maharashtra", "all"],
        "sizes": ["small", "medium", "large"],
        "stages": ["setup", "expansion"],
        "sla_days": 15,
        "sequence": 3,
        "documents": ["Fire layout", "Emergency plan"]
    },
    {
        "code": "FSSAI",
        "name": "Food Safety Registration / Licence",
        "department": "Food Safety Administration",
        "description": "Food-business registration/licensing workflow.",
        "sectors": ["food_processing"],
        "locations": ["maharashtra", "all"],
        "sizes": ["small", "medium", "large"],
        "stages": ["setup", "operating", "expansion"],
        "sla_days": 15,
        "sequence": 2,
        "documents": ["Food unit details", "Premises proof"]
    }
]

def matches(rule, profile):
    def ok(value, allowed):
        return value in allowed or "all" in allowed
    return (
        ok(profile.sector.lower(), rule["sectors"])
        and ok(profile.location.lower(), rule["locations"])
        and ok(profile.project_size.lower(), rule["sizes"])
        and ok(profile.operating_stage.lower(), rule["stages"])
    )

def applicable_rules(profile):
    return sorted([r for r in APPROVAL_RULES if matches(r, profile)], key=lambda x: x["sequence"])
