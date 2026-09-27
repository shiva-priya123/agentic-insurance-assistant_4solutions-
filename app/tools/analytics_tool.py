from typing import Dict

from app.database import SessionLocal
from app.models import Claim


def get_claim_analytics() -> Dict:
    """
    Calculate basic analytics across insurance claims
    using PostgreSQL data.
    """

    db = SessionLocal()

    try:
        claims = db.query(Claim).all()

        total_claims = len(claims)

        pending_claims = sum(
            1
            for claim in claims
            if claim.status == "PENDING"
        )

        high_priority_count = sum(
            1
            for claim in claims
            if claim.priority == "HIGH"
        )

        total_estimated_damage = sum(
            claim.estimated_damage
            for claim in claims
        )

        average_estimated_damage = (
            total_estimated_damage / total_claims
            if total_claims > 0
            else 0
        )

        return {
            "total_claims": total_claims,
            "pending_claims": pending_claims,
            "high_priority_claims": high_priority_count,
            "total_estimated_damage": total_estimated_damage,
            "average_estimated_damage": round(
                average_estimated_damage,
                2
            )
        }

    finally:
        db.close()