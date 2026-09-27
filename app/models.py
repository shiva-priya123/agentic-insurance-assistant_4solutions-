from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)
    estimated_damage = Column(Float, nullable=False)