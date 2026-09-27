from typing import List, Dict

from app.database import SessionLocal
from app.models import Claim


def get_claim(claim_id: int) -> Dict:
    """
    Retrieve a claim by claim ID from PostgreSQL.
    """

    db = SessionLocal()

    try:
        claim = db.query(Claim).filter(Claim.id == claim_id).first()

        if not claim:
            return {
                "error": f"Claim {claim_id} was not found."
            }

        return {
            "claim_id": claim.id,
            "claim_type": claim.claim_type,
            "status": claim.status,
            "priority": claim.priority,
            "estimated_damage": claim.estimated_damage
        }

    finally:
        db.close()


def get_high_priority_claims() -> List[Dict]:
    """
    Retrieve all high-priority claims from PostgreSQL.
    """

    db = SessionLocal()

    try:
        claims = (
            db.query(Claim)
            .filter(Claim.priority == "HIGH")
            .all()
        )

        return [
            {
                "claim_id": claim.id,
                "claim_type": claim.claim_type,
                "status": claim.status,
                "priority": claim.priority,
                "estimated_damage": claim.estimated_damage
            }
            for claim in claims
        ]

    finally:
        db.close()