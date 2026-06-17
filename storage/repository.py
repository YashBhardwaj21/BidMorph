from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import uuid

from .models import Impression, Outcome
from shared.schemas.logging import ImpressionLog
from shared.schemas.outcome import OutcomeRequest

def create_impression(db: Session, log: ImpressionLog) -> Impression:
    """Creates a new impression. Silently handles duplicates by returning existing."""
    existing = get_impression(db, log.impression_id)
    if existing:
        return existing
        
    # use model_dump() instead of dict() for newer pydantic versions, 
    # but .dict() works for both.
    db_impression = Impression(**log.dict())
    try:
        db.add(db_impression)
        db.commit()
        db.refresh(db_impression)
        return db_impression
    except IntegrityError:
        # Idempotency protection in case another thread inserted concurrently
        db.rollback()
        return get_impression(db, log.impression_id)

def get_impression(db: Session, impression_id: str) -> Optional[Impression]:
    return db.query(Impression).filter(Impression.impression_id == impression_id).first()

def create_outcome(db: Session, req: OutcomeRequest) -> Optional[Outcome]:
    """Creates a new outcome linked to an impression."""
    impression = get_impression(db, req.impression_id)
    if not impression:
        # Cannot log an outcome if the impression doesn't exist
        return None
        
    outcome_id = str(uuid.uuid4())
    db_outcome = Outcome(
        id=outcome_id,
        impression_id=req.impression_id,
        clicked=req.clicked,
        revenue=req.revenue
    )
    
    db.add(db_outcome)
    db.commit()
    db.refresh(db_outcome)
    return db_outcome

def get_outcomes_for_impression(db: Session, impression_id: str) -> List[Outcome]:
    return db.query(Outcome).filter(Outcome.impression_id == impression_id).all()
