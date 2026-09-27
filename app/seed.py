from app.database import SessionLocal
from app.models import Claim


claims = [
    Claim(
        id=1001,
        claim_type="Auto Accident",
        status="PENDING",
        priority="HIGH",
        estimated_damage=45000
    ),
    Claim(
        id=1002,
        claim_type="Property Damage",
        status="PENDING",
        priority="MEDIUM",
        estimated_damage=18000
    ),
    Claim(
        id=1003,
        claim_type="Theft",
        status="PENDING",
        priority="HIGH",
        estimated_damage=32000
    ),
]


db = SessionLocal()

try:
    for claim in claims:
        existing = db.query(Claim).filter(Claim.id == claim.id).first()

        if not existing:
            db.add(claim)

    db.commit()
    print("Claims inserted successfully")

finally:
    db.close()